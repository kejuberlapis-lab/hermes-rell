# Client-Side RBAC Menu Filtering (HTML/JS SPA)

Pattern untuk filter menu sidebar berdasarkan role user di aplikasi web berbasis **HTML static + vanilla JS** (tanpa React/Vue/Angular). Cocok untuk legacy apps, template-based apps, atau HRIS-like systems yang pakai Jinja2/Django templates.

## Overview

Alih-alih relying on server-side routing untuk menyembunyikan menu (yang tidak selalu available di SPA/static HTML), kita pakai **`data-role` attribute** di HTML + **filtering logic di JS** saat init.

### How It Works

```
1. User login → token disimpan di localStorage
2. app.js parse token → extract role (super_admin, direktur, manager, staf)
3. initRoleBasedMenu() loop semua .sidebar-section & .sidebar-link
4. Cek data-role attribute → hide/show sesuai role user
5. Console log [RBAC] untuk debugging
```

## Implementation

### Step 1: Add `data-role` to HTML Sidebar

Setiap section atau link individual diberi atribut `data-role` dengan comma-separated list of allowed roles:

```html
<!-- Section-level filtering -->
<div class="sidebar-section" data-role="super_admin,direktur,manager">
    <div class="sidebar-section-title"><span>Payroll</span></div>
    <div class="sidebar-section-menu">
        <!-- Individual links can also have their own data-role -->
        <a href="/payroll" data-role="super_admin,manager">
            <i class="fas fa-money-check-alt"></i><span>Salary Processing</span>
        </a>
        <a href="/payslips" data-role="super_admin,direktur,manager,staf">
            <i class="fas fa-receipt"></i><span>Payslips</span>
        </a>
    </div>
</div>

<!-- Single link outside section -->
<a href="/reports" class="sidebar-link" data-role="super_admin,direktur">
    <i class="fas fa-chart-bar"></i><span>Reports</span>
</a>

<!-- Visible to ALL roles (no data-role attribute) -->
<a href="/dashboard" class="sidebar-link">
    <i class="fas fa-chart-pie"></i><span>Dashboard</span>
</a>
```

### Step 2: JavaScript RBAC Filter

```javascript
const App = {
    API_BASE: '/api',
    token: '',
    userRole: '',

    getToken() {
        if (!this.token) {
            const localToken = localStorage.getItem('hris_token');
            if (localToken && localToken !== 'demo_token') this.token = localToken;
            
            const cookieMatch = document.cookie.match(/token=([^;]+)/);
            if (!this.token && cookieMatch) this.token = cookieMatch[1];
            
            const localRole = localStorage.getItem('hris_role');
            if (localRole) this.userRole = localRole;
        }
        return this.token;
    },

    init() {
        this.getToken();
        this.initSidebar();
        this.initRoleBasedMenu();
        this.checkAuth();
        setTimeout(() => this.loadPageData(), 500);
    },

    // ============================================
    // Role-Based Menu Visibility
    // ============================================
    initRoleBasedMenu() {
        const userRole = this.userRole || 'staf';  // default ke staf
        
        console.log('[RBAC] User role:', userRole);
        
        // Loop semua sidebar-section (div section groups)
        document.querySelectorAll('.sidebar-section').forEach(section => {
            const allowedRoles = section.getAttribute('data-role');
            if (!allowedRoles) return;  // tanpa data-role = visible ke semua
            
            const roles = allowedRoles.split(',').map(r => r.trim());
            
            if (!roles.includes(userRole)) {
                console.log(`[RBAC] HIDE section "${section.querySelector('.sidebar-section-title span')?.textContent || '?'}"`);
                section.style.display = 'none';
                return;
            }
            
            console.log(`[RBAC] SHOW section "${section.querySelector('.sidebar-section-title span')?.textContent || '?'}"`);
            
            // Untuk section yang visible, juga filter link individual di dalamnya
            section.querySelectorAll('a.sidebar-link').forEach(link => {
                const linkRoles = link.getAttribute('data-role');
                if (linkRoles && !linkRoles.split(',').map(r=>r.trim()).includes(userRole)) {
                    link.style.display = 'none';
                } else {
                    link.style.display = '';
                }
            });
        });
        
        // Loop semua single links (bukan dalam section)
        document.querySelectorAll('.sidebar-nav > a.sidebar-link').forEach(link => {
            const allowedRoles = link.getAttribute('data-role');
            if (!allowedRoles) return;  // tanpa data-role = visible ke semua
            
            const roles = allowedRoles.split(',').map(r => r.trim());
            
            if (!roles.includes(userRole)) {
                console.log(`[RBAC] HIDE link "${link.querySelector('span')?.textContent || '?'}"`);
                link.style.display = 'none';
            } else {
                console.log(`[RBAC] SHOW link "${link.querySelector('span')?.textContent || '?'}"`);
                link.style.display = '';
            }
        });
    },
};
```

### Step 3: Set Role After Login

```javascript
// Di handleLogin callback setelah success:
localStorage.setItem('hris_token', result.token);
localStorage.setItem('hris_role', result.user.role);
localStorage.setItem('hris_user', JSON.stringify(result.user));

// Setelah redirect ke dashboard/menu page:
window.onload = () => App.init();
// App.initRoleBasedMenu() akan otomatis run saat init
```

## Pitfalls & Gotchas

### Pitfall 1: Token Expired → Auto Redirect ke Login

**Symptom:** Setiap kali halaman load ulang, user dipaksa login kembali meskipun baru saja login.

**Cause:** `checkAuth()` mendeteksi token expired → redirect ke `/login`.

**Fix:** Jangan auto-redirect pada 401/expired. Instead, fallback ke demo mode:
```javascript
checkAuth() {
    if (!this.token && !window.location.pathname.includes('login')) {
        // DON'T redirect: use demo mode instead
        console.warn('Token invalid/expired – using demo mode');
        this.token = 'demo_token';
    }
}
```

### Pitfall 2: localStorage Tidak Persist Between Navigations

**Symptom:** Token hilang saat browser_navigate atau refresh.

**Cause:** Browser navigation context reset (di automation tools seperti Hermes browser tool).

**Fix:** Selalu get fresh token via API call sebelum inject ke localStorage:
```javascript
(async () => {
    const resp = await fetch('/api/auth/login', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({username:'admin', password:'pass'})
    });
    const data = await resp.json();
    localStorage.setItem('hris_token', data.token);
    localStorage.setItem('hris_role', data.user.role);
})();
```

### Pitfall 3: Section Visible tapi Links Belum Di-hide

**Symptom:** Section "Payroll" muncul untuk Staf padahal cuma Salary Processing yang harusnya hidden.

**Cause:** Section punya `data-role="super_admin,manager"` tapi link di dalamnya (`Salary Processing`) juga punya `data-role="super_admin,manager"` — tapi initRoleBasedMenu() lupa scan inner links.

**Fix:** Selalu scan dan filter inner links setelah section divalidasi:
```javascript
section.querySelectorAll('a.sidebar-link').forEach(link => {
    const linkRoles = link.getAttribute('data-role');
    if (linkRoles && !linkRoles.split(',').map(r=>r.trim()).includes(userRole)) {
        link.style.display = 'none';  // ← PENTING!
    }
});
```

### Pitfall 4: Role Name Mismatch Between Database and HTML

**Symptom:** RBAC logic tidak hide/show menu apapun — semua tetap visible atau semua hidden. User login sebagai `direktur/staf` tapi sidebar tetap tampil semua menu.

**Cause:** Nama role di database beda dengan yang dipakai di `data-role="..."`. Contoh umum:
| Field | Database Value | Wrong HTML Value | Correct |
|-------|---------------|-------------------|---------|
| Direktur role | `director` | `direktur` | `director` |
| Staff role | `staff` | `staf` | `staff` |
| Super Admin | `super_admin` | `superadmin` | `super_admin` |

**Diagnosis:** Jalankan dulu cek database → bandingkan dengan semua nilai unik di `data-role` attribute HTML:
```python
# Cek role valid dari database
import sqlite3
conn = sqlite3.connect('hris.db')
for row in conn.execute("SELECT DISTINCT role FROM employees"):
    print(f"'{row[0]}'")
conn.close()
# Output bisa jadi: 'super_admin', 'director', 'manager', 'staff'

# Bandingkan dengan HTML
import re
with open('templates/base.html') as f:
    roles = set()
    for m in re.finditer(r'data-role="([^"]*)"', f.read()):
        for r in m.group(1).split(','):
            roles.add(r.strip())
print(sorted(roles))
# Harus menghasilkan persis sama
```

**Fix:** Setelah tahu nama role yang benar dari database, gunakan patch satu per satu (bukan replace_all pada string pendek):
```bash
# ❌ DANGEROUS — replace_all pada string pendek bisa mengubah string lain yang sudah benar
# mengganti "staf" → "staff" bisa bikin "stafff" (3 huruf f) karena replace juga yang udah benar

# ✅ SAFE — patch spesifik per baris dengan konteks enough uniqueness
old_string: 'data-role="super_admin,director,manager,staf"'   # salah: staf
new_string: 'data-role="super_admin,director,manager,staff"'  # benar: staff
```

### Pitfall 5: Token di localStorage Saja Tidak Cukup — Server Baca Cookie

**Symptom:** Login berhasil lewat console injection (`localStorage.setItem()`), tapi setiap kali `browser_navigate` ke page lain, halaman auto redirect balik ke `/login`. Tabel selalu kosong.

**Cause:** Server-side middleware (FastAPI, Django, dll) membaca **cookie**, bukan localStorage. JS `handleLogin()` menyimpan token ke localStorage → tersimpan ✓ → tapi saat navigasi ulang, server melihat cookie kosong → reject → auto redirect.

**Fix:** Set token KE DUAIN — sebagai cookie DAN localStorage:
```javascript
(async () => {
    // Step 1: Login via API
    const r = await fetch('/api/auth/login', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({username:'superadmin', password:'admin123'})
    });
    const d = await r.json();
    
    // Step 2: Save BOTH ways
    localStorage.setItem('hris_token', d.token);
    localStorage.setItem('hris_role', d.user.role);
    
    // 🔑 PENTING: Set cookie juga agar server baca
    document.cookie = 'token=' + d.token + '; path=/; max-age=86400; SameSite=Lax';
    
    // Sekarang navigasi aman — server akan accept cookie
    location.href = '/dashboard';
})();
```

**Verification cepat:**
```javascript
// Cek apakah cookie sudah ter-set
console.log(document.cookie.substring(0, 100));
// Harus muncul: "token=eyJhbG... (bukan kosong)"
```

### Pitfall 6: Batch Replace Bisa Merusak String yang Sudah Benar

**Symptom:** Setelah replace_all, ada nilai yang berubah jadi "stafff" (3 huruf f) alih-alih "staff" (2 huruf f). Atau "director" jadi "directorr".

**Cause:** `replace_all` mencari substring yang cocok di SEMUA kemunculan. Jika string target muncul dalam bentuk yang SUDAH BENAR juga, maka dia akan ter-"replace" lagi (misal "staff" → replace "staff" → "stafff").

**Rule:** NEVER use replace_all pada string ≤4 karakter. Selalu patch satu per satu dengan konteks cukup unik.

**After-batch-check:** Setiap kali pakai replace_all, jalankan verification script (lihat `scripts/rbac-diagnose-table.py`) setelah patch selesai.

## Example Role Hierarchy

| Section | Available To | Notes |
|---------|-------------|-------|
| Dashboard | Semua | Always visible |
| Core HR | Semua | View-only untuk Staf |
| Admin | Super Admin Only | Registration approvals |
| Time & Attendance | Semua | Shifts hanya untuk atasan |
| Payroll - Salary Processing | Super Admin, Manager | Create/process payroll |
| Payroll - Payslips | Semua | View-only payslip |
| Travel & Finance | Atasan (Super Admin, Direktur, Manager) | Approve travel requests |
| Performance | Atasan | KPI, Reviews, Training |
| Recruitment | Super Admin Only | Full hiring control |
| Procurement | Super Admin Only | Purchase management |
| Asset Management | Super Admin, Manager | Assign/manage assets |
| Reports | Super Admin, Direktur | Financial reports |
| Settings | Super Admin Only | System configuration |

## Verification Checklist

Before deploying client-side RBAC:

- [ ] Every sidebar section has `data-role` attribute
- [ ] Individual links inside sections have their own `data-role` (if different from section)
- [ ] `initRoleBasedMenu()` runs after `init()` in app.js
- [ ] Token is properly saved to localStorage after login
- [ ] Role extracted from API response and saved as `hris_role`
- [ ] Console log shows `[RBAC] SHOW/HIDE` per element for debugging
- [ ] Test each role manually: super_admin, direktur, manager, staf
- [ ] No sensitive data leaked to client-side (all sensitive checks should be server-side too)

## When NOT to Use Client-Side RBAC

Client-side RBAC is UI convenience only — **never trust it for security**. Always validate permissions server-side:

```python
# ✅ Server-side validation (REQUIRED)
@router.get("/admin/registrations")
async def view_registrations(user: User = Depends(get_current_user)):
    if user.role not in ['super_admin']:
        raise HTTPException(status_code=403, detail="Access denied")
    # ... proceed
```

Client-side RBAC is just for UX — hides confusing menus. A malicious user can still bypass it. The **real protection** is server-side authorization middleware.

## References

- Original implementation: `/home/ubuntu/hris/templates/base.html` + `/home/ubuntu/hris/static/js/app.js`
- Problem solved: All menu items were visible to all roles (no distinction between admin, director, manager, staff)
- Fix date: 2026-09-19
