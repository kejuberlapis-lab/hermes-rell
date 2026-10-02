#!/usr/bin/env python3
"""
KPI Dashboard Quick Start Script
Easy way to access and test the KPI Dashboard
"""
import webbrowser
import time
import sys

def main():
    print("=" * 60)
    print("🚀 KPI DASHBOARD - QUICK START")
    print("=" * 60)
    print()
    
    # Server info
    base_url = "http://localhost:8090"
    dashboard_url = f"{base_url}/kpi-dashboard"
    api_url = f"{base_url}/api/kpi-dashboard"
    
    print("📊 KPI Dashboard URLs:")
    print(f"   🌐 Main Dashboard: {dashboard_url}")
    print(f"   📡 API Endpoints: {api_url}")
    print()
    
    print("🔗 Quick Links:")
    print(f"   1. Dashboard: {dashboard_url}")
    print(f"   2. Summary: {api_url}/summary")
    print(f"   3. Templates: {api_url}/templates")
    print(f"   4. Assignments: {api_url}/assignments")
    print(f"   5. Department Stats: {api_url}/department-stats")
    print(f"   6. Scoring Scale: {api_url}/scoring-scale")
    print(f"   7. Rewards: {api_url}/rewards")
    print()
    
    print("📋 Features:")
    print("   ✅ 33 KPI Templates")
    print("   ✅ 36 Employee Assignments")
    print("   ✅ 5 Departments Covered")
    print("   ✅ Interactive Charts")
    print("   ✅ Export Functionality")
    print("   ✅ Scoring Scale (1-5)")
    print("   ✅ Reward Scheme 2026")
    print()
    
    print("🎯 Scoring Scale (Fase Transisi):")
    print("   1 - Sangat Kurang: < 50% target")
    print("   2 - Kurang: 50-69% target")
    print("   3 - Memenuhi Harapan: 70-85% target")
    print("   4 - Baik: 86-100% target")
    print("   5 - Sangat Baik: > 100% target")
    print()
    
    print("🏆 Reward Scheme 2026:")
    print("   🌴 Extra PTO: 1 hari untuk skor 95%+ selama 4 kuartal")
    print("   🏠 WFH/WFA: 1 hari/bulan dengan persetujuan Manajer")
    print("   🎓 Sponsor Sertifikasi: Pembiayaan penuh ujian")
    print("   🏅 Employee of the Month: Sertifikat + Rp 250.000")
    print()
    
    # Ask to open browser
    response = input("🌐 Buka dashboard di browser? (y/n): ").strip().lower()
    if response == 'y' or response == '':
        print(f"   Membuka {dashboard_url}...")
        webbrowser.open(dashboard_url)
        time.sleep(2)
    
    print()
    print("📝 File Information:")
    print("   - Dashboard HTML: templates/pages/kpi_dashboard.html")
    print("   - API Routes: app/routes/kpi_dashboard.py")
    print("   - Export Files: kpi_export/")
    print("   - Test Script: test_kpi_dashboard.py")
    print("   - Documentation: KPI_DASHBOARD_README.md")
    print()
    
    print("🚀 To restart server:")
    print("   cd /home/ubuntu/hris")
    print("   python3 main.py")
    print()
    
    print("=" * 60)
    print("✅ KPI Dashboard is ready to use!")
    print("=" * 60)

if __name__ == "__main__":
    main()
