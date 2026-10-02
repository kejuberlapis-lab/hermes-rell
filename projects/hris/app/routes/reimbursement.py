"""
Reimbursement routes: submit/approve claims.
"""
from fastapi import APIRouter, Depends, HTTPException, Query
from pydantic import BaseModel
from typing import Optional
from app.database import get_db
from app.services.auth_service import get_current_user
import aiosqlite

router = APIRouter(prefix="/reimbursements", tags=["reimbursements"])

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

class ReimbursementSubmit(BaseModel):
    employee_id: Optional[int] = None
    category: str
    amount: float
    description: Optional[str] = None

class ReimbursementAction(BaseModel):
    status: str

@router.post("", status_code=201)
async def submit_reimbursement(body: ReimbursementSubmit, user=Depends(get_current_user), db: aiosqlite.Connection = Depends(get_db)):
    emp_id = body.employee_id
    if user.get("role") == "employee" or not emp_id:
        emp_id = await _resolve_emp_id(db, user)
    cursor = await db.execute("INSERT INTO reimbursement (employee_id, category, amount, description) VALUES (?, ?, ?, ?)",
        (emp_id, body.category, body.amount, body.description))
    await db.commit()
    await _notify_manager(db, emp_id, "Reimbursement Request", f"Reimbursement: {body.category} - ${body.amount}")
    return {"id": cursor.lastrowid, "message": "Reimbursement submitted"}

@router.put("/{reimb_id}")
async def update_reimbursement(reimb_id: int, body: ReimbursementAction, user=Depends(get_current_user), db: aiosqlite.Connection = Depends(get_db)):
    if user.get("role") not in ("super_admin", "director", "manager"):
        raise HTTPException(status_code=403, detail="Manager, director or admin access required")
    if body.status not in ("approved", "rejected"):
        raise HTTPException(status_code=400, detail="Status must be approved or rejected")
    emp_id = await _resolve_emp_id(db, user)
    
    # Manager or Director cannot approve own reimbursement request
    if user.get("role") in ("manager", "director"):
        chk = await db.execute("SELECT employee_id FROM reimbursement WHERE id = ?", (reimb_id,))
        r_row = await chk.fetchone()
        if r_row and r_row["employee_id"] == emp_id:
            raise HTTPException(status_code=400, detail="Tidak dapat menyetujui klaim reimbursement milik sendiri.")

    await db.execute("UPDATE reimbursement SET status = ?, approved_by = ? WHERE id = ?", (body.status, emp_id, reimb_id))
    await db.commit()
    return {"message": f"Reimbursement {body.status}"}

@router.get("")
async def list_reimbursements(employee_id: Optional[int] = None, status: Optional[str] = None, skip: int = 0, limit: int = 50, user=Depends(get_current_user), db: aiosqlite.Connection = Depends(get_db)):
    conditions, params = [], []
    role = user.get("role", "employee")
    if role == "employee":
        emp_id = await _resolve_emp_id(db, user)
        conditions.append("r.employee_id = ?")
        params.append(emp_id)
    elif role == "manager":
        mgr_eid = await _resolve_emp_id(db, user)
        conditions.append("(r.employee_id = ? OR r.employee_id IN (SELECT id FROM employees WHERE manager_id = ?))")
        params.extend([mgr_eid, mgr_eid])
    if employee_id:
        conditions.append("r.employee_id = ?")
        params.append(employee_id)
    if status:
        conditions.append("r.status = ?")
        params.append(status)
    where = " WHERE " + " AND ".join(conditions) if conditions else ""
    q = f"""SELECT r.*, e.full_name FROM reimbursement r JOIN employees e ON r.employee_id = e.id
            {where} ORDER BY r.created_at DESC LIMIT ? OFFSET ?"""
    params.extend([limit, skip])
    cursor = await db.execute(q, params)
    rows = await cursor.fetchall()
    return {"reimbursements": [dict(r) for r in rows], "total": len(rows)}
