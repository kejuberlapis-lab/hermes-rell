"""
Department CRUD routes.
"""
from fastapi import APIRouter, Depends, HTTPException, Query
from pydantic import BaseModel
from typing import Optional
from app.database import get_db
from app.services.auth_service import get_current_user
import aiosqlite

router = APIRouter(prefix="/departments", tags=["departments"])

class DepartmentCreate(BaseModel):
    name: str
    code: str
    description: Optional[str] = None
    manager_id: Optional[int] = None

class DepartmentUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    manager_id: Optional[int] = None

def _d(row):
    return dict(row) if row else None

@router.get("")
async def list_departments(skip: int = 0, limit: int = 50, user=Depends(get_current_user), db: aiosqlite.Connection = Depends(get_db)):
    cursor = await db.execute("SELECT * FROM departments ORDER BY name LIMIT ? OFFSET ?", (limit, skip))
    rows = await cursor.fetchall()
    cc = await db.execute("SELECT COUNT(*) FROM departments")
    total = (await cc.fetchone())[0]
    return {"departments": [_d(r) for r in rows], "total": total}

@router.get("/{dept_id}")
async def get_department(dept_id: int, user=Depends(get_current_user), db: aiosqlite.Connection = Depends(get_db)):
    cursor = await db.execute("SELECT * FROM departments WHERE id = ?", (dept_id,))
    dept = await cursor.fetchone()
    if not dept:
        raise HTTPException(status_code=404, detail="Department not found")
    return _d(dept)

@router.post("", status_code=201)
async def create_department(dept: DepartmentCreate, user=Depends(get_current_user), db: aiosqlite.Connection = Depends(get_db)):
    if user.get("role") not in ("super_admin", "director"):
        raise HTTPException(status_code=403, detail="Admin or Director access required")
    try:
        cursor = await db.execute(
            "INSERT INTO departments (name, code, description, manager_id) VALUES (?, ?, ?, ?)",
            (dept.name, dept.code, dept.description, dept.manager_id)
        )
        await db.commit()
        return {"id": cursor.lastrowid, "message": "Department created"}
    except Exception as e:
        if "UNIQUE" in str(e):
            raise HTTPException(status_code=400, detail="Department name or code already exists")
        raise

@router.put("/{dept_id}")
async def update_department(dept_id: int, dept: DepartmentUpdate, user=Depends(get_current_user), db: aiosqlite.Connection = Depends(get_db)):
    if user.get("role") not in ("super_admin", "director"):
        raise HTTPException(status_code=403, detail="Admin or Director access required")
    fields = {k: v for k, v in dept.dict().items() if v is not None}
    if not fields:
        raise HTTPException(status_code=400, detail="No fields to update")
    set_clause = ", ".join(f"{k} = ?" for k in fields)
    await db.execute(f"UPDATE departments SET {set_clause} WHERE id = ?", list(fields.values()) + [dept_id])
    await db.commit()
    return {"message": "Department updated"}

@router.delete("/{dept_id}")
async def delete_department(dept_id: int, user=Depends(get_current_user), db: aiosqlite.Connection = Depends(get_db)):
    if user.get("role") not in ("super_admin", "director"):
        raise HTTPException(status_code=403, detail="Admin or Director access required")
    await db.execute("DELETE FROM departments WHERE id = ?", (dept_id,))
    await db.commit()
    return {"message": "Department deleted"}
