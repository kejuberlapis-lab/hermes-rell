"""
Travel request routes: full CRUD + multi-level approval + finance workflow.
Uses sync sqlite3 for database access.
"""
import os
import sqlite3
from datetime import datetime
from fastapi import APIRouter, HTTPException, Query
from pydantic import BaseModel
from typing import Optional

router = APIRouter(prefix="/travel", tags=["travel"])

# ---------------------------------------------------------------------------
# Database path (same location as the async hris.db used elsewhere)
# ---------------------------------------------------------------------------
DB_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(
    os.path.abspath(__file__)))), "hris.db")

# ---------------------------------------------------------------------------
# Table creation — executed lazily on first request
# ---------------------------------------------------------------------------
_TABLE_CREATED = False

_CREATE_TRAVEL_SQL = """
CREATE TABLE IF NOT EXISTS travel_requests (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    employee_id INTEGER NOT NULL,
    destination TEXT NOT NULL,
    purpose TEXT,
    departure_date DATE NOT NULL,
    return_date DATE,
    transport_type TEXT NOT NULL CHECK(transport_type IN ('car','bus','train','plane')),
    accommodation_needed INTEGER NOT NULL DEFAULT 0,
    
    -- Cost breakdown fields
    estimated_cost REAL DEFAULT 0,
    transport_cost REAL DEFAULT 0,
    accommodation_rate_per_night REAL DEFAULT 0,
    accommodation_nights INTEGER DEFAULT 0,
    accommodation_total REAL DEFAULT 0,
    daily_allowance_per_day REAL DEFAULT 0,
    daily_allowance_days INTEGER DEFAULT 0,
    daily_allowance_total REAL DEFAULT 0,
    meals_per_day REAL DEFAULT 0,
    meal_days INTEGER DEFAULT 0,
    meal_total REAL DEFAULT 0,
    additional_items TEXT,
    notes TEXT,
    grand_total REAL DEFAULT 0,
    
    actual_cost REAL,
    advance_payment REAL,
    
    status TEXT NOT NULL DEFAULT 'draft'
        CHECK(status IN ('draft','pending_manager','pending_director','revision_required','approved','rejected','completed')),
    manager_id INTEGER,
    manager_approved_at TIMESTAMP,
    manager_notes TEXT,
    manager_revision_reason TEXT,
    director_id INTEGER,
    director_approved_at TIMESTAMP,
    director_notes TEXT,
    director_revision_reason TEXT,
    revision_count INTEGER NOT NULL DEFAULT 0,
    last_revision_by TEXT,
    last_revision_at TIMESTAMP,
    resubmit_history TEXT,
    finance_status TEXT NOT NULL DEFAULT 'not_submitted'
        CHECK(finance_status IN ('not_submitted','submitted','processing','completed')),
    finance_processed_by INTEGER,
    finance_processed_at TIMESTAMP,
    finance_amount REAL,
    finance_notes TEXT,
    receipt_path TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (employee_id) REFERENCES employees(id),
    FOREIGN KEY (manager_id) REFERENCES employees(id),
    FOREIGN KEY (director_id) REFERENCES employees(id)
);
"""


def _ensure_table():
    """Create travel_requests table if it does not yet exist."""
    global _TABLE_CREATED
    if _TABLE_CREATED:
        return
    conn = sqlite3.connect(DB_PATH)
    try:
        # Check if columns exist, add if not
        cur = conn.execute("PRAGMA table_info(travel_requests)")
        existing_cols = [row[1] for row in cur.fetchall()]
        
        if "manager_revision_reason" not in existing_cols:
            conn.execute("ALTER TABLE travel_requests ADD COLUMN manager_revision_reason TEXT")
        if "director_revision_reason" not in existing_cols:
            conn.execute("ALTER TABLE travel_requests ADD COLUMN director_revision_reason TEXT")
        if "revision_count" not in existing_cols:
            conn.execute("ALTER TABLE travel_requests ADD COLUMN revision_count INTEGER NOT NULL DEFAULT 0")
        if "last_revision_by" not in existing_cols:
            conn.execute("ALTER TABLE travel_requests ADD COLUMN last_revision_by TEXT")
        if "last_revision_at" not in existing_cols:
            conn.execute("ALTER TABLE travel_requests ADD COLUMN last_revision_at TIMESTAMP")
        if "resubmit_history" not in existing_cols:
            conn.execute("ALTER TABLE travel_requests ADD COLUMN resubmit_history TEXT")
        
        conn.executescript(_CREATE_TRAVEL_SQL)
        conn.commit()
    finally:
        conn.close()
    _TABLE_CREATED = True


def _get_conn() -> sqlite3.Connection:
    _ensure_table()
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA journal_mode=WAL")
    conn.execute("PRAGMA foreign_keys=ON")
    return conn


# ---------------------------------------------------------------------------
# Pydantic request bodies
# ---------------------------------------------------------------------------

class TravelCreate(BaseModel):
    employee_id: int
    destination: str
    purpose: Optional[str] = None
    departure_date: str
    return_date: Optional[str] = None
    transport_type: str
    # Cost breakdown
    estimated_cost: Optional[float] = 0
    transport_cost: Optional[float] = 0
    accommodation_needed: Optional[int] = 0
    accommodation_rate_per_night: Optional[float] = 0
    accommodation_nights: Optional[int] = 0
    accommodation_total: Optional[float] = 0
    daily_allowance_per_day: Optional[float] = 0
    daily_allowance_days: Optional[int] = 0
    daily_allowance_total: Optional[float] = 0
    meals_per_day: Optional[float] = 0
    meal_days: Optional[int] = 0
    meal_total: Optional[float] = 0
    additional_items: Optional[str] = ""
    notes: Optional[str] = ""
    grand_total: Optional[float] = 0


class TravelUpdate(BaseModel):
    employee_id: Optional[int] = None
    destination: Optional[str] = None
    purpose: Optional[str] = None
    departure_date: Optional[str] = None
    return_date: Optional[str] = None
    transport_type: Optional[str] = None
    accommodation_needed: Optional[int] = None
    estimated_cost: Optional[float] = None
    transport_cost: Optional[float] = None
    accommodation_rate_per_night: Optional[float] = None
    accommodation_nights: Optional[int] = None
    accommodation_total: Optional[float] = None
    daily_allowance_per_day: Optional[float] = None
    daily_allowance_days: Optional[int] = None
    daily_allowance_total: Optional[float] = None
    meals_per_day: Optional[float] = None
    meal_days: Optional[int] = None
    meal_total: Optional[float] = None
    additional_items: Optional[str] = None
    notes: Optional[str] = None
    grand_total: Optional[float] = None


class ApprovalBody(BaseModel):
    manager_id: Optional[int] = None
    director_id: Optional[int] = None
    notes: Optional[str] = ""


class RevisionBody(BaseModel):
    level: str  # "manager" or "director"
    reason: str  # Wajib alasan revisi
    approver_id: int


class FinanceSubmitBody(BaseModel):
    amount: float
    notes: Optional[str] = ""


class FinanceProcessBody(BaseModel):
    actual_cost: float
    advance_payment: float
    notes: Optional[str] = ""


class FinanceCompleteBody(BaseModel):
    finance_processed_by: int
    notes: Optional[str] = ""


# ---------------------------------------------------------------------------
# Status transition validators
# ---------------------------------------------------------------------------

_STATUS_TRANSITIONS = {
    'draft': ['pending_manager', 'pending_director', 'approved'],
    'pending_manager': ['pending_director', 'revision_required', 'pending_manager', 'rejected'],
    'revision_required': ['pending_manager', 'pending_director', 'approved'],  # Resubmit ke level yang sesuai
    'pending_director': ['approved', 'revision_required', 'pending_director', 'rejected'],
    'approved': ['completed', 'approved'],
    'rejected': ['draft', 'pending_manager', 'pending_director'],
    'completed': [],
}


def _validate_status_transition(current, target, transitions):
    valid_targets = transitions.get(current, [])
    if target not in valid_targets:
        raise HTTPException(
            status_code=400,
            detail=f"Cannot transition from '{current}' to '{target}'. Valid targets: {valid_targets}",
        )


def _create_notification(conn, user_id: int, title: str, message: str, link: str = "/travel"):
    try:
        conn.execute(
            "INSERT INTO notifications (user_id, title, message, is_read, link) VALUES (?, ?, ?, 0, ?)",
            (user_id, title, message, link)
        )
    except Exception as e:
        print(f"Error creating notification: {e}")


def _notify_travel_target(conn, travel_id: int, event_type: str, notes: str = ""):
    try:
        cur = conn.execute("""
            SELECT tr.*, e.full_name as emp_name, e.manager_id as direct_manager_id
            FROM travel_requests tr
            JOIN employees e ON tr.employee_id = e.id
            WHERE tr.id = ?
        """, (travel_id,))
        t = cur.fetchone()
        if not t:
            return
        
        emp_name = t["emp_name"]
        dest = t["destination"]
        total_cost = t["grand_total"] or t["estimated_cost"] or 0
        cost_str = f"Rp {int(total_cost):,}".replace(",", ".")

        if event_type == "submitted_to_manager":
            # Notify direct manager of the employee
            direct_mgr_id = t["direct_manager_id"]
            if direct_mgr_id:
                ucur = conn.execute("SELECT id FROM users WHERE employee_id = ?", (direct_mgr_id,))
                u = ucur.fetchone()
                if u:
                    _create_notification(
                        conn, u["id"],
                        "Pengajuan Perjalanan Dinas Baru",
                        f"{emp_name} mengajukan perjalanan dinas ke {dest} ({cost_str}) menunggu persetujuan Anda."
                    )
        elif event_type == "forwarded_to_director":
            # Notify all directors and super admins
            dcur = conn.execute("SELECT id FROM users WHERE role IN ('director', 'super_admin')")
            for u in dcur.fetchall():
                _create_notification(
                    conn, u["id"],
                    "Persetujuan Perjalanan Dinas (Direksi)",
                    f"Pengajuan perjalanan dinas {emp_name} ke {dest} ({cost_str}) memerlukan persetujuan Direktur Utama."
                )
        elif event_type == "approved":
            # Notify the employee who applied
            ucur = conn.execute("SELECT id FROM users WHERE employee_id = ?", (t["employee_id"],))
            u = ucur.fetchone()
            if u:
                _create_notification(
                    conn, u["id"],
                    "Perjalanan Dinas Disetujui",
                    f"Pengajuan perjalanan dinas Anda ke {dest} ({cost_str}) telah disetujui Direktur!"
                )
        elif event_type == "revision_required":
            # Notify the employee about revision
            ucur = conn.execute("SELECT id FROM users WHERE employee_id = ?", (t["employee_id"],))
            u = ucur.fetchone()
            if u:
                _create_notification(
                    conn, u["id"],
                    "Perjalanan Dinas Perlu Revisi",
                    f"Pengajuan ke {dest} dikembalikan untuk revisi. Catatan: {notes}"
                )
    except Exception as e:
        print(f"Error notifying travel target: {e}")


def _now():
    return datetime.utcnow().isoformat()


def _get_travel_or_404(conn, travel_id):
    cur = conn.execute("""
        SELECT tr.*, 
               e.full_name as employee_name, 
               e.employee_id_str,
               d.name as department_name,
               p.title as position_title
        FROM travel_requests tr
        LEFT JOIN employees e ON tr.employee_id = e.id
        LEFT JOIN departments d ON e.department_id = d.id
        LEFT JOIN positions p ON e.position_id = p.id
        WHERE tr.id = ?
    """, (travel_id,))
    row = cur.fetchone()
    if not row:
        raise HTTPException(status_code=404, detail="Travel request not found")
    return dict(row)


# ===========================================================================
# 1. GET /api/travel/stats — Dashboard stats
# ===========================================================================
@router.get("/stats")
def travel_stats():
    try:
        conn = _get_conn()
        try:
            total = conn.execute("SELECT COUNT(*) FROM travel_requests").fetchone()[0]
            pending_manager = conn.execute("SELECT COUNT(*) FROM travel_requests WHERE status='pending_manager'").fetchone()[0]
            pending_director = conn.execute("SELECT COUNT(*) FROM travel_requests WHERE status='pending_director'").fetchone()[0]
            revision_required = conn.execute("SELECT COUNT(*) FROM travel_requests WHERE status='revision_required'").fetchone()[0]
            approved = conn.execute("SELECT COUNT(*) FROM travel_requests WHERE status='approved'").fetchone()[0]
            completed = conn.execute("SELECT COUNT(*) FROM travel_requests WHERE status='completed'").fetchone()[0]
            rejected = conn.execute("SELECT COUNT(*) FROM travel_requests WHERE status='rejected'").fetchone()[0]
            total_cost = conn.execute("SELECT SUM(estimated_cost) FROM travel_requests").fetchone()[0] or 0
            return {
                "total": total,
                "pending_manager": pending_manager,
                "pending_director": pending_director,
                "revision_required": revision_required,
                "approved": approved,
                "completed": completed,
                "rejected": rejected,
                "total_cost": total_cost,
            }
        finally:
            conn.close()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ===========================================================================
# 2. GET /api/travel — List all (with optional filters)
# ===========================================================================
@router.get("")
def list_travels(
    status: Optional[str] = Query(None),
    finance_status: Optional[str] = Query(None),
):
    try:
        conn = _get_conn()
        try:
            query = """
                SELECT tr.*, 
                       e.full_name as employee_name, 
                       e.employee_id_str,
                       d.name as department_name,
                       p.title as position_title
                FROM travel_requests tr
                LEFT JOIN employees e ON tr.employee_id = e.id
                LEFT JOIN departments d ON e.department_id = d.id
                LEFT JOIN positions p ON e.position_id = p.id
                WHERE 1=1
            """
            params = []
            if status:
                query += f" AND tr.status = ?"
                params.append(status)
            if finance_status:
                query += f" AND tr.finance_status = ?"
                params.append(finance_status)
            query += " ORDER BY tr.id DESC"

            cur = conn.execute(query, params)
            results = [dict(r) for r in cur.fetchall()]
            return {"items": results, "total": len(results)}
        finally:
            conn.close()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ===========================================================================
# 3. GET /api/travel/{id} — Single travel request detail
# ===========================================================================
@router.get("/{travel_id}")
def get_travel(travel_id: int):
    try:
        conn = _get_conn()
        try:
            return _get_travel_or_404(conn, travel_id)
        finally:
            conn.close()
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ===========================================================================
# 4. POST /api/travel — Create new travel request (Auto-submit to approval queue)
# ===========================================================================
@router.post("", status_code=201)
def create_travel(body: TravelCreate):
    try:
        if body.transport_type not in ('car', 'bus', 'train', 'plane'):
            raise HTTPException(
                status_code=400,
                detail="transport_type must be one of car, bus, train, plane",
            )
        conn = _get_conn()
        try:
            # Verify employee exists and get department/position
            cur = conn.execute("""
                SELECT e.id, e.department_id, e.position_id, e.manager_id, p.title as pos_title
                FROM employees e
                LEFT JOIN positions p ON e.position_id = p.id
                WHERE e.id = ?
            """, (body.employee_id,))
            emp_row = cur.fetchone()
            if not emp_row:
                raise HTTPException(status_code=400, detail="Employee not found")

            pos_title = emp_row["pos_title"] or ""
            is_commissioner = (emp_row["department_id"] == 1 or emp_row["position_id"] == 1)
            is_director = (emp_row["position_id"] == 2 or "Direktur" in pos_title)
            is_manager = (emp_row["manager_id"] == 3 or "Manager" in pos_title or "Head" in pos_title)

            now = _now()
            if is_commissioner or is_director:
                init_status = "approved"
                mgr_id = None
                mgr_approved_at = None
                mgr_notes = None
                dir_id = body.employee_id
                dir_approved_at = now
                dir_notes = "Persetujuan Mandiri / Tugas Pimpinan"
                event_type = "approved"
            elif is_manager:
                init_status = "pending_director"
                mgr_id = body.employee_id
                mgr_approved_at = now
                mgr_notes = "Pengajuan Perjalanan Dinas Tingkat Manajer"
                dir_id = None
                dir_approved_at = None
                dir_notes = None
                event_type = "forwarded_to_director"
            else:
                init_status = "pending_manager"
                mgr_id = None
                mgr_approved_at = None
                mgr_notes = None
                dir_id = None
                dir_approved_at = None
                dir_notes = None
                event_type = "submitted_to_manager"

            # Generate sequential sppd_number starting from Gilang (1)
            cur_seq = conn.execute("SELECT COALESCE(MAX(sppd_number), 0) + 1 FROM travel_requests WHERE sppd_number IS NOT NULL")
            next_sppd_num = cur_seq.fetchone()[0]

            cur = conn.execute(
                """INSERT INTO travel_requests
                   (employee_id, sppd_number, destination, purpose, departure_date, return_date,
                    transport_type, accommodation_needed,
                    estimated_cost, transport_cost, accommodation_rate_per_night, accommodation_nights, accommodation_total,
                    daily_allowance_per_day, daily_allowance_days, daily_allowance_total,
                    meals_per_day, meal_days, meal_total,
                    additional_items, notes, grand_total, status,
                    manager_id, manager_approved_at, manager_notes,
                    director_id, director_approved_at, director_notes)
                   VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
                (
                    body.employee_id,
                    next_sppd_num,
                    body.destination,
                    body.purpose,
                    body.departure_date,
                    body.return_date,
                    body.transport_type,
                    body.accommodation_needed if body.accommodation_needed else 0,
                    body.grand_total or body.estimated_cost or 0,
                    body.transport_cost or 0,
                    body.accommodation_rate_per_night or 0,
                    body.accommodation_nights or 0,
                    body.accommodation_total or 0,
                    body.daily_allowance_per_day or 0,
                    body.daily_allowance_days or 0,
                    body.daily_allowance_total or 0,
                    body.meals_per_day or 0,
                    body.meal_days or 0,
                    body.meal_total or 0,
                    body.additional_items or "",
                    body.notes or "",
                    body.grand_total or 0,
                    init_status,
                    mgr_id,
                    mgr_approved_at,
                    mgr_notes,
                    dir_id,
                    dir_approved_at,
                    dir_notes
                ),
            )
            travel_id = cur.lastrowid
            conn.commit()

            # Trigger real-time notifications to direct manager / director
            _notify_travel_target(conn, travel_id, event_type)
            conn.commit()

            return {
                "id": travel_id,
                "status": init_status,
                "sppd_number": next_sppd_num,
                "message": "Pengajuan perjalanan dinas berhasil dibuat & langsung diajukan untuk persetujuan!"
            }
        finally:
            conn.close()
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ===========================================================================
# 5. PUT /api/travel/{id} — Update travel request (draft or revision_required)
# ===========================================================================
@router.put("/{travel_id}")
def update_travel(travel_id: int, body: TravelUpdate):
    try:
        conn = _get_conn()
        try:
            existing = _get_travel_or_404(conn, travel_id)
            if existing["status"] not in ("draft", "revision_required", "pending_director", "pending_manager"):
                raise HTTPException(
                    status_code=400,
                    detail="Can only update travel requests in draft, pending approval, or revision required status",
                )

            fields = {k: v for k, v in body.dict().items() if v is not None}
            if not fields:
                raise HTTPException(status_code=400, detail="No fields to update")

            if "transport_type" in fields and fields["transport_type"] not in ('car', 'bus', 'train', 'plane'):
                raise HTTPException(
                    status_code=400,
                    detail="transport_type must be one of car, bus, train, plane",
                )

            # Keep grand_total and estimated_cost in sync
            if "grand_total" in fields and "estimated_cost" not in fields:
                fields["estimated_cost"] = fields["grand_total"]
            elif "estimated_cost" in fields and "grand_total" not in fields:
                fields["grand_total"] = fields["estimated_cost"]

            fields["updated_at"] = _now()
            set_clause = ", ".join(f"{k} = ?" for k in fields)
            conn.execute(
                f"UPDATE travel_requests SET {set_clause} WHERE id = ?",
                list(fields.values()) + [travel_id],
            )
            conn.commit()
            return {"message": "Travel request updated successfully"}
        finally:
            conn.close()
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ===========================================================================
# 6. DELETE /api/travel/{id} — Delete travel request (draft only)
# ===========================================================================
@router.delete("/{travel_id}")
def delete_travel(travel_id: int):
    try:
        conn = _get_conn()
        try:
            existing = _get_travel_or_404(conn, travel_id)
            if existing["status"] != "draft":
                raise HTTPException(
                    status_code=400,
                    detail="Can only delete travel requests in draft status",
                )
            conn.execute("DELETE FROM travel_requests WHERE id = ?", (travel_id,))
            conn.commit()
            return {"message": "Travel request deleted"}
        finally:
            conn.close()
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ===========================================================================
# 7. POST /api/travel/{id}/submit — Submit for manager approval
# ===========================================================================
@router.post("/{travel_id}/submit")
def submit_travel(travel_id: int):
    try:
        conn = _get_conn()
        try:
            existing = _get_travel_or_404(conn, travel_id)
            
            # Get applicant position & department
            emp_cur = conn.execute("""
                SELECT e.id, e.department_id, e.position_id, e.manager_id, p.title as pos_title, d.name as dept_name
                FROM employees e
                LEFT JOIN positions p ON e.position_id = p.id
                LEFT JOIN departments d ON e.department_id = d.id
                WHERE e.id = ?
            """, (existing["employee_id"],))
            emp_row = emp_cur.fetchone()
            
            is_commissioner = emp_row and (emp_row["department_id"] == 1 or emp_row["position_id"] == 1)
            is_director = emp_row and (emp_row["position_id"] == 2 or "Direktur" in (emp_row["pos_title"] or ""))
            is_manager = emp_row and (emp_row["manager_id"] == 3 or "Manager" in (emp_row["pos_title"] or "") or "Head" in (emp_row["pos_title"] or ""))

            now = _now()
            if is_commissioner or is_director:
                # 1 Orang Tanda Tangan: Komisaris / Direktur Utama langsung approved (tanpa izin atasan)
                if existing["status"] == "approved":
                    return {"message": "Tugas Pimpinan / Direksi sudah disetujui (1 Tanda Tangan)"}
                conn.execute(
                    """UPDATE travel_requests 
                       SET status = 'approved',
                           director_id = ?,
                           director_approved_at = ?,
                           director_notes = 'Persetujuan Mandiri / Tugas Pimpinan',
                           updated_at = ?
                       WHERE id = ?""",
                    (existing["employee_id"], now, now, travel_id)
                )
                conn.commit()
                _notify_travel_target(conn, travel_id, "approved")
                conn.commit()
                return {"message": "Tugas Pimpinan / Direksi disetujui otomatis (1 Tanda Tangan)"}

            elif is_manager:
                # 2 Orang Tanda Tangan: Manager langsung ke Direktur Utama (bypass pending_manager)
                if existing["status"] == "pending_director":
                    return {"message": "Pengajuan Manajer sudah diteruskan ke Direktur Utama (2 Tanda Tangan)"}
                conn.execute(
                    """UPDATE travel_requests 
                       SET status = 'pending_director',
                           manager_id = ?,
                           manager_approved_at = ?,
                           manager_notes = 'Pengajuan Perjalanan Dinas Tingkat Manajer',
                           updated_at = ?
                       WHERE id = ?""",
                    (existing["employee_id"], now, now, travel_id)
                )
                conn.commit()
                _notify_travel_target(conn, travel_id, "forwarded_to_director")
                conn.commit()
                return {"message": "Pengajuan Manajer diteruskan langsung ke Direktur Utama (2 Tanda Tangan)"}

            else:
                # 3 Orang Tanda Tangan: Staf mengajukan ke Manager Divisi terlebih dahulu
                if existing["status"] == "pending_manager":
                    _notify_travel_target(conn, travel_id, "submitted_to_manager")
                    conn.commit()
                    return {"message": "Pengajuan sudah diteruskan dan sedang menunggu persetujuan Manajer (3 Tanda Tangan)"}
                _validate_status_transition(existing["status"], "pending_manager", _STATUS_TRANSITIONS)
                conn.execute(
                    "UPDATE travel_requests SET status = 'pending_manager', updated_at = ? WHERE id = ?",
                    (now, travel_id),
                )
                conn.commit()
                _notify_travel_target(conn, travel_id, "submitted_to_manager")
                conn.commit()
                return {"message": "Travel request submitted for manager approval (3 Tanda Tangan)"}
        finally:
            conn.close()
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ===========================================================================
# 8. POST /api/travel/{id}/approve-manager — Manager approves
# ===========================================================================
@router.post("/{travel_id}/approve-manager")
def approve_manager(travel_id: int, body: ApprovalBody):
    try:
        if not body.manager_id:
            raise HTTPException(status_code=400, detail="manager_id is required")
        conn = _get_conn()
        try:
            existing = _get_travel_or_404(conn, travel_id)
            _validate_status_transition(existing["status"], "pending_director", _STATUS_TRANSITIONS)

            now = _now()
            conn.execute(
                """UPDATE travel_requests
                   SET status = 'pending_director',
                       manager_id = ?,
                       manager_approved_at = ?,
                       manager_notes = ?,
                       manager_revision_reason = NULL,
                       updated_at = ?
                   WHERE id = ?""",
                (body.manager_id, now, body.notes, now, travel_id),
            )
            conn.commit()
            _notify_travel_target(conn, travel_id, "forwarded_to_director")
            conn.commit()
            return {"message": "Manager approved — pending director review"}
        finally:
            conn.close()
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ===========================================================================
# 9. POST /api/travel/{id}/revise-manager — Manager returns for revision
# ===========================================================================
@router.post("/{travel_id}/revise-manager")
def revise_manager(travel_id: int, body: RevisionBody):
    try:
        if body.level != "manager":
            raise HTTPException(status_code=400, detail="level must be 'manager'")
        if not body.reason or len(body.reason) < 5:
            raise HTTPException(status_code=400, detail="Alasan revisi wajib diisi minimal 5 karakter")
        if not body.approver_id:
            raise HTTPException(status_code=400, detail="approver_id is required")
            
        conn = _get_conn()
        try:
            existing = _get_travel_or_404(conn, travel_id)
            _validate_status_transition(existing["status"], "revision_required", _STATUS_TRANSITIONS)

            # Increment revision counter
            new_revision_count = (existing["revision_count"] or 0) + 1
            
            # Update history field (JSON string of revisions)
            import json
            history = existing.get("resubmit_history") or "[]"
            try:
                history_list = json.loads(history)
            except:
                history_list = []
            history_list.append({
                "revision": new_revision_count,
                "by_level": "manager",
                "by_approver_id": body.approver_id,
                "reason": body.reason,
                "at": _now()
            })
            history_str = json.dumps(history_list)
            
            now = _now()
            conn.execute(
                """UPDATE travel_requests
                   SET status = 'revision_required',
                       manager_revision_reason = ?,
                       revision_count = ?,
                       last_revision_by = 'manager',
                       last_revision_at = ?,
                       resubmit_history = ?,
                       updated_at = ?
                   WHERE id = ?""",
                (body.reason, new_revision_count, now, history_str, now, travel_id),
            )
            conn.commit()
            _notify_travel_target(conn, travel_id, "revision_required", body.reason)
            conn.commit()
            return {
                "message": f"Revision #{new_revision_count} requested by manager",
                "revision_number": new_revision_count,
                "reason": body.reason
            }
        finally:
            conn.close()
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ===========================================================================
# 10. POST /api/travel/{id}/revise-director — Director returns for revision
# ===========================================================================
@router.post("/{travel_id}/revise-director")
def revise_director(travel_id: int, body: RevisionBody):
    try:
        if body.level != "director":
            raise HTTPException(status_code=400, detail="level must be 'director'")
        if not body.reason or len(body.reason) < 5:
            raise HTTPException(status_code=400, detail="Alasan revisi wajib diisi minimal 5 karakter")
        if not body.approver_id:
            raise HTTPException(status_code=400, detail="approver_id is required")
            
        conn = _get_conn()
        try:
            existing = _get_travel_or_404(conn, travel_id)
            _validate_status_transition(existing["status"], "revision_required", _STATUS_TRANSITIONS)

            # Increment revision counter
            new_revision_count = (existing["revision_count"] or 0) + 1
            
            # Update history field
            import json
            history = existing.get("resubmit_history") or "[]"
            try:
                history_list = json.loads(history)
            except:
                history_list = []
            history_list.append({
                "revision": new_revision_count,
                "by_level": "director",
                "by_approver_id": body.approver_id,
                "reason": body.reason,
                "at": _now()
            })
            history_str = json.dumps(history_list)
            
            now = _now()
            conn.execute(
                """UPDATE travel_requests
                   SET status = 'revision_required',
                       director_revision_reason = ?,
                       revision_count = ?,
                       last_revision_by = 'director',
                       last_revision_at = ?,
                       resubmit_history = ?,
                       updated_at = ?
                   WHERE id = ?""",
                (body.reason, new_revision_count, now, history_str, now, travel_id),
            )
            conn.commit()
            _notify_travel_target(conn, travel_id, "revision_required", body.reason)
            conn.commit()
            return {
                "message": f"Revision #{new_revision_count} requested by director",
                "revision_number": new_revision_count,
                "reason": body.reason
            }
        finally:
            conn.close()
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ===========================================================================
# 11. POST /api/travel/{id}/approve-director — Director approves
# ===========================================================================
@router.post("/{travel_id}/approve-director")
def approve_director(travel_id: int, body: ApprovalBody):
    try:
        if not body.director_id:
            raise HTTPException(status_code=400, detail="director_id is required")
        conn = _get_conn()
        try:
            existing = _get_travel_or_404(conn, travel_id)
            _validate_status_transition(existing["status"], "approved", _STATUS_TRANSITIONS)

            now = _now()
            conn.execute(
                """UPDATE travel_requests
                   SET status = 'approved',
                       director_id = ?,
                       director_approved_at = ?,
                       director_notes = ?,
                       director_revision_reason = NULL,
                       updated_at = ?
                   WHERE id = ?""",
                (body.director_id, now, body.notes, now, travel_id),
            )
            conn.commit()
            _notify_travel_target(conn, travel_id, "approved")
            conn.commit()
            return {"message": "Director approved the travel request"}
        finally:
            conn.close()
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ===========================================================================
# 12. POST /api/travel/{id}/finance-submit — Finance receives
# ===========================================================================
@router.post("/{travel_id}/finance-submit")
def finance_submit(travel_id: int, body: FinanceSubmitBody):
    try:
        conn = _get_conn()
        try:
            existing = _get_travel_or_404(conn, travel_id)
            _validate_status_transition(
                existing["finance_status"], "submitted", {
                    'not_submitted': ['submitted'],
                    'submitted': ['processing'],
                    'processing': ['completed'],
                    'completed': [],
                }
            )

            now = _now()
            conn.execute(
                """UPDATE travel_requests
                   SET finance_status = 'submitted',
                       finance_amount = ?,
                       finance_notes = ?,
                       updated_at = ?
                   WHERE id = ?""",
                (body.amount, body.notes, now, travel_id),
            )
            conn.commit()
            return {"message": "Finance submission received"}
        finally:
            conn.close()
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ===========================================================================
# 13. POST /api/travel/{id}/finance-process — Finance processing
# ===========================================================================
@router.post("/{travel_id}/finance-process")
def finance_process(travel_id: int, body: FinanceProcessBody):
    try:
        conn = _get_conn()
        try:
            existing = _get_travel_or_404(conn, travel_id)
            _validate_status_transition(
                existing["finance_status"], "processing", {
                    'not_submitted': ['submitted'],
                    'submitted': ['processing'],
                    'processing': ['completed'],
                    'completed': [],
                }
            )

            now = _now()
            conn.execute(
                """UPDATE travel_requests
                   SET finance_status = 'processing',
                       actual_cost = ?,
                       advance_payment = ?,
                       finance_notes = ?,
                       updated_at = ?
                   WHERE id = ?""",
                (body.actual_cost, body.advance_payment, body.notes, now, travel_id),
            )
            conn.commit()
            return {"message": "Finance processing started"}
        finally:
            conn.close()
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ===========================================================================
# 14. POST /api/travel/{id}/finance-complete — Finance complete / transfer done
# ===========================================================================
@router.post("/{travel_id}/finance-complete")
def finance_complete(travel_id: int, body: FinanceCompleteBody):
    try:
        conn = _get_conn()
        try:
            existing = _get_travel_or_404(conn, travel_id)
            _validate_status_transition(
                existing["finance_status"], "completed", {
                    'not_submitted': ['submitted'],
                    'submitted': ['processing'],
                    'processing': ['completed'],
                    'completed': [],
                }
            )

            now = _now()
            # Finance complete also finalises the travel status to 'completed'
            conn.execute(
                """UPDATE travel_requests
                   SET finance_status = 'completed',
                       finance_processed_by = ?,
                       finance_processed_at = ?,
                       finance_notes = ?,
                       status = 'completed',
                       updated_at = ?
                   WHERE id = ?""",
                (body.finance_processed_by, now, body.notes, now, travel_id),
            )
            conn.commit()
            return {"message": "Finance processing completed — travel request closed"}
        finally:
            conn.close()
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
