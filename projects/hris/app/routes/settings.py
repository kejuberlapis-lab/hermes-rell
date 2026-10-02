"""
Settings routes: Company info, Attendance Geofence Rules, Office Coordinates.
"""
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from typing import Optional, Dict, Any
from app.database import get_db
from app.services.auth_service import get_current_user
import aiosqlite

router = APIRouter(prefix="/settings", tags=["settings"])

DEFAULT_OFFICE_SETTINGS = {
    "office_name": "Kantor Pusat PT Mitsindo Visual Pratama",
    "office_address": "Rukan Puri Delta Mas Blok I No. 46-47, Jalan Bandengan Selatan No. 43, Pejagalan, Penjaringan, Jakarta Utara, 14450",
    "office_lat": "-6.136820",
    "office_lng": "106.797240",
    "office_radius": "200",
    "enable_geofence": "1",
    "wfo_strict_mode": "0",  # 0 = flexible (record distance), 1 = strict (reject clock-in if outside radius)
    "work_start_time": "09:00",
    "work_end_time": "17:00",
    "grace_period_mins": "15"
}

async def get_all_settings(db: aiosqlite.Connection) -> Dict[str, str]:
    """Retrieve all company settings with defaults."""
    await db.execute("""
        CREATE TABLE IF NOT EXISTS company_settings (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            key TEXT NOT NULL UNIQUE,
            value TEXT NOT NULL,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    cursor = await db.execute("SELECT key, value FROM company_settings")
    rows = await cursor.fetchall()
    settings = dict(DEFAULT_OFFICE_SETTINGS)
    for r in rows:
        settings[r["key"]] = r["value"]
    return settings

async def set_setting(db: aiosqlite.Connection, key: str, value: str):
    """Upsert a single setting."""
    await db.execute("""
        CREATE TABLE IF NOT EXISTS company_settings (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            key TEXT NOT NULL UNIQUE,
            value TEXT NOT NULL,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    await db.execute("""
        INSERT INTO company_settings (key, value, updated_at)
        VALUES (?, ?, CURRENT_TIMESTAMP)
        ON CONFLICT(key) DO UPDATE SET value = excluded.value, updated_at = CURRENT_TIMESTAMP
    """, (key, str(value)))

class OfficeLocationUpdate(BaseModel):
    office_name: Optional[str] = None
    office_address: Optional[str] = None
    office_lat: float
    office_lng: float
    office_radius: float = 200.0
    enable_geofence: Optional[bool] = True
    wfo_strict_mode: Optional[bool] = False

class CompanySettingsUpdate(BaseModel):
    settings: Dict[str, Any]

@router.get("/company")
async def get_company_settings(user=Depends(get_current_user), db: aiosqlite.Connection = Depends(get_db)):
    """Get all settings (Accessible to all authenticated users)."""
    settings = await get_all_settings(db)
    return {"success": True, "settings": settings}

@router.get("/office-location")
async def get_office_location(user=Depends(get_current_user), db: aiosqlite.Connection = Depends(get_db)):
    """Get office coordinates & geofence config."""
    settings = await get_all_settings(db)
    return {
        "office_name": settings.get("office_name"),
        "office_address": settings.get("office_address"),
        "office_lat": float(settings.get("office_lat", -6.136820)),
        "office_lng": float(settings.get("office_lng", 106.797240)),
        "office_radius": float(settings.get("office_radius", 200.0)),
        "enable_geofence": settings.get("enable_geofence", "1") == "1",
        "wfo_strict_mode": settings.get("wfo_strict_mode", "0") == "1"
    }

@router.post("/office-location")
async def update_office_location(body: OfficeLocationUpdate, user=Depends(get_current_user), db: aiosqlite.Connection = Depends(get_db)):
    """Update office coordinates & geofence radius. Only Super Admin / Director can modify."""
    user_role = user.get("role", "")
    if user_role not in ["super_admin", "director", "admin"]:
        raise HTTPException(status_code=403, detail="Hanya Super Admin yang memiliki hak akses untuk mengubah titik koordinat kantor.")
    
    if body.office_name:
        await set_setting(db, "office_name", body.office_name)
    if body.office_address:
        await set_setting(db, "office_address", body.office_address)
    
    await set_setting(db, "office_lat", str(body.office_lat))
    await set_setting(db, "office_lng", str(body.office_lng))
    await set_setting(db, "office_radius", str(body.office_radius))
    await set_setting(db, "enable_geofence", "1" if body.enable_geofence else "0")
    await set_setting(db, "wfo_strict_mode", "1" if body.wfo_strict_mode else "0")
    
    await db.commit()
    
    return {
        "success": True,
        "message": "Pengaturan Titik Koordinat & Radius Geofencing Kantor berhasil disimpan!",
        "office_lat": body.office_lat,
        "office_lng": body.office_lng,
        "office_radius": body.office_radius
    }

@router.post("/save-section")
async def save_settings_section(body: Dict[str, Any], user=Depends(get_current_user), db: aiosqlite.Connection = Depends(get_db)):
    """Generic settings save endpoint for Super Admin."""
    if user.get("role") != "super_admin":
        raise HTTPException(status_code=403, detail="Hanya Super Admin yang dapat mengubah konfigurasi sistem.")
    
    for k, v in body.items():
        await set_setting(db, k, str(v))
    await db.commit()
    return {"success": True, "message": "Pengaturan berhasil diperbarui."}
