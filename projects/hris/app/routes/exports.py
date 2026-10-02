"""Export endpoints — generate Excel/PDF downloads for HRIS data."""

import io
import sqlite3
from datetime import date

from fastapi import APIRouter, Query
from fastapi.responses import StreamingResponse

from app.services.export_service import (
    export_assets_excel,
    export_attendance_excel,
    export_attendance_pdf,
    export_employees_excel,
    export_employees_pdf,
    export_leave_excel as export_leaves_excel,
    export_overtime_excel,
    export_payroll_excel,
    export_payroll_pdf,
    export_performance_excel,
    export_procurement_excel,
    export_reimbursement_excel,
    export_training_excel,
)

router = APIRouter(prefix="/exports", tags=["exports"])

from app.database import DATABASE_PATH
DB_PATH = DATABASE_PATH
TODAY = date.today().isoformat()


def _get_db() -> sqlite3.Connection:
    """Return a sync sqlite3 connection with Row factory."""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


# ---------------------------------------------------------------------------
# Employees
# ---------------------------------------------------------------------------

@router.get("/employees")
async def export_employees(
    format: str = Query("excel", description="Export format: excel or pdf"),
):
    conn = _get_db()
    try:
        if format == "pdf":
            data = export_employees_pdf(conn)
            buffer = io.BytesIO(data)
            return StreamingResponse(
                buffer,
                media_type="application/pdf",
                headers={
                    "Content-Disposition": f'inline; filename="employees_{TODAY}.pdf"'
                },
            )
        # Default: Excel
        data = export_employees_excel(conn)
        buffer = io.BytesIO(data)
        return StreamingResponse(
            buffer,
            media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            headers={
                "Content-Disposition": f'attachment; filename="employees_{TODAY}.xlsx"'
            },
        )
    finally:
        conn.close()


# ---------------------------------------------------------------------------
# Attendance
# ---------------------------------------------------------------------------

@router.get("/attendance")
async def export_attendance(
    format: str = Query("excel", description="Export format: excel or pdf"),
    start_date: str = Query(None, description="Start date (YYYY-MM-DD)"),
    end_date: str = Query(None, description="End date (YYYY-MM-DD)"),
):
    conn = _get_db()
    try:
        if format == "pdf":
            data = export_attendance_pdf(conn, filters={"start_date": start_date, "end_date": end_date})
            buffer = io.BytesIO(data)
            return StreamingResponse(
                buffer,
                media_type="application/pdf",
                headers={
                    "Content-Disposition": f'inline; filename="attendance_{TODAY}.pdf"'
                },
            )
        data = export_attendance_excel(conn, filters={"start_date": start_date, "end_date": end_date})
        buffer = io.BytesIO(data)
        return StreamingResponse(
            buffer,
            media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            headers={
                "Content-Disposition": f'attachment; filename="attendance_{TODAY}.xlsx"'
            },
        )
    finally:
        conn.close()


# ---------------------------------------------------------------------------
# Payroll
# ---------------------------------------------------------------------------

@router.get("/payroll")
async def export_payroll(
    format: str = Query("excel", description="Export format: excel or pdf"),
    period: str = Query(None, description="Payroll period (e.g. 2026-09)"),
):
    conn = _get_db()
    try:
        if format == "pdf":
            data = export_payroll_pdf(conn, filters={"period": period})
            buffer = io.BytesIO(data)
            return StreamingResponse(
                buffer,
                media_type="application/pdf",
                headers={
                    "Content-Disposition": f'inline; filename="payroll_{TODAY}.pdf"'
                },
            )
        data = export_payroll_excel(conn, filters={"period": period})
        buffer = io.BytesIO(data)
        return StreamingResponse(
            buffer,
            media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            headers={
                "Content-Disposition": f'attachment; filename="payroll_{TODAY}.xlsx"'
            },
        )
    finally:
        conn.close()


# ---------------------------------------------------------------------------
# Leaves
# ---------------------------------------------------------------------------

@router.get("/leaves")
async def export_leaves():
    conn = _get_db()
    try:
        data = export_leaves_excel(conn)
        buffer = io.BytesIO(data)
        return StreamingResponse(
            buffer,
            media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            headers={
                "Content-Disposition": f'attachment; filename="leaves_{TODAY}.xlsx"'
            },
        )
    finally:
        conn.close()


# ---------------------------------------------------------------------------
# Overtime
# ---------------------------------------------------------------------------

@router.get("/overtime")
async def export_overtime():
    conn = _get_db()
    try:
        data = export_overtime_excel(conn)
        buffer = io.BytesIO(data)
        return StreamingResponse(
            buffer,
            media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            headers={
                "Content-Disposition": f'attachment; filename="overtime_{TODAY}.xlsx"'
            },
        )
    finally:
        conn.close()


# ---------------------------------------------------------------------------
# Assets
# ---------------------------------------------------------------------------

@router.get("/assets")
async def export_assets():
    conn = _get_db()
    try:
        data = export_assets_excel(conn)
        buffer = io.BytesIO(data)
        return StreamingResponse(
            buffer,
            media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            headers={
                "Content-Disposition": f'attachment; filename="assets_{TODAY}.xlsx"'
            },
        )
    finally:
        conn.close()


# ---------------------------------------------------------------------------
# Procurement
# ---------------------------------------------------------------------------

@router.get("/procurement")
async def export_procurement():
    conn = _get_db()
    try:
        data = export_procurement_excel(conn)
        buffer = io.BytesIO(data)
        return StreamingResponse(
            buffer,
            media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            headers={
                "Content-Disposition": f'attachment; filename="procurement_{TODAY}.xlsx"'
            },
        )
    finally:
        conn.close()


# ---------------------------------------------------------------------------
# Performance
# ---------------------------------------------------------------------------

@router.get("/performance")
async def export_performance():
    conn = _get_db()
    try:
        data = export_performance_excel(conn)
        buffer = io.BytesIO(data)
        return StreamingResponse(
            buffer,
            media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            headers={
                "Content-Disposition": f'attachment; filename="performance_{TODAY}.xlsx"'
            },
        )
    finally:
        conn.close()


# ---------------------------------------------------------------------------
# Reimbursement
# ---------------------------------------------------------------------------

@router.get("/reimbursement")
async def export_reimbursement():
    conn = _get_db()
    try:
        data = export_reimbursement_excel(conn)
        buffer = io.BytesIO(data)
        return StreamingResponse(
            buffer,
            media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            headers={
                "Content-Disposition": f'attachment; filename="reimbursement_{TODAY}.xlsx"'
            },
        )
    finally:
        conn.close()


@router.get("/training")
async def export_training():
    conn = _get_db()
    try:
        data = export_training_excel(conn)
        buffer = io.BytesIO(data)
        return StreamingResponse(
            buffer,
            media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            headers={
                "Content-Disposition": f'attachment; filename="training_{TODAY}.xlsx"'
            },
        )
    finally:
        conn.close()


# ---------------------------------------------------------------------------
# Payslip Single PDF
# ---------------------------------------------------------------------------

@router.get("/payslip/{emp_id}")
async def export_single_payslip(
    emp_id: int,
    period_month: int = Query(None),
    period_year: int = Query(None),
):
    from app.services.export_service import export_single_payslip_pdf
    conn = _get_db()
    try:
        data = export_single_payslip_pdf(conn, emp_id=emp_id, period_month=period_month, period_year=period_year)
        buffer = io.BytesIO(data)
        return StreamingResponse(
            buffer,
            media_type="application/pdf",
            headers={
                "Content-Disposition": f'inline; filename="payslip_{emp_id}_{period_month or "latest"}_{period_year or "latest"}.pdf"'
            },
        )
    finally:
        conn.close()
