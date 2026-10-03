---
name: superpowers-agentic
description: Use when orchestrating agent workflows. Dispatches agents.
---

# Superpowers Agentic Framework

Framework teruji untuk brainstorming desain, orkestrasi agent otonom, dispatch subagent paralel, dan standarisasi proses development berskala besar.

## Workflow Inti
1. **Brainstorming Terstruktur:** Mengubah ide mentah menjadi spesifikasi teknis modular sebelum menulis kode satu baris pun.
2. **Parallel Subagent Dispatch:** Memecah tugas kompleks menjadi sub-tugas independen dan mengeksekusinya secara paralel menggunakan `delegate_task`.
3. **Quality Gates & Merge:** Setiap subagent harus memenuhi kriteria pengujian sebelum hasilnya digabungkan ke branch utama.
4. **Verifikasi Output Nyata:** Melarang pelaporan selesai tanpa bukti eksekusi dan verifikasi terminal nyata.
