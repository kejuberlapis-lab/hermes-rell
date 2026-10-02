"""
Procurement routes: requests, approval workflow.
"""
from fastapi import APIRouter, Depends, HTTPException, Query
from pydantic import BaseModel
from typing import Optional
from app.database import get_db
from app.services.auth_service import get_current_user
import aiosqlite

router = APIRouter(prefix="/procurement", tags=["procurement"])

def _uid(user):
    return user.get("user_id") or user.get("id")

class ProcurementCreate(BaseModel):
    title: str
    description: Optional[str] = None
    estimated_cost: float = 0
    department_id: Optional[int] = None

class ProcurementAction(BaseModel):
    status: str

@router.get("")
async def list_procurement(status: Optional[str] = None, department_id: Optional[int] = None, skip: int = 0, limit: int = 50, user=Depends(get_current_user), db: aiosqlite.Connection = Depends(get_db)):
    conditions, params = [], []
    role = user.get("role", "employee")
    if role == "employee":
        conditions.append("pr.requester_id = ?")
        params.append(_uid(user))
    if status:
        conditions.append("pr.status = ?")
        params.append(status)
    if department_id:
        conditions.append("pr.department_id = ?")
        params.append(department_id)
    where = " WHERE " + " AND ".join(conditions) if conditions else ""
    q = f"""SELECT pr.*, e.full_name, d.name as department_name FROM procurement_requests pr
            JOIN employees e ON pr.requester_id = e.id
            LEFT JOIN departments d ON pr.department_id = d.id
            {where} ORDER BY pr.created_at DESC LIMIT ? OFFSET ?"""
    params.extend([limit, skip])
    cursor = await db.execute(q, params)
    rows = await cursor.fetchall()
    return {"procurement": [dict(r) for r in rows], "total": len(rows)}

@router.post("", status_code=201)
async def create_procurement(body: ProcurementCreate, user=Depends(get_current_user), db: aiosqlite.Connection = Depends(get_db)):
    cursor = await db.execute("INSERT INTO procurement_requests (title, description, estimated_cost, requester_id, department_id) VALUES (?, ?, ?, ?, ?)",
        (body.title, body.description, body.estimated_cost, _uid(user), body.department_id))
    await db.commit()
    return {"id": cursor.lastrowid, "message": "Procurement request created"}

@router.put("/{proc_id}")
async def update_procurement(proc_id: int, body: ProcurementAction, user=Depends(get_current_user), db: aiosqlite.Connection = Depends(get_db)):
    if user.get("role") not in ("super_admin", "director", "manager"):
        raise HTTPException(status_code=403, detail="Manager, director or admin access required")
    if body.status not in ("approved", "rejected", "purchased"):
        raise HTTPException(status_code=400, detail="Invalid status")
    await db.execute("UPDATE procurement_requests SET status = ?, approved_by = ?, created_at = CURRENT_TIMESTAMP WHERE id = ?", (body.status, _uid(user), proc_id))
    await db.commit()
    return {"message": f"Procurement request {body.status}"}

@router.delete("/{proc_id}")
async def delete_procurement(proc_id: int, user=Depends(get_current_user), db: aiosqlite.Connection = Depends(get_db)):
    if user.get("role") not in ("super_admin", "director"):
        raise HTTPException(status_code=403, detail="Admin or Director access required")
    await db.execute("DELETE FROM procurement_requests WHERE id = ?", (proc_id,))
    await db.commit()
    return {"message": "Procurement request deleted"}
