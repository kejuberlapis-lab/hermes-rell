"""
Performance routes: KPIs, OKRs, performance reviews.
"""
from fastapi import APIRouter, Depends, HTTPException, Query
from pydantic import BaseModel
from typing import Optional
from app.database import get_db
from app.services.auth_service import get_current_user
import aiosqlite

router = APIRouter(prefix="/performance", tags=["performance"])

def _uid(user):
    return user.get("user_id") or user.get("id")

# --- KPI ---
class KPICreate(BaseModel):
    employee_id: int
    period: str
    target: Optional[str] = None
    actual: Optional[str] = None
    score: Optional[float] = None
    description: Optional[str] = None

class KPIUpdate(BaseModel):
    target: Optional[str] = None
    actual: Optional[str] = None
    score: Optional[float] = None
    description: Optional[str] = None

@router.get("/kpis")
async def list_kpis(employee_id: Optional[int] = None, period: Optional[str] = None, user=Depends(get_current_user), db: aiosqlite.Connection = Depends(get_db)):
    conditions, params = [], []
    if user.get("role") == "employee":
        cursor = await db.execute("SELECT employee_id FROM users WHERE id = ?", (_uid(user),))
        row = await cursor.fetchone()
        conditions.append("k.employee_id = ?")
        params.append(row["employee_id"] if row and row["employee_id"] else _uid(user))
    if employee_id:
        conditions.append("k.employee_id = ?")
        params.append(employee_id)
    if period:
        conditions.append("k.period = ?")
        params.append(period)
    where = " WHERE " + " AND ".join(conditions) if conditions else ""
    q = f"SELECT k.*, e.full_name FROM kpis k JOIN employees e ON k.employee_id = e.id {where} ORDER BY k.created_at DESC"
    cursor = await db.execute(q, params)
    rows = await cursor.fetchall()
    return {"kpis": [dict(r) for r in rows]}

@router.post("/kpis", status_code=201)
async def create_kpi(body: KPICreate, user=Depends(get_current_user), db: aiosqlite.Connection = Depends(get_db)):
    cursor = await db.execute("INSERT INTO kpis (employee_id, period, target, actual, score, description) VALUES (?, ?, ?, ?, ?, ?)",
        (body.employee_id, body.period, body.target, body.actual, body.score, body.description))
    await db.commit()
    return {"id": cursor.lastrowid, "message": "KPI created"}

@router.put("/kpis/{kpi_id}")
async def update_kpi(kpi_id: int, body: KPIUpdate, user=Depends(get_current_user), db: aiosqlite.Connection = Depends(get_db)):
    fields = {k: v for k, v in body.dict().items() if v is not None}
    if not fields:
        raise HTTPException(status_code=400, detail="No fields to update")
    set_clause = ", ".join(f"{k} = ?" for k in fields)
    await db.execute(f"UPDATE kpis SET {set_clause} WHERE id = ?", list(fields.values()) + [kpi_id])
    await db.commit()
    return {"message": "KPI updated"}

@router.delete("/kpis/{kpi_id}")
async def delete_kpi(kpi_id: int, user=Depends(get_current_user), db: aiosqlite.Connection = Depends(get_db)):
    await db.execute("DELETE FROM kpis WHERE id = ?", (kpi_id,))
    await db.commit()
    return {"message": "KPI deleted"}

# --- OKR ---
class OKRCreate(BaseModel):
    employee_id: int
    objective: str
    key_result: str
    progress: Optional[float] = 0
    period: Optional[str] = None

class OKRUpdate(BaseModel):
    objective: Optional[str] = None
    key_result: Optional[str] = None
    progress: Optional[float] = None
    period: Optional[str] = None
    status: Optional[str] = None

@router.get("/okrs")
async def list_okrs(employee_id: Optional[int] = None, period: Optional[str] = None, user=Depends(get_current_user), db: aiosqlite.Connection = Depends(get_db)):
    conditions, params = [], []
    if user.get("role") == "employee":
        cursor = await db.execute("SELECT employee_id FROM users WHERE id = ?", (_uid(user),))
        row = await cursor.fetchone()
        conditions.append("o.employee_id = ?")
        params.append(row["employee_id"] if row and row["employee_id"] else _uid(user))
    if employee_id:
        conditions.append("o.employee_id = ?")
        params.append(employee_id)
    if period:
        conditions.append("o.period = ?")
        params.append(period)
    where = " WHERE " + " AND ".join(conditions) if conditions else ""
    q = f"SELECT o.*, e.full_name FROM okrs o JOIN employees e ON o.employee_id = e.id {where} ORDER BY o.employee_id"
    cursor = await db.execute(q, params)
    rows = await cursor.fetchall()
    return {"okrs": [dict(r) for r in rows]}

@router.post("/okrs", status_code=201)
async def create_okr(body: OKRCreate, user=Depends(get_current_user), db: aiosqlite.Connection = Depends(get_db)):
    cursor = await db.execute("INSERT INTO okrs (employee_id, objective, key_result, progress, period) VALUES (?, ?, ?, ?, ?)",
        (body.employee_id, body.objective, body.key_result, body.progress, body.period))
    await db.commit()
    return {"id": cursor.lastrowid, "message": "OKR created"}

@router.put("/okrs/{okr_id}")
async def update_okr(okr_id: int, body: OKRUpdate, user=Depends(get_current_user), db: aiosqlite.Connection = Depends(get_db)):
    fields = {k: v for k, v in body.dict().items() if v is not None}
    if not fields:
        raise HTTPException(status_code=400, detail="No fields to update")
    set_clause = ", ".join(f"{k} = ?" for k in fields)
    await db.execute(f"UPDATE okrs SET {set_clause} WHERE id = ?", list(fields.values()) + [okr_id])
    await db.commit()
    return {"message": "OKR updated"}

@router.delete("/okrs/{okr_id}")
async def delete_okr(okr_id: int, user=Depends(get_current_user), db: aiosqlite.Connection = Depends(get_db)):
    await db.execute("DELETE FROM okrs WHERE id = ?", (okr_id,))
    await db.commit()
    return {"message": "OKR deleted"}

# --- Performance Reviews ---
class ReviewCreate(BaseModel):
    employee_id: int
    reviewer_id: Optional[int] = None
    period: str
    score: Optional[float] = None
    comments: Optional[str] = None
    review_type: str = "manager"

class ReviewUpdate(BaseModel):
    period: Optional[str] = None
    score: Optional[float] = None
    comments: Optional[str] = None
    review_type: Optional[str] = None

@router.get("/reviews")
async def list_reviews(employee_id: Optional[int] = None, period: Optional[str] = None, user=Depends(get_current_user), db: aiosqlite.Connection = Depends(get_db)):
    conditions, params = [], []
    role = user.get("role", "employee")
    if role == "employee":
        cursor = await db.execute("SELECT employee_id FROM users WHERE id = ?", (_uid(user),))
        row = await cursor.fetchone()
        conditions.append("pr.employee_id = ?")
        params.append(row["employee_id"] if row and row["employee_id"] else _uid(user))
    elif role == "manager":
        cursor = await db.execute("SELECT employee_id FROM users WHERE id = ?", (_uid(user),))
        row = await cursor.fetchone()
        mgr_eid = row["employee_id"] if row and row["employee_id"] else _uid(user)
        conditions.append("(pr.employee_id = ? OR pr.reviewer_id = ? OR pr.employee_id IN (SELECT id FROM employees WHERE manager_id = ?))")
        params.extend([mgr_eid, mgr_eid, mgr_eid])
    if employee_id:
        conditions.append("pr.employee_id = ?")
        params.append(employee_id)
    if period:
        conditions.append("pr.period = ?")
        params.append(period)
    where = " WHERE " + " AND ".join(conditions) if conditions else ""
    q = f"""SELECT pr.*, e.full_name as emp_name, r.full_name as reviewer_name
            FROM performance_reviews pr
            JOIN employees e ON pr.employee_id = e.id
            JOIN employees r ON pr.reviewer_id = r.id
            {where} ORDER BY pr.created_at DESC"""
    cursor = await db.execute(q, params)
    rows = await cursor.fetchall()
    return {"reviews": [dict(r) for r in rows]}

@router.post("/reviews", status_code=201)
async def create_review(body: ReviewCreate, user=Depends(get_current_user), db: aiosqlite.Connection = Depends(get_db)):
    if user.get("role") not in ("super_admin", "director", "manager"):
        raise HTTPException(status_code=403, detail="Manager, director or admin access required to evaluate performance")
    
    reviewer_id = body.reviewer_id
    if not reviewer_id:
        cursor = await db.execute("SELECT employee_id FROM users WHERE id = ?", (_uid(user),))
        row = await cursor.fetchone()
        reviewer_id = row["employee_id"] if row and row["employee_id"] else _uid(user)

    cursor = await db.execute(
        "INSERT INTO performance_reviews (employee_id, reviewer_id, period, score, comments, review_type) VALUES (?, ?, ?, ?, ?, ?)",
        (body.employee_id, reviewer_id, body.period, body.score, body.comments, body.review_type)
    )
    await db.commit()
    return {"id": cursor.lastrowid, "message": "Review created successfully"}

@router.put("/reviews/{review_id}")
async def update_review(review_id: int, body: ReviewUpdate, user=Depends(get_current_user), db: aiosqlite.Connection = Depends(get_db)):
    fields = {k: v for k, v in body.dict().items() if v is not None}
    if not fields:
        raise HTTPException(status_code=400, detail="No fields to update")
    set_clause = ", ".join(f"{k} = ?" for k in fields)
    await db.execute(f"UPDATE performance_reviews SET {set_clause} WHERE id = ?", list(fields.values()) + [review_id])
    await db.commit()
    return {"message": "Review updated"}

@router.delete("/reviews/{review_id}")
async def delete_review(review_id: int, user=Depends(get_current_user), db: aiosqlite.Connection = Depends(get_db)):
    await db.execute("DELETE FROM performance_reviews WHERE id = ?", (review_id,))
    await db.commit()
    return {"message": "Review deleted"}
