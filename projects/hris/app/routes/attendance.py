"""
Attendance routes: clock in/out, records, summaries.
"""
from fastapi import APIRouter, Depends, HTTPException, Query, UploadFile, File
from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime, date, timedelta
import openpyxl
import io
import re
import math
import base64
import os
from pathlib import Path
from app.database import get_db
from app.services.auth_service import get_current_user
import aiosqlite
from app.routes.settings import get_all_settings

router = APIRouter(prefix="/attendance", tags=["attendance"])

def calculate_distance(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    """Calculate distance in meters between two GPS coordinates using Haversine formula."""
    try:
        R = 6371000  # Earth radius in meters
        dLat = math.radians(lat2 - lat1)
        dLon = math.radians(lon2 - lon1)
        a = (math.sin(dLat / 2) * math.sin(dLat / 2) +
             math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) *
             math.sin(dLon / 2) * math.sin(dLon / 2))
        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
        return R * c
    except Exception:
        return 0.0

def save_attendance_photo(photo_b64: str, prefix: str, emp_id: int, date_str: str) -> Optional[str]:
    """Save base64 image data to static/uploads/attendance/ and return web accessible path."""
    if not photo_b64:
        return None
    try:
        if "," in photo_b64:
            photo_b64 = photo_b64.split(",", 1)[1]
        img_bytes = base64.b64decode(photo_b64)
        
        timestamp = datetime.now().strftime("%H%M%S")
        filename = f"att_{prefix}_{emp_id}_{date_str.replace('-', '')}_{timestamp}.jpg"
        
        upload_dir = Path(__file__).resolve().parent.parent.parent / "static" / "uploads" / "attendance"
        upload_dir.mkdir(parents=True, exist_ok=True)
        
        file_path = upload_dir / filename
        with open(file_path, "wb") as f:
            f.write(img_bytes)
            
        return f"/static/uploads/attendance/{filename}"
    except Exception as e:
        print(f"Error saving attendance photo: {e}")
        return None

def _uid(user):
    return user.get("user_id") or user.get("id")

async def _resolve_emp_id(db, user):
    cursor = await db.execute("SELECT employee_id FROM users WHERE id = ?", (_uid(user),))
    row = await cursor.fetchone()
    return row["employee_id"] if row and row["employee_id"] else _uid(user)

CUSTOM_NAME_MAP = {
    'lim mei ie': 'MVP0008',               # Mei
    'auw septiawati keristin': 'MVP0010', # Kristin
    'herlambang': 'MVP0018',               # Bagus Juono
    'furkon': 'MVP0014',                   # Furqon
    'lily suwily': 'MVP0020',              # Meytilien
    'fitria': 'MVP0007',                   # Wina
    'joko agus widodo': 'MVP0031',         # Joko
    'andreas pakasi': 'MVP0005',           # Andreas
    'annisa bayyinatu jannah': 'MVP0004',  # Annisa
    'arvina mirdana': 'MVP0019',           # Arvina
    'gilang pramudhita': 'MVP0025',        # Gilang Ramadhan
    'abdul rahman': 'MVP0027',             # Rahman
    'iwan wijaya saputra': 'MVP0012',      # Iwan
    'jeni heryanto': 'MVP0013',            # Jeni
    'ravena theresia hedriyan': 'MVP0009', # Ravena
    'alwan ramadhani': 'MVP0006',          # Alwan
    'sugeng haryanto': 'MVP0030',          # Sugeng
    'sureha diah marwati': 'MVP0033',      # Sureha
    'agnes fransisca': 'MVP0011',          # Agnes
    'andi saputra': 'MVP0024',             # Andi Saputra
}

def match_employee_record(emp_list, name_str):
    if not name_str:
        return None
    clean = str(name_str).strip().lower()
    
    # 1. Custom dictionary match
    if clean in CUSTOM_NAME_MAP:
        target_str = CUSTOM_NAME_MAP[clean]
        for e in emp_list:
            if e['employee_id_str'] == target_str:
                return e

    # 2. Direct exact or substring match
    for e in emp_list:
        db_name = e['full_name'].strip().lower()
        if db_name == clean or db_name in clean or clean in db_name:
            return e

    # 3. Token intersection match
    parts_clean = set(re.findall(r'\w+', clean))
    for e in emp_list:
        parts_db = set(re.findall(r'\w+', e['full_name'].strip().lower()))
        if len(parts_clean.intersection(parts_db)) > 0:
            return e

    return None

@router.post("/import-excel")
async def import_attendance_excel(
    file: UploadFile = File(...),
    user=Depends(get_current_user),
    db: aiosqlite.Connection = Depends(get_db)
):
    role = user.get("role", "employee")
    emp_id = user.get("employee_id") or user.get("id")
    
    # Hak Akses: Super Admin atau Andreas (Manager GA - emp_id 5) atau role manager
    if role not in ["super_admin", "manager"]:
        raise HTTPException(status_code=403, detail="Hanya Manajer GA / Administrator yang dapat mengimpor data presensi.")

    if not file.filename.endswith(('.xlsx', '.xls')):
        raise HTTPException(status_code=400, detail="Format file harus berupa Excel (.xlsx / .xls)")

    contents = await file.read()
    try:
        wb = openpyxl.load_workbook(io.BytesIO(contents), data_only=True)
        ws = wb.active
    except Exception as ex:
        raise HTTPException(status_code=400, detail=f"Gagal membaca file Excel: {str(ex)}")

    # Fetch all employees from DB
    cursor = await db.execute("SELECT id, employee_id_str, full_name FROM employees")
    rows = await cursor.fetchall()
    emp_list = [dict(r) for r in rows]

    imported_count = 0
    updated_count = 0
    skipped_count = 0
    errors = []

    # Iterate rows starting from row 8 (standard fingerprint sheet)
    # Detect start row
    start_row = 1
    for r in range(1, min(25, ws.max_row + 1)):
        v2 = str(ws.cell(r, 2).value or '').strip().lower()
        v3 = str(ws.cell(r, 3).value or '').strip().lower()
        if 'no' in v2 and 'nama' in v3:
            start_row = r + 1
            break
        elif 'nama' in v2:
            start_row = r + 1
            break

    # If header found, advance past sub-headers
    for r in range(start_row, ws.max_row + 1):
        id_val = ws.cell(r, 2).value
        name_val = ws.cell(r, 3).value
        tgl_val = ws.cell(r, 4).value

        # Skip rows without name or summary rows
        if not id_val or not name_val or not tgl_val:
            continue
        if str(id_val).strip().lower() in ['no. id', 'no', 'id', 'total']:
            continue

        # Parse Date
        tgl_str = None
        if isinstance(tgl_val, datetime):
            tgl_str = tgl_val.strftime('%Y-%m-%d')
        elif isinstance(tgl_val, date):
            tgl_str = tgl_val.strftime('%Y-%m-%d')
        elif isinstance(tgl_val, str):
            for fmt_str in ['%d-%b-%y', '%d-%b-%Y', '%Y-%m-%d', '%d/%m/%Y', '%d-%m-%Y']:
                try:
                    tgl_str = datetime.strptime(tgl_val.strip(), fmt_str).strftime('%Y-%m-%d')
                    break
                except Exception:
                    pass

        if not tgl_str:
            skipped_count += 1
            continue

        matched_emp = match_employee_record(emp_list, str(name_val).strip())
        if not matched_emp:
            skipped_count += 1
            errors.append(f"Karyawan '{name_val}' tidak ditemukan di database.")
            continue

        scan_in = ws.cell(r, 7).value
        scan_out = ws.cell(r, 8).value
        terlambat = ws.cell(r, 9).value
        ket = ws.cell(r, 11).value

        scan_in_str = None
        if scan_in is not None:
            if hasattr(scan_in, 'strftime'):
                scan_in_str = scan_in.strftime('%H:%M')
            else:
                s_str = str(scan_in).strip()
                if s_str: scan_in_str = s_str[:5]

        scan_out_str = None
        if scan_out is not None:
            if hasattr(scan_out, 'strftime'):
                scan_out_str = scan_out.strftime('%H:%M')
            else:
                s_str = str(scan_out).strip()
                if s_str: scan_out_str = s_str[:5]

        ket_clean = str(ket).strip().lower() if ket else ''
        late_clean = str(terlambat).strip() if terlambat else ''

        status = 'present'
        notes_arr = []

        if 'terlambat' in ket_clean or (late_clean and late_clean != '0' and late_clean != '00:00'):
            status = 'late'
            notes_arr.append(f"Terlambat {late_clean}" if late_clean else "Terlambat")
        elif ket_clean in ['s', 'sakit']:
            status = 'sick'
            notes_arr.append('Sakit (Surat Dokter)')
        elif ket_clean in ['c', 'cuti']:
            status = 'leave'
            notes_arr.append('Cuti Tahunan')
        elif ket_clean in ['penugasan', 'dinas', 'tugas']:
            status = 'duty'
            notes_arr.append('Penugasan Luar Kantor')
        elif ket_clean in ['a', 'alpa', 'alpha'] or (not scan_in_str and not scan_out_str):
            status = 'absent'
            notes_arr.append('Tidak Masuk / Tanpa Keterangan')
        else:
            status = 'present'

        if ket and status == 'present':
            notes_arr.append(str(ket).strip())

        notes_str = "; ".join(notes_arr) if notes_arr else None

        # Check existing attendance record
        chk_cursor = await db.execute(
            "SELECT id FROM attendance WHERE employee_id = ? AND date = ?",
            (matched_emp['id'], tgl_str)
        )
        existing = await chk_cursor.fetchone()

        if existing:
            await db.execute(
                """UPDATE attendance
                   SET clock_in = ?, clock_out = ?, status = ?, notes = ?
                   WHERE id = ?""",
                (scan_in_str, scan_out_str, status, notes_str, existing['id'])
            )
            updated_count += 1
        else:
            await db.execute(
                """INSERT INTO attendance (employee_id, date, clock_in, clock_out, status, notes)
                   VALUES (?, ?, ?, ?, ?, ?)""",
                (matched_emp['id'], tgl_str, scan_in_str, scan_out_str, status, notes_str)
            )
            imported_count += 1

    await db.commit()

    return {
        "success": True,
        "message": f"Berhasil mengimpor {imported_count} data baru dan memperbarui {updated_count} data presensi.",
        "imported": imported_count,
        "updated": updated_count,
        "skipped": skipped_count,
        "errors": list(set(errors))[:10]
    }

class ClockAction(BaseModel):
    employee_id: Optional[int] = None
    notes: Optional[str] = None
    location_lat: Optional[float] = None
    location_lng: Optional[float] = None
    address: Optional[str] = None
    photo_base64: Optional[str] = None
    attendance_type: Optional[str] = "wfo"  # 'wfo', 'dinas' (duty)

@router.get("/today-status")
async def get_today_status(user=Depends(get_current_user), db: aiosqlite.Connection = Depends(get_db)):
    today = date.today().isoformat()
    emp_id = await _resolve_emp_id(db, user)
    settings = await get_all_settings(db)
    office_lat = float(settings.get("office_lat", -6.136820))
    office_lng = float(settings.get("office_lng", 106.797240))
    office_radius = float(settings.get("office_radius", 200.0))
    office_name = settings.get("office_name", "Kantor Pusat PT Mitsindo Visual Pratama")

    cursor = await db.execute("SELECT * FROM attendance WHERE employee_id = ? AND date = ?", (emp_id, today))
    row = await cursor.fetchone()
    if not row:
        return {
            "has_clocked_in": False,
            "has_clocked_out": False,
            "attendance": None,
            "office": {
                "lat": office_lat,
                "lng": office_lng,
                "radius": office_radius,
                "name": office_name
            }
        }
    att = dict(row)
    return {
        "has_clocked_in": bool(att.get("clock_in")),
        "has_clocked_out": bool(att.get("clock_out")),
        "attendance": att,
        "office": {
            "lat": office_lat,
            "lng": office_lng,
            "radius": office_radius,
            "name": office_name
        }
    }

@router.post("/clock-in")
async def clock_in(body: ClockAction = ClockAction(), user=Depends(get_current_user), db: aiosqlite.Connection = Depends(get_db)):
    today = date.today().isoformat()
    emp_id = body.employee_id or await _resolve_emp_id(db, user)
    now_dt = datetime.now()
    now = now_dt.strftime("%H:%M:%S")
    
    settings = await get_all_settings(db)
    office_lat = float(settings.get("office_lat", -6.136820))
    office_lng = float(settings.get("office_lng", 106.797240))
    office_radius = float(settings.get("office_radius", 200.0))
    strict_mode = settings.get("wfo_strict_mode", "0") == "1"
    
    cursor = await db.execute("SELECT id FROM attendance WHERE employee_id = ? AND date = ?", (emp_id, today))
    if await cursor.fetchone():
        raise HTTPException(status_code=400, detail="Anda sudah melakukan presensi masuk (Clock In) hari ini.")
        
    att_type = (body.attendance_type or "wfo").lower()
    if att_type not in ["wfo", "dinas", "duty"]:
        att_type = "wfo"
        
    dist_m = None
    if body.location_lat is not None and body.location_lng is not None:
        dist_m = round(calculate_distance(body.location_lat, body.location_lng, office_lat, office_lng), 1)
        
    # Geofence validation for WFO
    if att_type == "wfo":
        if strict_mode:
            if dist_m is None:
                raise HTTPException(status_code=400, detail="Lokasi GPS wajib diaktifkan untuk presensi WFO.")
            if dist_m > office_radius:
                dist_label = f"{dist_m/1000:.1f} km" if dist_m >= 1000 else f"{dist_m:.0f} meter"
                raise HTTPException(
                    status_code=400,
                    detail=f"Presensi WFO ditolak: Posisi Anda ({dist_label}) berada di luar radius kantor ({office_radius:.0f} meter). Silakan pilih 'Dinas Luar' jika bertugas di luar kantor."
                )
        
    # Status determination (present / late) with grace period
    status = "present"
    work_start_str = settings.get("work_start_time", "09:00")
    grace_mins = int(settings.get("grace_period_mins", "15"))
    try:
        start_parts = [int(x) for x in work_start_str.split(":")]
        start_dt = datetime.combine(now_dt.date(), datetime.min.time()).replace(hour=start_parts[0], minute=start_parts[1])
        grace_threshold = (start_dt + timedelta(minutes=grace_mins)).time()
        if now_dt.time() > grace_threshold:
            status = "late"
    except Exception:
        if now_dt.time() > datetime.strptime("09:15:00", "%H:%M:%S").time():
            status = "late"
        
    photo_url = None
    if body.photo_base64:
        photo_url = save_attendance_photo(body.photo_base64, "in", emp_id, today)
        
    await db.execute(
        """INSERT INTO attendance (
            employee_id, date, clock_in, status, notes,
            location_lat, location_lng, photo_in, address,
            distance_meters, attendance_type
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
        (
            emp_id, today, now, status, body.notes,
            body.location_lat, body.location_lng, photo_url, body.address,
            dist_m, att_type
        )
    )
    await db.commit()
    return {
        "success": True,
        "message": f"Presensi Masuk ({att_type.upper()}) berhasil dicatat pada {now} WIB ({status.upper()})",
        "date": today,
        "time": now,
        "status": status,
        "photo_url": photo_url,
        "distance_meters": dist_m,
        "attendance_type": att_type
    }

@router.post("/clock-out")
async def clock_out(body: ClockAction = ClockAction(), user=Depends(get_current_user), db: aiosqlite.Connection = Depends(get_db)):
    today = date.today().isoformat()
    emp_id = body.employee_id or await _resolve_emp_id(db, user)
    now = datetime.now().strftime("%H:%M:%S")
    
    settings = await get_all_settings(db)
    office_lat = float(settings.get("office_lat", -6.136820))
    office_lng = float(settings.get("office_lng", 106.797240))
    
    cursor = await db.execute("SELECT * FROM attendance WHERE employee_id = ? AND date = ?", (emp_id, today))
    row = await cursor.fetchone()
    if not row:
        raise HTTPException(status_code=400, detail="Belum ada catatan presensi masuk hari ini. Silakan Clock In terlebih dahulu.")
    if row["clock_out"]:
        raise HTTPException(status_code=400, detail="Anda sudah melakukan presensi keluar (Clock Out) hari ini.")
        
    dist_m = None
    if body.location_lat is not None and body.location_lng is not None:
        dist_m = round(calculate_distance(body.location_lat, body.location_lng, office_lat, office_lng), 1)
        
    photo_url = None
    if body.photo_base64:
        photo_url = save_attendance_photo(body.photo_base64, "out", emp_id, today)
        
    notes = row["notes"] or ""
    if body.notes:
        notes = f"{notes} | Out: {body.notes}" if notes else body.notes

    await db.execute(
        """UPDATE attendance SET 
            clock_out = ?,
            photo_out = ?,
            location_lat_out = ?,
            location_lng_out = ?,
            address_out = ?,
            notes = ?
        WHERE id = ?""",
        (now, photo_url, body.location_lat, body.location_lng, body.address, notes, row["id"])
    )
    await db.commit()
    return {
        "success": True,
        "message": f"Presensi Keluar berhasil dicatat pada {now} WIB",
        "date": today,
        "time": now,
        "photo_url": photo_url,
        "distance_meters": dist_m
    }

@router.get("")
async def list_attendance(
    employee_id: Optional[int] = Query(None),
    start_date: Optional[str] = Query(None),
    end_date: Optional[str] = Query(None),
    skip: int = 0, limit: int = 50,
    user=Depends(get_current_user), db: aiosqlite.Connection = Depends(get_db),
):
    conditions, params = [], []
    role = user.get("role", "employee")
    if role == "employee":
        emp_id = await _resolve_emp_id(db, user)
        conditions.append("a.employee_id = ?")
        params.append(emp_id)
    elif role == "manager":
        mgr_eid = await _resolve_emp_id(db, user)
        conditions.append("a.employee_id IN (SELECT id FROM employees WHERE manager_id = ?)")
        params.append(mgr_eid)
    if employee_id:
        conditions.append("a.employee_id = ?")
        params.append(employee_id)
    if start_date:
        conditions.append("a.date >= ?")
        params.append(start_date)
    if end_date:
        conditions.append("a.date <= ?")
        params.append(end_date)
    where = " WHERE " + " AND ".join(conditions) if conditions else ""
    q = f"""SELECT a.*, e.full_name FROM attendance a
            JOIN employees e ON a.employee_id = e.id
            {where} ORDER BY a.date DESC LIMIT ? OFFSET ?"""
    params.extend([limit, skip])
    cursor = await db.execute(q, params)
    rows = await cursor.fetchall()
    return {"attendance": [dict(r) for r in rows], "total": len(rows)}

@router.get("/summary")
async def attendance_company_summary(user=Depends(get_current_user), db: aiosqlite.Connection = Depends(get_db)):
    today = date.today().isoformat()
    cursor = await db.execute(
        """SELECT
           SUM(CASE WHEN status='present' THEN 1 ELSE 0 END) as present,
           SUM(CASE WHEN status='absent' THEN 1 ELSE 0 END) as absent,
           SUM(CASE WHEN status='late' THEN 1 ELSE 0 END) as late,
           SUM(CASE WHEN status='half_day' THEN 1 ELSE 0 END) as half_day
           FROM attendance WHERE date = ?""",
        (today,)
    )
    row = await cursor.fetchone()
    return {
        "present": row["present"] or 0,
        "absent": row["absent"] or 0,
        "late": row["late"] or 0,
        "half_day": row["half_day"] or 0,
        "on_leave": 0
    } if row else {"present": 0, "absent": 0, "late": 0, "half_day": 0, "on_leave": 0}

@router.get("/summary/{emp_id}")
async def attendance_summary(emp_id: int, month: Optional[str] = None, user=Depends(get_current_user), db: aiosqlite.Connection = Depends(get_db)):
    if user.get("role") == "employee":
        own = await _resolve_emp_id(db, user)
        if own != emp_id:
            raise HTTPException(status_code=403, detail="Access denied")
    like_pattern = f"{month}%" if month else f"{date.today().strftime('%Y-%m')}"
    cursor = await db.execute(
        """SELECT COUNT(*) as total_days,
           SUM(CASE WHEN status='present' THEN 1 ELSE 0 END) as present,
           SUM(CASE WHEN status='absent' THEN 1 ELSE 0 END) as absent,
           SUM(CASE WHEN status='late' THEN 1 ELSE 0 END) as late,
           SUM(CASE WHEN clock_out IS NOT NULL THEN 1 ELSE 0 END) as clocked_out
           FROM attendance WHERE employee_id = ? AND date LIKE ?""",
        (emp_id, like_pattern)
    )
    row = await cursor.fetchone()
    return dict(row) if row else {}
