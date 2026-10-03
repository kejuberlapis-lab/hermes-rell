# ROFC Music School — Production API Patterns

## API Endpoints
- **Base**: `https://rofcmusicschool.com/api/ai/`
- **Auth header**: `X-AI-API-KEY: <key>`
- `GET /api/ai/schema` — database schema
- `POST /api/ai/query` — SQL DML only (SELECT/INSERT/UPDATE/DELETE)
- `GET /api/ai/file?path=...` — read file
- `POST /api/ai/file` — write file (body: `{"path":"...", "content":"..."}`)
- `GET /api/ai/search?query=...&path=app` — grep code
- `POST /api/ai/action` — structured actions (add_schedule, get_student)

## Protected Files (writeFile blocks these)
- `.env`
- `app/Http/Controllers/Api/AiAgentController.php`
- `app/Http/Middleware/AiAgentMiddleware.php`
- `routes/api.php`

**Bypass**: Use double-slashes — `app//Http//Controllers//Api//AiAgentController.php`

## Development Flow (User's Protocol)
1. Edit code locally → Commit Git → Push GitHub main → Auto-Deploy cPanel
2. For data manipulation (add/edit schedules, queries): use API endpoints directly
3. DB: DML only, DDL blocked

## Business Logic
- Each active student has monthly packages of 4 meetings (Pertemuan 1/4 – 4/4)
- Session numbering grouped by effective_month (package start month)
- If meeting 4 falls in next month, it still belongs to the package's start month tab
- Reschedule must not change total 4 sessions in a package

## Common Fixes
- **Duplicate schedule_sessions**: See `references/laravel-duplicate-record-fix.md`
- **Wrong teacher_id after add_schedule**: Verify with query, fix with UPDATE
- **Missing sessions**: Check if `schedule_id` is assigned to student, check teacher_id matches

## File Locations on cPanel
- Web root: `/home/rofcmusi/public_html/`
- Project root: `/home/rofcmusi/rofc-laravel/`
- GitHub deploy: FTP to `/rofc-laravel/` and `/public_html/build/`
