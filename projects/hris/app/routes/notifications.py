"""
Notification routes: list, mark as read.
"""
from fastapi import APIRouter, Depends, Query
from app.database import get_db
from app.services.auth_service import get_current_user
import aiosqlite

router = APIRouter(prefix="/notifications", tags=["notifications"])

def _uid(user):
    return user.get("user_id") or user.get("id")

@router.get("")
async def list_notifications(unread_only: bool = False, skip: int = 0, limit: int = 50, user=Depends(get_current_user), db: aiosqlite.Connection = Depends(get_db)):
    conditions = ["n.user_id = ?"]
    params = [_uid(user)]
    if unread_only:
        conditions.append("n.is_read = 0")
    where = " WHERE " + " AND ".join(conditions)
    cursor = await db.execute(f"SELECT * FROM notifications n{where} ORDER BY n.created_at DESC LIMIT ? OFFSET ?", params + [limit, skip])
    rows = await cursor.fetchall()
    count_cursor = await db.execute(f"SELECT COUNT(*) FROM notifications n{where}", params)
    total = (await count_cursor.fetchone())[0]
    unread_cursor = await db.execute("SELECT COUNT(*) FROM notifications WHERE user_id = ? AND is_read = 0", (_uid(user),))
    unread = (await unread_cursor.fetchone())[0]
    return {"notifications": [dict(r) for r in rows], "total": total, "unread": unread}

@router.put("/{notif_id}/read")
async def mark_as_read(notif_id: int, user=Depends(get_current_user), db: aiosqlite.Connection = Depends(get_db)):
    await db.execute("UPDATE notifications SET is_read = 1 WHERE id = ? AND user_id = ?", (notif_id, _uid(user)))
    await db.commit()
    return {"message": "Notification marked as read"}

@router.put("/read-all")
async def mark_all_read(user=Depends(get_current_user), db: aiosqlite.Connection = Depends(get_db)):
    await db.execute("UPDATE notifications SET is_read = 1 WHERE user_id = ? AND is_read = 0", (_uid(user),))
    await db.commit()
    return {"message": "All notifications marked as read"}
