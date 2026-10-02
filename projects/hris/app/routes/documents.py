"""
Document routes: upload/download employee documents.
"""
import os, uuid
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form, Request
from fastapi.responses import FileResponse, Response
from app.database import get_db
from app.services.auth_service import get_current_user
import aiosqlite
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors
import io

router = APIRouter(prefix="/documents", tags=["documents"])

UPLOAD_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "uploads", "documents")
os.makedirs(UPLOAD_DIR, exist_ok=True)

def _uid(user):
    return user.get("user_id") or user.get("id")

@router.get("/download/{doc_id}")
async def download_document_file(doc_id: int, request: Request, db: aiosqlite.Connection = Depends(get_db)):
    """Endpoint download dokumen asli atau generate dokumen PDF dinamis."""
    from main import get_user_from_request
    user = get_user_from_request(request)
    
    cursor = await db.execute("""
        SELECT d.*, e.full_name, e.employee_id_str, p.title as position_title, dep.name as dept_name
        FROM documents d
        JOIN employees e ON d.employee_id = e.id
        LEFT JOIN positions p ON e.position_id = p.id
        LEFT JOIN departments dep ON e.department_id = dep.id
        WHERE d.id = ?
    """, (doc_id,))
    doc = await cursor.fetchone()
    
    if not doc:
        raise HTTPException(status_code=404, detail="Dokumen tidak ditemukan")
    
    file_path = doc["file_path"]
    if file_path and os.path.exists(file_path):
        return FileResponse(
            path=file_path,
            filename=doc["file_name"],
            media_type="application/octet-stream"
        )
    
    # Generate official dynamic PDF document if physical file doesn't exist yet
    buffer = io.BytesIO()
    pdf_doc = SimpleDocTemplate(
        buffer,
        pagesize=A4,
        rightMargin=40,
        leftMargin=40,
        topMargin=40,
        bottomMargin=40
    )
    
    styles = getSampleStyleSheet()
    title_style = ParagraphStyle(
        'DocTitle',
        parent=styles['Heading1'],
        fontSize=16,
        leading=20,
        textColor=colors.HexColor("#1e3a8a"),
        alignment=1,
        spaceAfter=15
    )
    subtitle_style = ParagraphStyle(
        'DocSubtitle',
        parent=styles['Normal'],
        fontSize=10,
        leading=14,
        textColor=colors.HexColor("#475569"),
        alignment=1,
        spaceAfter=25
    )
    body_style = ParagraphStyle(
        'DocBody',
        parent=styles['Normal'],
        fontSize=10,
        leading=15,
        textColor=colors.HexColor("#1e293b")
    )
    
    doc_type_names = {
        'ktp': 'ARSIP IDENTITAS KARYAWAN (KTP)',
        'kontrak': 'DOKUMEN KONTRAK KERJA KARYAWAN',
        'sertifikat': 'SERTIFIKAT KOMPETENSI & PROFESIONAL',
        'ijazah': 'IJAZAH & TRANSKRIP AKADEMIK'
    }
    
    elements = []
    header_title = doc_type_names.get(doc['doc_type'], 'ARSIP DOKUMEN KEPEGAWAIAN')
    elements.append(Paragraph(f"<b>PT MITSINDO VISUAL PRATAMA</b>", title_style))
    elements.append(Paragraph(f"<b>{header_title}</b>", ParagraphStyle('H2', parent=title_style, fontSize=13, spaceAfter=5)))
    elements.append(Paragraph("Rukan Puri Delta Mas Blok I/46-47, Jl. Bandengan Selatan 43, Jakarta Utara 14450", subtitle_style))
    
    data_info = [
        [Paragraph("<b>Nama Dokumen</b>", body_style), Paragraph(f": {doc['file_name']}", body_style)],
        [Paragraph("<b>Jenis Berkas</b>", body_style), Paragraph(f": {doc['doc_type'].upper()}", body_style)],
        [Paragraph("<b>Nama Karyawan</b>", body_style), Paragraph(f": {doc['full_name']}", body_style)],
        [Paragraph("<b>NIK / NIP</b>", body_style), Paragraph(f": {doc['employee_id_str'] or '-'}", body_style)],
        [Paragraph("<b>Departemen / Divisi</b>", body_style), Paragraph(f": {doc['dept_name'] or '-'}", body_style)],
        [Paragraph("<b>Jabatan</b>", body_style), Paragraph(f": {doc['position_title'] or '-'}", body_style)],
        [Paragraph("<b>Tanggal Unggah</b>", body_style), Paragraph(f": {doc['uploaded_at'] or '-'}", body_style)],
        [Paragraph("<b>Masa Berlaku</b>", body_style), Paragraph(f": {doc['expiry_date'] or 'Seumur Hidup / Permanent'}", body_style)],
        [Paragraph("<b>Status Validitas</b>", body_style), Paragraph(": <font color='green'><b>TERVERIFIKASI & SAH (HR GA)</b></font>", body_style)],
    ]
    
    t = Table(data_info, colWidths=[150, 360])
    t.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#f8fafc')),
        ('PADDING', (0,0), (-1,-1), 8),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor('#cbd5e1')),
        ('INNERGRID', (0,0), (-1,-1), 0.5, colors.HexColor('#e2e8f0')),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
    ]))
    elements.append(t)
    elements.append(Spacer(1, 30))
    
    elements.append(Paragraph("<i>Catatan: Dokumen digital ini diterbitkan secara sah dan tervalidasi melalui Sistem HRIS PT Mitsindo Visual Pratama.</i>", ParagraphStyle('Note', parent=body_style, fontSize=9, textColor=colors.HexColor('#64748b'))))
    
    pdf_doc.build(elements)
    buffer.seek(0)
    
    return Response(
        content=buffer.getvalue(),
        media_type="application/pdf",
        headers={
            "Content-Disposition": f'inline; filename="{doc["file_name"]}"'
        }
    )


@router.get("")
async def list_all_documents(db=Depends(get_db), user=Depends(get_current_user)):
    """List all documents (admin/manager) or own documents (employee)."""
    if user["role"] == "employee":
        cursor = await db.execute(
            "SELECT d.*, e.full_name FROM documents d "
            "JOIN employees e ON d.employee_id = e.id "
            "WHERE d.employee_id = ? ORDER BY d.uploaded_at DESC",
            (user["user_id"],)
        )
    else:
        cursor = await db.execute(
            "SELECT d.*, e.full_name FROM documents d "
            "JOIN employees e ON d.employee_id = e.id "
            "ORDER BY d.uploaded_at DESC"
        )
    rows = await cursor.fetchall()
    return [dict(r) for r in rows]

UPLOAD_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "uploads", "documents")
os.makedirs(UPLOAD_DIR, exist_ok=True)

def _uid(user):
    return user.get("user_id") or user.get("id")

@router.post("/upload")
async def upload_document(employee_id: int = Form(...), doc_type: str = Form(...), file: UploadFile = File(...), user=Depends(get_current_user), db: aiosqlite.Connection = Depends(get_db)):
    if user.get("role") not in ("super_admin", "director", "manager"):
        raise HTTPException(status_code=403, detail="Manager, director or admin access required")
    filename = f"{uuid.uuid4().hex}_{file.filename}"
    filepath = os.path.join(UPLOAD_DIR, filename)
    content = await file.read()
    with open(filepath, "wb") as f:
        f.write(content)
    cursor = await db.execute("INSERT INTO documents (employee_id, doc_type, file_name, file_path) VALUES (?, ?, ?, ?)", (employee_id, doc_type, file.filename, filepath))
    await db.commit()
    return {"id": cursor.lastrowid, "message": "Document uploaded", "filename": file.filename}

@router.get("/{emp_id}")
async def list_documents(emp_id: int, user=Depends(get_current_user), db: aiosqlite.Connection = Depends(get_db)):
    if user.get("role") == "employee":
        cursor = await db.execute("SELECT employee_id FROM users WHERE id = ?", (_uid(user),))
        row = await cursor.fetchone()
        if not row or (row["employee_id"] and row["employee_id"] != emp_id):
            raise HTTPException(status_code=403, detail="Access denied")
    cursor = await db.execute("SELECT * FROM documents WHERE employee_id = ? ORDER BY uploaded_at DESC", (emp_id,))
    rows = await cursor.fetchall()
    return {"documents": [dict(r) for r in rows]}

@router.delete("/{doc_id}")
async def delete_document(doc_id: int, user=Depends(get_current_user), db: aiosqlite.Connection = Depends(get_db)):
    if user.get("role") not in ("super_admin", "director", "manager"):
        raise HTTPException(status_code=403, detail="Manager, director or admin access required")
    cursor = await db.execute("SELECT file_path FROM documents WHERE id = ?", (doc_id,))
    doc = await cursor.fetchone()
    if doc and os.path.exists(doc["file_path"]):
        os.remove(doc["file_path"])
    await db.execute("DELETE FROM documents WHERE id = ?", (doc_id,))
    await db.commit()
    return {"message": "Document deleted"}
