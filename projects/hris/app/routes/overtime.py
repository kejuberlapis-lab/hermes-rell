"""
Overtime routes: submit, approve/reject, list.
"""
from fastapi import APIRouter, Depends, HTTPException, Query
from pydantic import BaseModel
from typing import Optional
from app.database import get_db
from app.services.auth_service import get_current_user
import aiosqlite

router = APIRouter(prefix="/overtime", tags=["overtime"])

def _uid(user):
    return user.get("user_id") or user.get("id")

async def _resolve_emp_id(db, user):
    cursor = await db.execute("SELECT employee_id FROM users WHERE id = ?", (_uid(user),))
    row = await cursor.fetchone()
    return row["employee_id"] if row and row["employee_id"] else _uid(user)

async def _notify_manager(db, emp_id, title, message):
    cursor = await db.execute("SELECT manager_id FROM employees WHERE id = ?", (emp_id,))
    mgr = await cursor.fetchone()
    if mgr and mgr["manager_id"]:
        ucur = await db.execute("SELECT id FROM users WHERE employee_id = ?", (mgr["manager_id"],))
        u = await ucur.fetchone()
        if u:
            await db.execute("INSERT INTO notifications (user_id, title, message) VALUES (?, ?, ?)", (u["id"], title, message))
            await db.commit()

class OvertimeSubmit(BaseModel):
    employee_id: Optional[int] = None
    date: str
    hours: float
    reason: Optional[str] = None

class OvertimeAction(BaseModel):
    status: str

@router.post("", status_code=201)
async def submit_overtime(body: OvertimeSubmit, user=Depends(get_current_user), db: aiosqlite.Connection = Depends(get_db)):
    emp_id = body.employee_id
    if user.get("role") == "employee" or not emp_id:
        emp_id = await _resolve_emp_id(db, user)
    cursor = await db.execute("INSERT INTO overtime (employee_id, date, hours, reason) VALUES (?, ?, ?, ?)", (emp_id, body.date, body.hours, body.reason))
    await db.commit()
    await _notify_manager(db, emp_id, "Overtime Request", f"New overtime request: {body.hours}h on {body.date}")
    return {"id": cursor.lastrowid, "message": "Overtime submitted"}

@router.put("/{ot_id}")
async def update_overtime(ot_id: int, body: OvertimeAction, user=Depends(get_current_user), db: aiosqlite.Connection = Depends(get_db)):
    if user.get("role") not in ("super_admin", "director", "manager"):
        raise HTTPException(status_code=403, detail="Manager, director or admin access required")
    if body.status not in ("approved", "rejected"):
        raise HTTPException(status_code=400, detail="Status must be approved or rejected")
    mgr_eid = await _resolve_emp_id(db, user)
    
    # Manager or Director cannot approve own overtime request
    if user.get("role") in ("manager", "director"):
        chk = await db.execute("SELECT employee_id FROM overtime WHERE id = ?", (ot_id,))
        o_row = await chk.fetchone()
        if o_row and o_row["employee_id"] == mgr_eid:
            raise HTTPException(status_code=400, detail="Tidak dapat menyetujui lembur milik sendiri.")

    await db.execute("UPDATE overtime SET status = ?, approved_by = ?, approved_at = CURRENT_TIMESTAMP WHERE id = ?", (body.status, mgr_eid, ot_id))
    await db.commit()
    return {"message": f"Overtime {body.status}"}

@router.get("")
async def list_overtime(employee_id: Optional[int] = None, status: Optional[str] = None, skip: int = 0, limit: int = 50, user=Depends(get_current_user), db: aiosqlite.Connection = Depends(get_db)):
    conditions, params = [], []
    role = user.get("role", "employee")
    if role == "employee":
        emp_id = await _resolve_emp_id(db, user)
        conditions.append("o.employee_id = ?")
        params.append(emp_id)
    elif role == "manager":
        mgr_eid = await _resolve_emp_id(db, user)
        conditions.append("(o.employee_id = ? OR o.employee_id IN (SELECT id FROM employees WHERE manager_id = ?))")
        params.extend([mgr_eid, mgr_eid])
    if employee_id:
        conditions.append("o.employee_id = ?")
        params.append(employee_id)
    if status:
        conditions.append("o.status = ?")
        params.append(status)
    where = " WHERE " + " AND ".join(conditions) if conditions else ""
    q = f"""SELECT o.*, e.full_name FROM overtime o JOIN employees e ON o.employee_id = e.id
            {where} ORDER BY o.created_at DESC LIMIT ? OFFSET ?"""
    params.extend([limit, skip])
    cursor = await db.execute(q, params)
    rows = await cursor.fetchall()
    return {"overtime": [dict(r) for r in rows], "total": len(rows)}
