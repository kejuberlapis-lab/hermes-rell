---
name: graphify-knowledge-graph
description: Use when analyzing architectures. Builds knowledge graphs.
---

# Graphify Codebase Knowledge Graph & GraphRAG

Transformasi codebase dan arsitektur repositori menjadi graf pengetahuan (*Knowledge Graph*) interaktif untuk analisis dependensi dan pencarian semantik tingkat tinggi.

## Fitur Inti
1. **AST & Dependency Mapping:** Memetakan relasi antar modul, fungsi, kelas, dan file impor ke dalam simpul dan sisi graf.
2. **Architectural Analysis:** Mendeteksi siklus dependensi melingkar (*circular dependencies*), titik kritis kegagalan (*bottlenecks*), dan kopling ketat.
3. **GraphRAG Exploration:** Menjawab pertanyaan arsitektur kompleks dengan menelusuri lintasan graf relasi kode.
