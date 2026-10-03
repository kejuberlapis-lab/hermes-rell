---
name: docker-container-supervisor
description: Use when managing Docker. Builds & audits containers.
---

# Production Docker Container Supervisor

Standar operasional pengelolaan kontainer Docker, Dockerfile, dan Docker Compose.

### Standar Kerja Docker:
1. **Build & Optimasi Image:**
   - Gunakan base image minimal (Alpine atau Slim) untuk mempercepat build dan menghemat storage server.
   - Gunakan multi-stage build untuk memisahkan dependensi kompilasi dari image produksi akhir.

2. **Pengawasan Kesehatan & Storage:**
   - Monitor penggunaan CPU, RAM, dan disk space kontainer secara berkala.
   - Bersihkan image dangling dan build cache yang tidak terpakai menggunakan `docker system prune` secara terukur.

3. **Isolasi Jaringan & Volume:**
   - Gunakan named volume untuk persistensi data database penting.
   - Pisahkan jaringan kontainer (internal network vs bridge) untuk mengamankan komunikasi antar-layanan.
