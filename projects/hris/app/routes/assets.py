"""
Asset routes: CRUD and assignment workflow.
"""
from fastapi import APIRouter, Depends, HTTPException, Query
from pydantic import BaseModel
from typing import Optional
from app.database import get_db
from app.services.auth_service import get_current_user
import aiosqlite

router = APIRouter(prefix="/assets", tags=["assets"])

def _uid(user):
    return user.get("user_id") or user.get("id")

class AssetCreate(BaseModel):
    name: str
    category: str
    serial_number: Optional[str] = None
    purchase_date: Optional[str] = None
    purchase_price: Optional[float] = 0
    location: Optional[str] = None
    department_id: Optional[int] = None

class AssetUpdate(BaseModel):
    name: Optional[str] = None
    category: Optional[str] = None
    serial_number: Optional[str] = None
    purchase_price: Optional[float] = None
    status: Optional[str] = None
    location: Optional[str] = None
    condition: Optional[str] = None

class AssetAssign(BaseModel):
    employee_id: int

@router.get("")
async def list_assets(category: Optional[str] = None, status: Optional[str] = None, assigned_to: Optional[int] = None, skip: int = 0, limit: int = 50, user=Depends(get_current_user), db: aiosqlite.Connection = Depends(get_db)):
    conditions, params = [], []
    role = user.get("role", "employee")
    if role == "employee":
        cursor = await db.execute("SELECT employee_id FROM users WHERE id = ?", (_uid(user),))
        row = await cursor.fetchone()
        conditions.append("a.assigned_to = ?")
        params.append(row["employee_id"] if row and row["employee_id"] else _uid(user))
    if category:
        conditions.append("a.category = ?")
        params.append(category)
    if status:
        conditions.append("a.status = ?")
        params.append(status)
    if assigned_to:
        conditions.append("a.assigned_to = ?")
        params.append(assigned_to)
    where = " WHERE " + " AND ".join(conditions) if conditions else ""
    q = f"""SELECT a.*, e.full_name as assigned_name FROM assets a
            LEFT JOIN employees e ON a.assigned_to = e.id
            {where} ORDER BY a.id LIMIT ? OFFSET ?"""
    params.extend([limit, skip])
    cursor = await db.execute(q, params)
    rows = await cursor.fetchall()
    return {"assets": [dict(r) for r in rows], "total": len(rows)}

@router.get("/{asset_id}")
async def get_asset(asset_id: int, user=Depends(get_current_user), db: aiosqlite.Connection = Depends(get_db)):
    cursor = await db.execute("SELECT * FROM assets WHERE id = ?", (asset_id,))
    asset = await cursor.fetchone()
    if not asset:
        raise HTTPException(status_code=404, detail="Asset not found")
    return dict(asset)

@router.post("", status_code=201)
async def create_asset(body: AssetCreate, user=Depends(get_current_user), db: aiosqlite.Connection = Depends(get_db)):
    if user.get("role") not in ("super_admin", "director", "manager"):
        raise HTTPException(status_code=403, detail="Manager, director or admin access required")
    cursor = await db.execute("INSERT INTO assets (name, category, serial_number, purchase_date, purchase_price, location, department_id) VALUES (?, ?, ?, ?, ?, ?, ?)",
        (body.name, body.category, body.serial_number, body.purchase_date, body.purchase_price, body.location, body.department_id))
    await db.commit()
    return {"id": cursor.lastrowid, "message": "Asset created"}

@router.put("/{asset_id}")
async def update_asset(asset_id: int, body: AssetUpdate, user=Depends(get_current_user), db: aiosqlite.Connection = Depends(get_db)):
    if user.get("role") not in ("super_admin", "director", "manager"):
        raise HTTPException(status_code=403, detail="Manager, director or admin access required")
    fields = {k: v for k, v in body.dict().items() if v is not None}
    if not fields:
        raise HTTPException(status_code=400, detail="No fields to update")
    set_clause = ", ".join(f"{k} = ?" for k in fields)
    await db.execute(f"UPDATE assets SET {set_clause} WHERE id = ?", list(fields.values()) + [asset_id])
    await db.commit()
    return {"message": "Asset updated"}

@router.post("/{asset_id}/assign")
async def assign_asset(asset_id: int, body: AssetAssign, user=Depends(get_current_user), db: aiosqlite.Connection = Depends(get_db)):
    if user.get("role") not in ("super_admin", "director", "manager"):
        raise HTTPException(status_code=403, detail="Manager, director or admin access required")
    await db.execute("UPDATE assets SET assigned_to = ?, status = 'assigned' WHERE id = ?", (body.employee_id, asset_id))
    await db.commit()
    return {"message": "Asset assigned"}

@router.post("/{asset_id}/unassign")
async def unassign_asset(asset_id: int, user=Depends(get_current_user), db: aiosqlite.Connection = Depends(get_db)):
    if user.get("role") not in ("super_admin", "director", "manager"):
        raise HTTPException(status_code=403, detail="Manager, director or admin access required")
    await db.execute("UPDATE assets SET assigned_to = NULL, status = 'available' WHERE id = ?", (asset_id,))
    await db.commit()
    return {"message": "Asset unassigned"}

@router.delete("/{asset_id}")
async def delete_asset(asset_id: int, user=Depends(get_current_user), db: aiosqlite.Connection = Depends(get_db)):
    if user.get("role") not in ("super_admin", "director"):
        raise HTTPException(status_code=403, detail="Admin or Director access required")
    await db.execute("DELETE FROM assets WHERE id = ?", (asset_id,))
    await db.commit()
    return {"message": "Asset deleted"}
