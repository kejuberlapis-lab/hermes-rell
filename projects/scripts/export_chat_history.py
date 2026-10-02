#!/usr/bin/env python3
import sqlite3
import json
import os
import datetime

DB_PATH = '/home/ubuntu/.hermes/profiles/profil-admin-mvp/state.db'
OUT_DIR = '/home/ubuntu/hermes_vps_backup/hermes_core/chat_history'
os.makedirs(OUT_DIR, exist_ok=True)

conn = sqlite3.connect(DB_PATH)
c = conn.cursor()

c.execute('SELECT id, display_name, started_at, message_count, title FROM sessions ORDER BY started_at ASC')
sessions = c.fetchall()

print(f"Total sessions found: {len(sessions)}")

for sess_id, disp_name, started_at, msg_count, title in sessions:
    if started_at:
        try:
            if isinstance(started_at, (int, float)):
                dt = datetime.datetime.fromtimestamp(started_at)
                date_str = dt.strftime('%Y-%m-%d_%H%M')
            else:
                date_str = str(started_at)[:10]
        except Exception:
            date_str = "session"
    else:
        date_str = "session"

    title_safe = "".join(c if c.isalnum() or c in ('-', '_') else '_' for c in (title or disp_name or sess_id))[:35]
    filename = f"{date_str}_{sess_id[:8]}_{title_safe}.md"
    filepath = os.path.join(OUT_DIR, filename)

    c.execute('''
        SELECT role, content, tool_name, timestamp 
        FROM messages 
        WHERE session_id = ? 
        ORDER BY id ASC
    ''', (sess_id,))
    msgs = c.fetchall()

    if not msgs:
        continue

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(f"# Chat History — {title or disp_name or sess_id}\n\n")
        f.write(f"- **Session ID:** `{sess_id}`\n")
        f.write(f"- **Started At:** {date_str}\n")
        f.write(f"- **Total Messages:** {len(msgs)}\n\n---\n\n")

        for role, content, tool_name, ts in msgs:
            ts_str = ""
            if ts:
                try:
                    if isinstance(ts, (int, float)):
                        ts_str = f" *({datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')})*"
                    else:
                        ts_str = f" *({ts})*"
                except Exception:
                    pass

            if role == 'user':
                f.write(f"### 👤 User{ts_str}\n\n{content}\n\n---\n\n")
            elif role == 'assistant':
                f.write(f"### 🤖 Hermes Agent{ts_str}\n\n{content}\n\n---\n\n")
            elif role == 'tool':
                tool_label = tool_name or 'tool'
                content_str = str(content)
                if len(content_str) > 2000:
                    content_str = content_str[:2000] + "\n... [truncated]"
                f.write(f"#### ⚙️ Tool Result [{tool_label}]{ts_str}\n\n```\n{content_str}\n```\n\n---\n\n")

print(f"✓ All chat history successfully exported to Markdown in: {OUT_DIR}")
