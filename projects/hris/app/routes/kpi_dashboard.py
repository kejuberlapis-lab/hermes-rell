"""
KPI Dashboard API Routes
Provides endpoints for KPI data retrieval and management
"""
from fastapi import APIRouter, Depends, HTTPException, Query
from pydantic import BaseModel
from typing import Optional, List
from app.database import get_db
from app.services.auth_service import get_current_user
import aiosqlite
import json

router = APIRouter(prefix="/kpi-dashboard", tags=["kpi-dashboard"])

class KPITemplateResponse(BaseModel):
    id: int
    template_name: str
    department: str
    position: str
    kpi_name: str
    formula_name: Optional[str]
    formula: Optional[str]
    target_standard: Optional[str]
    weight_percentage: float
    scoring_scale: Optional[dict]
    transition_notes: Optional[str]

class EmployeeKPIResponse(BaseModel):
    id: int
    employee_id: int
    employee_name: str
    department: str
    template_name: str
    kpi_name: str
    period: str
    target_value: Optional[str]
    actual_value: Optional[str]
    score: Optional[float]
    achievement_percentage: Optional[float]
    comments: Optional[str]

class KPISummary(BaseModel):
    total_templates: int
    total_assignments: int
    departments: List[str]
    positions: List[str]

@router.get("/summary")
async def get_kpi_summary(user=Depends(get_current_user), db: aiosqlite.Connection = Depends(get_db)):
    """Get KPI dashboard summary"""
    cursor = await db.execute("SELECT COUNT(*) FROM kpi_templates")
    template_count = (await cursor.fetchone())[0]
    
    cursor = await db.execute("SELECT COUNT(*) FROM employee_kpis")
    assignment_count = (await cursor.fetchone())[0]
    
    cursor = await db.execute("SELECT DISTINCT department FROM kpi_templates")
    departments = [row[0] for row in await cursor.fetchall()]
    
    cursor = await db.execute("SELECT DISTINCT position FROM kpi_templates")
    positions = [row[0] for row in await cursor.fetchall()]
    
    return KPISummary(
        total_templates=template_count,
        total_assignments=assignment_count,
        departments=departments,
        positions=positions
    )

@router.get("/templates")
async def get_kpi_templates(
    department: Optional[str] = None,
    position: Optional[str] = None,
    user=Depends(get_current_user),
    db: aiosqlite.Connection = Depends(get_db)
):
    """Get KPI templates with optional filtering"""
    conditions, params = [], []
    
    if department:
        conditions.append("kt.department = ?")
        params.append(department)
    if position:
        conditions.append("kt.position = ?")
        params.append(position)
    
    where = " WHERE " + " AND ".join(conditions) if conditions else ""
    
    query = f"""
        SELECT kt.*, 
            (SELECT kf.name FROM kpi_formulas kf WHERE kf.formula LIKE kt.formula || '%') as formula_name,
            kf.formula as formula_ref, 
            kf.description as formula_description
        FROM kpi_templates kt
        LEFT JOIN kpi_formulas kf ON 1=0
        {where}
        ORDER BY kt.department, kt.position, kt.weight_percentage DESC
    """
    
    cursor = await db.execute(query, params)
    rows = await cursor.fetchall()
    
    templates = []
    for row in rows:
        template_dict = dict(row)
        if template_dict.get('scoring_scale'):
            try:
                template_dict['scoring_scale'] = json.loads(template_dict['scoring_scale'])
            except:
                template_dict['scoring_scale'] = {}
        templates.append(template_dict)
    
    return {"templates": templates}

@router.get("/assignments")
async def get_employee_kpi_assignments(
    employee_id: Optional[int] = None,
    department: Optional[str] = None,
    period: Optional[str] = None,
    user=Depends(get_current_user),
    db: aiosqlite.Connection = Depends(get_db)
):
    """Get employee KPI assignments with optional filtering"""
    conditions, params = [], []
    
    if employee_id:
        conditions.append("ek.employee_id = ?")
        params.append(employee_id)
    if department:
        conditions.append("d.name = ?")
        params.append(department)
    if period:
        conditions.append("ek.period = ?")
        params.append(period)
    
    where = " WHERE " + " AND ".join(conditions) if conditions else ""
    
    query = f"""
        SELECT 
            ek.id,
            ek.employee_id,
            e.full_name as employee_name,
            d.name as department,
            kt.template_name,
            kt.kpi_name,
            ek.period,
            ek.target_value,
            ek.actual_value,
            ek.score,
            ek.achievement_percentage,
            ek.comments
        FROM employee_kpis ek
        JOIN employees e ON ek.employee_id = e.id
        JOIN kpi_templates kt ON ek.template_id = kt.id
        JOIN departments d ON e.department_id = d.id
        {where}
        ORDER BY e.department_id, e.id, kt.weight_percentage DESC
    """
    
    cursor = await db.execute(query, params)
    rows = await cursor.fetchall()
    
    return {"assignments": [dict(row) for row in rows]}

@router.get("/department-stats")
async def get_department_statistics(
    user=Depends(get_current_user),
    db: aiosqlite.Connection = Depends(get_db)
):
    """Get KPI statistics by department"""
    query = """
        SELECT 
            d.name as department,
            COUNT(DISTINCT kt.id) as template_count,
            COUNT(DISTINCT ek.employee_id) as employee_count,
            COUNT(ek.id) as assignment_count,
            AVG(ek.score) as avg_score
        FROM departments d
        LEFT JOIN employees e ON d.id = e.department_id
        LEFT JOIN employee_kpis ek ON e.id = ek.employee_id
        LEFT JOIN kpi_templates kt ON ek.template_id = kt.id
        GROUP BY d.id, d.name
        ORDER BY d.name
    """
    
    cursor = await db.execute(query)
    rows = await cursor.fetchall()
    
    return {"departments": [dict(row) for row in rows]}

@router.get("/scoring-scale")
async def get_scoring_scale():
    """Get the KPI scoring scale for transition phase"""
    return {
        "scoring_scale": {
            "1": {
                "name": "Sangat Kurang",
                "description": "Pencapaian di bawah 50% dari target",
                "range": "< 50%"
            },
            "2": {
                "name": "Kurang",
                "description": "Pencapaian 50% - 69% dari target",
                "range": "50% - 69%"
            },
            "3": {
                "name": "Memenuhi Harapan",
                "description": "Pencapaian 70% - 85% dari target (Batas aman dalam fase transisi)",
                "range": "70% - 85%"
            },
            "4": {
                "name": "Baik",
                "description": "Pencapaian 86% - 100% dari target",
                "range": "86% - 100%"
            },
            "5": {
                "name": "Sangat Baik",
                "description": "Pencapaian di atas 100% dari target",
                "range": "> 100%"
            }
        },
        "phase": "Fase Transisi 2026",
        "notes": "Skala ini dirancang untuk pembentukan kebiasaan dan kedisiplinan pelaporan"
    }

@router.get("/rewards")
async def get_reward_scheme():
    """Get the reward scheme for 2026"""
    return {
        "rewards": [
            {
                "name": "Tambahan Cuti Berbayar (Extra PTO)",
                "description": "1 hari kerja tambahan untuk karyawan dengan skor KPI minimal 95% selama 4 kuartal terakhir",
                "requirement": "Employee of the Month selama 4 kuartal",
                "type": "non_financial"
            },
            {
                "name": "Fleksibilitas Kerja (WFH/WFA Privileges)",
                "description": "Work From Home 1 hari dalam satu bulan dengan persetujuan Manajer",
                "requirement": "Untuk divisi Presales, Digital Marketing, atau Sales dengan target administrasi tertentu",
                "type": "non_financial"
            },
            {
                "name": "Sponsor & Pengembangan Karir",
                "description": "Pembiayaan penuh ujian sertifikasi profesional atau pelatihan tingkat internasional",
                "requirement": "Karyawan berprestasi (Tim Teknis, Presales, Finance)",
                "type": "development"
            },
            {
                "name": "Penghargaan Internal (Employee of the Month)",
                "description": "Sertifikat, plakat, dan penghargaan uang sebesar Rp 250.000",
                "requirement": "Diberikan setiap bulan di hadapan seluruh tim",
                "type": "recognition"
            }
        ]
    }

class EmployeeKPIScoreUpdate(BaseModel):
    actual_value: Optional[str] = None
    score: Optional[float] = None
    achievement_percentage: Optional[float] = None
    comments: Optional[str] = None

class EmployeeKPICreate(BaseModel):
    employee_id: int
    template_id: int
    period: str
    target_value: Optional[str] = None
    actual_value: Optional[str] = None
    score: Optional[float] = None
    achievement_percentage: Optional[float] = None
    comments: Optional[str] = None

@router.put("/assignments/{assignment_id}")
async def update_kpi_assignment(
    assignment_id: int,
    body: EmployeeKPIScoreUpdate,
    user=Depends(get_current_user),
    db: aiosqlite.Connection = Depends(get_db)
):
    """Update KPI score and actual achievement for an employee"""
    if user.get("role") not in ("super_admin", "director", "manager"):
        raise HTTPException(status_code=403, detail="Manager, director or admin access required to evaluate KPI")
    
    uid = user.get("user_id") or user.get("id")
    cursor = await db.execute("SELECT employee_id FROM users WHERE id = ?", (uid,))
    row = await cursor.fetchone()
    reviewer_id = row["employee_id"] if row and row["employee_id"] else uid

    fields = {k: v for k, v in body.dict().items() if v is not None}
    if not fields:
        raise HTTPException(status_code=400, detail="No fields to update")
    
    fields["reviewed_by"] = reviewer_id
    fields["reviewed_at"] = "CURRENT_TIMESTAMP"
    
    set_clause = ", ".join(f"{k} = ?" if k != "reviewed_at" else f"{k} = CURRENT_TIMESTAMP" for k in fields)
    params = [v for k, v in fields.items() if k != "reviewed_at"] + [assignment_id]
    
    await db.execute(f"UPDATE employee_kpis SET {set_clause} WHERE id = ?", params)
    await db.commit()
    return {"message": "KPI evaluation saved successfully"}

@router.post("/assignments", status_code=201)
async def create_kpi_assignment(
    body: EmployeeKPICreate,
    user=Depends(get_current_user),
    db: aiosqlite.Connection = Depends(get_db)
):
    """Assign a KPI template to an employee"""
    if user.get("role") not in ("super_admin", "director", "manager"):
        raise HTTPException(status_code=403, detail="Manager, director or admin access required")
    
    uid = user.get("user_id") or user.get("id")
    cursor = await db.execute("SELECT employee_id FROM users WHERE id = ?", (uid,))
    row = await cursor.fetchone()
    reviewer_id = row["employee_id"] if row and row["employee_id"] else uid

    cursor = await db.execute("""
        INSERT INTO employee_kpis (employee_id, template_id, period, target_value, actual_value, score, achievement_percentage, comments, reviewed_by)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (body.employee_id, body.template_id, body.period, body.target_value, body.actual_value, body.score, body.achievement_percentage, body.comments, reviewer_id))
    await db.commit()
    return {"id": cursor.lastrowid, "message": "KPI assigned successfully"}
