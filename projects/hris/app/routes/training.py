"""
Training routes: programs CRUD, enrollments.
"""
from fastapi import APIRouter, Depends, HTTPException, Query
from pydantic import BaseModel
from typing import Optional
from app.database import get_db
from app.services.auth_service import get_current_user
import aiosqlite

router = APIRouter(prefix="/training", tags=["training"])

def _uid(user):
    return user.get("user_id") or user.get("id")

class ProgramCreate(BaseModel):
    title: str
    description: Optional[str] = None
    trainer: Optional[str] = None
    start_date: str
    end_date: str
    capacity: Optional[int] = 30

class ProgramUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    trainer: Optional[str] = None
    start_date: Optional[str] = None
    end_date: Optional[str] = None
    capacity: Optional[int] = None
    status: Optional[str] = None

class EnrollmentCreate(BaseModel):
    training_id: int
    employee_id: Optional[int] = None

# --- Training Programs ---
@router.get("/programs")
async def list_programs(status: Optional[str] = None, skip: int = 0, limit: int = 50, user=Depends(get_current_user), db: aiosqlite.Connection = Depends(get_db)):
    conditions, params = [], []
    if status:
        conditions.append("status = ?")
        params.append(status)
    where = " WHERE " + " AND ".join(conditions) if conditions else ""
    cursor = await db.execute(f"SELECT * FROM training{where} ORDER BY start_date DESC LIMIT ? OFFSET ?", params + [limit, skip])
    rows = await cursor.fetchall()
    return {"programs": [dict(r) for r in rows], "total": len(rows)}

@router.get("/programs/{prog_id}")
async def get_program(prog_id: int, user=Depends(get_current_user), db: aiosqlite.Connection = Depends(get_db)):
    cursor = await db.execute("SELECT * FROM training WHERE id = ?", (prog_id,))
    prog = await cursor.fetchone()
    if not prog:
        raise HTTPException(status_code=404, detail="Program not found")
    ec = await db.execute("SELECT COUNT(*) FROM training_enrollments WHERE training_id = ?", (prog_id,))
    count = (await ec.fetchone())[0]
    result = dict(prog)
    result["enrolled_count"] = count
    return result

@router.post("/programs", status_code=201)
async def create_program(body: ProgramCreate, user=Depends(get_current_user), db: aiosqlite.Connection = Depends(get_db)):
    if user.get("role") not in ("super_admin", "director", "manager"):
        raise HTTPException(status_code=403, detail="Manager, director or admin access required")
    cursor = await db.execute("INSERT INTO training (title, description, trainer, start_date, end_date, capacity) VALUES (?, ?, ?, ?, ?, ?)",
        (body.title, body.description, body.trainer, body.start_date, body.end_date, body.capacity))
    await db.commit()
    return {"id": cursor.lastrowid, "message": "Program created"}

@router.put("/programs/{prog_id}")
async def update_program(prog_id: int, body: ProgramUpdate, user=Depends(get_current_user), db: aiosqlite.Connection = Depends(get_db)):
    if user.get("role") not in ("super_admin", "director", "manager"):
        raise HTTPException(status_code=403, detail="Manager, director or admin access required")
    fields = {k: v for k, v in body.dict().items() if v is not None}
    if not fields:
        raise HTTPException(status_code=400, detail="No fields to update")
    set_clause = ", ".join(f"{k} = ?" for k in fields)
    await db.execute(f"UPDATE training SET {set_clause} WHERE id = ?", list(fields.values()) + [prog_id])
    await db.commit()
    return {"message": "Program updated"}

@router.delete("/programs/{prog_id}")
async def delete_program(prog_id: int, user=Depends(get_current_user), db: aiosqlite.Connection = Depends(get_db)):
    if user.get("role") not in ("super_admin", "director"):
        raise HTTPException(status_code=403, detail="Admin or Director access required")
    await db.execute("DELETE FROM training WHERE id = ?", (prog_id,))
    await db.commit()
    return {"message": "Program deleted"}

# --- Enrollments ---
@router.get("/enrollments")
async def list_enrollments(training_id: Optional[int] = None, employee_id: Optional[int] = None, user=Depends(get_current_user), db: aiosqlite.Connection = Depends(get_db)):
    conditions, params = [], []
    if user.get("role") == "employee":
        cursor = await db.execute("SELECT employee_id FROM users WHERE id = ?", (_uid(user),))
        row = await cursor.fetchone()
        conditions.append("te.employee_id = ?")
        params.append(row["employee_id"] if row and row["employee_id"] else _uid(user))
    if training_id:
        conditions.append("te.training_id = ?")
        params.append(training_id)
    if employee_id:
        conditions.append("te.employee_id = ?")
        params.append(employee_id)
    where = " WHERE " + " AND ".join(conditions) if conditions else ""
    q = f"""SELECT te.*, t.title as program_title, e.full_name
            FROM training_enrollments te
            JOIN training t ON te.training_id = t.id
            JOIN employees e ON te.employee_id = e.id
            {where} ORDER BY te.id DESC"""
    cursor = await db.execute(q, params)
    rows = await cursor.fetchall()
    return {"enrollments": [dict(r) for r in rows]}

@router.post("/enrollments", status_code=201)
async def create_enrollment(body: EnrollmentCreate, user=Depends(get_current_user), db: aiosqlite.Connection = Depends(get_db)):
    emp_id = body.employee_id
    if user.get("role") == "employee" or not emp_id:
        cursor = await db.execute("SELECT employee_id FROM users WHERE id = ?", (_uid(user),))
        row = await cursor.fetchone()
        emp_id = row["employee_id"] if row and row["employee_id"] else _uid(user)
    pc = await db.execute("SELECT capacity FROM training WHERE id = ?", (body.training_id,))
    prog = await pc.fetchone()
    if not prog:
        raise HTTPException(status_code=404, detail="Program not found")
    ec = await db.execute("SELECT COUNT(*) FROM training_enrollments WHERE training_id = ?", (body.training_id,))
    count = (await ec.fetchone())[0]
    if count >= prog["capacity"]:
        raise HTTPException(status_code=400, detail="Program is full")
    cursor = await db.execute("INSERT INTO training_enrollments (training_id, employee_id) VALUES (?, ?)", (body.training_id, emp_id))
    await db.commit()
    return {"id": cursor.lastrowid, "message": "Enrolled successfully"}

@router.put("/enrollments/{enr_id}")
async def update_enrollment(enr_id: int, user=Depends(get_current_user), db: aiosqlite.Connection = Depends(get_db)):
    await db.execute("UPDATE training_enrollments SET status = 'completed' WHERE id = ?", (enr_id,))
    await db.commit()
    return {"message": "Enrollment updated"}
