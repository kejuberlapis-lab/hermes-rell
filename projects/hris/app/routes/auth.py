"""
Auth routes: login, logout, register, admin approval.
"""
from fastapi import APIRouter, Depends, HTTPException, Form, Response
from pydantic import BaseModel
from typing import Optional
from datetime import datetime
import aiosqlite

from app.database import get_db
from app.services.auth_service import verify_password, create_access_token, get_current_user, get_password_hash

router = APIRouter(prefix="/auth", tags=["auth"])

class LoginRequest(BaseModel):
    username: str
    password: str

# ---------------------------------------------------------------------------
# Public Register
# ---------------------------------------------------------------------------

class RegisterRequest(BaseModel):
    full_name: str
    email: str  # Changed from EmailStr to str (no email-validator needed)
    username: str
    phone: str
    department: Optional[str] = None
    position: Optional[str] = None
    password: str


@router.post("/register")
async def register(req: RegisterRequest, db: aiosqlite.Connection = Depends(get_db)):
    """Submit registration request (pending admin approval)."""
    hash_pw = get_password_hash(req.password)

    try:
        await db.execute(
            """INSERT INTO registration_requests 
               (full_name, email, username, phone, department, position, password_hash, status)
               VALUES (?, ?, ?, ?, ?, ?, ?, 'pending')""",
            (req.full_name, req.email, req.username, req.phone,
             req.department, req.position, hash_pw),
        )
        await db.commit()
    except Exception as e:
        raise HTTPException(status_code=409, detail=f"Email atau username sudah terdaftar")

    return {"message": "Registration submitted successfully"}


@router.get("/approvals")
async def list_approvals(db: aiosqlite.Connection = Depends(get_db)):
    """List pending registration approvals."""
    cursor = await db.execute(
        "SELECT * FROM registration_requests WHERE status='pending' ORDER BY id DESC"
    )
    rows = await cursor.fetchall()
    return {"requests": [dict(r) for r in rows]}


@router.post("/approve/{request_id}")
async def approve_request(request_id: int, user=Depends(get_current_user), db: aiosqlite.Connection = Depends(get_db)):
    """Approve a registration request and create user account."""
    cursor = await db.execute("SELECT * FROM registration_requests WHERE id = ?", (request_id,))
    reg = await cursor.fetchone()
    
    if not reg or reg["status"] != "pending":
        raise HTTPException(status_code=404, detail="Registration request not found")
    
    hash_pw = reg["password_hash"]
    
    try:
        # Create employee record in employees table
        cursor_emp = await db.execute(
            """INSERT INTO employees 
               (employee_id_str, full_name, email, phone, hire_date, status)
               VALUES (?, ?, ?, ?, date('now'), 'active')""",
            (f"MVP{datetime.now().strftime('%Y%m%d%H%M%S')}", reg["full_name"], reg["email"], reg["phone"]),
        )
        emp_id = cursor_emp.lastrowid
        
        # Create user record in users table
        await db.execute(
            """INSERT INTO users (username, email, password_hash, role, employee_id, is_active, is_verified)
               VALUES (?, ?, ?, 'employee', ?, 1, 1)""",
            (reg["username"], reg["email"], hash_pw, emp_id),
        )
        
        # Update registration request status
        await db.execute(
            "UPDATE registration_requests SET status='approved', approved_at=CURRENT_TIMESTAMP WHERE id=?",
            (request_id,),
        )
        
        await db.commit()
    except Exception as e:
        await db.rollback()
        raise HTTPException(status_code=500, detail=str(e))
    
    return {"message": f"User '{reg['full_name']}' approved and created successfully"}


@router.post("/reject/{request_id}")
async def reject_request(request_id: int, user=Depends(get_current_user), db: aiosqlite.Connection = Depends(get_db)):
    """Reject a registration request."""
    cursor = await db.execute("SELECT * FROM registration_requests WHERE id = ?", (request_id,))
    reg = await cursor.fetchone()
    
    if not reg or reg["status"] != "pending":
        raise HTTPException(status_code=404, detail="Registration request not found")
    
    await db.execute(
        "UPDATE registration_requests SET status='rejected', rejected_at=CURRENT_TIMESTAMP WHERE id=?",
        (request_id,),
    )
    await db.commit()
    
    return {"message": f"Registration request rejected."}


# ---------------------------------------------------------------------------
# Existing routes
# ---------------------------------------------------------------------------

@router.post("/login")
async def login(req: LoginRequest, response: Response, db: aiosqlite.Connection = Depends(get_db)):
    """Login with username/email/employee_id and password."""
    identifier = req.username.strip()
    cursor = await db.execute(
        """SELECT u.id, u.username, u.email, u.password_hash, u.role, u.is_active, u.employee_id,
                  COALESCE(e.full_name, u.username) as full_name
           FROM users u
           LEFT JOIN employees e ON u.employee_id = e.id
           WHERE LOWER(TRIM(u.username)) = LOWER(?)
              OR LOWER(TRIM(u.email)) = LOWER(?)
              OR LOWER(TRIM(COALESCE(e.email, ''))) = LOWER(?)
              OR LOWER(TRIM(COALESCE(e.employee_id_str, ''))) = LOWER(?)""",
        (identifier, identifier, identifier, identifier),
    )
    user = await cursor.fetchone()
    
    if not user or not user["password_hash"]:
        raise HTTPException(status_code=401, detail="Username atau password salah")
    
    if not user["is_active"]:
        raise HTTPException(status_code=403, detail="Akun tidak aktif. Hubungi administrator.")
    
    if not verify_password(req.password, user["password_hash"]):
        raise HTTPException(status_code=401, detail="Username atau password salah")
    
    role = user["role"] if user["role"] else "employee"
    full_name = user["full_name"] or user["username"]
    
    token = create_access_token({
        "user_id": user["id"],
        "username": user["username"],
        "role": role,
        "full_name": full_name,
        "employee_id": user["employee_id"],
    })
    
    # Set server-side cookie
    response.set_cookie(
        key="token",
        value=token,
        max_age=60 * 60 * 24,
        path="/",
        httponly=False,
        samesite="lax",
    )
    
    return {
        "token": token, 
        "user": {
            "id": user["id"], 
            "username": user["username"], 
            "role": role,
            "full_name": full_name,
            "email": user["email"],
            "employee_id": user["employee_id"]
        }
    }


class ChangePasswordRequest(BaseModel):
    old_password: str
    new_password: str

@router.post("/change-password")
async def change_password(req: ChangePasswordRequest, user=Depends(get_current_user), db: aiosqlite.Connection = Depends(get_db)):
    """Change current user password."""
    user_id = user["user_id"]
    cursor = await db.execute("SELECT password_hash FROM users WHERE id = ?", (user_id,))
    row = await cursor.fetchone()
    if not row:
        raise HTTPException(status_code=404, detail="User not found")
    
    if not verify_password(req.old_password, row["password_hash"]):
        raise HTTPException(status_code=400, detail="Password lama tidak sesuai")
    
    if len(req.new_password) < 6:
        raise HTTPException(status_code=400, detail="Password baru minimal 6 karakter")
    
    new_hash = get_password_hash(req.new_password)
    await db.execute("UPDATE users SET password_hash = ?, must_change_password = 0 WHERE id = ?", (new_hash, user_id))
    await db.commit()
    return {"message": "Password berhasil diubah"}

@router.post("/logout")
async def logout(response: Response, user=Depends(get_current_user)):
    response.delete_cookie(key="token", path="/")
    return {"message": "Logged out successfully"}


@router.get("/me")
async def get_me(user=Depends(get_current_user), db: aiosqlite.Connection = Depends(get_db)):
    uid = user.get("user_id") or user.get("id")
    cursor = await db.execute(
        """SELECT u.id, u.username, u.email, u.role, u.employee_id,
                  COALESCE(e.full_name, u.username) as full_name
           FROM users u
           LEFT JOIN employees e ON u.employee_id = e.id
           WHERE u.id = ?""",
        (uid,),
    )
    row = await cursor.fetchone()
    if not row:
        raise HTTPException(status_code=404, detail="User not found")
    return {
        "id": row["id"], 
        "username": row["username"], 
        "role": row["role"] if row["role"] else "employee",
        "full_name": row["full_name"],
        "email": row["email"],
        "employee_id": row["employee_id"],
    }
