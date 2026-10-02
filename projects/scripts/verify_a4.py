import re

with open('/home/ubuntu/hris/templates/pages/travel.html', 'r') as f:
    html = f.read()

# Extract <style> block
match = re.search(r'<style>(.*?)</style>', html, re.DOTALL)
if not match:
    print("NOT FOUND")
    exit()

style = match.group(1)

checks = {
    "@page": r'@page[\s\S]*?size:\s*A4\s*portrait',
    "body-width": r'body[\s\S]*?width:\s*100%[\s\S]*?max-width:\s*none',
    ".page-wrap": r'\.page-wrap[\s\S]*?width:\s*170mm',
    "font-size-body": r'body[\s\S]*?font-size:\s*10pt',
    "letterhead-h1": r'\.letterhead h1[\s\S]*?font-size:\s*13pt',
    "info-padd": r'\.info-tbl td[\s\S]*?padding:\s*1px\s*4px',
    "cost-font": r'\.cost-tbl[\s\S]*?font-size:\s*8\.5pt',
    "sig-height": r'\.garis-ttd[\s\S]*?height:\s*45px',
    "media-print": r'@media\s+print',
}

print("=" * 55)
print("VERIFIKASI CSS CETAK A4 - TRAVEL REQUEST PDF")
print("=" * 55)
all_ok = True
for name, pattern in checks.items():
    found = bool(re.search(pattern, style))
    status = "✅" if found else "❌"
    if not found:
        all_ok = False
    print(f"{status} {name:<25}")

print("\n" + "=" * 55)
if all_ok:
    print("🎉 SEMUA PENGATURAN A4 SUDAH BENAR!")
else:
    print("⚠️ ADA YANG BELUM OPTIMAL")
print("=" * 55)
