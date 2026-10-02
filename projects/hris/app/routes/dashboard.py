"""
Dashboard routes: aggregated stats.
"""
from fastapi import APIRouter, Depends
from datetime import date
from app.database import get_db
from app.services.auth_service import get_current_user
import aiosqlite

router = APIRouter(prefix="/dashboard", tags=["dashboard"])

@router.get("")
async def dashboard_stats(user=Depends(get_current_user), db: aiosqlite.Connection = Depends(get_db)):
    today = date.today().isoformat()
    current_month = date.today().month
    current_year = date.today().year

    cursor = await db.execute("SELECT COUNT(*) as total, SUM(CASE WHEN status='active' THEN 1 ELSE 0 END) as active FROM employees")
    emp_row = await cursor.fetchone()

    cursor = await db.execute("SELECT COUNT(*) as total FROM attendance WHERE date = ?", (today,))
    att_row = await cursor.fetchone()

    ot_pending = await db.execute("SELECT COUNT(*) FROM overtime WHERE status = 'pending'")
    ot_count = (await ot_pending.fetchone())[0]
    lv_pending = await db.execute("SELECT COUNT(*) FROM leaves WHERE status = 'pending'")
    lv_count = (await lv_pending.fetchone())[0]
    pr_pending = await db.execute("SELECT COUNT(*) FROM procurement_requests WHERE status = 'pending'")
    pr_count = (await pr_pending.fetchone())[0]

    cursor = await db.execute("SELECT COUNT(*) as processed, COALESCE(SUM(net_salary), 0) as total_payout FROM payroll WHERE period_month = ? AND period_year = ?", (current_month, current_year))
    payroll_row = await cursor.fetchone()

    cursor = await db.execute("SELECT COUNT(*) FROM departments")
    dept_count = (await cursor.fetchone())[0]

    return {
        "employees": {"total": emp_row["total"] or 0, "active": emp_row["active"] or 0},
        "attendance_today": {"total": att_row["total"] or 0},
        "pending_approvals": {"overtime": ot_count, "leave": lv_count, "procurement": pr_count, "total": ot_count + lv_count + pr_count},
        "payroll_this_month": {"processed": payroll_row["processed"] or 0, "total_payout": payroll_row["total_payout"] or 0},
        "departments": dept_count,
    }
