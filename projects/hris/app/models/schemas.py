"""
Pydantic models for HRIS entities.
"""
from pydantic import BaseModel, Field, EmailStr
from typing import Optional, List
from datetime import date, datetime
from enum import Enum


# ---------------------------------------------------------------------------
# Enums
# ---------------------------------------------------------------------------

class UserRole(str, Enum):
    super_admin = "super_admin"
    manager = "manager"
    employee = "employee"


class EmployeeStatus(str, Enum):
    active = "active"
    inactive = "inactive"
    on_leave = "on_leave"


class Gender(str, Enum):
    male = "Male"
    female = "Female"
    other = "Other"


class MaritalStatus(str, Enum):
    single = "Single"
    married = "Married"
    divorced = "Divorced"
    widowed = "Widowed"


class AttendanceStatus(str, Enum):
    present = "present"
    absent = "absent"
    late = "late"
    half_day = "half_day"


class RequestStatus(str, Enum):
    pending = "pending"
    approved = "approved"
    rejected = "rejected"


class PayrollStatus(str, Enum):
    draft = "draft"
    processed = "processed"
    paid = "paid"


class AssetCondition(str, Enum):
    good = "good"
    fair = "fair"
    poor = "poor"


class AssetStatus(str, Enum):
    available = "available"
    assigned = "assigned"
    maintenance = "maintenance"
    retired = "retired"


class DocType(str, Enum):
    ktp = "ktp"
    kontrak = "kontrak"
    sertifikat = "sertifikat"
    other = "other"


class TrainingEnrollmentStatus(str, Enum):
    enrolled = "enrolled"
    completed = "completed"
    cancelled = "cancelled"


class RequisitionStatus(str, Enum):
    open = "open"
    closed = "closed"
    cancelled = "cancelled"


class ApplicantStatus(str, Enum):
    new = "new"
    screening = "screening"
    interview = "interview"
    offer = "offer"
    hired = "hired"
    rejected = "rejected"


class InterviewStatus(str, Enum):
    scheduled = "scheduled"
    completed = "completed"
    cancelled = "cancelled"


class ProcurementStatus(str, Enum):
    pending = "pending"
    approved = "approved"
    purchased = "purchased"
    rejected = "rejected"


class ReviewType(str, Enum):
    self_ = "self"
    manager = "manager"
    three_sixty = "360"


# ---------------------------------------------------------------------------
# Base schemas
# ---------------------------------------------------------------------------

class DepartmentBase(BaseModel):
    name: str
    code: str
    description: Optional[str] = None
    manager_id: Optional[int] = None
    parent_dept_id: Optional[int] = None


class DepartmentCreate(DepartmentBase):
    pass


class DepartmentOut(DepartmentBase):
    id: int

    model_config = {"from_attributes": True}


class PositionBase(BaseModel):
    title: str
    level: str
    department_id: Optional[int] = None
    description: Optional[str] = None
    salary_min: Optional[float] = None
    salary_max: Optional[float] = None


class PositionCreate(PositionBase):
    pass


class PositionOut(PositionBase):
    id: int

    model_config = {"from_attributes": True}


class EmployeeBase(BaseModel):
    employee_id_str: str
    full_name: str
    email: str
    phone: Optional[str] = None
    department_id: Optional[int] = None
    position_id: Optional[int] = None
    manager_id: Optional[int] = None
    hire_date: date
    contract_end_date: Optional[date] = None
    status: EmployeeStatus = EmployeeStatus.active
    avatar_url: Optional[str] = None
    address: Optional[str] = None
    date_of_birth: Optional[date] = None
    gender: Optional[Gender] = None
    marital_status: Optional[MaritalStatus] = None
    religion: Optional[str] = None
    bank_account: Optional[str] = None
    bank_name: Optional[str] = None
    npwp: Optional[str] = None
    bpjs_ketenagakerjaan: Optional[str] = None
    bpjs_kesehatan: Optional[str] = None


class EmployeeCreate(EmployeeBase):
    pass


class EmployeeUpdate(BaseModel):
    full_name: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None
    department_id: Optional[int] = None
    position_id: Optional[int] = None
    manager_id: Optional[int] = None
    status: Optional[EmployeeStatus] = None
    address: Optional[str] = None
    bank_account: Optional[str] = None
    bank_name: Optional[str] = None


class EmployeeOut(EmployeeBase):
    id: int

    model_config = {"from_attributes": True}


class EmployeeBrief(BaseModel):
    id: int
    employee_id_str: str
    full_name: str
    email: str
    department_id: Optional[int] = None
    position_id: Optional[int] = None

    model_config = {"from_attributes": True}


# ---------------------------------------------------------------------------
# User
# ---------------------------------------------------------------------------

class UserBase(BaseModel):
    username: str
    email: str
    role: UserRole = UserRole.employee
    employee_id: Optional[int] = None


class UserCreate(BaseModel):
    username: str
    email: str
    password: str
    role: UserRole = UserRole.employee
    employee_id: Optional[int] = None


class UserOut(UserBase):
    id: int
    is_active: bool
    created_at: Optional[datetime] = None

    model_config = {"from_attributes": True}


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"


class TokenData(BaseModel):
    user_id: Optional[int] = None
    username: Optional[str] = None
    role: Optional[str] = None


# ---------------------------------------------------------------------------
# Auth
# ---------------------------------------------------------------------------

class LoginRequest(BaseModel):
    username: str
    password: str


# ---------------------------------------------------------------------------
# Documents
# ---------------------------------------------------------------------------

class DocumentBase(BaseModel):
    employee_id: int
    doc_type: DocType
    file_name: str
    file_path: str
    expiry_date: Optional[date] = None


class DocumentCreate(DocumentBase):
    pass


class DocumentOut(DocumentBase):
    id: int
    uploaded_at: Optional[datetime] = None

    model_config = {"from_attributes": True}


# ---------------------------------------------------------------------------
# Attendance
# ---------------------------------------------------------------------------

class AttendanceBase(BaseModel):
    employee_id: int
    date: date
    clock_in: Optional[str] = None
    clock_out: Optional[str] = None
    status: AttendanceStatus
    location_lat: Optional[float] = None
    location_lng: Optional[float] = None
    notes: Optional[str] = None


class AttendanceCreate(AttendanceBase):
    pass


class AttendanceOut(AttendanceBase):
    id: int

    model_config = {"from_attributes": True}


# ---------------------------------------------------------------------------
# Shifts
# ---------------------------------------------------------------------------

class ShiftBase(BaseModel):
    name: str
    start_time: str
    end_time: str
    description: Optional[str] = None


class ShiftCreate(ShiftBase):
    pass


class ShiftOut(ShiftBase):
    id: int

    model_config = {"from_attributes": True}


class EmployeeShiftBase(BaseModel):
    employee_id: int
    shift_id: int
    date: date


class EmployeeShiftCreate(EmployeeShiftBase):
    pass


class EmployeeShiftOut(EmployeeShiftBase):
    id: int

    model_config = {"from_attributes": True}


# ---------------------------------------------------------------------------
# Overtime
# ---------------------------------------------------------------------------

class OvertimeBase(BaseModel):
    employee_id: int
    date: date
    hours: float
    reason: Optional[str] = None


class OvertimeCreate(OvertimeBase):
    pass


class OvertimeOut(BaseModel):
    id: int
    employee_id: int
    date: date
    hours: float
    reason: Optional[str] = None
    status: RequestStatus
    approved_by: Optional[int] = None
    approved_at: Optional[datetime] = None
    created_at: Optional[datetime] = None

    model_config = {"from_attributes": True}


# ---------------------------------------------------------------------------
# Leave Types & Leaves
# ---------------------------------------------------------------------------

class LeaveTypeBase(BaseModel):
    name: str
    code: str
    days_allowed: int = 0
    description: Optional[str] = None


class LeaveTypeCreate(LeaveTypeBase):
    pass


class LeaveTypeOut(LeaveTypeBase):
    id: int

    model_config = {"from_attributes": True}


class LeaveBase(BaseModel):
    employee_id: int
    leave_type_id: int
    start_date: date
    end_date: date
    reason: Optional[str] = None


class LeaveCreate(LeaveBase):
    pass


class LeaveOut(BaseModel):
    id: int
    employee_id: int
    leave_type_id: int
    start_date: date
    end_date: date
    reason: Optional[str] = None
    status: RequestStatus
    approved_by: Optional[int] = None
    approved_at: Optional[datetime] = None
    created_at: Optional[datetime] = None

    model_config = {"from_attributes": True}


# ---------------------------------------------------------------------------
# Payroll
# ---------------------------------------------------------------------------

class PayrollBase(BaseModel):
    period_month: int
    period_year: int
    employee_id: int
    base_salary: float = 0
    allowance: float = 0
    overtime_pay: float = 0
    bonus: float = 0
    deduction: float = 0
    tax_pph21: float = 0
    bpjs_ketenagakerjaan: float = 0
    bpjs_kesehatan: float = 0
    net_salary: float = 0
    status: PayrollStatus = PayrollStatus.draft


class PayrollCreate(PayrollBase):
    pass


class PayrollOut(BaseModel):
    id: int
    period_month: int
    period_year: int
    employee_id: int
    base_salary: float
    allowance: float
    overtime_pay: float
    bonus: float
    deduction: float
    tax_pph21: float
    bpjs_ketenagakerjaan: float
    bpjs_kesehatan: float
    net_salary: float
    status: PayrollStatus
    processed_at: Optional[datetime] = None
    paid_at: Optional[datetime] = None

    model_config = {"from_attributes": True}


# ---------------------------------------------------------------------------
# Reimbursement
# ---------------------------------------------------------------------------

class ReimbursementBase(BaseModel):
    employee_id: int
    category: str
    amount: float
    description: Optional[str] = None
    receipt_path: Optional[str] = None


class ReimbursementCreate(ReimbursementBase):
    pass


class ReimbursementOut(BaseModel):
    id: int
    employee_id: int
    category: str
    amount: float
    description: Optional[str] = None
    receipt_path: Optional[str] = None
    status: RequestStatus
    approved_by: Optional[int] = None
    created_at: Optional[datetime] = None

    model_config = {"from_attributes": True}


# ---------------------------------------------------------------------------
# KPIs
# ---------------------------------------------------------------------------

class KPIBase(BaseModel):
    employee_id: int
    period: str
    target: Optional[str] = None
    actual: Optional[str] = None
    score: Optional[float] = None
    description: Optional[str] = None


class KPICreate(KPIBase):
    pass


class KPIOut(BaseModel):
    id: int
    employee_id: int
    period: str
    target: Optional[str] = None
    actual: Optional[str] = None
    score: Optional[float] = None
    description: Optional[str] = None
    created_at: Optional[datetime] = None

    model_config = {"from_attributes": True}


# ---------------------------------------------------------------------------
# OKRs
# ---------------------------------------------------------------------------

class OKRBase(BaseModel):
    employee_id: int
    objective: str
    key_result: str
    progress: float = 0
    period: Optional[str] = None
    status: str = "in_progress"


class OKRCreate(OKRBase):
    pass


class OKROut(BaseModel):
    id: int
    employee_id: int
    objective: str
    key_result: str
    progress: float
    period: Optional[str] = None
    status: str

    model_config = {"from_attributes": True}


# ---------------------------------------------------------------------------
# Performance Reviews
# ---------------------------------------------------------------------------

class PerformanceReviewBase(BaseModel):
    employee_id: int
    reviewer_id: int
    period: str
    score: Optional[float] = None
    comments: Optional[str] = None
    review_type: ReviewType


class PerformanceReviewCreate(PerformanceReviewBase):
    pass


class PerformanceReviewOut(BaseModel):
    id: int
    employee_id: int
    reviewer_id: int
    period: str
    score: Optional[float] = None
    comments: Optional[str] = None
    review_type: ReviewType
    created_at: Optional[datetime] = None

    model_config = {"from_attributes": True}


# ---------------------------------------------------------------------------
# Training & Training Enrollments
# ---------------------------------------------------------------------------

class TrainingBase(BaseModel):
    title: str
    description: Optional[str] = None
    start_date: date
    end_date: date
    trainer: Optional[str] = None
    capacity: int = 30
    status: str = "active"


class TrainingCreate(TrainingBase):
    pass


class TrainingOut(TrainingBase):
    id: int

    model_config = {"from_attributes": True}


class TrainingEnrollmentBase(BaseModel):
    training_id: int
    employee_id: int
    status: TrainingEnrollmentStatus = TrainingEnrollmentStatus.enrolled
    score: Optional[float] = None


class TrainingEnrollmentCreate(TrainingEnrollmentBase):
    pass


class TrainingEnrollmentOut(BaseModel):
    id: int
    training_id: int
    employee_id: int
    status: TrainingEnrollmentStatus
    score: Optional[float] = None
    completed_at: Optional[datetime] = None

    model_config = {"from_attributes": True}


# ---------------------------------------------------------------------------
# Job Requisitions
# ---------------------------------------------------------------------------

class JobRequisitionBase(BaseModel):
    title: str
    department_id: Optional[int] = None
    position_id: Optional[int] = None
    headcount: int = 1
    salary_range: Optional[str] = None
    status: RequisitionStatus = RequisitionStatus.open
    created_by: Optional[int] = None


class JobRequisitionCreate(JobRequisitionBase):
    pass


class JobRequisitionOut(BaseModel):
    id: int
    title: str
    department_id: Optional[int] = None
    position_id: Optional[int] = None
    headcount: int
    salary_range: Optional[str] = None
    status: RequisitionStatus
    created_by: Optional[int] = None
    created_at: Optional[datetime] = None

    model_config = {"from_attributes": True}


# ---------------------------------------------------------------------------
# Applicants & Interviews
# ---------------------------------------------------------------------------

class ApplicantBase(BaseModel):
    requisition_id: int
    full_name: str
    email: str
    phone: Optional[str] = None
    resume_path: Optional[str] = None
    source: Optional[str] = None
    status: ApplicantStatus = ApplicantStatus.new


class ApplicantCreate(ApplicantBase):
    pass


class ApplicantOut(BaseModel):
    id: int
    requisition_id: int
    full_name: str
    email: str
    phone: Optional[str] = None
    resume_path: Optional[str] = None
    source: Optional[str] = None
    status: ApplicantStatus
    created_at: Optional[datetime] = None

    model_config = {"from_attributes": True}


class InterviewBase(BaseModel):
    applicant_id: int
    interviewer_id: int
    scheduled_at: datetime
    notes: Optional[str] = None
    rating: Optional[float] = None
    status: InterviewStatus = InterviewStatus.scheduled


class InterviewCreate(InterviewBase):
    pass


class InterviewOut(BaseModel):
    id: int
    applicant_id: int
    interviewer_id: int
    scheduled_at: datetime
    notes: Optional[str] = None
    rating: Optional[float] = None
    status: InterviewStatus

    model_config = {"from_attributes": True}


# ---------------------------------------------------------------------------
# Procurement Requests
# ---------------------------------------------------------------------------

class ProcurementRequestBase(BaseModel):
    requester_id: int
    department_id: Optional[int] = None
    title: str
    description: Optional[str] = None
    estimated_cost: float = 0
    status: ProcurementStatus = ProcurementStatus.pending
    approved_by: Optional[int] = None


class ProcurementRequestCreate(BaseModel):
    title: str
    description: Optional[str] = None
    estimated_cost: float


class ProcurementRequestOut(ProcurementRequestBase):
    id: int
    created_at: Optional[datetime] = None

    model_config = {"from_attributes": True}


# ---------------------------------------------------------------------------
# Assets
# ---------------------------------------------------------------------------

class AssetBase(BaseModel):
    name: str
    category: str
    serial_number: Optional[str] = None
    purchase_date: Optional[date] = None
    purchase_price: Optional[float] = None
    condition: AssetCondition = AssetCondition.good
    assigned_to: Optional[int] = None
    department_id: Optional[int] = None
    status: AssetStatus = AssetStatus.available
    location: Optional[str] = None


class AssetCreate(AssetBase):
    pass


class AssetOut(AssetBase):
    id: int

    model_config = {"from_attributes": True}


# ---------------------------------------------------------------------------
# Notifications
# ---------------------------------------------------------------------------

class NotificationBase(BaseModel):
    user_id: int
    title: str
    message: str
    is_read: bool = False
    link: Optional[str] = None


class NotificationCreate(BaseModel):
    title: str
    message: str
    link: Optional[str] = None


class NotificationOut(BaseModel):
    id: int
    user_id: int
    title: str
    message: str
    is_read: bool
    link: Optional[str] = None
    created_at: Optional[datetime] = None

    model_config = {"from_attributes": True}


# ---------------------------------------------------------------------------
# Dashboard / aggregation schemas
# ---------------------------------------------------------------------------

class DashboardStats(BaseModel):
    total_employees: int = 0
    active_employees: int = 0
    total_departments: int = 0
    pending_leaves: int = 0
    pending_overtime: int = 0
    pending_reimbursement: int = 0
    open_requisitions: int = 0


class EmployeeListResponse(BaseModel):
    total: int
    items: List[EmployeeOut]


class PaginatedResponse(BaseModel):
    total: int
    page: int = 1
    page_size: int = 20
    items: list
