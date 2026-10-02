"""
HRIS FastAPI Application Entry Point.
Serves API routes and Jinja2 template pages.
"""
import os
import sys
from contextlib import asynccontextmanager
from fastapi import FastAPI, Request, Depends, HTTPException, Query
from typing import Optional
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse, HTMLResponse

# Ensure app module is importable
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app.database import init_db
from app.services.auth_service import decode_access_token, get_current_user

# --- Import all routers ---
from app.routes.auth import router as auth_router
from app.routes.employees import router as employees_router
from app.routes.departments import router as departments_router
from app.routes.attendance import router as attendance_router
from app.routes.overtime import router as overtime_router
from app.routes.leave import router as leave_router
from app.routes.payroll import router as payroll_router
from app.routes.performance import router as performance_router
from app.routes.recruitment import router as recruitment_router
from app.routes.procurement import router as procurement_router
from app.routes.assets import router as assets_router
from app.routes.notifications import router as notifications_router
from app.routes.dashboard import router as dashboard_router
from app.routes.documents import router as documents_router
from app.routes.training import router as training_router
from app.routes.reimbursement import router as reimbursement_router
from app.routes.exports import router as exports_router
from app.routes.travel import router as travel_router
from app.routes.kpi_dashboard import router as kpi_dashboard_router
from app.routes.settings import router as settings_router, get_all_settings

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Startup and shutdown events."""
    await init_db()
    yield

app = FastAPI(
    title="HRIS System",
    description="Human Resource Information System",
    version="1.0.0",
    lifespan=lifespan,
)

# --- Mount static files ---
STATIC_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "static")
os.makedirs(STATIC_DIR, exist_ok=True)
app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")

# --- Templates ---
TEMPLATE_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "templates")
os.makedirs(TEMPLATE_DIR, exist_ok=True)
templates = Jinja2Templates(directory=TEMPLATE_DIR)

# --- Include API routers ---
api_prefix = "/api"
app.include_router(auth_router, prefix=api_prefix)
app.include_router(employees_router, prefix=api_prefix)
app.include_router(departments_router, prefix=api_prefix)
app.include_router(attendance_router, prefix=api_prefix)
app.include_router(overtime_router, prefix=api_prefix)
app.include_router(leave_router, prefix=api_prefix)
app.include_router(payroll_router, prefix=api_prefix)
app.include_router(performance_router, prefix=api_prefix)
app.include_router(recruitment_router, prefix=api_prefix)
app.include_router(procurement_router, prefix=api_prefix)
app.include_router(assets_router, prefix=api_prefix)
app.include_router(notifications_router, prefix=api_prefix)
app.include_router(dashboard_router, prefix=api_prefix)
app.include_router(documents_router, prefix=api_prefix)
app.include_router(training_router, prefix=api_prefix)
app.include_router(reimbursement_router, prefix=api_prefix)
app.include_router(exports_router, prefix=api_prefix)
app.include_router(travel_router, prefix=api_prefix)
app.include_router(kpi_dashboard_router, prefix=api_prefix)
app.include_router(settings_router, prefix=api_prefix)


from app.database import init_db, get_db_connection

# --- Helper: extract user from cookie/header for template rendering ---
def get_user_from_request(request: Request):
    """Try to get current user from Authorization header or cookie."""
    token = request.cookies.get("token") or request.cookies.get("access_token")
    if not token:
        auth_header = request.headers.get("authorization", "")
        if auth_header.startswith("Bearer "):
            token = auth_header[7:]
    if not token:
        return None
    try:
        payload = decode_access_token(token)
        uid = payload.get("user_id") or payload.get("sub", 0)
        
        must_change = 0
        try:
            import sqlite3
            from app.database import DATABASE_PATH
            conn = sqlite3.connect(DATABASE_PATH)
            cursor = conn.cursor()
            cursor.execute("SELECT must_change_password FROM users WHERE id = ?", (int(uid),))
            row = cursor.fetchone()
            conn.close()
            if row and row[0] == 1:
                must_change = 1
        except Exception:
            pass

        return {
            "id": int(uid),
            "user_id": int(uid),
            "username": payload.get("username", ""),
            "role": payload.get("role", "employee"),
            "full_name": payload.get("full_name", payload.get("username", "")),
            "employee_id": payload.get("employee_id"),
            "must_change_password": must_change,
        }
    except Exception:
        return None


# --- Page routes (Jinja2 templates) ---

@app.api_route("/", methods=["GET", "HEAD"], response_class=HTMLResponse)
async def login_page(request: Request):
    """Render login page."""
    user = get_user_from_request(request)
    if user:
        return RedirectResponse(url="/dashboard", status_code=302)
    return templates.TemplateResponse("login.html", {"request": request})


@app.get("/profile", response_class=HTMLResponse)
async def profile_redirect(request: Request):
    """Redirect user to their own employee profile page."""
    user = get_user_from_request(request)
    if not user:
        return RedirectResponse(url="/", status_code=302)
    emp_id = user.get("employee_id") or user.get("id") or 1
    return RedirectResponse(url=f"/employees/{emp_id}", status_code=302)


@app.get("/dashboard", response_class=HTMLResponse)
async def dashboard_page(request: Request):
    """Render main dashboard with role-isolated live metrics."""
    user = get_user_from_request(request)
    if not user:
        return RedirectResponse(url="/", status_code=302)
    
    db = await get_db_connection()
    try:
        role = user.get("role", "employee")
        emp_id = user.get("employee_id") or user.get("id")

        kpi_data = {}
        if role == "employee":
            # Personal data & KPI for Staff
            att_count = (await (await db.execute("SELECT COUNT(*) FROM attendance WHERE employee_id = ? AND status='present'", (emp_id,))).fetchone())[0]
            pending_leaves = (await (await db.execute("SELECT COUNT(*) FROM leaves WHERE employee_id = ? AND status='pending'", (emp_id,))).fetchone())[0]
            
            # Fetch Staff KPI Review & Achievement
            cur_kpi = await db.execute("""
                SELECT ek.*, kt.kpi_name, kt.target_standard, kt.weight_percentage
                FROM employee_kpis ek
                JOIN kpi_templates kt ON ek.template_id = kt.id
                WHERE ek.employee_id = ?
                ORDER BY ek.id
            """, (emp_id,))
            staff_kpis = [dict(r) for r in await cur_kpi.fetchall()]
            
            cur_rev = await db.execute("""
                SELECT pr.*, e.full_name as reviewer_name, p.title as reviewer_pos
                FROM performance_reviews pr
                LEFT JOIN employees e ON pr.reviewer_id = e.id
                LEFT JOIN positions p ON e.position_id = p.id
                WHERE pr.employee_id = ?
                ORDER BY pr.id DESC LIMIT 1
            """, (emp_id,))
            staff_review_row = await cur_rev.fetchone()
            staff_review = dict(staff_review_row) if staff_review_row else None
            
            kpi_data = {
                "kpis": staff_kpis,
                "review": staff_review
            }
            
            cursor_recent = await db.execute("""
                SELECT e.*, d.name as department_name, p.title as position_title
                FROM employees e
                LEFT JOIN departments d ON e.department_id = d.id
                LEFT JOIN positions p ON e.position_id = p.id
                WHERE e.id = ?
            """, (emp_id,))
            recent_employees = [dict(r) for r in await cursor_recent.fetchall()]

            cursor_upcoming = await db.execute("""
                SELECT l.*, lt.name as leave_type_name, e.full_name, e.employee_id_str
                FROM leaves l
                LEFT JOIN leave_types lt ON l.leave_type_id = lt.id
                JOIN employees e ON l.employee_id = e.id
                WHERE l.employee_id = ?
                ORDER BY l.start_date DESC LIMIT 5
            """, (emp_id,))
            upcoming_leaves = [dict(r) for r in await cursor_upcoming.fetchall()]

            stats = {
                "total_employees": 1,
                "total_departments": 1,
                "present_today": att_count,
                "pending_approvals": pending_leaves,
            }
        elif role == "manager":
            # Manager sees team subordinates overview + team approval counts + Team KPI Achievements
            team_emp_count = (await (await db.execute("SELECT COUNT(*) FROM employees WHERE manager_id = ? AND status='active'", (emp_id,))).fetchone())[0]
            team_dept_count = (await (await db.execute("SELECT COUNT(DISTINCT department_id) FROM employees WHERE manager_id = ? OR id = ?", (emp_id, emp_id))).fetchone())[0]
            
            team_present = (await (await db.execute("""
                SELECT COUNT(DISTINCT a.employee_id) 
                FROM attendance a 
                JOIN employees e ON a.employee_id = e.id 
                WHERE (e.manager_id = ? OR e.id = ?) AND a.status='present' AND a.date = date('now')
            """, (emp_id, emp_id))).fetchone())[0]
            
            # Pending approvals from staff under this manager
            p_leaves = (await (await db.execute("SELECT COUNT(*) FROM leaves l JOIN employees e ON l.employee_id = e.id WHERE e.manager_id = ? AND l.status='pending'", (emp_id,))).fetchone())[0]
            p_ot = (await (await db.execute("SELECT COUNT(*) FROM overtime o JOIN employees e ON o.employee_id = e.id WHERE e.manager_id = ? AND o.status='pending'", (emp_id,))).fetchone())[0]
            p_reimb = (await (await db.execute("SELECT COUNT(*) FROM reimbursement r JOIN employees e ON r.employee_id = e.id WHERE e.manager_id = ? AND r.status='pending'", (emp_id,))).fetchone())[0]
            p_travel = (await (await db.execute("SELECT COUNT(*) FROM travel_requests tr JOIN employees e ON tr.employee_id = e.id WHERE e.manager_id = ? AND tr.status='pending_manager'", (emp_id,))).fetchone())[0]
            
            total_pending = p_leaves + p_ot + p_reimb + p_travel
            
            # Fetch Manager's Team KPI performance
            cur_team_kpi = await db.execute("""
                SELECT e.id, e.employee_id_str, e.full_name, p.title as position_title,
                       ROUND(AVG(ek.achievement_percentage), 1) as avg_achievement,
                       COUNT(ek.id) as kpi_count,
                       pr.score as review_score,
                       pr.comments as review_comments
                FROM employees e
                LEFT JOIN positions p ON e.position_id = p.id
                LEFT JOIN employee_kpis ek ON e.id = ek.employee_id
                LEFT JOIN performance_reviews pr ON e.id = pr.employee_id
                WHERE e.manager_id = ? OR e.id = ?
                GROUP BY e.id
                ORDER BY avg_achievement DESC
            """, (emp_id, emp_id))
            team_kpi_list = [dict(r) for r in await cur_team_kpi.fetchall()]
            
            kpi_data = {
                "team_kpis": team_kpi_list
            }
            
            cursor_recent = await db.execute("""
                SELECT e.*, d.name as department_name, p.title as position_title
                FROM employees e
                LEFT JOIN departments d ON e.department_id = d.id
                LEFT JOIN positions p ON e.position_id = p.id
                WHERE e.manager_id = ? OR e.id = ?
                ORDER BY (CASE WHEN e.id = ? THEN 0 ELSE 1 END), e.id LIMIT 5
            """, (emp_id, emp_id, emp_id))
            recent_employees = [dict(r) for r in await cursor_recent.fetchall()]

            cursor_upcoming = await db.execute("""
                SELECT l.*, lt.name as leave_type_name, e.full_name, e.employee_id_str
                FROM leaves l
                LEFT JOIN leave_types lt ON l.leave_type_id = lt.id
                JOIN employees e ON l.employee_id = e.id
                WHERE e.manager_id = ? OR l.employee_id = ?
                ORDER BY l.start_date DESC LIMIT 5
            """, (emp_id, emp_id))
            upcoming_leaves = [dict(r) for r in await cursor_upcoming.fetchall()]
            
            stats = {
                "total_employees": team_emp_count + 1,
                "team_members_count": team_emp_count,
                "total_departments": team_dept_count or 1,
                "present_today": team_present,
                "pending_approvals": total_pending,
                "pending_leaves": p_leaves,
                "pending_overtime": p_ot,
                "pending_reimbursement": p_reimb,
                "pending_travel": p_travel,
            }
        elif role == "director" or role == "super_admin":
            emp_count = (await (await db.execute("SELECT COUNT(*) FROM employees WHERE status='active'")).fetchone())[0]
            dept_count = (await (await db.execute("SELECT COUNT(*) FROM departments")).fetchone())[0]
            att_count = (await (await db.execute("SELECT COUNT(*) FROM attendance WHERE status='present' AND date = date('now')")).fetchone())[0]
            
            # Pending approvals for Director
            p_travel_dir = (await (await db.execute("SELECT COUNT(*) FROM travel_requests WHERE status='pending_director'")).fetchone())[0]
            p_leaves = (await (await db.execute("SELECT COUNT(*) FROM leaves WHERE status='pending'")).fetchone())[0]
            p_ot = (await (await db.execute("SELECT COUNT(*) FROM overtime WHERE status='pending'")).fetchone())[0]
            p_reimb = (await (await db.execute("SELECT COUNT(*) FROM reimbursement WHERE status='pending'")).fetchone())[0]
            
            total_pending = p_travel_dir + p_leaves + p_ot + p_reimb
            
            # Fetch Company-wide Division / Department KPI Aggregations
            cur_dept_kpi = await db.execute("""
                SELECT d.id, d.name as department_name, d.code,
                       COUNT(DISTINCT e.id) as employee_count,
                       ROUND(AVG(ek.achievement_percentage), 1) as avg_achievement,
                       ROUND(AVG(ek.score), 2) as avg_score_4,
                       mgr.full_name as manager_name
                FROM departments d
                LEFT JOIN employees e ON d.id = e.department_id
                LEFT JOIN employees mgr ON d.manager_id = mgr.id
                LEFT JOIN employee_kpis ek ON e.id = ek.employee_id
                GROUP BY d.id
                ORDER BY avg_achievement DESC
            """)
            dept_kpi_list = [dict(r) for r in await cur_dept_kpi.fetchall()]
            
            kpi_data = {
                "division_kpis": dept_kpi_list
            }
            
            cursor_recent = await db.execute("""
                SELECT e.*, d.name as department_name, p.title as position_title
                FROM employees e
                LEFT JOIN departments d ON e.department_id = d.id
                LEFT JOIN positions p ON e.position_id = p.id
                ORDER BY e.id LIMIT 5
            """)
            recent_employees = [dict(r) for r in await cursor_recent.fetchall()]

            cursor_upcoming = await db.execute("""
                SELECT l.*, lt.name as leave_type_name, e.full_name, e.employee_id_str
                FROM leaves l
                LEFT JOIN leave_types lt ON l.leave_type_id = lt.id
                JOIN employees e ON l.employee_id = e.id
                WHERE l.status IN ('approved', 'pending')
                ORDER BY l.start_date DESC LIMIT 5
            """)
            upcoming_leaves = [dict(r) for r in await cursor_upcoming.fetchall()]
            
            stats = {
                "total_employees": emp_count,
                "total_departments": dept_count,
                "present_today": att_count,
                "pending_approvals": total_pending,
                "pending_travel_director": p_travel_dir,
                "pending_leaves": p_leaves,
                "pending_overtime": p_ot,
                "pending_reimbursement": p_reimb,
            }
        else:
            emp_count = (await (await db.execute("SELECT COUNT(*) FROM employees WHERE status='active'")).fetchone())[0]
            dept_count = (await (await db.execute("SELECT COUNT(*) FROM departments")).fetchone())[0]
            att_count = (await (await db.execute("SELECT COUNT(*) FROM attendance WHERE status='present' AND date = date('now')")).fetchone())[0]
            pending_leaves = (await (await db.execute("SELECT COUNT(*) FROM leaves WHERE status='pending'")).fetchone())[0]
            
            cursor_recent = await db.execute("""
                SELECT e.*, d.name as department_name, p.title as position_title
                FROM employees e
                LEFT JOIN departments d ON e.department_id = d.id
                LEFT JOIN positions p ON e.position_id = p.id
                ORDER BY e.id LIMIT 5
            """)
            recent_employees = [dict(r) for r in await cursor_recent.fetchall()]

            cursor_upcoming = await db.execute("""
                SELECT l.*, lt.name as leave_type_name, e.full_name, e.employee_id_str
                FROM leaves l
                LEFT JOIN leave_types lt ON l.leave_type_id = lt.id
                JOIN employees e ON l.employee_id = e.id
                WHERE l.status IN ('approved', 'pending')
                ORDER BY l.start_date DESC LIMIT 5
            """)
            upcoming_leaves = [dict(r) for r in await cursor_upcoming.fetchall()]
            
            stats = {
                "total_employees": emp_count,
                "total_departments": dept_count,
                "present_today": att_count,
                "pending_approvals": pending_leaves,
            }
    finally:
        await db.close()

    return templates.TemplateResponse("pages/dashboard.html", {
        "request": request,
        "user": user,
        "stats": stats,
        "kpi_data": kpi_data,
        "recent_employees": recent_employees,
        "upcoming_leaves": upcoming_leaves,
        "active_page": "dashboard",
    })


@app.get("/employees", response_class=HTMLResponse)
async def employees_page(request: Request):
    user = get_user_from_request(request)
    if not user:
        return RedirectResponse(url="/", status_code=302)
    
    role = user.get("role", "employee")
    emp_id = user.get("employee_id") or user.get("id")

    # If employee, redirect directly to their personal detail profile page
    if role == "employee":
        return RedirectResponse(url=f"/employees/{emp_id}", status_code=302)
    
    db = await get_db_connection()
    try:
        if role == "manager":
            cursor = await db.execute("""
                SELECT e.*, p.title as position_title, d.name as department_name
                FROM employees e
                LEFT JOIN positions p ON e.position_id = p.id
                LEFT JOIN departments d ON e.department_id = d.id
                WHERE e.id = ? OR e.manager_id = ?
                ORDER BY e.id
            """, (emp_id, emp_id))
        else:
            cursor = await db.execute("""
                SELECT e.*, p.title as position_title, d.name as department_name
                FROM employees e
                LEFT JOIN positions p ON e.position_id = p.id
                LEFT JOIN departments d ON e.department_id = d.id
                ORDER BY e.id
            """)
        rows = await cursor.fetchall()
        employees = [dict(r) for r in rows]
    finally:
        await db.close()

    return templates.TemplateResponse("pages/employees.html", {
        "request": request,
        "user": user,
        "employees": employees,
        "active_page": "employees",
    })


@app.get("/employees/{emp_id}", response_class=HTMLResponse)
async def employee_detail_page(request: Request, emp_id: int):
    user = get_user_from_request(request)
    if not user:
        return RedirectResponse(url="/", status_code=302)
    
    role = user.get("role", "employee")
    own_id = user.get("employee_id") or user.get("id")

    # Employee can only view their own detail profile
    if role == "employee" and emp_id != own_id:
        return RedirectResponse(url=f"/employees/{own_id}", status_code=302)
    
    db = await get_db_connection()
    try:
        cursor = await db.execute("""
            SELECT e.*, p.title as position_title, p.salary_min, p.salary_max,
                   d.name as department_name, mgr.full_name as manager_name
            FROM employees e
            LEFT JOIN positions p ON e.position_id = p.id
            LEFT JOIN departments d ON e.department_id = d.id
            LEFT JOIN employees mgr ON e.manager_id = mgr.id
            WHERE e.id = ?
        """, (emp_id,))
        row = await cursor.fetchone()
        if not row:
            return RedirectResponse(url="/dashboard", status_code=302)
        employee = dict(row)

        # 1. Documents
        cursor_doc = await db.execute("SELECT * FROM documents WHERE employee_id = ? ORDER BY uploaded_at DESC", (emp_id,))
        documents = [dict(r) for r in await cursor_doc.fetchall()]

        # 2. Attendance
        cursor_att = await db.execute("SELECT * FROM attendance WHERE employee_id = ? ORDER BY date DESC LIMIT 30", (emp_id,))
        attendance = [dict(r) for r in await cursor_att.fetchall()]
        
        att_present = sum(1 for a in attendance if a.get("status") == "present")
        att_late = sum(1 for a in attendance if a.get("status") == "late")
        att_absent = sum(1 for a in attendance if a.get("status") == "absent")
        att_leave = sum(1 for a in attendance if a.get("status") == "leave")
        att_stats = {
            "present": att_present,
            "late": att_late,
            "absent": att_absent,
            "leave": att_leave
        }

        # 3. Leaves
        cursor_leave = await db.execute("""
            SELECT l.*, lt.name as leave_type_name
            FROM leaves l
            LEFT JOIN leave_types lt ON l.leave_type_id = lt.id
            WHERE l.employee_id = ?
            ORDER BY l.id DESC
        """, (emp_id,))
        leaves = [dict(r) for r in await cursor_leave.fetchall()]

        # 4. Payroll
        cursor_pay = await db.execute("""
            SELECT * FROM payroll WHERE employee_id = ? ORDER BY period_year DESC, period_month DESC
        """, (emp_id,))
        payrolls = [dict(r) for r in await cursor_pay.fetchall()]

        # 5. Performance reviews & trainings
        cursor_rev = await db.execute("""
            SELECT pr.*, rev.full_name as reviewer_name
            FROM performance_reviews pr
            LEFT JOIN employees rev ON pr.reviewer_id = rev.id
            WHERE pr.employee_id = ?
            ORDER BY pr.period DESC
        """, (emp_id,))
        reviews = [dict(r) for r in await cursor_rev.fetchall()]

        cursor_tr = await db.execute("""
            SELECT t.*, te.status as enrollment_status, te.score as my_score
            FROM training t
            JOIN training_enrollments te ON t.id = te.training_id
            WHERE te.employee_id = ?
            ORDER BY t.start_date DESC
        """, (emp_id,))
        trainings = [dict(r) for r in await cursor_tr.fetchall()]

    finally:
        await db.close()

    return templates.TemplateResponse("pages/employee_detail.html", {
        "request": request,
        "user": user,
        "active_page": "employee_detail",
        "emp_id": emp_id,
        "employee": employee,
        "documents": documents,
        "attendance": attendance,
        "att_stats": att_stats,
        "leaves": leaves,
        "payrolls": payrolls,
        "reviews": reviews,
        "trainings": trainings,
    })


@app.get("/departments", response_class=HTMLResponse)
async def departments_page(request: Request):
    user = get_user_from_request(request)
    if not user:
        return RedirectResponse(url="/", status_code=302)
    
    # Employee cannot access departments management
    if user.get("role") not in ["super_admin", "director", "manager"]:
        return RedirectResponse(url="/dashboard", status_code=302)
    
    db = await get_db_connection()
    try:
        cursor = await db.execute("""
            SELECT d.*, e.full_name as manager_name,
                   (SELECT COUNT(*) FROM employees WHERE department_id = d.id) as employee_count
            FROM departments d
            LEFT JOIN employees e ON d.manager_id = e.id
            ORDER BY d.id
        """)
        departments = [dict(r) for r in await cursor.fetchall()]
    finally:
        await db.close()

    return templates.TemplateResponse("pages/departments.html", {
        "request": request,
        "user": user,
        "departments": departments,
        "active_page": "departments",
    })


@app.get("/attendance", response_class=HTMLResponse)
async def attendance_page(
    request: Request,
    period: Optional[str] = Query("all"),
    month: Optional[str] = Query(None),
    year: Optional[str] = Query(None),
    limit_count: Optional[int] = Query(200)
):
    user = get_user_from_request(request)
    if not user:
        return RedirectResponse(url="/", status_code=302)
    
    db = await get_db_connection()
    try:
        from datetime import datetime, date
        role = user.get("role", "employee")
        emp_id = user.get("employee_id") or user.get("id")
        now = datetime.now()
        
        # Build filter conditions: Strictly for the logged-in user
        conditions = ["a.employee_id = ?"]
        params = [emp_id]

        if period == "this_month":
            curr_month_str = now.strftime('%Y-%m')
            conditions.append("strftime('%Y-%m', a.date) = ?")
            params.append(curr_month_str)
        elif period == "last_month":
            # Last month calculation
            first_of_curr = now.replace(day=1)
            last_month_end = first_of_curr - datetime.timedelta(days=1)
            conditions.append("strftime('%Y-%m', a.date) = ?")
            params.append(last_month_end.strftime('%Y-%m'))
        elif period == "this_year":
            conditions.append("strftime('%Y', a.date) = ?")
            params.append(str(now.year))
        elif month:
            conditions.append("strftime('%Y-%m', a.date) = ?")
            params.append(month)
        elif year:
            conditions.append("strftime('%Y', a.date) = ?")
            params.append(year)

        where_clause = " WHERE " + " AND ".join(conditions)

        # Get list of attendance
        query = f"""
            SELECT a.*, e.full_name, e.employee_id_str, d.name as department_name
            FROM attendance a
            JOIN employees e ON a.employee_id = e.id
            LEFT JOIN departments d ON e.department_id = d.id
            {where_clause}
            ORDER BY a.date DESC, a.id DESC
            LIMIT ?
        """
        queryParams = list(params) + [limit_count]
        cursor = await db.execute(query, queryParams)
        attendance = [dict(r) for r in await cursor.fetchall()]

        # Calculate statistics for the logged in user
        stats_cursor = await db.execute(f"""
            SELECT
                COALESCE(SUM(CASE WHEN a.status='present' THEN 1 ELSE 0 END), 0) as present,
                COALESCE(SUM(CASE WHEN a.status='absent' THEN 1 ELSE 0 END), 0) as absent,
                COALESCE(SUM(CASE WHEN a.status='late' THEN 1 ELSE 0 END), 0) as late,
                COALESCE(SUM(CASE WHEN a.status='duty' THEN 1 ELSE 0 END), 0) as duty,
                COALESCE(SUM(CASE WHEN a.status IN ('leave', 'sick') THEN 1 ELSE 0 END), 0) as on_leave
            FROM attendance a
            {where_clause}
        """, params)
        att_stats = dict(await stats_cursor.fetchone() or {})

        # Get distinct available years and months for filter dropdowns
        ym_cursor = await db.execute("""
            SELECT DISTINCT strftime('%Y', date) as yr, strftime('%Y-%m', date) as ym
            FROM attendance WHERE employee_id = ?
            ORDER BY date DESC
        """, (emp_id,))
        ym_rows = await ym_cursor.fetchall()
        available_years = sorted(list(set([r["yr"] for r in ym_rows if r["yr"]])), reverse=True)
        available_months = [r["ym"] for r in ym_rows if r["ym"]]

    finally:
        await db.close()

    return templates.TemplateResponse("pages/attendance.html", {
        "request": request,
        "user": user,
        "attendance": attendance,
        "att_stats": att_stats,
        "active_page": "attendance",
        "current_period": period,
        "current_month": month,
        "current_year": year,
        "current_limit": limit_count,
        "available_years": available_years,
        "available_months": available_months,
    })


@app.get("/overtime", response_class=HTMLResponse)
async def overtime_page(request: Request):
    user = get_user_from_request(request)
    if not user:
        return RedirectResponse(url="/", status_code=302)
    
    db = await get_db_connection()
    try:
        role = user.get("role", "employee")
        emp_id = user.get("employee_id") or user.get("id")

        if role == "employee":
            cursor = await db.execute("""
                SELECT o.*, e.full_name, e.employee_id_str, d.name as department_name
                FROM overtime o
                JOIN employees e ON o.employee_id = e.id
                LEFT JOIN departments d ON e.department_id = d.id
                WHERE o.employee_id = ?
                ORDER BY o.date DESC, o.id DESC
            """, (emp_id,))
            overtimes = [dict(r) for r in await cursor.fetchall()]
            pending_overtimes = []
            my_overtimes = overtimes
        elif role == "manager":
            cursor = await db.execute("""
                SELECT o.*, e.full_name, e.employee_id_str, d.name as department_name, e.manager_id
                FROM overtime o
                JOIN employees e ON o.employee_id = e.id
                LEFT JOIN departments d ON e.department_id = d.id
                WHERE o.employee_id = ? OR o.employee_id IN (SELECT id FROM employees WHERE manager_id = ?)
                ORDER BY o.date DESC, o.id DESC
            """, (emp_id, emp_id))
            overtimes = [dict(r) for r in await cursor.fetchall()]
            # Manager approves pending requests from subordinates
            pending_overtimes = [o for o in overtimes if o.get("status") == "pending" and o.get("employee_id") != emp_id]
            my_overtimes = [o for o in overtimes if o.get("employee_id") == emp_id]
        else:
            cursor = await db.execute("""
                SELECT o.*, e.full_name, e.employee_id_str, d.name as department_name
                FROM overtime o
                JOIN employees e ON o.employee_id = e.id
                LEFT JOIN departments d ON e.department_id = d.id
                ORDER BY o.date DESC, o.id DESC
            """)
            overtimes = [dict(r) for r in await cursor.fetchall()]
            pending_overtimes = [o for o in overtimes if o.get("status") == "pending"]
            my_overtimes = [o for o in overtimes if o.get("employee_id") == emp_id]
    finally:
        await db.close()

    return templates.TemplateResponse("pages/overtime.html", {
        "request": request,
        "user": user,
        "overtimes": overtimes,
        "pending_overtimes": pending_overtimes,
        "my_overtimes": my_overtimes,
        "active_page": "overtime"
    })


@app.get("/leave", response_class=HTMLResponse)
async def leave_page(request: Request):
    user = get_user_from_request(request)
    if not user:
        return RedirectResponse(url="/", status_code=302)
    
    db = await get_db_connection()
    try:
        cursor_lt = await db.execute("SELECT * FROM leave_types ORDER BY id")
        leave_types = [dict(r) for r in await cursor_lt.fetchall()]
        role = user.get("role", "employee")
        emp_id = user.get("employee_id") or user.get("id")
        
        if role == "employee":
            cursor = await db.execute("""
                SELECT l.*, lt.name as leave_type_name, lt.code as leave_type_code, e.full_name, e.employee_id_str
                FROM leaves l
                LEFT JOIN leave_types lt ON l.leave_type_id = lt.id
                JOIN employees e ON l.employee_id = e.id
                WHERE l.employee_id = ?
                ORDER BY l.id DESC
            """, (emp_id,))
            leaves = [dict(r) for r in await cursor.fetchall()]
            pending_leaves = [l for l in leaves if l.get("status") == "pending"]
            my_leaves = leaves
        elif role == "manager":
            cursor = await db.execute("""
                SELECT l.*, lt.name as leave_type_name, lt.code as leave_type_code, e.full_name, e.employee_id_str, e.manager_id
                FROM leaves l
                LEFT JOIN leave_types lt ON l.leave_type_id = lt.id
                JOIN employees e ON l.employee_id = e.id
                WHERE l.employee_id = ? OR l.employee_id IN (SELECT id FROM employees WHERE manager_id = ?)
                ORDER BY l.id DESC
            """, (emp_id, emp_id))
            leaves = [dict(r) for r in await cursor.fetchall()]
            # Manager approves pending requests from subordinates
            pending_leaves = [l for l in leaves if l.get("status") == "pending" and l.get("employee_id") != emp_id]
            my_leaves = [l for l in leaves if l.get("employee_id") == emp_id]
        else:
            cursor = await db.execute("""
                SELECT l.*, lt.name as leave_type_name, lt.code as leave_type_code, e.full_name, e.employee_id_str
                FROM leaves l
                LEFT JOIN leave_types lt ON l.leave_type_id = lt.id
                JOIN employees e ON l.employee_id = e.id
                ORDER BY l.id DESC
            """)
            leaves = [dict(r) for r in await cursor.fetchall()]
            pending_leaves = [l for l in leaves if l.get("status") == "pending"]
            my_leaves = [l for l in leaves if l.get("employee_id") == emp_id]
    finally:
        await db.close()

    return templates.TemplateResponse("pages/leave.html", {
        "request": request,
        "user": user,
        "leaves": leaves,
        "pending_leaves": pending_leaves,
        "my_leaves": my_leaves,
        "leave_types": leave_types,
        "active_page": "leave"
    })


@app.get("/payroll", response_class=HTMLResponse)
async def payroll_page(request: Request):
    user = get_user_from_request(request)
    if not user:
        return RedirectResponse(url="/", status_code=302)
    if user.get("role") != "super_admin":
        return RedirectResponse(url="/payslips", status_code=302)
    return templates.TemplateResponse("pages/payroll.html", {"request": request, "user": user, "active_page": "payroll"})


@app.get("/performance", response_class=HTMLResponse)
async def performance_page(request: Request):
    user = get_user_from_request(request)
    if not user:
        return RedirectResponse(url="/", status_code=302)
    if user.get("role") not in ["super_admin", "director"]:
        return RedirectResponse(url="/reviews", status_code=302)
    return templates.TemplateResponse("pages/performance.html", {"request": request, "user": user})


@app.get("/kpi-dashboard", response_class=HTMLResponse)
async def kpi_dashboard_page(request: Request):
    user = get_user_from_request(request)
    if not user:
        return RedirectResponse(url="/", status_code=302)
    if user.get("role") not in ["super_admin", "director", "manager"]:
        return RedirectResponse(url="/reviews", status_code=302)
    return templates.TemplateResponse("pages/kpi_dashboard.html", {"request": request, "user": user, "active_page": "kpi-dashboard"})


@app.get("/recruitment", response_class=HTMLResponse)
async def recruitment_page(request: Request):
    user = get_user_from_request(request)
    if not user:
        return RedirectResponse(url="/", status_code=302)
    if user.get("role") not in ["super_admin", "director"]:
        return RedirectResponse(url="/dashboard", status_code=302)
    return templates.TemplateResponse("pages/recruitment.html", {"request": request, "user": user})


@app.get("/procurement", response_class=HTMLResponse)
async def procurement_page(request: Request):
    user = get_user_from_request(request)
    if not user:
        return RedirectResponse(url="/", status_code=302)
    if user.get("role") not in ["super_admin", "director", "manager"]:
        return RedirectResponse(url="/dashboard", status_code=302)
    return templates.TemplateResponse("pages/procurement.html", {"request": request, "user": user})


@app.get("/assets", response_class=HTMLResponse)
async def assets_page(request: Request):
    user = get_user_from_request(request)
    if not user:
        return RedirectResponse(url="/", status_code=302)
    if user.get("role") not in ["super_admin", "director", "manager"]:
        return RedirectResponse(url="/dashboard", status_code=302)
    return templates.TemplateResponse("pages/assets.html", {"request": request, "user": user})


@app.get("/training", response_class=HTMLResponse)
async def training_page(request: Request):
    user = get_user_from_request(request)
    if not user:
        return RedirectResponse(url="/", status_code=302)
    
    db = await get_db_connection()
    try:
        role = user.get("role", "employee")
        emp_id = user.get("employee_id") or user.get("id")
        
        if role == "employee":
            cursor = await db.execute("""
                SELECT t.*, te.status as enrollment_status, te.score as my_score, te.completed_at
                FROM training t
                LEFT JOIN training_enrollments te ON t.id = te.training_id AND te.employee_id = ?
                ORDER BY t.start_date DESC
            """, (emp_id,))
        else:
            cursor = await db.execute("""
                SELECT t.*, 
                       (SELECT COUNT(*) FROM training_enrollments WHERE training_id = t.id) as enrolled_count
                FROM training t
                ORDER BY t.start_date DESC
            """)
        trainings = [dict(r) for r in await cursor.fetchall()]
        
        active_count = sum(1 for t in trainings if t.get("status") == "active")
        completed_count = sum(1 for t in trainings if t.get("status") == "completed" or t.get("enrollment_status") == "completed")
        train_stats = {
            "total": len(trainings),
            "active": active_count,
            "completed": completed_count
        }
    finally:
        await db.close()

    return templates.TemplateResponse("pages/training.html", {
        "request": request,
        "user": user,
        "trainings": trainings,
        "train_stats": train_stats,
        "active_page": "training"
    })


@app.get("/reports", response_class=HTMLResponse)
async def reports_page(request: Request):
    user = get_user_from_request(request)
    if not user:
        return RedirectResponse(url="/", status_code=302)
    if user.get("role") not in ["super_admin", "director", "manager"]:
        return RedirectResponse(url="/dashboard", status_code=302)
    return templates.TemplateResponse("pages/reports.html", {"request": request, "user": user})


@app.get("/settings", response_class=HTMLResponse)
async def settings_page(request: Request):
    user = get_user_from_request(request)
    if not user:
        return RedirectResponse(url="/", status_code=302)
    if user.get("role") not in ["super_admin", "director", "admin"]:
        return RedirectResponse(url="/dashboard", status_code=302)
        
    db = await get_db_connection()
    try:
        settings = await get_all_settings(db)
    finally:
        await db.close()
        
    return templates.TemplateResponse("pages/settings.html", {
        "request": request,
        "user": user,
        "settings": settings,
        "active_page": "settings"
    })


@app.get("/documents", response_class=HTMLResponse)
async def documents_page(request: Request):
    user = get_user_from_request(request)
    if not user:
        return RedirectResponse(url="/", status_code=302)
    
    db = await get_db_connection()
    try:
        role = user.get("role", "employee")
        emp_id = user.get("employee_id") or user.get("id")
        
        if role == "employee":
            cursor = await db.execute("""
                SELECT d.*, e.full_name, e.employee_id_str
                FROM documents d
                JOIN employees e ON d.employee_id = e.id
                WHERE d.employee_id = ?
                ORDER BY d.uploaded_at DESC
            """, (emp_id,))
        else:
            cursor = await db.execute("""
                SELECT d.*, e.full_name, e.employee_id_str
                FROM documents d
                JOIN employees e ON d.employee_id = e.id
                ORDER BY d.uploaded_at DESC
            """)
        documents = [dict(r) for r in await cursor.fetchall()]
        
        from datetime import date
        today_str = date.today().isoformat()
        valid_count = sum(1 for d in documents if not d.get("expiry_date") or d.get("expiry_date") >= today_str)
        expired_count = len(documents) - valid_count
        doc_stats = {
            "total": len(documents),
            "valid": valid_count,
            "expiring": 0,
            "expired": expired_count
        }
    finally:
        await db.close()

    return templates.TemplateResponse("pages/documents.html", {
        "request": request,
        "user": user,
        "documents": documents,
        "doc_stats": doc_stats,
        "active_page": "documents"
    })


@app.get("/org-chart", response_class=HTMLResponse)
async def orgchart_page(request: Request):
    user = get_user_from_request(request)
    if not user:
        return RedirectResponse(url="/", status_code=302)
    return templates.TemplateResponse("pages/orgchart.html", {"request": request, "user": user, "active_page": "org-chart"})


@app.get("/shifts", response_class=HTMLResponse)
async def shifts_page(request: Request):
    user = get_user_from_request(request)
    if not user:
        return RedirectResponse(url="/", status_code=302)
    
    db = await get_db_connection()
    try:
        cursor_shifts = await db.execute("SELECT * FROM shifts ORDER BY id")
        shifts = [dict(r) for r in await cursor_shifts.fetchall()]
        
        role = user.get("role", "employee")
        emp_id = user.get("employee_id") or user.get("id")
        
        if role == "employee":
            cursor_es = await db.execute("""
                SELECT es.*, s.name as shift_name, s.start_time, s.end_time, s.description
                FROM employee_shifts es
                JOIN shifts s ON es.shift_id = s.id
                WHERE es.employee_id = ?
                ORDER BY es.date DESC
            """, (emp_id,))
            my_shifts = [dict(r) for r in await cursor_es.fetchall()]
            assigned_shifts = my_shifts
        else:
            cursor_es = await db.execute("""
                SELECT es.*, s.name as shift_name, s.start_time, s.end_time, s.description, e.full_name, e.employee_id_str
                FROM employee_shifts es
                JOIN shifts s ON es.shift_id = s.id
                JOIN employees e ON es.employee_id = e.id
                ORDER BY es.date DESC
            """)
            assigned_shifts = [dict(r) for r in await cursor_es.fetchall()]
            my_shifts = []
    finally:
        await db.close()

    return templates.TemplateResponse("pages/shifts.html", {
        "request": request,
        "user": user,
        "shifts": shifts,
        "assigned_shifts": assigned_shifts,
        "my_shifts": my_shifts,
        "active_page": "shifts"
    })


@app.get("/payslips", response_class=HTMLResponse)
async def payslips_page(request: Request):
    user = get_user_from_request(request)
    if not user:
        return RedirectResponse(url="/", status_code=302)
    
    db = await get_db_connection()
    try:
        role = user.get("role", "employee")
        emp_id = user.get("employee_id") or user.get("id")

        if role == "employee":
            cursor = await db.execute("""
                SELECT p.*, e.full_name, e.employee_id_str, d.name as department_name, pos.title as position_title
                FROM payroll p
                JOIN employees e ON p.employee_id = e.id
                LEFT JOIN departments d ON e.department_id = d.id
                LEFT JOIN positions pos ON e.position_id = pos.id
                WHERE p.employee_id = ?
                ORDER BY p.period_year DESC, p.period_month DESC
            """, (emp_id,))
        elif role == "manager":
            cursor = await db.execute("""
                SELECT p.*, e.full_name, e.employee_id_str, d.name as department_name, pos.title as position_title
                FROM payroll p
                JOIN employees e ON p.employee_id = e.id
                LEFT JOIN departments d ON e.department_id = d.id
                LEFT JOIN positions pos ON e.position_id = pos.id
                WHERE p.employee_id = ? OR p.employee_id IN (SELECT id FROM employees WHERE manager_id = ?)
                ORDER BY p.period_year DESC, p.period_month DESC
            """, (emp_id, emp_id))
        else:
            cursor = await db.execute("""
                SELECT p.*, e.full_name, e.employee_id_str, d.name as department_name, pos.title as position_title
                FROM payroll p
                JOIN employees e ON p.employee_id = e.id
                LEFT JOIN departments d ON e.department_id = d.id
                LEFT JOIN positions pos ON e.position_id = pos.id
                ORDER BY p.period_year DESC, p.period_month DESC
            """)
        
        payslips = [dict(r) for r in await cursor.fetchall()]
        
        # Calculate summary statistics
        total_payslips = len(payslips)
        processed_count = sum(1 for p in payslips if p.get("status") == "processed")
        pending_count = total_payslips - processed_count
        total_net = sum(p.get("net_salary") or 0 for p in payslips)
        
        stats = {
            "total": total_payslips,
            "processed": processed_count,
            "pending": pending_count,
            "total_net": total_net,
        }
    finally:
        await db.close()

    return templates.TemplateResponse("pages/payslips.html", {
        "request": request,
        "user": user,
        "payslips": payslips,
        "stats": stats,
        "active_page": "payslips"
    })


@app.get("/reimbursement", response_class=HTMLResponse)
async def reimbursement_page(request: Request):
    user = get_user_from_request(request)
    if not user:
        return RedirectResponse(url="/", status_code=302)
    
    db = await get_db_connection()
    try:
        role = user.get("role", "employee")
        emp_id = user.get("employee_id") or user.get("id")

        if role == "employee":
            cursor = await db.execute("""
                SELECT r.*, e.full_name, e.employee_id_str
                FROM reimbursement r
                JOIN employees e ON r.employee_id = e.id
                WHERE r.employee_id = ?
                ORDER BY r.id DESC
            """, (emp_id,))
            reimbursements = [dict(r) for r in await cursor.fetchall()]
            pending_reimbursements = []
            my_reimbursements = reimbursements
        elif role == "manager":
            cursor = await db.execute("""
                SELECT r.*, e.full_name, e.employee_id_str, e.manager_id
                FROM reimbursement r
                JOIN employees e ON r.employee_id = e.id
                WHERE r.employee_id = ? OR r.employee_id IN (SELECT id FROM employees WHERE manager_id = ?)
                ORDER BY r.id DESC
            """, (emp_id, emp_id))
            reimbursements = [dict(r) for r in await cursor.fetchall()]
            pending_reimbursements = [r for r in reimbursements if r.get("status") == "pending" and r.get("employee_id") != emp_id]
            my_reimbursements = [r for r in reimbursements if r.get("employee_id") == emp_id]
        else:
            cursor = await db.execute("""
                SELECT r.*, e.full_name, e.employee_id_str
                FROM reimbursement r
                JOIN employees e ON r.employee_id = e.id
                ORDER BY r.id DESC
            """)
            reimbursements = [dict(r) for r in await cursor.fetchall()]
            pending_reimbursements = [r for r in reimbursements if r.get("status") == "pending"]
            my_reimbursements = [r for r in reimbursements if r.get("employee_id") == emp_id]
    finally:
        await db.close()

    return templates.TemplateResponse("pages/reimbursement.html", {
        "request": request, 
        "user": user, 
        "reimbursements": reimbursements,
        "pending_reimbursements": pending_reimbursements,
        "my_reimbursements": my_reimbursements,
        "active_page": "reimbursement"
    })


@app.get("/reviews", response_class=HTMLResponse)
async def reviews_page(request: Request):
    user = get_user_from_request(request)
    if not user:
        return RedirectResponse(url="/", status_code=302)
    
    db = await get_db_connection()
    try:
        role = user.get("role", "employee")
        emp_id = user.get("employee_id") or user.get("id")
        team_members = []
        
        if role == "employee":
            cursor = await db.execute("""
                SELECT pr.*, e.full_name as employee_name, e.employee_id_str, rev.full_name as reviewer_name
                FROM performance_reviews pr
                JOIN employees e ON pr.employee_id = e.id
                LEFT JOIN employees rev ON pr.reviewer_id = rev.id
                WHERE pr.employee_id = ?
                ORDER BY pr.period DESC
            """, (emp_id,))
            reviews = [dict(r) for r in await cursor.fetchall()]
            team_reviews = []
            my_reviews = reviews
        elif role == "manager":
            cursor = await db.execute("""
                SELECT pr.*, e.full_name as employee_name, e.employee_id_str, rev.full_name as reviewer_name
                FROM performance_reviews pr
                JOIN employees e ON pr.employee_id = e.id
                LEFT JOIN employees rev ON pr.reviewer_id = rev.id
                WHERE pr.employee_id = ? OR pr.reviewer_id = ? OR pr.employee_id IN (SELECT id FROM employees WHERE manager_id = ?)
                ORDER BY pr.period DESC
            """, (emp_id, emp_id, emp_id))
            reviews = [dict(r) for r in await cursor.fetchall()]
            
            # Fetch subordinate team members that this manager evaluates
            tm_cursor = await db.execute("""
                SELECT id, employee_id_str, full_name, email, department_id
                FROM employees
                WHERE manager_id = ?
                ORDER BY full_name
            """, (emp_id,))
            team_members = [dict(r) for r in await tm_cursor.fetchall()]
            
            team_reviews = [r for r in reviews if r.get("employee_id") != emp_id]
            my_reviews = [r for r in reviews if r.get("employee_id") == emp_id]
        else:
            cursor = await db.execute("""
                SELECT pr.*, e.full_name as employee_name, e.employee_id_str, rev.full_name as reviewer_name
                FROM performance_reviews pr
                JOIN employees e ON pr.employee_id = e.id
                LEFT JOIN employees rev ON pr.reviewer_id = rev.id
                ORDER BY pr.period DESC
            """)
            reviews = [dict(r) for r in await cursor.fetchall()]
            
            tm_cursor = await db.execute("SELECT id, employee_id_str, full_name, email, department_id FROM employees WHERE status='active' ORDER BY full_name")
            team_members = [dict(r) for r in await tm_cursor.fetchall()]
            team_reviews = reviews
            my_reviews = [r for r in reviews if r.get("employee_id") == emp_id]
        
        scores = [r["score"] for r in reviews if r.get("score") is not None]
        avg_score = round(sum(scores) / len(scores), 1) if scores else 0.0
        
        rev_stats = {
            "total": len(reviews),
            "avg_score": avg_score,
            "completed": len([r for r in reviews if r.get("score") is not None]),
            "scheduled": len([r for r in reviews if r.get("score") is None]),
            "team_count": len(team_members)
        }
    finally:
        await db.close()

    return templates.TemplateResponse("pages/reviews.html", {
        "request": request,
        "user": user,
        "reviews": reviews,
        "team_reviews": team_reviews,
        "my_reviews": my_reviews,
        "team_members": team_members,
        "rev_stats": rev_stats,
        "active_page": "reviews"
    })


@app.get("/requisitions", response_class=HTMLResponse)
async def requisitions_page(request: Request):
    user = get_user_from_request(request)
    if not user:
        return RedirectResponse(url="/", status_code=302)
    if user.get("role") not in ["super_admin", "director", "manager"]:
        return RedirectResponse(url="/dashboard", status_code=302)
    return templates.TemplateResponse("pages/requisitions.html", {"request": request, "user": user, "active_page": "requisitions"})


@app.get("/register", response_class=HTMLResponse)
async def register_page(request: Request):
    """Render registration page."""
    user = get_user_from_request(request)
    if user:
        return RedirectResponse(url="/dashboard", status_code=302)
    return templates.TemplateResponse("pages/register.html", {"request": request})


@app.get("/admin/registrations", response_class=HTMLResponse)
async def admin_registrations_page(request: Request):
    """Admin approval panel for registrations."""
    user = get_user_from_request(request)
    if not user:
        return RedirectResponse(url="/", status_code=302)
    if user.get("role") != "super_admin":
        raise HTTPException(status_code=403, detail="Super admin access required")
    return templates.TemplateResponse("pages/registrations.html", {"request": request, "user": user, "active_page": "registrations"})


@app.get("/interviews", response_class=HTMLResponse)
async def interviews_page(request: Request):
    user = get_user_from_request(request)
    if not user:
        return RedirectResponse(url="/", status_code=302)
    if user.get("role") not in ["super_admin", "director", "manager"]:
        return RedirectResponse(url="/dashboard", status_code=302)
    return templates.TemplateResponse("pages/interviews.html", {"request": request, "user": user, "active_page": "interviews"})


@app.get("/travel", response_class=HTMLResponse)
async def travel_page(request: Request):
    user = get_user_from_request(request)
    if not user:
        return RedirectResponse(url="/", status_code=302)
    
    db = await get_db_connection()
    try:
        role = user.get("role", "employee")
        emp_id = user.get("employee_id") or user.get("id")
        
        if role == "employee":
            cursor = await db.execute("""
                SELECT tr.*, e.full_name as employee_name, e.employee_id_str, d.name as department_name, p.title as position_title, m.full_name as manager_name
                FROM travel_requests tr
                JOIN employees e ON tr.employee_id = e.id
                LEFT JOIN departments d ON e.department_id = d.id
                LEFT JOIN positions p ON e.position_id = p.id
                LEFT JOIN employees m ON e.manager_id = m.id
                WHERE tr.employee_id = ?
                ORDER BY tr.id DESC
            """, (emp_id,))
        elif role == "manager":
            cursor = await db.execute("""
                SELECT tr.*, e.full_name as employee_name, e.employee_id_str, d.name as department_name, p.title as position_title, m.full_name as manager_name
                FROM travel_requests tr
                JOIN employees e ON tr.employee_id = e.id
                LEFT JOIN departments d ON e.department_id = d.id
                LEFT JOIN positions p ON e.position_id = p.id
                LEFT JOIN employees m ON e.manager_id = m.id
                WHERE tr.employee_id = ? OR tr.employee_id IN (SELECT id FROM employees WHERE manager_id = ?)
                ORDER BY tr.id DESC
            """, (emp_id, emp_id))
        else:
            cursor = await db.execute("""
                SELECT tr.*, e.full_name as employee_name, e.employee_id_str, d.name as department_name, p.title as position_title, m.full_name as manager_name
                FROM travel_requests tr
                JOIN employees e ON tr.employee_id = e.id
                LEFT JOIN departments d ON e.department_id = d.id
                LEFT JOIN positions p ON e.position_id = p.id
                LEFT JOIN employees m ON e.manager_id = m.id
                ORDER BY tr.id DESC
            """)
        travels = [dict(r) for r in await cursor.fetchall()]
        
        total_requests = len(travels)
        pending_count = sum(1 for t in travels if "pending" in (t.get("status") or "") or t.get("status") == "revision_required")
        approved_count = sum(1 for t in travels if t.get("status") in ["approved", "completed"])
        total_cost = sum(t.get("grand_total") or t.get("estimated_cost") or 0 for t in travels)
        
        cursor_emps = await db.execute("SELECT id, full_name, employee_id_str, department_id FROM employees WHERE status='active' ORDER BY full_name")
        employees = [dict(r) for r in await cursor_emps.fetchall()]

        travel_stats = {
            "total": total_requests,
            "pending": pending_count,
            "approved": approved_count,
            "total_cost": total_cost,
        }
    finally:
        await db.close()

    return templates.TemplateResponse("pages/travel.html", {
        "request": request,
        "user": user,
        "travels": travels,
        "employees": employees,
        "travel_stats": travel_stats,
        "active_page": "travel",
    })


@app.get("/travel/{travel_id}/print", response_class=HTMLResponse)
async def print_sppd_page(request: Request, travel_id: int):
    # Public / Auth accessible print preview
    user = get_user_from_request(request) or {"role": "employee", "username": "public"}

    db = await get_db_connection()
    try:
        cursor = await db.execute("""
            SELECT tr.*, 
                   e.full_name as employee_name, 
                   e.employee_id_str, 
                   d.name as department_name, 
                   p.title as position_title, 
                   m.full_name as manager_name,
                   m_pos.title as manager_position_title,
                   dir.full_name as director_name
            FROM travel_requests tr
            JOIN employees e ON tr.employee_id = e.id
            LEFT JOIN departments d ON e.department_id = d.id
            LEFT JOIN positions p ON e.position_id = p.id
            LEFT JOIN employees m ON e.manager_id = m.id
            LEFT JOIN positions m_pos ON m.position_id = m_pos.id
            LEFT JOIN employees dir ON tr.director_id = dir.id
            WHERE tr.id = ?
        """, (travel_id,))
        travel = await cursor.fetchone()
        if not travel:
            raise HTTPException(status_code=404, detail="Dokumen SPPD tidak ditemukan")
        travel = dict(travel)
    finally:
        await db.close()

    return templates.TemplateResponse("pages/sppd_document.html", {
        "request": request,
        "user": user,
        "req": travel,
    })


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8090, reload=True)
