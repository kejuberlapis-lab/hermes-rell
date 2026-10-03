# Community Repo Shortlist & Validation (Hermes)

Ringkasan pola validasi cepat sebelum instal kontribusi komunitas.

## Sumber shortlist awal
- https://github.com/0xNyk/awesome-hermes-agent
- https://github.com/Undermybelt/hermes-skills
- https://github.com/wong2/awesome-mcp-servers

## Metode validasi metadata (tanpa web_extract)
Saat backend extract = ddgs (search-only), gunakan GitHub API:

- `GET https://api.github.com/repos/<owner>/<repo>`
- Ambil minimal:
  - `full_name`
  - `stargazers_count`
  - `updated_at`
  - `html_url`

Tujuan: estimasi trust & maintenance sebelum instal.

## Keputusan operasional yang direkomendasikan
1. Pilih 1–2 repo dulu (jangan borongan).
2. Install hanya untuk 1 use-case prioritas.
3. Verifikasi hasil kerja real.
4. Baru scale ke repo/skill tambahan.
