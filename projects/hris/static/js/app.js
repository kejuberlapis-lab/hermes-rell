/**
 * HRIS Application JavaScript
 * Handles UI interactions, API calls, charts, and form submissions
 */

const App = {
    API_BASE: '/api',
    token: '',
    userRole: '',

    // Helper to get fresh token from multiple sources
    getToken() {
        if (!this.token || this.token === 'demo_token') {
            const localToken = localStorage.getItem('hris_token');
            if (localToken && localToken !== 'demo_token') {
                this.token = localToken;
            } else if (document.cookie) {
                const cookieMatch = document.cookie.match(/(?:^|;\s*)token=([^;]+)/);
                if (cookieMatch && cookieMatch[1] && cookieMatch[1] !== 'demo_token') {
                    this.token = cookieMatch[1];
                }
            }
            const localRole = localStorage.getItem('hris_role');
            if (localRole) this.userRole = localRole;
        }
        return this.token;
    },

    // ============================================
    // Initialization
    // ============================================
    init() {
        this.getToken();  // Get token on init
        this.initSidebar();
        this.initRoleBasedMenu();
        this.initTableFilters();
        this.initNotifications();
        // Polling notifikasi live setiap 30 detik
        setInterval(() => this.initNotifications(), 30000);
        this.checkAuth();
        this.loadPageData();
    },

    loadPageData() {
        const path = window.location.pathname;
        if (path.includes('/dashboard')) this.loadDashboardStats();
        else if (path.includes('/employees')) this.loadEmployees();
        // else if (path.includes('/attendance')) this.loadAttendanceSummary();
        else if (path.includes('/travel')) this.loadTravelRequests();
        else if (path.includes('/leave')) this.loadLeaveRequests();
        else if (path.includes('/overtime')) this.loadOvertimeRequests();
        else if (path.includes('/payroll')) this.loadPayrollSummary();
        else if (path.includes('/assets')) this.loadAssetSummary();
    },

    // ============================================
    // Sidebar
    // ============================================
    initSidebar() {
        const toggle = document.getElementById('sidebarToggle');
        const close = document.getElementById('sidebarClose');
        const overlay = document.getElementById('sidebarOverlay');
        const sidebar = document.getElementById('sidebar');

        if (toggle) {
            toggle.addEventListener('click', () => {
                if (window.innerWidth <= 991) {
                    sidebar.classList.toggle('open');
                    overlay.classList.toggle('show');
                } else {
                    document.body.classList.toggle('sidebar-collapsed');
                    sidebar.classList.toggle('collapsed-sidebar');
                }
            });
        }

        if (close) {
            close.addEventListener('click', () => {
                sidebar.classList.remove('open');
                overlay.classList.remove('show');
            });
        }

        if (overlay) {
            overlay.addEventListener('click', () => {
                sidebar.classList.remove('open');
                overlay.classList.remove('show');
            });
        }

        // Section collapse/expand
        document.querySelectorAll('.sidebar-section-title').forEach(title => {
            title.addEventListener('click', () => {
                title.parentElement.classList.toggle('collapsed');
            });
        });
    },

    // ============================================
    // Role-Based Menu Visibility
    // ============================================
    initRoleBasedMenu() {
        const role = this.userRole || (this.user ? this.user.role : 'employee');
        if (role !== 'super_admin') {
            document.querySelectorAll('[data-role="super_admin"], .sidebar-admin').forEach(el => {
                el.style.display = 'none';
            });
        }
    },

    // ============================================
    // Authentication
    // ============================================
    checkAuth() {
        if (!this.token && !window.location.pathname.includes('login')) {
            // Uncomment for production:
            // window.location.href = '/login';
        }
    },

    handleLogin(event) {
        event.preventDefault();
        const form = event.target;
        const btn = document.getElementById('loginBtn');
        const spinner = btn ? btn.querySelector('.spinner-border') : null;
        const btnText = btn ? btn.querySelector('.btn-text') : null;

        if (btnText) btnText.textContent = 'Memproses...';
        if (spinner) spinner.classList.remove('d-none');
        if (btn) btn.disabled = true;

        const data = {
            username: form.username.value.trim(),
            password: form.password.value,
            remember: form.remember ? form.remember.checked : false
        };

        fetch(`${this.API_BASE}/auth/login`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(data)
        })
        .then(async res => {
            const result = await res.json().catch(() => ({}));
            if (res.ok && result.token) {
                this.token = result.token;
                this.user = result.user;
                this.userRole = result.user ? result.user.role : 'employee';
                localStorage.setItem('hris_token', result.token);
                localStorage.setItem('hris_role', this.userRole);
                localStorage.setItem('hris_user', JSON.stringify(result.user));
                const maxAge = data.remember ? (60 * 60 * 24 * 30) : (60 * 60 * 24); // 30 days if remember
                document.cookie = 'token=' + result.token + '; path=/; max-age=' + maxAge + '; SameSite=Lax';
                window.location.replace('/dashboard');
            } else {
                this.showAlert(result.detail || 'Username atau password salah', 'danger');
            }
        })
        .catch(err => {
            console.error('Login error:', err);
            this.showAlert('Gagal terhubung ke server. Silakan coba lagi.', 'danger');
        })
        .finally(() => {
            if (btnText) btnText.textContent = 'Sign In';
            if (spinner) spinner.classList.add('d-none');
            if (btn) btn.disabled = false;
        });

        return false;
    },

    logout() {
        localStorage.removeItem('hris_token');
        localStorage.removeItem('hris_role');
        localStorage.removeItem('hris_user');
        document.cookie = 'token=; expires=Thu, 01 Jan 1970 00:00:00 UTC; path=/;';
        window.location.href = '/';
    },

    showAlert(message, type) {
        const alert = document.getElementById('loginAlert');
        if (alert) {
            alert.className = `alert alert-${type}`;
            alert.textContent = message;
            alert.classList.remove('d-none');
        } else {
            // Fallback untuk login/register di halaman depan
            const globalAlert = document.getElementById('authAlert');
            if (globalAlert) {
                globalAlert.className = `alert alert-${type}`;
                globalAlert.textContent = message;
                globalAlert.classList.remove('d-none');
                setTimeout(() => globalAlert.classList.add('d-none'), 5000);
            }
        }
    },

    handleRegister(event) {
        event.preventDefault();
        const form = event.target;
        const btn = document.getElementById('regBtn');
        const spinner = btn.querySelector('.spinner-border');
        const btnText = btn.querySelector('.btn-text');

        btnText.textContent = 'Registering...';
        spinner.classList.remove('d-none');
        btn.disabled = true;

        const data = {
            full_name: form.full_name.value,
            email: form.email.value,
            username: form.username.value,
            phone: form.phone.value,
            department: form.department.value || null,
            position: form.position.value || null,
            password: form.password.value
        };

        fetch(`${this.API_BASE}/auth/register`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(data)
        })
        .then(res => res.json())
        .then(result => {
            if (result.message && !result.token) {
                showAlert('Registration successful! Please wait for admin approval.', 'success');
                // Reset form dan kembali ke login setelah 3 detik
                setTimeout(() => {
                    form.reset();
                    showLogin();
                }, 2000);
            } else if (result.detail) {
                showAlert(result.detail, 'danger');
            }
        })
        .catch(err => {
            console.error('Registration Error:', err);
            showAlert('An error occurred during registration.', 'danger');
        })
        .finally(() => {
            btnText.textContent = 'Create Account';
            spinner.classList.add('d-none');
            btn.disabled = false;
        });

        return false;
    },

    // ============================================
    // API Calls
    // ============================================
    apiCall(endpoint, method = 'GET', data = null) {
        const options = {
            method,
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${this.token}`
            }
        };
        if (data) options.body = JSON.stringify(data);

        return fetch(`${this.API_BASE}${endpoint}`, options)
            .then(res => {
                if (res.status === 401) {
                    this.logout();
                    return;
                }
                return res.json();
            })
            .catch(err => {
                console.error('API Error:', err);
                this.showToast('An error occurred. Please try again.', 'danger');
            });
    },

    // ============================================
    // Dashboard Charts
    // ============================================
    initDashboardCharts() {
        this.initAttendanceChart();
        this.initDeptChart();
    },

    initAttendanceChart() {
        const ctx = document.getElementById('attendanceChart');
        if (!ctx) return;

        new Chart(ctx, {
            type: 'line',
            data: {
                labels: ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat'],
                datasets: [
                    {
                        label: 'Present',
                        data: [142, 138, 140, 135, 142, 89],
                        borderColor: '#22c55e',
                        backgroundColor: 'rgba(34, 197, 94, 0.1)',
                        fill: true,
                        tension: 0.3,
                        pointRadius: 4,
                        pointHoverRadius: 6
                    },
                    {
                        label: 'Late',
                        data: [8, 12, 5, 15, 8, 3],
                        borderColor: '#f59e0b',
                        backgroundColor: 'rgba(245, 158, 11, 0.1)',
                        fill: true,
                        tension: 0.3,
                        pointRadius: 4,
                        pointHoverRadius: 6
                    },
                    {
                        label: 'Absent',
                        data: [6, 6, 11, 6, 6, 4],
                        borderColor: '#ef4444',
                        backgroundColor: 'rgba(239, 68, 68, 0.1)',
                        fill: true,
                        tension: 0.3,
                        pointRadius: 4,
                        pointHoverRadius: 6
                    }
                ]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: {
                        position: 'bottom',
                        labels: { usePointStyle: true, padding: 20, font: { size: 12 } }
                    }
                },
                scales: {
                    y: {
                        beginAtZero: true,
                        grid: { color: '#f0f0f0' },
                        ticks: { font: { size: 11 } }
                    },
                    x: {
                        grid: { display: false },
                        ticks: { font: { size: 11 } }
                    }
                }
            }
        });
    },

    initDeptChart() {
        const ctx = document.getElementById('deptChart');
        if (!ctx) return;

        new Chart(ctx, {
            type: 'doughnut',
            data: {
                labels: ['Engineering', 'Marketing', 'Finance', 'HR', 'Operations', 'Sales', 'IT'],
                datasets: [{
                    data: [35, 22, 18, 12, 20, 15, 34],
                    backgroundColor: [
                        '#1e3a5f', '#2c5282', '#3b82f6',
                        '#22c55e', '#f59e0b', '#ef4444', '#8b5cf6'
                    ],
                    borderWidth: 2,
                    borderColor: '#fff'
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                cutout: '65%',
                plugins: {
                    legend: {
                        position: 'bottom',
                        labels: {
                            usePointStyle: true,
                            padding: 12,
                            font: { size: 11 }
                        }
                    }
                }
            }
        });
    },

    initAttendanceChart() {
        const ctx = document.getElementById('attSummaryChart');
        if (!ctx) return;

        new Chart(ctx, {
            type: 'doughnut',
            data: {
                labels: ['Present', 'Absent', 'Late', 'On Leave'],
                datasets: [{
                    data: [142, 5, 8, 12],
                    backgroundColor: ['#22c55e', '#ef4444', '#f59e0b', '#3b82f6'],
                    borderWidth: 2,
                    borderColor: '#fff'
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                cutout: '60%',
                plugins: {
                    legend: {
                        position: 'bottom',
                        labels: { usePointStyle: true, padding: 12, font: { size: 11 } }
                    }
                }
            }
        });
    },

    // ============================================
    // Table Filtering & Search
    // ============================================
    initTableFilters() {
        // Global search
        const globalSearch = document.getElementById('globalSearch');
        if (globalSearch) {
            globalSearch.addEventListener('keyup', this.debounce(() => {
                const query = globalSearch.value.toLowerCase();
                this.showToast(`Searching for "${query}"...`, 'info');
            }, 300));
        }
    },

    filterEmployees() {
        const search = (document.getElementById('empSearch')?.value || '').toLowerCase();
        const dept = document.getElementById('empDeptFilter')?.value || '';
        const status = document.getElementById('empStatusFilter')?.value || '';
        const rows = document.querySelectorAll('#employeeTable tbody tr');

        rows.forEach(row => {
            const text = row.textContent.toLowerCase();
            const matchSearch = !search || text.includes(search);
            const matchDept = !dept || text.includes(dept.toLowerCase());
            const matchStatus = !status || row.querySelector(`.badge.bg-${status === 'active' ? 'success' : status === 'inactive' ? 'danger' : 'warning'}`);

            row.style.display = (matchSearch && matchDept) ? '' : 'none';
        });
    },

    resetEmployeeFilters() {
        document.getElementById('empSearch').value = '';
        document.getElementById('empDeptFilter').value = '';
        document.getElementById('empStatusFilter').value = '';
        document.getElementById('empPositionFilter').value = '';
        document.querySelectorAll('#employeeTable tbody tr').forEach(r => r.style.display = '');
    },

    // ============================================
    // Select All / Bulk Actions
    // ============================================
    toggleSelectAll(checkbox) {
        const checkboxes = document.querySelectorAll('.emp-check');
        checkboxes.forEach(cb => cb.checked = checkbox.checked);
        this.updateBulkActions();
    },

    updateBulkActions() {
        const checked = document.querySelectorAll('.emp-check:checked');
        const bar = document.getElementById('bulkActionsBar');
        const count = document.getElementById('selectedCount');

        if (bar) {
            if (checked.length > 0) {
                bar.classList.remove('d-none');
                if (count) count.textContent = checked.length;
            } else {
                bar.classList.add('d-none');
            }
        }
    },

    bulkAction(action) {
        const ids = Array.from(document.querySelectorAll('.emp-check:checked')).map(cb => cb.value);
        if (ids.length === 0) {
            this.showToast('No items selected', 'warning');
            return;
        }
        this.showToast(`Bulk ${action} action on ${ids.length} employees`, 'info');
    },

    // ============================================
    // Form Submissions
    // ============================================
    submitEmployee(event) {
        event.preventDefault();
        const form = event.target;
        const data = Object.fromEntries(new FormData(form));

        this.showToast('Employee added successfully', 'success');

        // Close modal
        const modal = bootstrap.Modal.getInstance(document.getElementById('addEmployeeModal'));
        if (modal) modal.hide();
        form.reset();
        return false;
    },

    submitLeaveRequest(event) {
        event.preventDefault();
        const form = event.target;
        const data = {
            leave_type_id: parseInt(form.leave_type_id.value) || 1,
            start_date: form.start_date.value,
            end_date: form.end_date.value,
            reason: form.reason.value || ''
        };

        fetch(`${this.API_BASE}/leave`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${this.token}`
            },
            body: JSON.stringify(data)
        })
        .then(async res => {
            if (!res.ok) {
                const err = await res.json().catch(() => ({}));
                throw new Error(err.detail || 'Gagal mengajukan permohonan cuti');
            }
            return res.json();
        })
        .then(result => {
            this.showToast('Pengajuan cuti berhasil dikirim!', 'success');
            const modalEl = document.getElementById('leaveRequestModal');
            if (modalEl) {
                const modal = bootstrap.Modal.getInstance(modalEl);
                if (modal) modal.hide();
            }
            setTimeout(() => window.location.reload(), 600);
        })
        .catch(err => {
            this.showToast(err.message, 'danger');
        });
        return false;
    },

    submitOvertimeRequest(event) {
        event.preventDefault();
        const form = event.target;
        const data = {
            date: form.date.value,
            hours: parseFloat(form.hours.value) || 2.0,
            reason: form.reason.value || ''
        };

        fetch(`${this.API_BASE}/overtime`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${this.token}`
            },
            body: JSON.stringify(data)
        })
        .then(async res => {
            if (!res.ok) {
                const err = await res.json().catch(() => ({}));
                throw new Error(err.detail || 'Gagal mengajukan permohonan lembur');
            }
            return res.json();
        })
        .then(result => {
            this.showToast('Pengajuan lembur berhasil dikirim!', 'success');
            const modalEl = document.getElementById('overtimeRequestModal');
            if (modalEl) {
                const modal = bootstrap.Modal.getInstance(modalEl);
                if (modal) modal.hide();
            }
            setTimeout(() => window.location.reload(), 600);
        })
        .catch(err => {
            this.showToast(err.message, 'danger');
        });
        return false;
    },

    submitReimbursementRequest(event) {
        event.preventDefault();
        const form = event.target;
        const data = {
            category: form.category.value,
            amount: parseFloat(form.amount.value) || 0,
            description: form.description.value || ''
        };

        fetch(`${this.API_BASE}/reimbursements`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${this.token}`
            },
            body: JSON.stringify(data)
        })
        .then(async res => {
            if (!res.ok) {
                const err = await res.json().catch(() => ({}));
                throw new Error(err.detail || 'Gagal mengajukan reimbursement');
            }
            return res.json();
        })
        .then(result => {
            this.showToast('Klaim reimbursement berhasil diajukan!', 'success');
            const modalEl = document.getElementById('reimbursementModal');
            if (modalEl) {
                const modal = bootstrap.Modal.getInstance(modalEl);
                if (modal) modal.hide();
            }
            setTimeout(() => window.location.reload(), 600);
        })
        .catch(err => {
            this.showToast(err.message, 'danger');
        });
        return false;
    },

    submitKpi(event) {
        event.preventDefault();
        this.showToast('KPI added successfully', 'success');
        return false;
    },

    openReviewModal(empId, empName, period, score, comments) {
        const empSelect = document.getElementById('reviewEmployeeId');
        const periodSelect = document.getElementById('reviewPeriod');
        const scoreInput = document.getElementById('reviewScore');
        const commentsInput = document.getElementById('reviewComments');
        
        if (empSelect && empId) empSelect.value = empId;
        if (periodSelect && period) periodSelect.value = period;
        if (scoreInput && score) scoreInput.value = score;
        if (commentsInput && comments) commentsInput.value = comments;
        
        const modalEl = document.getElementById('addReviewModal');
        if (modalEl) {
            const modal = bootstrap.Modal.getInstance(modalEl) || new bootstrap.Modal(modalEl);
            modal.show();
        }
    },

    submitPerformanceReview(event) {
        event.preventDefault();
        const form = event.target;
        const employeeId = parseInt(form.employee_id.value);
        const period = form.period.value;
        const reviewType = form.review_type ? form.review_type.value : 'manager';
        const score = parseFloat(form.score.value);
        const comments = form.comments.value.trim();

        if (!employeeId || isNaN(employeeId)) {
            this.showToast('Silakan pilih karyawan yang akan dinilai', 'warning');
            return false;
        }

        const data = {
            employee_id: employeeId,
            period: period,
            review_type: reviewType,
            score: score,
            comments: comments
        };

        fetch(`${this.API_BASE}/performance/reviews`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${this.token || this.getToken()}`
            },
            body: JSON.stringify(data)
        })
        .then(async res => {
            const result = await res.json().catch(() => ({}));
            if (!res.ok) throw new Error(result.detail || 'Gagal menyimpan penilaian kinerja');
            this.showToast('Penilaian kinerja berhasil disimpan!', 'success');
            const modalEl = document.getElementById('addReviewModal');
            if (modalEl) {
                const modal = bootstrap.Modal.getInstance(modalEl);
                if (modal) modal.hide();
            }
            setTimeout(() => window.location.reload(), 700);
        })
        .catch(err => {
            this.showToast(err.message, 'danger');
        });

        return false;
    },

    submitApplicant(event) {
        event.preventDefault();
        this.showToast('Applicant added successfully', 'success');
        return false;
    },

    submitProcurement(event) {
        event.preventDefault();
        this.showToast('Procurement request submitted', 'success');
        return false;
    },

    submitAsset(event) {
        event.preventDefault();
        this.showToast('Asset added successfully', 'success');
        return false;
    },

    submitTraining(event) {
        event.preventDefault();
        this.showToast('Training program created', 'success');
        return false;
    },

    saveSettings(event, section) {
        event.preventDefault();
        this.showToast(`${section} settings saved`, 'success');
        return false;
    },

    // ============================================
    // Actions
    // ============================================
    clockAction(type) {
        const endpoint = type === 'in' ? '/attendance/clock-in' : '/attendance/clock-out';
        fetch(`${this.API_BASE}${endpoint}`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${this.token}`
            },
            body: JSON.stringify({})
        })
        .then(async res => {
            if (!res.ok) {
                const err = await res.json().catch(() => ({}));
                throw new Error(err.detail || 'Clock action failed');
            }
            return res.json();
        })
        .then(result => {
            this.showToast(`Absensi ${type === 'in' ? 'Masuk' : 'Keluar'} berhasil dicatat pada ${result.time}!`, 'success');
            setTimeout(() => window.location.reload(), 700);
        })
        .catch(err => {
            this.showToast(err.message, 'warning');
        });
    },

    approveLeave(id) {
        fetch(`${this.API_BASE}/leave/${id}`, {
            method: 'PUT',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${this.token}`
            },
            body: JSON.stringify({ status: 'approved' })
        })
        .then(async res => {
            if (!res.ok) throw new Error('Gagal menyetujui cuti');
            this.showToast('Pengajuan cuti telah disetujui!', 'success');
            setTimeout(() => window.location.reload(), 600);
        })
        .catch(err => this.showToast(err.message, 'danger'));
    },

    rejectLeave(id) {
        fetch(`${this.API_BASE}/leave/${id}`, {
            method: 'PUT',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${this.token}`
            },
            body: JSON.stringify({ status: 'rejected' })
        })
        .then(async res => {
            if (!res.ok) throw new Error('Gagal menolak cuti');
            this.showToast('Pengajuan cuti ditolak', 'warning');
            setTimeout(() => window.location.reload(), 600);
        })
        .catch(err => this.showToast(err.message, 'danger'));
    },

    approveOvertime(id) {
        fetch(`${this.API_BASE}/overtime/${id}`, {
            method: 'PUT',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${this.token}`
            },
            body: JSON.stringify({ status: 'approved' })
        })
        .then(async res => {
            if (!res.ok) throw new Error('Gagal menyetujui lembur');
            this.showToast('Pengajuan lembur telah disetujui!', 'success');
            setTimeout(() => window.location.reload(), 600);
        })
        .catch(err => this.showToast(err.message, 'danger'));
    },

    rejectOvertime(id) {
        fetch(`${this.API_BASE}/overtime/${id}`, {
            method: 'PUT',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${this.token}`
            },
            body: JSON.stringify({ status: 'rejected' })
        })
        .then(async res => {
            if (!res.ok) throw new Error('Gagal menolak lembur');
            this.showToast('Pengajuan lembur ditolak', 'warning');
            setTimeout(() => window.location.reload(), 600);
        })
        .catch(err => this.showToast(err.message, 'danger'));
    },

    approveReimbursement(id) {
        fetch(`${this.API_BASE}/reimbursements/${id}`, {
            method: 'PUT',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${this.token}`
            },
            body: JSON.stringify({ status: 'approved' })
        })
        .then(async res => {
            if (!res.ok) throw new Error('Gagal menyetujui reimbursement');
            this.showToast('Klaim reimbursement disetujui!', 'success');
            setTimeout(() => window.location.reload(), 600);
        })
        .catch(err => this.showToast(err.message, 'danger'));
    },

    rejectReimbursement(id) {
        fetch(`${this.API_BASE}/reimbursements/${id}`, {
            method: 'PUT',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${this.token}`
            },
            body: JSON.stringify({ status: 'rejected' })
        })
        .then(async res => {
            if (!res.ok) throw new Error('Gagal menolak reimbursement');
            this.showToast('Klaim reimbursement ditolak', 'warning');
            setTimeout(() => window.location.reload(), 600);
        })
        .catch(err => this.showToast(err.message, 'danger'));
    },

    processPayroll() {
        const month = parseInt(document.getElementById('payrollMonth')?.value) || (new Date().getMonth() + 1);
        const year = parseInt(document.getElementById('payrollYear')?.value) || new Date().getFullYear();

        if (confirm(`Apakah Anda yakin ingin memproses penggajian (Payroll) untuk Periode ${month}/${year} untuk seluruh karyawan aktif?`)) {
            this.showToast('Sedang memproses kalkulasi gaji...', 'info');
            this.apiCall('/payroll/process', {
                method: 'POST',
                body: JSON.stringify({
                    period_month: month,
                    period_year: year
                })
            }).then(res => {
                if (res) {
                    this.showToast(res.message || 'Payroll berhasil diproses!', 'success');
                    setTimeout(() => window.location.reload(), 1500);
                }
            }).catch(err => {
                this.showToast(`Gagal memproses payroll: ${err.message}`, 'danger');
            });
        }
    },

    downloadPayslip(empId, periodMonth, periodYear) {
        const id = parseInt(empId);
        if (isNaN(id)) {
            this.showToast('Invalid employee ID', 'warning');
            return;
        }
        
        const month = periodMonth || new Date().getMonth() + 1;
        const year = periodYear || new Date().getFullYear();
        
        const url = `${this.API_BASE}/payroll/payslip/${id}?period_month=${month}&period_year=${year}`;
        
        fetch(url, {
            method: 'GET',
            headers: {
                'Authorization': `Bearer ${this.token}`,
                'Content-Type': 'application/json'
            }
        })
        .then(res => {
            if (!res.ok) throw new Error(`HTTP ${res.status}`);
            return res.json();
        })
        .then(data => {
            this.showToast('Payslip loaded successfully!', 'success');
            console.log('Payslip data:', data);
            
            const htmlContent = `<!DOCTYPE html>
<html>
<head>
    <title>Payslip - PT Mitsindo</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.min.css" rel="stylesheet">
    <style>
        body { font-family: 'Inter', sans-serif; background: #f8f9fa; padding: 40px; }
        .payslip-card { max-width: 700px; margin: 0 auto; background: white; padding: 40px; border-radius: 8px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }
        .header { text-align: center; border-bottom: 2px solid #1e3a5f; padding-bottom: 20px; margin-bottom: 30px; }
        .label { font-weight: 600; color: #6c757d; font-size: 0.85rem; }
        .value { font-weight: 600; color: #212529; }
        .money { font-family: 'Courier New', monospace; font-weight: 700; }
        .net-salary { background: #1e3a5f; color: white; padding: 15px; border-radius: 8px; text-align: center; margin-top: 20px; }
    </style>
</head>
<body>
    <div class="payslip-card">
        <div class="header text-center pb-3 border-bottom mb-4">
            <img src="/static/img/logo.png" alt="PT Mitsindo" style="width: 60px; height: 60px; object-fit: contain; margin-bottom: 8px;">
            <h3 style="color: #1e3a5f; font-weight: 700; margin-bottom: 2px;">PT MITSINDO</h3>
            <p class="text-muted mb-0" style="font-size: 0.9rem;">Human Resource Information System</p>
            <h5 class="mt-3 fw-bold text-dark">SLIP GAJI / PAYSLIP</h5>
        </div>
        
        <div class="row mb-4">
            <div class="col-6">
                <div class="label">Employee Name</div>
                <div class="value">${data.full_name || 'N/A'}</div>
            </div>
            <div class="col-6">
                <div class="label">Employee ID</div>
                <div class="value">${data.employee_id_str || 'N/A'}</div>
            </div>
        </div>
        <div class="row mb-4">
            <div class="col-6">
                <div class="label">Department</div>
                <div class="value">${data.department_name || 'N/A'}</div>
            </div>
            <div class="col-6">
                <div class="label">Period</div>
                <div class="value">${month}/${year}</div>
            </div>
        </div>
        
        <table class="table table-bordered">
            <thead class="table-light">
                <tr>
                    <th style="width: 60%;">Description</th>
                    <th class="text-end">Amount (Rp)</th>
                </tr>
            </thead>
            <tbody>
                <tr><td>Basic Salary</td><td class="text-end money">Rp ${typeof data.base_salary === 'number' ? data.base_salary.toLocaleString() : '0'}</td></tr>
                <tr><td>Allowance</td><td class="text-end money">Rp ${typeof data.allowance === 'number' ? data.allowance.toLocaleString() : '0'}</td></tr>
                <tr><td>Overtime Pay</td><td class="text-end money">Rp ${typeof data.overtime_pay === 'number' ? data.overtime_pay.toLocaleString() : '0'}</td></tr>
                <tr><td>Bonus</td><td class="text-end money">Rp ${typeof data.bonus === 'number' ? data.bonus.toLocaleString() : '0'}</td></tr>
                <tr class="table-danger"><td>Deduction</td><td class="text-end money">- Rp ${typeof data.deduction === 'number' ? data.deduction.toLocaleString() : '0'}</td></tr>
                <tr class="table-warning"><td>Tax (PPH21)</td><td class="text-end money">- Rp ${typeof data.tax_pph21 === 'number' ? data.tax_pph21.toLocaleString() : '0'}</td></tr>
                <tr class="table-info"><td>BPJS Ketenagakerjaan</td><td class="text-end money">- Rp ${typeof data.bpjs_ketenagakerjaan === 'number' ? data.bpjs_ketenagakerjaan.toLocaleString() : '0'}</td></tr>
                <tr class="table-info"><td>BPJS Kesehatan</td><td class="text-end money">- Rp ${typeof data.bpjs_kesehatan === 'number' ? data.bpjs_kesehatan.toLocaleString() : '0'}</td></tr>
            </tbody>
        </table>
        
        <div class="net-salary">
            <div class="label mb-2" style="font-size: 1rem;">NET SALARY</div>
            <div style="font-size: 1.8rem;" class="money">Rp ${typeof data.net_salary === 'number' ? data.net_salary.toLocaleString() : '0'}</div>
        </div>
        
        <hr class="my-4">
        <div class="text-center text-muted small">
            Generated on ${new Date().toLocaleDateString()} at ${new Date().toLocaleTimeString()}<br>
            This is a system-generated document. No signature required.
        </div>
        
        <div class="text-center mt-4">
            <button onclick="window.print()" class="btn btn-primary me-2"><i class="fas fa-print"></i> Print</button>
            <button onclick="window.close()" class="btn btn-outline-secondary"><i class="fas fa-times"></i> Close</button>
        </div>
    </div>
</body>
</html>`;
            
            const win = window.open('', '_blank');
            if (win) {
                win.document.write(htmlContent);
                win.document.close();
            }
        })
        .catch(err => {
            console.error('Payslip error:', err);
            let errorMsg = 'Failed to load payslip';
            if (err.message.includes('401')) errorMsg = 'Please login again to access payslips';
            else if (err.message.includes('403')) errorMsg = 'You are not authorized to view this payslip';
            else if (err.message.includes('404')) errorMsg = 'Payslip not found for this period';
            this.showToast(errorMsg, 'danger');
        });
    },

    moveApplicant(id, stage) {
        this.showToast(`Applicant moved to ${stage}`, 'success');
    },

    confirmDelete(type, id) {
        if (!confirm(`Are you sure you want to delete this ${type}? This action cannot be undone.`)) return;
        fetch(`${this.API_BASE}/${type}s/${id}`, {
            method: 'DELETE',
            headers: { 'Authorization': `Bearer ${this.token}` }
        })
        .then(res => {
            if (!res.ok) throw new Error(`HTTP ${res.status}`);
            return res.json();
        })
        .then(() => {
            this.showToast(`${type} deleted successfully`, 'success');
            // Remove the closest table row
            const row = document.querySelector(`tr:has(input[value="${id}"])`) ||
                        document.querySelector(`button[onclick*="${type}'\\,${id}"]`)?.closest('tr');
            if (row) row.remove();
        })
        .catch(err => {
            console.error('Delete error:', err);
            this.showToast(`Failed to delete ${type}: ${err.message}`, 'danger');
        });
    },

    // ============================================
    // Modal Helpers
    // ============================================
    showEditModal(title, id, fields) {
        const modalId = 'editModal_' + Date.now();
        const fieldsHtml = fields.map(f => {
            if (f.type === 'select') {
                const opts = f.options.map(o => `<option value="${o}" ${o === f.value ? 'selected' : ''}>${o}</option>`).join('');
                return `<div class="mb-3"><label class="form-label fw-semibold">${f.label}</label><select class="form-select" name="${f.name}" id="${f.name}">${opts}</select></div>`;
            }
            return `<div class="mb-3"><label class="form-label fw-semibold">${f.label}</label><input type="${f.type || 'text'}" class="form-control" name="${f.name}" id="${f.name}" value="${f.value || ''}"></div>`;
        }).join('');

        const modalHtml = `
        <div class="modal fade" id="${modalId}" tabindex="-1">
            <div class="modal-dialog"><div class="modal-content">
                <div class="modal-header"><h5 class="modal-title fw-bold">${title} #${id}</h5><button type="button" class="btn-close" data-bs-dismiss="modal"></button></div>
                <div class="modal-body"><form id="${modalId}_form">${fieldsHtml}</form></div>
                <div class="modal-footer">
                    <button type="button" class="btn btn-light" data-bs-dismiss="modal">Cancel</button>
                    <button type="button" class="btn btn-primary" onclick="App.saveEdit('${modalId}', '${title.toLowerCase()}', ${id})">Save Changes</button>
                </div>
            </div></div>
        </div>`;
        document.body.insertAdjacentHTML('beforeend', modalHtml);
        const modal = new bootstrap.Modal(document.getElementById(modalId));
        modal.show();
        document.getElementById(modalId).addEventListener('hidden.bs.modal', () => document.getElementById(modalId).remove());
    },

    saveEdit(modalId, type, id) {
        const form = document.getElementById(modalId + '_form');
        const data = Object.fromEntries(new FormData(form));
        fetch(`${this.API_BASE}/${type}/${id}`, {
            method: 'PUT',
            headers: {'Content-Type': 'application/json', 'Authorization': `Bearer ${this.token}`},
            body: JSON.stringify(data)
        })
        .then(res => {
            if (!res.ok) throw new Error(`HTTP ${res.status}`);
            return res.json();
        })
        .then(() => {
            bootstrap.Modal.getInstance(document.getElementById(modalId)).hide();
            this.showToast(`${type} updated successfully`, 'success');
            setTimeout(() => location.reload(), 1000);
        })
        .catch(err => this.showToast(`Failed to save: ${err.message}`, 'danger'));
    },

    showDetailModal(title, rows) {
        const modalId = 'detailModal_' + Date.now();
        const rowsHtml = rows.map(([k,v]) => `<tr><td class="fw-semibold text-muted" style="width:140px">${k}</td><td>${v || '-'}</td></tr>`).join('');
        const html = `
        <div class="modal fade" id="${modalId}" tabindex="-1">
            <div class="modal-dialog"><div class="modal-content">
                <div class="modal-header"><h5 class="modal-title fw-bold">${title}</h5><button type="button" class="btn-close" data-bs-dismiss="modal"></button></div>
                <div class="modal-body"><table class="table table-borderless">${rowsHtml}</table></div>
                <div class="modal-footer"><button type="button" class="btn btn-light" data-bs-dismiss="modal">Close</button></div>
            </div></div>
        </div>`;
        document.body.insertAdjacentHTML('beforeend', html);
        const modal = new bootstrap.Modal(document.getElementById(modalId));
        modal.show();
        document.getElementById(modalId).addEventListener('hidden.bs.modal', () => document.getElementById(modalId).remove());
    },

    // ============================================
    // Entity Edit / View / Approve Actions
    // ============================================
    editEmployee(id) {
        fetch(`${this.API_BASE}/employees/${id}`, {headers: {'Authorization': `Bearer ${this.token}`}})
        .then(r => r.json())
        .then(emp => {
            const e = emp.data || emp;
            this.showEditModal('Edit Employee', id, [
                {name: 'full_name', label: 'Full Name', value: e.full_name, type: 'text'},
                {name: 'email', label: 'Email', value: e.email, type: 'text'},
                {name: 'phone', label: 'Phone', value: e.phone, type: 'text'},
                {name: 'department_id', label: 'Department ID', value: e.department_id, type: 'number'},
                {name: 'position_id', label: 'Position ID', value: e.position_id, type: 'number'},
                {name: 'status', label: 'Status', value: e.status, type: 'select', options: ['active','inactive','on_leave']}
            ]);
        })
        .catch(err => this.showToast('Failed to load employee: ' + err.message, 'danger'));
    },

    viewEmployee(id) {
        window.location.href = `/employees/${id}`;
    },

    editAsset(id) {
        fetch(`${this.API_BASE}/assets/${id}`, {headers: {'Authorization': `Bearer ${this.token}`}})
        .then(r => r.json())
        .then(a => {
            const d = a.data || a;
            this.showEditModal('Edit Asset', id, [
                {name: 'name', label: 'Asset Name', value: d.name, type: 'text'},
                {name: 'asset_code', label: 'Asset Code', value: d.asset_code, type: 'text'},
                {name: 'category', label: 'Category', value: d.category, type: 'text'},
                {name: 'status', label: 'Status', value: d.status, type: 'select', options: ['available','in_use','maintenance','retired']}
            ]);
        })
        .catch(err => this.showToast('Failed to load asset: ' + err.message, 'danger'));
    },

    viewAsset(id) {
        fetch(`${this.API_BASE}/assets/${id}`, {headers: {'Authorization': `Bearer ${this.token}`}})
        .then(r => r.json())
        .then(a => {
            const d = a.data || a;
            this.showDetailModal('Asset Details', [
                ['Name', d.name], ['Code', d.asset_code], ['Category', d.category],
                ['Status', d.status], ['Location', d.location], ['Purchase Date', d.purchase_date]
            ]);
        })
        .catch(err => this.showToast('Failed to load asset', 'danger'));
    },

    editShift(id) {
        this.showEditModal('Edit Shift', id, [
            {name: 'name', label: 'Shift Name', value: '', type: 'text'},
            {name: 'start_time', label: 'Start Time', value: '', type: 'text'},
            {name: 'end_time', label: 'End Time', value: '', type: 'text'}
        ]);
    },

    editReview(id) {
        this.showEditModal('Edit Review', id, [
            {name: 'review_title', label: 'Review Title', value: '', type: 'text'},
            {name: 'rating', label: 'Rating', value: '', type: 'select', options: ['1','2','3','4','5']}
        ]);
    },

    viewReview(id) {
        this.showDetailModal('Review Details', [['Review', 'Performance Review #' + id], ['Status', 'Completed']]);
    },

    editTraining(id) {
        this.showEditModal('Edit Training', id, [
            {name: 'title', label: 'Title', value: '', type: 'text'},
            {name: 'category', label: 'Category', value: '', type: 'text'}
        ]);
    },

    viewTraining(id) {
        this.showDetailModal('Training Details', [['Program', 'Training #' + id]]);
    },

    editRole(id) {
        this.showEditModal('Edit Role', id, [
            {name: 'role_name', label: 'Role Name', value: '', type: 'text'}
        ]);
    },

    viewDocument(id) {
        this.showDetailModal('Document Details', [['Document', 'Document #' + id]]);
    },

    editOrgChart() {
        this.showToast('Org Chart editor coming soon', 'info');
    },

    viewReimbursement(id) {
        this.showDetailModal('Reimbursement Details', [['Reimbursement', 'Request #' + id]]);
    },

    approveReimbursement(id) {
        if (!confirm('Approve this reimbursement request?')) return;
        fetch(`${this.API_BASE}/reimbursements/${id}/approve`, {
            method: 'POST',
            headers: {'Authorization': `Bearer ${this.token}`}
        })
        .then(r => { if (!r.ok) throw new Error('HTTP ' + r.status); return r.json(); })
        .then(() => { this.showToast('Reimbursement approved', 'success'); setTimeout(() => location.reload(), 1000); })
        .catch(err => this.showToast('Failed: ' + err.message, 'danger'));
    },

    rejectReimbursement(id) {
        if (!confirm('Reject this reimbursement request?')) return;
        fetch(`${this.API_BASE}/reimbursements/${id}/reject`, {
            method: 'POST',
            headers: {'Authorization': `Bearer ${this.token}`}
        })
        .then(r => { if (!r.ok) throw new Error('HTTP ' + r.status); return r.json(); })
        .then(() => { this.showToast('Reimbursement rejected', 'danger'); setTimeout(() => location.reload(), 1000); })
        .catch(err => this.showToast('Failed: ' + err.message, 'danger'));
    },

    viewRequisition(id) {
        this.showDetailModal('Requisition Details', [['Requisition', 'Requisition #' + id]]);
    },

    viewInterview(id) {
        this.showDetailModal('Interview Details', [['Interview', 'Interview #' + id]]);
    },

    refreshDashboard() {
        this.showToast('Dashboard refreshed', 'info');
    },

    generateReport(reportType) {
        const format = document.querySelector('#reportFormat')?.value || 'excel';
        const period = document.querySelector('#reportPeriod')?.value || '';
        
        // Map report types to export modules
        const moduleMap = {
            'Headcount Report': 'employees',
            'Attendance Summary': 'attendance',
            'Payroll Summary': 'payroll',
            'Leave Report': 'leaves',
            'Overtime Report': 'overtime',
            'Assets Report': 'assets',
            'Procurement Report': 'procurement',
            'Performance Report': 'performance'
        };
        
        const module = moduleMap[reportType];
        if (!module) {
            this.showToast('Pilih jenis laporan terlebih dahulu', 'warning');
            return;
        }
        
        let url = `${this.API_BASE}/exports/${module}?format=${format}`;
        if (period) {
            url += `&period=${encodeURIComponent(period)}`;
        }
        
        // Open in new tab for download (PDF will show inline, Excel will prompt save)
        const win = window.open(url, '_blank');
        if (win) {
            win.focus();
        }
        this.showToast(`Generating ${format.toUpperCase()} report...`, 'info');
    },

    scheduleReport() {
        this.showToast('Report scheduled', 'success');
    },

    exportTable(module, name) {
        const url = `${this.API_BASE}/exports/${module}?format=excel`;
        window.open(url, '_blank');
        this.showToast(`Downloading ${name} export...`, 'info');
    },

    handleImportFile(input) {
        const file = input.files[0];
        if (!file) return;
        document.getElementById('importFileName').style.display = 'block';
        document.getElementById('importFileName').innerHTML = '<i class="fas fa-file me-1"></i>' + file.name + ' (' + (file.size / 1024).toFixed(1) + ' KB)';
        document.getElementById('importBtn').disabled = false;
    },

    submitImport() {
        const file = document.getElementById('importFile').files[0];
        if (!file) return;

        const formData = new FormData();
        formData.append('file', file);

        document.getElementById('importProgress').style.display = 'block';
        document.getElementById('importBtn').disabled = true;
        document.getElementById('importBtn').innerHTML = '<i class="fas fa-spinner fa-spin me-1"></i> Importing...';

        fetch(this.API_BASE + '/employees/import', {
            method: 'POST',
            headers: { 'Authorization': 'Bearer ' + this.token },
            body: formData
        })
        .then(r => { if (!r.ok) throw new Error('HTTP ' + r.status); return r.json(); })
        .then(data => {
            document.getElementById('importProgressBar').style.width = '100%';
            document.getElementById('importResult').style.display = 'block';
            let html = '<div class="alert alert-success"><i class="fas fa-check-circle me-2"></i>Import complete!</div>';
            html += '<p class="mb-1"><strong>Imported:</strong> ' + data.imported + ' of ' + data.total_rows + '</p>';
            if (data.errors && data.errors.length > 0) {
                html += '<div class="mt-2"><strong class="text-danger">Errors:</strong><ul class="mb-0 mt-1">';
                data.errors.forEach(e => html += '<li class="small text-muted">' + e + '</li>');
                html += '</ul></div>';
            }
            document.getElementById('importResult').innerHTML = html;
            document.getElementById('importBtn').innerHTML = '<i class="fas fa-check me-1"></i> Done';
            setTimeout(() => location.reload(), 2000);
        })
        .catch(err => {
            document.getElementById('importResult').style.display = 'block';
            document.getElementById('importResult').innerHTML = '<div class="alert alert-danger"><i class="fas fa-exclamation-circle me-2"></i>Import failed: ' + err.message + '</div>';
            document.getElementById('importBtn').disabled = false;
            document.getElementById('importBtn').innerHTML = '<i class="fas fa-upload me-1"></i> Import Now';
        });
    },

    backupNow() {
        this.showToast('Backup started. This may take a few minutes.', 'info');
        setTimeout(() => this.showToast('Backup completed successfully', 'success'), 3000);
    },

    loadAttendance() {
        this.showToast('Loading attendance data...', 'info');
    },

    // ============================================
    // Toast Notifications
    // ============================================
    showToast(message, type = 'info') {
        const container = document.getElementById('toastContainer');
        if (!container) return;

        const icons = {
            success: 'fas fa-check-circle',
            danger: 'fas fa-exclamation-circle',
            warning: 'fas fa-exclamation-triangle',
            info: 'fas fa-info-circle'
        };

        const toastId = 'toast_' + Date.now();
        const toastHtml = `
            <div id="${toastId}" class="toast align-items-center text-bg-${type} border-0" role="alert">
                <div class="d-flex">
                    <div class="toast-body">
                        <i class="${icons[type] || icons.info} me-2"></i>${message}
                    </div>
                    <button type="button" class="btn-close btn-close-white me-2 m-auto" data-bs-dismiss="toast"></button>
                </div>
            </div>
        `;

        container.insertAdjacentHTML('beforeend', toastHtml);

        const toastEl = document.getElementById(toastId);
        const toast = new bootstrap.Toast(toastEl, { delay: 3000 });
        toast.show();

        toastEl.addEventListener('hidden.bs.toast', () => toastEl.remove());
    },

    // ============================================
    // Notifications
    // ============================================
    initNotifications() {
        const badge = document.getElementById('notifBadge');
        const notifList = document.querySelector('.notification-list');
        const markAllBtn = document.querySelector('.notification-dropdown .dropdown-header a');

        if (!notifList) return;

        // Fetch live notifications from API
        this.apiCall('/notifications?limit=10').then(data => {
            if (!data) return;
            const notifs = data.notifications || [];
            const unreadCount = data.unread || 0;

            if (badge) {
                badge.textContent = unreadCount || 0;
                badge.style.display = unreadCount ? 'inline-block' : 'none';
            }

            if (notifs.length === 0) {
                notifList.innerHTML = `
                    <div class="text-center py-4 text-muted small">
                        <i class="fas fa-bell-slash fa-2x mb-2 d-block opacity-50"></i>
                        Tidak ada notifikasi baru
                    </div>`;
                return;
            }

            let html = '';
            notifs.forEach(n => {
                const unreadClass = n.is_read ? '' : 'unread';
                let iconClass = 'fa-bell text-primary';
                let bgClass = 'bg-primary-subtle';
                
                if (n.title.toLowerCase().includes('perjalanan') || n.title.toLowerCase().includes('travel')) {
                    iconClass = 'fa-plane-departure text-warning';
                    bgClass = 'bg-warning-subtle';
                } else if (n.title.toLowerCase().includes('cuti') || n.title.toLowerCase().includes('leave')) {
                    iconClass = 'fa-calendar-check text-info';
                    bgClass = 'bg-info-subtle';
                } else if (n.title.toLowerCase().includes('lembur') || n.title.toLowerCase().includes('overtime')) {
                    iconClass = 'fa-clock text-warning';
                    bgClass = 'bg-warning-subtle';
                } else if (n.title.toLowerCase().includes('reimburse') || n.title.toLowerCase().includes('klaim')) {
                    iconClass = 'fa-receipt text-success';
                    bgClass = 'bg-success-subtle';
                }

                html += `
                    <a href="${n.link || '#'}" class="notification-item ${unreadClass}" onclick="App.markNotifRead(${n.id}, event)">
                        <div class="notification-icon ${bgClass}">
                            <i class="fas ${iconClass}"></i>
                        </div>
                        <div class="notification-content">
                            <p class="mb-0 fw-semibold text-dark" style="font-size: 0.85rem;">${n.title}</p>
                            <small class="text-secondary d-block" style="font-size: 0.78rem;">${n.message}</small>
                            <small class="text-muted" style="font-size: 0.7rem;">${n.created_at || ''}</small>
                        </div>
                    </a>`;
            });
            notifList.innerHTML = html;
        });

        if (markAllBtn) {
            markAllBtn.onclick = (e) => {
                e.preventDefault();
                this.apiCall('/notifications/read-all', { method: 'PUT' }).then(() => {
                    this.initNotifications();
                });
            };
        }
    },

    markNotifRead(id, event) {
        this.apiCall(`/notifications/${id}/read`, { method: 'PUT' });
    },

    // ============================================
    // Utilities
    // ============================================
    debounce(func, wait) {
        let timeout;
        return function executedFunction(...args) {
            const later = () => {
                clearTimeout(timeout);
                func(...args);
            };
            clearTimeout(timeout);
            timeout = setTimeout(later, wait);
        };
    },

    formatDate(dateStr) {
        if (!dateStr) return '-';
        return new Date(dateStr).toLocaleDateString('en-US', {
            year: 'numeric', month: 'short', day: 'numeric'
        });
    },

    formatCurrency(amount) {
        return new Intl.NumberFormat('id-ID', {
            style: 'currency', currency: 'IDR', minimumFractionDigits: 0
        }).format(amount);
    },

    // ============================================
    // DASHBOARD DATA LOADER
    // ============================================
    loadDashboardStats() {
        this.apiCall('/dashboard').then(data => {
            if (!data) return;
            const e = data?.employees || {};
            const a = data?.attendance_today || {};
            const p = data?.pending_approvals || {};
            const pl = data?.payroll_this_month || {};

            const statCards = document.querySelectorAll('.card-body');
            statCards.forEach((card) => {
                const label = card.querySelector('.stat-label');
                const valueEl = card.querySelector('.stat-value:not([type])');
                if (!valueEl) return;
                
                const labelText = label?.textContent.trim() || '';
                if (labelText.includes('Total Employees')) {
                    valueEl.textContent = e.active || e.total || 0;
                } else if (labelText.includes('Present Today')) {
                    valueEl.textContent = a.total || 0;
                } else if (labelText.includes('Pending Approvals')) {
                    valueEl.textContent = p.total || 0;
                } else if (labelText.includes('Monthly Payroll') || labelText.includes('Payroll')) {
                    if (pl.total_payout) {
                        valueEl.textContent = new Intl.NumberFormat('id-ID', {
                            style: 'currency', currency: 'IDR', minimumFractionDigits: 0
                        }).format(pl.total_payout);
                    } else {
                        valueEl.textContent = 'Rp 0';
                    }
                }
            });
        }).catch(err => console.error('Dashboard stats error:', err));
    },

    // ============================================
    // EMPLOYEES DATA LOADER
    // ============================================
    loadEmployees() {
        this.apiCall('/employees?skip=0&limit=50').then(data => {
            const items = data?.employees || data?.items || [];
            const tbody = document.querySelector('#employeeTable tbody');
            if (!tbody) return;

            if (!data || items.length === 0) {
                tbody.innerHTML = '<tr><td colspan="8" class="text-center text-muted py-5">Belum ada karyawan terdaftar.</td></tr>';
                const countEl = document.getElementById('empCount');
                if (countEl) countEl.textContent = 0;
                return;
            }

            tbody.innerHTML = '';
            items.forEach(emp => {
                const statusClass = emp.status === 'active' ? 'success' : emp.status === 'inactive' ? 'danger' : 'warning';
                const deptName = emp.department_name || emp.department || (emp.department_id ? `Dept #${emp.department_id}` : '-');
                const posTitle = emp.position_title || emp.position || '-';
                const joinDate = emp.hire_date ? new Date(emp.hire_date).toLocaleDateString('id-ID') : '-';
                const initials = (emp.full_name || '?').substring(0, 2).toUpperCase();
                const row = document.createElement('tr');
                row.innerHTML = `
                    <td><div class="form-check"><input class="form-check-input emp-check" type="checkbox" value="${emp.id}"></div></td>
                    <td>
                        <div class="d-flex align-items-center">
                            <div class="avatar-sm bg-primary-subtle rounded-circle me-2 d-flex align-items-center justify-content-center" style="width:36px;height:36px;">
                                <span class="text-primary fw-semibold">${initials}</span>
                            </div>
                            <div>
                                <div class="fw-medium">${emp.full_name}</div>
                                <small class="text-muted">${emp.email || '-'}</small>
                            </div>
                        </div>
                    </td>
                    <td>${emp.employee_id_str || '#' + emp.id}</td>
                    <td>${deptName}</td>
                    <td>${posTitle}</td>
                    <td>${joinDate}</td>
                    <td><span class="badge bg-${statusClass}">${emp.status || 'active'}</span></td>
                    <td>
                        <button class="btn btn-sm btn-outline-primary me-1" onclick="App.viewEmployee(${emp.id})" title="Lihat Detail"><i class="fas fa-eye"></i></button>
                        <button class="btn btn-sm btn-outline-secondary" onclick="App.editEmployee(${emp.id})" title="Edit"><i class="fas fa-edit"></i></button>
                    </td>`;
                tbody.appendChild(row);
            });

            // Update footer count & pagination
            const countEl = document.getElementById('empCount');
            const totalEl = document.getElementById('empTotal');
            const paginationEl = document.getElementById('empPagination');
            const totalCount = data.total || items.length;
            if (countEl) countEl.textContent = items.length;
            if (totalEl) totalEl.textContent = totalCount;
            if (paginationEl) {
                const totalPages = Math.ceil(totalCount / 10);
                if (totalPages <= 1) {
                    paginationEl.classList.add('d-none');
                } else {
                    paginationEl.classList.remove('d-none');
                    let pagHtml = `<ul class="pagination pagination-sm mb-0"><li class="page-item disabled"><a class="page-link" href="#">Prev</a></li>`;
                    for (let p = 1; p <= totalPages; p++) {
                        pagHtml += `<li class="page-item ${p === 1 ? 'active' : ''}"><a class="page-link" href="#">${p}</a></li>`;
                    }
                    pagHtml += `<li class="page-item ${totalPages <= 1 ? 'disabled' : ''}"><a class="page-link" href="#">Next</a></li></ul>`;
                    paginationEl.innerHTML = pagHtml;
                }
            }
        }).catch(err => console.error('Load employees error:', err));
    },

    viewEmployee(id) { window.location.href = `/employees/${id}`; },
    editEmployee(id) {
        this.apiCall(`/employees/${id}`).then(emp => {
            if (!emp) return;
            const e = emp.data || emp;
            const modalEl = document.getElementById('editEmployeeModal');
            if (modalEl) {
                document.getElementById('editEmpId').value = e.id;
                document.getElementById('editFullName').value = e.full_name;
                document.getElementById('editEmail').value = e.email;
                const modal = bootstrap.Modal.getInstance(modalEl) || new bootstrap.Modal(modalEl);
                modal.show();
            } else {
                this.showEditModal('Edit Employee', id, [
                    {name: 'full_name', label: 'Full Name', value: e.full_name, type: 'text'},
                    {name: 'email', label: 'Email', value: e.email, type: 'text'},
                    {name: 'phone', label: 'Phone', value: e.phone, type: 'text'},
                    {name: 'status', label: 'Status', value: e.status, type: 'select', options: ['active','inactive','on_leave']}
                ]);
            }
        });
    },

    // ============================================
    // ATTENDANCE DATA LOADER
    // ============================================
    loadAttendanceSummary() {
        this.apiCall('/attendance/summary').then(data => {
            if (!data) return;
            const pres = document.getElementById('attPresent');
            const absent = document.getElementById('attAbsent');
            const late = document.getElementById('attLate');
            const leave = document.getElementById('attLeave');
            if (pres) pres.textContent = data?.present ?? '-';
            if (absent) absent.textContent = data?.absent ?? '-';
            if (late) late.textContent = data?.late ?? '-';
            if (leave) leave.textContent = data?.on_leave ?? '-';
        }).catch(err => console.error('Attendance summary error:', err));
    },

    // ============================================
    // TRAVEL REQUESTS DATA LOADER
    // ============================================
    loadTravelRequests() {
        this.apiCall('/travel').then(data => {
            const items = data?.items || [];
            const tbody = document.querySelector('#travelTable tbody');
            if (!tbody) return;

            if (!data || items.length === 0) {
                tbody.innerHTML = '<tr><td colspan="7" class="text-center text-muted py-5">Belum ada permintaan perjalanan dinas.</td></tr>';
                return;
            }

            const statusBadge = (s) => {
                const map = {
                    draft: 'secondary', pending_manager: 'warning', pending_director: 'info',
                    approved: 'success', completed: 'primary', rejected: 'danger',
                    revision_required: 'warning'
                };
                return map[s] || 'secondary';
            };

            tbody.innerHTML = '';
            items.forEach(req => {
                const badgeCls = statusBadge(req.status);
                const row = document.createElement('tr');
                row.innerHTML = `
                    <td>#${req.id}</td>
                    <td>${req.departure_date ? new Date(req.departure_date).toLocaleDateString('id-ID') : '-'}</td>
                    <td>${req.destination || '-'}</td>
                    <td><span class="badge bg-${badgeCls}">${req.status}</span></td>
                    <td>
                        <button class="btn btn-sm btn-outline-info me-1" onclick="App.viewTravelRequest(${req.id})"><i class="fas fa-eye"></i></button>
                        <button class="btn btn-sm btn-outline-primary" onclick="App.printTravel(${req.id})"><i class="fas fa-print"></i></button>
                    </td>`;
                tbody.appendChild(row);
            });
        }).catch(err => console.error('Load travel error:', err));
    },

    viewTravelRequest(id) {
        this.apiCall(`/travel/${id}`).then(req => {
            if (!req) return;
            const destEl = document.getElementById('viewTravelDest');
            if (destEl) destEl.value = req.destination;
            const modalEl = document.getElementById('viewTravelModal');
            if (modalEl) {
                const modal = new bootstrap.Modal(modalEl);
                modal.show();
            }
        });
    },

    printTravel(id) {
        window.open(`${this.API_BASE}/travel/${id}/print-pdf`, '_blank');
    },

    // ============================================
    // LEAVE DATA LOADER
    // ============================================
    loadLeaveRequests() {
        this.apiCall('/leave?skip=0&limit=50').then(data => {
            const items = data?.leaves || data?.items || [];
            const tbody = document.querySelector('#leaveTable tbody');
            if (!tbody) return;

            if (!data || items.length === 0) {
                tbody.innerHTML = '<tr><td colspan="6" class="text-center text-muted py-5">Belum ada pengajuan cuti.</td></tr>';
                return;
            }

            const statusBadge = (s) => {
                const map = {
                    pending: 'warning', approved: 'success',
                    rejected: 'danger', cancelled: 'secondary'
                };
                return map[s] || 'secondary';
            };

            tbody.innerHTML = '';
            items.forEach(lv => {
                const badgeCls = statusBadge(lv.status);
                const row = document.createElement('tr');
                row.innerHTML = `
                    <td>${lv.leave_type_name || lv.leave_type || '-'}</td>
                    <td>${lv.start_date ? new Date(lv.start_date).toLocaleDateString('id-ID') : '-'}</td>
                    <td>${lv.end_date ? new Date(lv.end_date).toLocaleDateString('id-ID') : '-'}</td>
                    <td>${lv.days || 1} hari</td>
                    <td><span class="badge bg-${badgeCls}">${lv.status}</span></td>
                    <td>
                        <button class="btn btn-sm btn-outline-info"><i class="fas fa-eye"></i></button>
                    </td>`;
                tbody.appendChild(row);
            });
        }).catch(err => console.error('Load leaves error:', err));
    },

    // ============================================
    // OVERTIME DATA LOADER
    // ============================================
    loadOvertimeRequests() {
        this.apiCall('/overtime?skip=0&limit=50').then(data => {
            const items = data?.overtimes || data?.items || [];
            const tbody = document.querySelector('#overtimeTable tbody');
            if (!tbody) return;

            if (!data || items.length === 0) {
                tbody.innerHTML = '<tr><td colspan="5" class="text-center text-muted py-5">Belum ada pengajuan lembur.</td></tr>';
                return;
            }

            const statusBadge = (s) => {
                const map = {
                    pending: 'warning', approved: 'success',
                    rejected: 'danger', paid: 'info'
                };
                return map[s] || 'secondary';
            };

            tbody.innerHTML = '';
            items.forEach(ot => {
                const badgeCls = statusBadge(ot.status);
                const row = document.createElement('tr');
                row.innerHTML = `
                    <td>${ot.date || '-'}</td>
                    <td>${ot.hours || 0} Jam</td>
                    <td>Rp ${(ot.compensation || 0).toLocaleString('id-ID')}</td>
                    <td><span class="badge bg-${badgeCls}">${ot.status}</span></td>
                    <td>
                        <button class="btn btn-sm btn-outline-info"><i class="fas fa-eye"></i></button>
                    </td>`;
                tbody.appendChild(row);
            });
        }).catch(err => console.error('Load overtime error:', err));
    },

    // ============================================
    // PAYROLL DATA LOADER
    // ============================================
    loadPayrollSummary() {
        this.apiCall('/payroll/summary').then(data => {
            if (!data) return;
            const totalEmp = document.getElementById('payrollTotalEmp');
            const processed = document.getElementById('payrollProcessed');
            const totalAmount = document.getElementById('payrollTotalAmount');
            const pending = document.getElementById('payrollPending');
            if (totalEmp) totalEmp.textContent = data?.total_employees || 0;
            if (processed) processed.textContent = data?.processed || 0;
            if (pending) pending.textContent = data?.pending || 0;
            if (totalAmount && data?.total_amount) {
                totalAmount.textContent = new Intl.NumberFormat('id-ID', {
                    style: 'currency', currency: 'IDR', minimumFractionDigits: 0
                }).format(data.total_amount);
            }
        }).catch(err => console.error('Payroll summary error:', err));
    },

    // ============================================
    // ASSETS DATA LOADER
    // ============================================
    loadAssetSummary() {
        this.apiCall('/assets?limit=100').then(data => {
            const items = data?.items || data?.assets || [];
            const total = document.getElementById('assetTotal');
            const assigned = document.getElementById('assetAssigned');
            const storage = document.getElementById('assetStorage');
            const repair = document.getElementById('assetRepair');
            if (total) total.textContent = items.length;
            if (assigned) assigned.textContent = items.filter(a => a.status === 'assigned' || a.status === 'in_use').length;
            if (storage) storage.textContent = items.filter(a => a.status === 'in_storage' || a.status === 'available').length;
            if (repair) repair.textContent = items.filter(a => a.status === 'under_repair' || a.status === 'maintenance').length;
        }).catch(err => console.error('Assets summary error:', err));
    },

    // ============================================
    // CHART DATA LOADER — replaces hardcoded values
    // ============================================
    initChartFromApi(chartType, chartId, apiUrl) {
        const ctx = document.getElementById(chartId);
        if (!ctx) return;

        this.apiCall(apiUrl.replace(this.API_BASE, '')).then(data => {
            if (!data) return;
            if (chartType === 'line') {
                const labels = data?.labels || ['Mon', 'Tue', 'Wed', 'Thu', 'Fri'];
                const datasets = [
                    { label: 'Present', data: data?.present || [0,0,0,0,0], borderColor: '#22c55e', backgroundColor: 'rgba(34,197,94,0.1)', fill: true, tension: 0.3, pointRadius: 4 },
                    { label: 'Late', data: data?.late || [0,0,0,0,0], borderColor: '#f59e0b', backgroundColor: 'rgba(245,158,11,0.1)', fill: true, tension: 0.3, pointRadius: 4 },
                    { label: 'Absent', data: data?.absent || [0,0,0,0,0], borderColor: '#ef4444', backgroundColor: 'rgba(239,68,68,0.1)', fill: true, tension: 0.3, pointRadius: 4 }
                ];
                new Chart(ctx, {
                    type: 'line',
                    data: { labels, datasets },
                    options: { responsive: true, maintainAspectRatio: false, plugins: { legend: { position: 'bottom' } }, scales: { y: { beginAtZero: true } } }
                });
            } else if (chartType === 'doughnut') {
                const labels = data?.labels || ['Engineering', 'HR', 'Finance'];
                const values = data?.values || [0, 0, 0];
                const colors = ['#1e3a5f', '#22c55e', '#f59e0b'];
                new Chart(ctx, {
                    type: 'doughnut',
                    data: {
                        labels,
                        datasets: [{ data: values, backgroundColor: colors, borderWidth: 2, borderColor: '#fff' }]
                    },
                    options: { responsive: true, maintainAspectRatio: false, cutout: '65%', plugins: { legend: { position: 'bottom' } } }
                });
            }
        }).catch(err => {
            console.error(`Chart load error (${chartType}, ${chartId}):`, err);
            if (ctx && ctx.parentElement) ctx.parentElement.style.display = 'none';
        });
    },

    // Override initDashboardCharts to use real API data
    overrideInitDashboardCharts() {
        // Will be called after DOM loads if on dashboard page
    }
};

// Import drag and drop
const dropZone = document.getElementById('importDropZone');
if (dropZone) {
    dropZone.addEventListener('dragover', e => { e.preventDefault(); dropZone.style.borderColor = '#0d6efd'; dropZone.style.background = '#e7f1ff'; });
    dropZone.addEventListener('dragleave', e => { e.preventDefault(); dropZone.style.borderColor = '#dee2e6'; dropZone.style.background = ''; });
    dropZone.addEventListener('drop', e => {
        e.preventDefault();
        dropZone.style.borderColor = '#dee2e6';
        dropZone.style.background = '';
        const fileInput = document.getElementById('importFile');
        fileInput.files = e.dataTransfer.files;
        App.handleImportFile(fileInput);
    });
}

// Initialize on DOM ready
document.addEventListener('DOMContentLoaded', () => App.init());
