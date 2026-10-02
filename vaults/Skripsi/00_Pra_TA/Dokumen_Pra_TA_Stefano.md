---
title: PTA.01 Pendaftaran Pra-Tugas Akhir
author: Stefano Garrent Khristiawan
nim: 124230117
prodi: Sistem Informasi
keminatan: Data Science
bidang_ta: SPK dan Machine Learning
bahasa_pemrograman: Python
dospem: Dr. Herlina Jayadianti, S.T., M.T. / Andiko Putro Suryotomo, S.Kom., M.Cs. / Bambang Yuwono, S.T., M.T.
koordinator_ta: Hari Prapcoyo, S.Kom., MICT. (NIDN: 0008128204)
status: Usulan Judul & Draft Siap Review
date: 2026-09-29
tags:
  - pra-ta
  - proposal
  - pta01
  - upnyk
  - yolo
  - fuzzy-logic
  - computer-vision
  - spk
---

# 📝 PTA.01 — PENDAFTARAN PRA-TUGAS AKHIR
**Program Studi Sistem Informasi — Jurusan Informatika**  
**Fakultas Teknik Industri, Universitas Pembangunan Nasional "Veteran" Yogyakarta**

Kembali ke [[MOC - Skripsi]] | File Dokumen Word Asli: `[[Pra-TA Stefano.docx]]`

---

## 📌 Data Mahasiswa & Usulan Tugas Akhir

| Field | Keterangan Data |
| :--- | :--- |
| **Nama Mahasiswa** | **Stefano Garrent Khristiawan** |
| **NIM** | **124230117** |
| **Program Studi** | **Sistem Informasi** |
| **Keminatan** | **Data Science** |
| **Bidang Tugas Akhir** | **SPK dan Machine Learning** |
| **Bahasa Pemrograman** | **Python** |
| **Rencana Judul Tugas Akhir** | **Rancang Bangun Sistem Pendukung Keputusan Alokasi dan Penjadwalan Staf Kafe Berbasis *Vision Analytics* Menggunakan Integrasi Algoritma YOLO dan *Fuzzy Inference System* pada Kafe X** |
| **Calon Dosen Pembimbing** | 1. Dr. Herlina Jayadianti, S.T., M.T.<br>2. Andiko Putro Suryotomo, S.Kom., M.Cs.<br>3. Bambang Yuwono, S.T., M.T. |
| **Koordinator TA** | **Hari Prapcoyo, S.Kom., MICT.** (NIDN: 0008128204) |

---

## 📑 DESKRIPSI SINGKAT RENCANA TUGAS AKHIR

### 1. Latar Belakang Masalah

Industri *Food and Beverage* (F&B), khususnya bisnis kedai kopi (*coffee shop*), mengalami pertumbuhan yang sangat pesat dan menjadi salah satu sektor usaha gaya hidup yang sangat kompetitif di Indonesia. Dalam mengelola operasional kafe, keberhasilan bisnis tidak hanya ditentukan oleh cita rasa produk, melainkan sangat dipengaruhi oleh efisiensi manajemen alokasi tenaga kerja (*workforce management*) dan kualitas kecepatan pelayanan kepada pelanggan ([Khaira et al., 2022](https://journal.admi.or.id/index.php/JAMAN/article/view/350)). Penataan alokasi jumlah karyawan—khususnya barista dan staf pelayanan—pada setiap giliran kerja (*shift*) merupakan faktor penentu utama yang mempengaruhi kelancaran operasional serta struktur biaya operasional tenaga kerja (*labor cost*) ([Ferwany et al., 2024](https://justme.ft-uim.ac.id/index.php/JUSTME/article/view/58)). Namun, pada praktiknya, sebagian besar pengelola kafe masih menyusun jadwal kerja secara manual berdasarkan perkiraan kasual (*instinct-based*) atau pola jadwal statis mingguan. Pendekatan konvensional ini kerap menimbulkan ketidaksesuaian beban kerja riil (*workload mismatch*), di mana terjadi kekurangan staf (*understaffing*) saat jam-jam sibuk (*rush hour*) yang memperlambat waktu saji minuman (*cycle time*), atau sebaliknya terjadi kelebihan staf (*overstaffing*) saat kafe sepi yang memicu inefisiensi biaya operasional ([Ferwany et al., 2024](https://justme.ft-uim.ac.id/index.php/JUSTME/article/view/58)).

Permasalahan manajemen operasional tersebut diperparah oleh keterbatasan sistem kasir (*Point of Sale* / POS) yang umum digunakan pada bisnis kafe saat ini. Sistem POS konvensional hanya berfokus pada pencatatan transaksi pemesanan menu dan pelaporan keuangan kasir ([Rosi et al., 2025](https://ojs.uajy.ac.id/index.php/jiaj/article/view/13119)), namun tidak memiliki kapabilitas sensor visual untuk memantau pergerakan orang serta mengevaluasi dinamika fisik di area tempat usaha ([Fahrezi & Widiyanto, 2024](https://jurnal.mdp.ac.id/index.php/jatisi/article/view/9050)). Ketiadaan integrasi data spasial ini menyebabkan sistem informasi eksisting tidak mampu mendeteksi durasi nyata pelanggan berada di meja (*dwell time*), tingkat okupansi riil kursi, maupun beban antrean fisik peracikan kopi barista. Akibatnya, pengelola kafe kerap menghadapi fenomena *phantom occupancy*, yaitu kondisi di mana area meja tampak penuh terisi oleh pengunjung dalam durasi lama untuk bekerja atau mengerjakan tugas namun dengan frekuensi pemesanan rendah ([Marzuqi & Fardani, 2024](https://journal.ipm2kpe.or.id/index.php/COSTING/article/view/12819)), sehingga menghalangi pelanggan baru untuk datang serta menimbulkan bias data saat manajer memperkirakan kebutuhan jumlah staf yang bertugas.

Berdasarkan kajian studi literatur terkini (2021–2026), pemanfaatan teknologi *Computer Vision* berbasis algoritma *deep learning*—khususnya keluarga arsitektur YOLO (*You Only Look Once*)—telah terbukti sangat efektif, tangguh, dan akurat dalam mendeteksi keberadaan manusia serta memantau pergerakan pengunjung di area publik secara *real-time* ([Hasani et al., 2022](https://jurnal.iaii.or.id/index.php/RESTI/article/view/3808); [Fahrezi & Widiyanto, 2024](https://jurnal.mdp.ac.id/index.php/jatisi/article/view/9050); [Satria et al., 2026](https://ejurnal.stmik-budidarma.ac.id/index.php/jurikom/article/view/9502)). Namun, sebagian besar implementasi visi komputer tersebut hanya berhenti pada tahap ekstraksi data visual mentah (*people counting*) tanpa diintegrasikan lebih lanjut ke dalam sistem pendukung keputusan manajerial. Di sisi lain, penelitian di bidang Sistem Pendukung Keputusan (SPK) yang menerapkan metode penalaran logika *Fuzzy* terbukti unggul dalam memodelkan optimasi penjadwalan dan alokasi tenaga kerja di bawah kondisi yang dinamis ([Supriyono et al., 2025](https://jurnal.unigal.ac.id/GAMMA-NC/article/view/18946); [Nursyanti et al., 2021](https://jurnal.ubl.ac.id/index.php/explore/article/view/2008)), khususnya pada operasional *coffee shop* ([Elis & Octora, 2025](https://infeb.org/index.php/infeb/article/view/1335)), namun mayoritas penerapannya masih sangat bergantung pada penginputan data nilai manual atau kuesioner statis yang rentan terhadap kelalaian rekapitulasi serta subjektivitas pengambil keputusan (*research gap*).

Padahal, dinamika operasional kafe memiliki tingkat ketidakpastian (*uncertainty*) dan keabuan (*vagueness*) tinggi yang sangat tepat dimodelkan menggunakan *Fuzzy Inference System* ([Supriyono et al., 2025](https://jurnal.unigal.ac.id/GAMMA-NC/article/view/18946); [Nursyanti et al., 2021](https://jurnal.ubl.ac.id/index.php/explore/article/view/2008)). Hubungan antara kepadatan pengunjung, durasi duduk (*dwell time*), dan laju penyajian pesanan terhadap kebutuhan jumlah staf tidak bersifat linier kaku, melainkan berupa pernyataan linguistik (*linguistic variables*). Oleh karena itu, penelitian ini mengusulkan **Rancang Bangun Sistem Pendukung Keputusan Alokasi dan Penjadwalan Staf Kafe Berbasis *Vision Analytics* Menggunakan Integrasi Algoritma YOLO dan *Fuzzy Inference System***. Algoritma YOLOv8 ([Fahrezi & Widiyanto, 2024](https://jurnal.mdp.ac.id/index.php/jatisi/article/view/9050); [Hasani et al., 2022](https://jurnal.iaii.or.id/index.php/RESTI/article/view/3808)) dan *multi-object tracking* ByteTrack ([Zhang et al., 2022](https://arxiv.org/abs/2110.06864)) diimplementasikan sebagai instrumen ekstraksi data operasional otomatis (*automated data stream*) yang merekam metrik durasi singgah pengunjung serta kepadatan area secara *real-time*. Data metrik visual tersebut kemudian diolah ke dalam *Fuzzy Inference System* (Metode Mamdani) guna memetakan derajat beban kerja dan menghasilkan rekomendasi alokasi serta jadwal *shift* kerja staf yang objektif, adaptif, serta mampu meminimalkan *labor cost* tanpa mengorbankan kualitas layanan ([Ferwany et al., 2024](https://justme.ft-uim.ac.id/index.php/JUSTME/article/view/58); [Khaira et al., 2022](https://journal.admi.or.id/index.php/JAMAN/article/view/350)).

---

### 2. Rumusan Masalah

Berdasarkan latar belakang di atas, rumusan masalah dalam penelitian tugas akhir ini adalah:
1. Bagaimana merancang dan mengimplementasikan model *Computer Vision* berbasis algoritma YOLOv8 ([Fahrezi & Widiyanto, 2024](https://jurnal.mdp.ac.id/index.php/jatisi/article/view/9050)) dan pelacak *multi-object tracking* ByteTrack ([Zhang et al., 2022](https://arxiv.org/abs/2110.06864)) untuk mengekstraksi metrik durasi singgah pengunjung (*dwell time*) dan tingkat okupansi area kafe secara otomatis dan akurat?
2. Bagaimana memformulasikan fungsi keanggotaan dan basis aturan (*rule base*) pada *Fuzzy Inference System* Metode Mamdani ([Supriyono et al., 2025](https://jurnal.unigal.ac.id/GAMMA-NC/article/view/18946); [Nursyanti et al., 2021](https://jurnal.ubl.ac.id/index.php/explore/article/view/2008)) dengan memanfaatkan masukan data metrik *Vision Analytics* guna menentukan indeks beban kerja dan kebutuhan alokasi staf kafe ([Ferwany et al., 2024](https://justme.ft-uim.ac.id/index.php/JUSTME/article/view/58))?
3. Sejauh mana kinerja teknis model deteksi objek YOLO (berdasarkan metrik *Precision*, *Recall*, dan *Mean Average Precision / mAP*) ([Upuy, 2025](https://ejurnal.umri.ac.id/index.php/coscitech/article/view/11189)) serta akurasi inferensi keputusan metode *Fuzzy* dalam menghasilkan rekomendasi staf yang optimal berdasarkan metrik *Mean Absolute Percentage Error* (MAPE) terhadap keputusan manajerial pakar ([Chicco et al., 2021](https://peerj.com/articles/cs-623/))?

---

### 3. Tujuan Penelitian

Tujuan yang ingin dicapai dari pelaksanaan penelitian tugas akhir ini adalah:
1. Merancang, melatih, dan menguji model deteksi objek YOLOv8 ([Fahrezi & Widiyanto, 2024](https://jurnal.mdp.ac.id/index.php/jatisi/article/view/9050)) serta algoritma pelacak *multi-object tracking* ByteTrack ([Zhang et al., 2022](https://arxiv.org/abs/2110.06864)) untuk mengekstraksi metrik durasi singgah pengunjung (*dwell time*) dan tingkat okupansi area kafe secara otomatis dan akurat.
2. Membangun model Sistem Pendukung Keputusan menggunakan *Fuzzy Inference System* (Metode Mamdani) ([Supriyono et al., 2025](https://jurnal.unigal.ac.id/GAMMA-NC/article/view/18946); [Nursyanti et al., 2021](https://jurnal.ubl.ac.id/index.php/explore/article/view/2008)) yang memproses variabel masukan visual dinamis guna menginferensi kebutuhan jumlah staf dan penataan jadwal *shift* kerja staf kafe secara adaptif ([Ferwany et al., 2024](https://justme.ft-uim.ac.id/index.php/JUSTME/article/view/58)).
3. Mengevaluasi performa teknis model visi komputer (*Precision*, *Recall*, *mAP@0.5*, dan FPS) ([Upuy, 2025](https://ejurnal.umri.ac.id/index.php/coscitech/article/view/11189); [Terven & Cordova-Esparza, 2023](https://doi.org/10.3390/make5040083)), menguji validitas hasil rekomendasi alokasi staf SPK Fuzzy menggunakan metrik *Mean Absolute Percentage Error* (MAPE) terhadap keputusan manajerial pakar ([Chicco et al., 2021](https://peerj.com/articles/cs-623/)), serta menguji keandalan fungsionalitas antarmuka perangkat lunak menggunakan *Black Box Testing* ([Dewi et al., 2023](https://ojs.uajy.ac.id/index.php/konstelasi/article/view/7046)).

---

### 4. Manfaat Penelitian

Manfaat yang diharapkan dari hasil penelitian tugas akhir ini adalah:
- **Bagi Pengembangan Keilmuan (Manfaat Teoretis):** Memberikan kontribusi akademik dalam bidang Sistem Informasi, *Data Science*, dan Sistem Pendukung Keputusan mengenai integrasi aliran data visual otomatis (*Vision Analytics*) berbasis YOLOv8 dan ByteTrack ([Fahrezi & Widiyanto, 2024](https://jurnal.mdp.ac.id/index.php/jatisi/article/view/9050); [Zhang et al., 2022](https://arxiv.org/abs/2110.06864)) sebagai masukan dinamis pada model penalaran *Fuzzy Inference System* Metode Mamdani untuk menyelesaikan permasalahan alokasi tenaga kerja pada industri jasa ([Supriyono et al., 2025](https://jurnal.unigal.ac.id/GAMMA-NC/article/view/18946); [Nursyanti et al., 2021](https://jurnal.ubl.ac.id/index.php/explore/article/view/2008)).
- **Bagi Pengelola Kafe (Manfaat Praktis):** Menyediakan sistem otomasi pendukung keputusan yang membantu manajer kafe menyusun alokasi jumlah staf dan penataan jadwal *shift* kerja karyawan secara objektif, adil, dan adaptif berbasis data keramaian riil, sehingga mampu meminimalkan pembengkakan biaya tenaga kerja (*labor cost*) di jam sepi serta menjaga standar kecepatan dan kualitas pelayanan pelanggan di jam sibuk (*rush hour*) ([Ferwany et al., 2024](https://justme.ft-uim.ac.id/index.php/JUSTME/article/view/58); [Elis & Octora, 2025](https://doi.org/10.37034/infeb.v7i4.1335); [Khaira et al., 2022](https://journal.admi.or.id/index.php/JAMAN/article/view/350)).

---

### 5. Tahapan Penelitian / Metodologi dan Perancangan Model

Metodologi penelitian ini dirancang secara sistematis dengan mengacu pada literatur ilmiah terkini:

#### 5.1 Tahapan Penelitian
1. **Identifikasi Masalah & Studi Pustaka:** Mengkaji literatur mutakhir terkait arsitektur YOLOv8 ([Upuy, 2025](https://ejurnal.umri.ac.id/index.php/coscitech/article/view/11189); [Fahrezi & Widiyanto, 2024](https://jurnal.mdp.ac.id/index.php/jatisi/article/view/9050)), algoritma pelacakan multi-objek ByteTrack ([Zhang et al., 2022](https://arxiv.org/abs/2110.06864)), penerapan *Fuzzy Inference System* dalam alokasi tenaga kerja ([Supriyono et al., 2025](https://jurnal.unigal.ac.id/GAMMA-NC/article/view/18946); [Nursyanti et al., 2021](https://jurnal.ubl.ac.id/index.php/explore/article/view/2008)), serta manajemen operasional *shift* kerja staf kafe ([Ferwany et al., 2024](https://justme.ft-uim.ac.id/index.php/JUSTME/article/view/58); [Elis & Octora, 2025](https://doi.org/10.37034/infeb.v7i4.1335)).
2. **Pengumpulan Data Video CCTV & Pelabelan:** Perekaman video CCTV pada area meja makan pengunjung dan meja bar barista kafe. Dataset dianotasi dengan *bounding box* (kategori: *person*, *barista*, *cup*, *table*) menggunakan format anotasi YOLO melalui platform CVAT / Roboflow.
3. **Pra-pengolahan Data Citra:** Penerapan augmentasi citra (*brightness adjustment, scaling, horizontal flip*) untuk memperkuat generalisasi model terhadap variasi pencahayaan kafe serta pembagian dataset menjadi data *training* (70%), *validation* (15%), dan *testing* (15%).
4. **Pengembangan Pipeline Vision Analytics (YOLOv8 + ByteTrack):**
   - Pelatihan model deteksi YOLOv8 untuk mengenali pengunjung dan cup minuman secara *real-time* ([Upuy, 2025](https://ejurnal.umri.ac.id/index.php/coscitech/article/view/11189); [Terven & Cordova-Esparza, 2023](https://doi.org/10.3390/make5040083); [Syaifuddin et al., 2026](https://ejurnal.stmik-budidarma.ac.id/index.php/jurikom/article/view/9298)).
   - Implementasi pelacakan ByteTrack ([Zhang et al., 2022](https://arxiv.org/abs/2110.06864)) untuk penomoran ID unik pengunjung guna menghitung durasi duduk (*Dwell Time*) per meja tanpa kehilangan pelacakan akibat oklusi.
   - Deteksi interaksi barista dan cup untuk menghitung laju *Throughput* produksi minuman per interval waktu ([Elis & Octora, 2025](https://doi.org/10.37034/infeb.v7i4.1335)).
5. **Perancangan Model SPK Fuzzy Inference System (Mamdani):**
   - **Fuzzifikasi:** Pembentukan fungsi keanggotaan kurva representasi (Segitiga/Trapesium) untuk 3 variabel input (*Dwell Time*, Kepadatan Pengunjung, *Cup Throughput*) dan 1 variabel output (Indeks Kebutuhan Staf) ([Supriyono et al., 2025](https://jurnal.unigal.ac.id/GAMMA-NC/article/view/18946); [Nursyanti et al., 2021](https://jurnal.ubl.ac.id/index.php/explore/article/view/2008)).
   - **Penyusunan Basis Aturan (Rule Base):** Merumuskan himpunan aturan *IF-THEN* berbasis wawancara pakar/manajer kafe (misal: *IF Kepadatan Tinggi AND Dwell Time Lama AND Throughput Tinggi THEN Kebutuhan Staf = Sangat Banyak*).
   - **Mesin Inferensi:** Penerapan operator implikasi Min (Mamdani) dan komposisi aturan Max ([Supriyono et al., 2025](https://jurnal.unigal.ac.id/GAMMA-NC/article/view/18946); [Nursyanti et al., 2021](https://jurnal.ubl.ac.id/index.php/explore/article/view/2008)).
   - **Defuzzifikasi:** Konversi daerah himpunan fuzzy menjadi nilai tegas (*crisp value*) menggunakan metode *Centroid / Center of Gravity* untuk menentukan jumlah riil staf per shift ([Ferwany et al., 2024](https://justme.ft-uim.ac.id/index.php/JUSTME/article/view/58)).
6. **Pengembangan Antarmuka Sistem Informasi (Prototyping):**
   - Mengadopsi metode pengembangan **Prototyping** ([Prihantara et al., 2024](https://ejurnal.swadharma.ac.id/index.php/jris/article/view/565)) untuk membangun antarmuka *dashboard* analitik berbasis web menggunakan Python (Streamlit / Flask) yang menyajikan data okupansi *real-time* dan rekomendasi jadwal kerja.
7. **Pengujian Sistem & Evaluasi Penelitian.**

#### 5.2 Pengujian Sistem
Pengujian fungsionalitas perangkat lunak dilakukan menggunakan metode **Black Box Testing** ([Dewi et al., 2023](https://ojs.uajy.ac.id/index.php/konstelasi/article/view/7046)) untuk memverifikasi bahwa antarmuka sistem, modul pemrosesan video, eksekusi inferensi fuzzy, dan modul ekspor jadwal shift bekerja sesuai dengan spesifikasi kebutuhan pengguna.

#### 5.3 Pengujian Penelitian
Pengujian performa ilmiah dilakukan melalui dua aspek metrik kuantitatif:
- **Evaluasi Model Computer Vision:** Mengukur nilai *Precision*, *Recall*, *Mean Average Precision* (*mAP@0.5* dan *mAP@0.5:0.95*), serta kecepatan pemrosesan *Frames Per Second* (FPS) ([Upuy, 2025](https://ejurnal.umri.ac.id/index.php/coscitech/article/view/11189); [Terven & Cordova-Esparza, 2023](https://doi.org/10.3390/make5040083)).
- **Evaluasi Model SPK Fuzzy:** Mengukur akurasi keputusan model terhadap keputusan riil manajer kafe (*ground truth*) menggunakan metrik *Mean Absolute Percentage Error* (MAPE) ([Chicco et al., 2021](https://peerj.com/articles/cs-623/)):
  $$	ext{MAPE} = \frac{1}{n} \sum_{t=1}^{n} \left| \frac{A_t - F_t}{A_t} \right| 	imes 100\%$$

---

### 6. Referensi (Daftar Publikasi Ilmiah 5 Tahun Terakhir: 2021–2026)

1. Chicco, D., Warrens, M. J., & Jurman, G. (2021). "The Coefficient of Determination R-Squared is More Informative than SMAPE, MAE, MAPE, MSE and RMSE in Regression Analysis Evaluation". *PeerJ Computer Science*, 7, e623. https://doi.org/10.7717/peerj-cs.623.
2. Dewi, F. K. S., Adithama, S. P., & Suhardi, A. T. (2023). "Pengujian Aplikasi Menggunakan Metode Black Box Testing". *KONSTELASI: Konvergensi Teknologi dan Sistem Informasi*, 3(1), hal. 61-72. https://doi.org/10.24002/konstelasi.v3i1.7046.
3. Elis, & Octora, S. E. S. (2025). "Analisis Pengaruh Motivasi Kerja terhadap Kinerja Karyawan Gen Z di Coffee Shop melalui Work-Life Balance di Kota Pontianak". *Jurnal Informatika Ekonomi Bisnis (INFEB)*, 7(4), hal. 1024-1030. https://doi.org/10.37034/infeb.v7i4.1335.
4. Fahrezi, M. A., & Widiyanto, E. P. (2024). "Implementasi YOLOv8 Dalam Penghitung Masuk Dan Keluar Manusia Pada Gedung". *JATISI: Jurnal Teknik Informatika dan Sistem Informasi*, 11(3), hal. 335-345. https://doi.org/10.35957/jatisi.v11i3.9050.
5. Ferwany, M., Hanafie, A., & Syarifuddin, R. (2024). "Penjadwalan Shift Tenaga Kerja Menggunakan Metode Algoritma untuk Meningkatkan Produktivitas Kerja". *Journal Industrial Engineering and Management (JUST-ME)*, 5(1), hal. 27-36. https://doi.org/10.47398/justme.v5i01.58.
6. Hasani, M. C., Milenasari, F., & Setyawan, N. (2022). "Pemantauan Physical Distance Pada Area Umum Menggunakan YOLO Tiny V3". *Jurnal RESTI (Rekayasa Sistem dan Teknologi Informasi)*, 6(1), hal. 146-152. https://doi.org/10.29207/resti.v6i1.3808.
7. Khaira, N., Saputra, F., & Syarief, F. (2022). "Pengaruh Persepsi Harga dan Kualitas Pelayanan terhadap Keputusan Pembelian di Kafe Sudut Halaman". *JAMAN: Jurnal Akuntansi dan Manajemen Bisnis*, 2(3), hal. 24-30. https://doi.org/10.56127/jaman.v2i3.350.
8. Marzuqi, A. M., & Fardani, F. F. (2024). "Kepuasan Konsumsi Kopi Lokal Gen Z Ditinjau dari Store Atmosphere dan Customer Experience di Kota Solo Tahun 2024". *COSTING: Journal of Economic, Business and Accounting*, 7(6), hal. 4272-4280. https://doi.org/10.31539/costing.v7i6.12819.
9. Nursyanti, R., Nasution, V. M., & Kurniawan, C. (2021). "Fuzzy Logic Metode Mamdani Untuk Pendukung Keputusan Penerimaan Karyawan". *Explore: Jurnal Sistem Informasi dan Telematika*, 12(1), hal. 72-81. https://jurnal.ubl.ac.id/index.php/explore/article/view/2008.
10. Prihantara, A., Abda'u, P. D., & Fauzi, H. M. (2024). "Perancangan Sistem Informasi Inventaris Barang dan Aset Desa Berbasis Website Menggunakan Metode Prototyping". *JRIS: Jurnal Rekayasa Informasi Swadharma*, 4(2), hal. 1-7. https://doi.org/10.56486/jris.v4i2.565.
11. Rosi, F., Julianto, E., & Adithama, S. P. (2025). "Pembangunan Website Point of Sale Pada Kafe Opak Kopi". *JIAJ: Jurnal Informatika Atma Jogja*, 6(2), hal. 95-104. https://doi.org/10.24002/jiaj.v6i2.13119.
12. Satria, F., Hamdhana, D., & Rosnita, L. (2026). "Sistem Presensi Mahasiswa Berbasis Pengenalan Wajah Real-Time dengan Deteksi Anti-Spoofing Menggunakan YOLOv8 dan ArcFace". *JURIKOM (Jurnal Riset Komputer)*, 13(1), hal. 441-450. https://doi.org/10.30865/jurikom.v13i1.9502.
13. Supriyono, P. T., Zahro, L. A., & Mayyani, H. (2025). "Optimisasi Penjadwalan Karyawan: Perbandingan Fuzzy Programming dan Goal Programming". *Proceeding Galuh Mathematics National Conference*, 5(1), hal. 168-174. https://jurnal.unigal.ac.id/GAMMA-NC/article/view/18946.
14. Syaifuddin, Labolo, I., Paemo, N. D., & Buna, A. M. I. (2026). "Edge AI Berbasis Computer Vision Untuk Meningkatkan Efektivitas Sistem Deteksi Pemilahan Sampah Real-Time Integrasi YOLOv8, Raspberry Pi 5 dan SEE". *JURIKOM (Jurnal Riset Komputer)*, 13(1), hal. 19-28. https://doi.org/10.30865/jurikom.v13i1.9298.
15. Terven, J., & Cordova-Esparza, D. M. (2023). "A Comprehensive Review of YOLO Architectures in Computer Vision: From YOLOv1 to YOLOv8 and YOLO-NAS". *Machine Learning and Knowledge Extraction*, 5(4), pp. 1680-1716. https://doi.org/10.3390/make5040083.
16. Upuy, D. (2025). "Comparison of YOLOv8n and YOLOv8s Model Performance in Object Detection Using Evaluation Metrics and Confidence Scores". *Jurnal CoSciTech (Computer Science and Information Technology)*, 7(1), hal. 51-57. https://doi.org/10.37859/coscitech.v7i1.11189.
17. Zhang, Y., Sun, P., Dong, Y., Jiang, Y., Yu, D., Yuan, Z., Luo, P., Liu, W., & Wang, X. (2022). "ByteTrack: Multi-Object Tracking by Associating Every Detection Box". *In European Conference on Computer Vision (ECCV)*, Springer, pp. 1-21. https://doi.org/10.1007/978-3-031-20047-2_1.

---

## 📋 FORM PERSETUJUAN PROPOSAL TUGAS AKHIR *(Lembar Pengesahan)*

Berdasarkan hasil penilaian oleh Koordinator Tugas Akhir dan dosen pembimbing terhadap proposal tugas akhir yang diusulkan oleh:

- **Nama:** Stefano Garrent Khristiawan
- **NIM:** 124230117
- **Judul TA:** **Rancang Bangun Sistem Pendukung Keputusan Alokasi dan Penjadwalan Staf Kafe Berbasis *Vision Analytics* Menggunakan Integrasi Algoritma YOLO dan *Fuzzy Inference System* pada Kafe X**

maka proposal tugas akhir tersebut dinyatakan: **DITERIMA / TIDAK DITERIMA\*** dengan dosen pembimbing: *(diplot oleh Koordinator TA)*

**Catatan dari Dosen Pembimbing:**
*(Akan dicatat saat sesi konsultasi pengajuan judul)*

---

| Mengetahui, Koordinator TA | Calon Dosen Pembimbing | Tanda Tangan Mahasiswa |
| :---: | :---: | :---: |
| <br><br><br>**(Hari Prapcoyo, S.Kom., MICT.)**<br>NIDN: 0008128204 | <br><br><br>**(_____________________)**<br>NIDN: | <br><br><br>**(Stefano Garrent Khristiawan)**<br>NIM: 124230117 |
