"""
Recruitment routes: job requisitions, applicants, interviews.
"""
from fastapi import APIRouter, Depends, HTTPException, Query
from pydantic import BaseModel
from typing import Optional
from app.database import get_db
from app.services.auth_service import get_current_user
import aiosqlite

router = APIRouter(prefix="/recruitment", tags=["recruitment"])

def _uid(user):
    return user.get("user_id") or user.get("id")

# --- Job Requisitions ---
class RequisitionCreate(BaseModel):
    title: str
    department_id: Optional[int] = None
    headcount: Optional[int] = 1
    salary_range: Optional[str] = None

class RequisitionUpdate(BaseModel):
    title: Optional[str] = None
    department_id: Optional[int] = None
    headcount: Optional[int] = None
    salary_range: Optional[str] = None
    status: Optional[str] = None

@router.get("/requisitions")
async def list_requisitions(status: Optional[str] = None, user=Depends(get_current_user), db: aiosqlite.Connection = Depends(get_db)):
    conditions, params = [], []
    if status:
        conditions.append("jr.status = ?")
        params.append(status)
    where = " WHERE " + " AND ".join(conditions) if conditions else ""
    cursor = await db.execute(f"SELECT jr.*, d.name as department_name FROM job_requisitions jr LEFT JOIN departments d ON jr.department_id = d.id {where} ORDER BY jr.created_at DESC", params)
    rows = await cursor.fetchall()
    return {"requisitions": [dict(r) for r in rows]}

@router.post("/requisitions", status_code=201)
async def create_requisition(body: RequisitionCreate, user=Depends(get_current_user), db: aiosqlite.Connection = Depends(get_db)):
    cursor = await db.execute(
        "INSERT INTO job_requisitions (title, department_id, headcount, salary_range, created_by) VALUES (?, ?, ?, ?, ?)",
        (body.title, body.department_id, body.headcount, body.salary_range, _uid(user))
    )
    await db.commit()
    return {"id": cursor.lastrowid, "message": "Requisition created"}

@router.put("/requisitions/{req_id}")
async def update_requisition(req_id: int, body: RequisitionUpdate, user=Depends(get_current_user), db: aiosqlite.Connection = Depends(get_db)):
    fields = {k: v for k, v in body.dict().items() if v is not None}
    if not fields:
        raise HTTPException(status_code=400, detail="No fields to update")
    set_clause = ", ".join(f"{k} = ?" for k in fields)
    await db.execute(f"UPDATE job_requisitions SET {set_clause} WHERE id = ?", list(fields.values()) + [req_id])
    await db.commit()
    return {"message": "Requisition updated"}

@router.delete("/requisitions/{req_id}")
async def delete_requisition(req_id: int, user=Depends(get_current_user), db: aiosqlite.Connection = Depends(get_db)):
    if user.get("role") not in ("super_admin", "director"):
        raise HTTPException(status_code=403, detail="Admin or Director access required")
    await db.execute("DELETE FROM job_requisitions WHERE id = ?", (req_id,))
    await db.commit()
    return {"message": "Requisition deleted"}

# --- Applicants ---
class ApplicantCreate(BaseModel):
    requisition_id: int
    full_name: str
    email: str
    phone: Optional[str] = None
    resume_path: Optional[str] = None
    source: Optional[str] = None

class ApplicantUpdate(BaseModel):
    full_name: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None
    status: Optional[str] = None

@router.get("/applicants")
async def list_applicants(requisition_id: Optional[int] = None, user=Depends(get_current_user), db: aiosqlite.Connection = Depends(get_db)):
    conditions, params = [], []
    if requisition_id:
        conditions.append("a.requisition_id = ?")
        params.append(requisition_id)
    where = " WHERE " + " AND ".join(conditions) if conditions else ""
    cursor = await db.execute(f"SELECT a.*, jr.title as requisition_title FROM applicants a JOIN job_requisitions jr ON a.requisition_id = jr.id {where} ORDER BY a.created_at DESC", params)
    rows = await cursor.fetchall()
    return {"applicants": [dict(r) for r in rows]}

@router.post("/applicants", status_code=201)
async def create_applicant(body: ApplicantCreate, user=Depends(get_current_user), db: aiosqlite.Connection = Depends(get_db)):
    cursor = await db.execute("INSERT INTO applicants (requisition_id, full_name, email, phone, resume_path, source) VALUES (?, ?, ?, ?, ?, ?)",
        (body.requisition_id, body.full_name, body.email, body.phone, body.resume_path, body.source))
    await db.commit()
    return {"id": cursor.lastrowid, "message": "Applicant added"}

@router.put("/applicants/{app_id}")
async def update_applicant(app_id: int, body: ApplicantUpdate, user=Depends(get_current_user), db: aiosqlite.Connection = Depends(get_db)):
    fields = {k: v for k, v in body.dict().items() if v is not None}
    if not fields:
        raise HTTPException(status_code=400, detail="No fields to update")
    set_clause = ", ".join(f"{k} = ?" for k in fields)
    await db.execute(f"UPDATE applicants SET {set_clause} WHERE id = ?", list(fields.values()) + [app_id])
    await db.commit()
    return {"message": "Applicant updated"}

# --- Interviews ---
class InterviewCreate(BaseModel):
    applicant_id: int
    interviewer_id: int
    scheduled_at: str

class InterviewUpdate(BaseModel):
    notes: Optional[str] = None
    rating: Optional[float] = None
    status: Optional[str] = None

@router.get("/interviews")
async def list_interviews(status: Optional[str] = None, user=Depends(get_current_user), db: aiosqlite.Connection = Depends(get_db)):
    conditions, params = [], []
    if status:
        conditions.append("i.status = ?")
        params.append(status)
    where = " WHERE " + " AND ".join(conditions) if conditions else ""
    cursor = await db.execute(f"""SELECT i.*, a.full_name as applicant_name, r.full_name as interviewer_name
        FROM interviews i JOIN applicants a ON i.applicant_id = a.id
        JOIN employees r ON i.interviewer_id = r.id {where} ORDER BY i.scheduled_at DESC""", params)
    rows = await cursor.fetchall()
    return {"interviews": [dict(r) for r in rows]}

@router.post("/interviews", status_code=201)
async def create_interview(body: InterviewCreate, user=Depends(get_current_user), db: aiosqlite.Connection = Depends(get_db)):
    cursor = await db.execute("INSERT INTO interviews (applicant_id, interviewer_id, scheduled_at) VALUES (?, ?, ?)",
        (body.applicant_id, body.interviewer_id, body.scheduled_at))
    await db.commit()
    return {"id": cursor.lastrowid, "message": "Interview scheduled"}

@router.put("/interviews/{int_id}")
async def update_interview(int_id: int, body: InterviewUpdate, user=Depends(get_current_user), db: aiosqlite.Connection = Depends(get_db)):
    fields = {k: v for k, v in body.dict().items() if v is not None}
    if not fields:
        raise HTTPException(status_code=400, detail="No fields to update")
    set_clause = ", ".join(f"{k} = ?" for k in fields)
    await db.execute(f"UPDATE interviews SET {set_clause} WHERE id = ?", list(fields.values()) + [int_id])
    await db.commit()
    return {"message": "Interview updated"}
