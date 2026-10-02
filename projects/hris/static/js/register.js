/**
 * Register Page JS — handle registration form submission
 */
const Register = {
    API_BASE: '/api',

    init() {
        const form = document.getElementById('registerForm');
        if (form) {
            form.addEventListener('submit', (e) => this.handleSubmit(e));
        }
    },

    handleSubmit(e) {
        e.preventDefault();
        const form = e.target;
        const btn = form.querySelector('.btn-primary');
        const spinner = btn?.querySelector('.spinner-border');
        const alertBox = document.getElementById('regAlert');

        // Validate
        const pw = form.password.value;
        const pwc = form.confirm_password.value;
        if (pw !== pwc) {
            this.showAlert(alertBox, 'Passwords do not match', 'danger');
            return;
        }
        if (pw.length < 6) {
            this.showAlert(alertBox, 'Password must be at least 6 characters', 'danger');
            return;
        }

        btn.disabled = true;
        if (spinner) spinner.classList.remove('d-none');
        if (alertBox) alertBox.className = 'alert d-none';

        const data = {
            full_name: form.full_name.value,
            email: form.email.value,
            username: form.username.value,
            phone: form.phone.value,
            department: form.department.value || null,
            position: form.position.value || null,
            password: pw
        };

        fetch(`${this.API_BASE}/auth/register`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(data)
        })
        .then(res => res.json())
        .then(result => {
            if (result.message && !result.detail) {
                form.innerHTML = `
                    <div class="text-center py-5">
                        <i class="fas fa-check-circle text-success" style="font-size:4rem"></i>
                        <h4 class="mt-3">Registration Successful!</h4>
                        <p class="text-muted">Your registration is awaiting admin approval.<br>We will notify you via email once approved.</p>
                        <a href="/" class="btn btn-primary mt-3">Back to Login</a>
                    </div>`;
            } else if (result.detail) {
                this.showAlert(alertBox, result.detail, 'danger');
                btn.disabled = false;
                if (spinner) spinner.classList.add('d-none');
            }
        })
        .catch(() => {
            this.showAlert(alertBox, 'Network error. Please try again.', 'danger');
            btn.disabled = false;
            if (spinner) spinner.classList.add('d-none');
        });

        return false;
    },

    showAlert(el, msg, type) {
        if (el) {
            el.className = `alert alert-${type}`;
            el.textContent = msg;
        }
    }
};

Register.init();
