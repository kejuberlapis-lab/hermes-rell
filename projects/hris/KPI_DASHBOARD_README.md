# KPI Dashboard - HRIS System

## Overview
Dashboard KPI untuk HRIS Solution Integration Profesional - Fase Transisi 2026

## Features
- 📊 **Overview KPI**: Statistik total template, karyawan, dan departemen
- 🏢 **Breakdown Departemen**: KPI per departemen (Executive, Finance, Marketing, Operations)
- 👥 **Assignment KPI**: Tabel assignment KPI karyawan dengan filter
- 📈 **Analisis & Laporan**: Chart distribusi, bobot, dan tren pencapaian
- 🏆 **Skema Reward**: Informasi reward non-finansial

## Akses Dashboard
```
http://localhost:8090/kpi-dashboard
```

## API Endpoints
```
GET /api/kpi-dashboard/summary          - Ringkasan KPI
GET /api/kpi-dashboard/templates        - Template KPI
GET /api/kpi-dashboard/assignments      - Assignment karyawan
GET /api/kpi-dashboard/department-stats - Statistik departemen
GET /api/kpi-dashboard/scoring-scale    - Skala penilaian
GET /api/kpi-dashboard/rewards          - Skema reward
```

## File Structure
```
/home/ubuntu/hris/
├── templates/pages/kpi_dashboard.html  # Dashboard UI
├── app/routes/kpi_dashboard.py         # API routes
├── kpi_export/                         # Export files
│   ├── kpi_formulas.csv
│   ├── kpi_formulas.json
│   ├── kpi_formulas.sql
│   ├── kpi_excel_template.csv
│   └── kpi_summary_report.txt
└── test_kpi_dashboard.py              # Test script
```

## Database Tables
- `kpi_formulas`: Formula perhitungan KPI
- `kpi_templates`: Template KPI per departemen/posisi
- `employee_kpis`: Assignment KPI karyawan

## Scoring Scale (Fase Transisi)
1. **Sangat Kurang**: < 50% dari target
2. **Kurang**: 50% - 69% dari target
3. **Memenuhi Harapan**: 70% - 85% dari target
4. **Baik**: 86% - 100% dari target
5. **Sangat Baik**: > 100% dari target

## Reward Scheme 2026
- **Extra PTO**: 1 hari untuk skor KPI minimal 95% selama 4 kuartal
- **WFH/WFA**: 1 hari/bulan dengan persetujuan Manajer
- **Sponsor Sertifikasi**: Pembiayaan penuh ujian sertifikasi
- **Employee of the Month**: Sertifikat + Rp 250.000

## Testing
```bash
python3 test_kpi_dashboard.py
```

## Start Server
```bash
cd /home/ubuntu/hris
python3 main.py
```

Server akan berjalan di: `http://0.0.0.0:8090`
