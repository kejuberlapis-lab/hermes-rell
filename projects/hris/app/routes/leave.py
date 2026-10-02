"""
Leave routes: submit, approve/reject, list, balances.
"""
from fastapi import APIRouter, Depends, HTTPException, Query
from pydantic import BaseModel
from typing import Optional
from datetime import date
from app.database import get_db
from app.services.auth_service import get_current_user
import aiosqlite

router = APIRouter(prefix="/leave", tags=["leave"])

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

class LeaveSubmit(BaseModel):
    employee_id: Optional[int] = None
    leave_type_id: int
    start_date: str
    end_date: str
    reason: Optional[str] = None

class LeaveAction(BaseModel):
    status: str

@router.post("", status_code=201)
async def submit_leave(body: LeaveSubmit, user=Depends(get_current_user), db: aiosqlite.Connection = Depends(get_db)):
    emp_id = body.employee_id
    if user.get("role") == "employee" or not emp_id:
        emp_id = await _resolve_emp_id(db, user)
    cursor = await db.execute(
        "INSERT INTO leaves (employee_id, leave_type_id, start_date, end_date, reason) VALUES (?, ?, ?, ?, ?)",
        (emp_id, body.leave_type_id, body.start_date, body.end_date, body.reason)
    )
    await db.commit()
    await _notify_manager(db, emp_id, "Leave Request", f"Leave request for {body.start_date} to {body.end_date}")
    return {"id": cursor.lastrowid, "message": "Leave submitted"}

@router.put("/{leave_id}")
async def update_leave(leave_id: int, body: LeaveAction, user=Depends(get_current_user), db: aiosqlite.Connection = Depends(get_db)):
    if user.get("role") not in ("super_admin", "director", "manager"):
        raise HTTPException(status_code=403, detail="Manager, director or admin access required")
    if body.status not in ("approved", "rejected"):
        raise HTTPException(status_code=400, detail="Status must be approved or rejected")
    mgr_eid = await _resolve_emp_id(db, user)
    
    # Manager or Director cannot approve own leave request
    if user.get("role") in ("manager", "director"):
        chk = await db.execute("SELECT employee_id FROM leaves WHERE id = ?", (leave_id,))
        l_row = await chk.fetchone()
        if l_row and l_row["employee_id"] == mgr_eid:
            raise HTTPException(status_code=400, detail="Tidak dapat menyetujui pengajuan cuti milik sendiri.")

    await db.execute("UPDATE leaves SET status = ?, approved_by = ?, approved_at = CURRENT_TIMESTAMP WHERE id = ?", (body.status, mgr_eid, leave_id))
    await db.commit()
    return {"message": f"Leave {body.status}"}

@router.get("")
async def list_leave(employee_id: Optional[int] = None, status: Optional[str] = None, skip: int = 0, limit: int = 50, user=Depends(get_current_user), db: aiosqlite.Connection = Depends(get_db)):
    conditions, params = [], []
    role = user.get("role", "employee")
    if role == "employee":
        emp_id = await _resolve_emp_id(db, user)
        conditions.append("l.employee_id = ?")
        params.append(emp_id)
    elif role == "manager":
        mgr_eid = await _resolve_emp_id(db, user)
        conditions.append("(l.employee_id = ? OR l.employee_id IN (SELECT id FROM employees WHERE manager_id = ?))")
        params.extend([mgr_eid, mgr_eid])
    if employee_id:
        conditions.append("l.employee_id = ?")
        params.append(employee_id)
    if status:
        conditions.append("l.status = ?")
        params.append(status)
    where = " WHERE " + " AND ".join(conditions) if conditions else ""
    q = f"""SELECT l.*, e.full_name, lt.name as leave_type_name FROM leaves l
            JOIN employees e ON l.employee_id = e.id
            LEFT JOIN leave_types lt ON l.leave_type_id = lt.id
            {where} ORDER BY l.created_at DESC LIMIT ? OFFSET ?"""
    params.extend([limit, skip])
    cursor = await db.execute(q, params)
    rows = await cursor.fetchall()
    return {"leaves": [dict(r) for r in rows], "total": len(rows)}

@router.get("/balances")
async def leave_balances(employee_id: Optional[int] = None, user=Depends(get_current_user), db: aiosqlite.Connection = Depends(get_db)):
    conditions, params = [], []
    if user.get("role") == "employee":
        emp_id = await _resolve_emp_id(db, user)
        conditions.append("l.employee_id = ?")
        params.append(emp_id)
    if employee_id:
        conditions.append("l.employee_id = ?")
        params.append(employee_id)
    where = " WHERE " + " AND ".join(conditions) if conditions else ""
    q = f"""SELECT lt.id, lt.name, lt.days_allowed,
            COUNT(CASE WHEN l.status = 'approved' THEN 1 END) as approved_count
            FROM leave_types lt
            LEFT JOIN leaves l ON lt.id = l.leave_type_id {where.replace('WHERE', 'AND') if where else ''}
            GROUP BY lt.id"""
    cursor = await db.execute(q, params if where else [])
    rows = await cursor.fetchall()
    return {"balances": [dict(r) for r in rows]}
