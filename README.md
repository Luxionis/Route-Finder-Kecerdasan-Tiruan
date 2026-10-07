# Route Finder — Optimasi Rute Terpendek (Algoritma Dijkstra)

> **Tugas 2 — Pemrograman Kecerdasan Tiruan (Kelas I)**  
> Program Studi Teknologi Informasi, Fakultas Teknik, Universitas Udayana  
> Dosen Pengampu: **I Nyoman Prayana Trisna, S.Kom., M.Cs.**

![Python Version](https://img.shields.io/badge/Python-3.10%2B-blue?logo=python&logoColor=white)
![Dependencies](https://img.shields.io/badge/Dependencies-Standard%20Library%20Only-success)
![Platform](https://img.shields.io/badge/Platform-Windows%20%7C%20Linux%20%7C%20macOS-lightgrey)
![Architecture](https://img.shields.io/badge/Architecture-Procedural%20%26%20Clean%20Code-orange)

---

## Daftar Isi
- [Identitas Penulis](#identitas-penulis)
- [Gambaran Umum](#gambaran-umum)
- [Fitur Utama](#fitur-utama)
- [Landasan Teori Algoritma](#landasan-teori-algoritma)
- [Struktur Repositori](#struktur-repositori)
- [Prasyarat Sistem](#prasyarat-sistem)
- [Panduan Penggunaan](#panduan-penggunaan)
- [Studi Kasus & Pembahasan Logika](#studi-kasus--pembahasan-logika)
  - [Topologi Graf Statis](#topologi-graf-statis)
  - [Hasil Komputasi](#hasil-komputasi)
  - [Contoh Tabel Tracing](#contoh-tabel-tracing)
- [Ketahanan Sistem & Penanganan Kasus Khusus](#ketahanan-sistem--penanganan-kasus-khusus)
- [Dokumen Pendukung](#dokumen-pendukung)

---

## Identitas Penulis

Program ini dikembangkan oleh **Kelompok 6** untuk memenuhi evaluasi Tugas 2 mata kuliah Kecerdasan Tiruan:

| No | Nama Lengkap | NIM | Peran / Kontribusi |
|:--:|:---|:---:|:---|
| 1 | **Nyoman Gede Adi Mahardika** | `2405551062` | Desain Algoritma & Tracing Matrix |
| 2 | **Ida Bagus Dalem Werda Adnyana** | `2505551131` | Validasi Input, Flow Control & Arsitektur CLI |
| 3 | **Tyo Putra Kharinata** | `2405551162` | Perancangan Pseudocode & Dokumentasi |
| 4 | **Cornel Asmara Noya Oleona** | `2505551164` | Visualisasi Flowchart & Pengujian Sistem |

---

## Gambaran Umum

`Route Finder` adalah aplikasi Command Line Interface (CLI) berbasis Python murni (*zero external dependencies*) yang mengimplementasikan **Algoritma Dijkstra** untuk mencari lintasan terpendek (*Single-Source Shortest Path*) pada graf berarah dan berbobot non-negatif.

Aplikasi ini dirancang dengan standar kode terstruktur (*procedural clean code*), pembersihan layar terminal yang konsisten, serta sistem validasi input defensif (*foolproof*) yang menjamin program tidak berhenti mendadak (*crash*) akibat kesalahan pengetikan pengguna. Selain menghitung rute optimal, aplikasi menyajikan **tabel tracing matriks pembaruan jarak langkah demi langkah** sebagaimana standar pengujian akademik di bangku perkuliahan.

---

## Fitur Utama

1. **Simulasi Rute Statis (Studi Kasus 6 Node: A ke E)**
   - Mengevaluasi graf acuan standar berbobot dengan 6 simpul (`A, B, C, D, E, F`).
   - Menyajikan log relaksasi per iterasi, matriks jarak kumulatif, dan rincian akumulasi bobot segmen per segmen.
2. **Kalkulator Rute Dinamis (Graf Kustom)**
   - Mengizinkan pembentukan graf secara mandiri dengan jumlah simpul antara 2 hingga 26 simpul (`A` sampai `Z`).
   - Input bobot sisi iteratif dengan mekanisme pintas: tekan `ENTER` atau ketik `0` jika dua simpul tidak memiliki jalur penghubung.
   - Pengecekan simpul asal (*Start*) dan tujuan (*End*) secara *case-insensitive*.
3. **Visualisasi Tabel Tracing Akademik**
   - Menampilkan status himpunan simpul permanen ($S$), penanda nilai permanen (`*`), relaksasi sementara dengan pencatatan simpul pendahulu `(pred)`, serta jarak tak terjangkau (`inf`).
4. **Validasi Input Defensif (*Foolproof*)**
   - Setiap masukan (pilihan menu, jumlah simpul, bobot sisi, nama simpul) dibungkus dalam loop `while True` dan blok penanganan eksepsi `try-except`.
   - Menolak nilai kosong, karakter non-numerik, nilai di luar rentang, dan bobot bernilai negatif ($w < 0$).
5. **Portabilitas Penuh & Kompatibilitas Encoding**
   - Menggunakan 100% pustaka bawaan (*Python Standard Library*).
   - Dilengkapi konfigurasi otomatis encoding output (`utf-8` fallback) agar tidak mengalami `UnicodeEncodeError` pada terminal Windows (*code page 1252 / 437*).

---

## Landasan Teori Algoritma

Algoritma Dijkstra bekerja dengan prinsip *greedy*: pada setiap iterasi, algoritma memilih simpul yang belum dikunjungi (*unvisited*) dengan estimasi jarak terpendek dari simpul asal, menjadikannya permanen, lalu melakukan **relaksasi** pada seluruh sisi tetangganya.

### 1. Formulasi Relaksasi Sisi
Diberikan graf terarah $G = (V, E)$ dengan fungsi bobot sisi non-negatif $w: E \to \mathbb{R}_{\ge 0}$. Untuk setiap simpul $u \in V$ yang sedang aktif dan tetangganya $v \in V$:

$$\text{Jika } d[u] + w(u, v) < d[v], \quad \text{maka } d[v] \leftarrow d[u] + w(u, v) \quad \text{dan} \quad \pi[v] \leftarrow u$$

Di mana:
- $d[v]$ adalah estimasi jarak terpendek saat ini dari simpul awal ke $v$.
- $\pi[v]$ (*predecessor*) adalah simpul pendahulu sebelum $v$ dalam rute terpendek.

### 2. Kompleksitas Algoritma
- **Kompleksitas Waktu:** $\mathcal{O}(|V|^2)$ pada representasi matriks/daftar ketetanggaan tanpa heap biner, atau $\mathcal{O}(|V| \log |V| + |E|)$ dengan prioritas antrean. Karena graf pada studi kasus berukuran sedang ($|V| \le 26$), pencarian linear simpul minimum memberikan waktu eksekusi instan ($< 1$ ms) dengan transparansi status tiap langkah yang sempurna.
- **Kompleksitas Ruang:** $\mathcal{O}(|V| + |E|)$ untuk menyimpan struktur daftar ketetanggaan (*adjacency dictionary*), vektor jarak, dan riwayat langkah (*trace records*).
- **Determinisme:** Pemilihan simpul jarak minimum saat terjadi nilai kembar (*tie*) diselesaikan secara alfabetis, menjamin hasil langkah iterasi selalu konsisten pada setiap pengujian.

---

## Struktur Repositori

```text
├── .gitignore               # Konfigurasi pengabaian file sampah & bytecode
├── Pseudocode.txt           # Dokumentasi pseudocode formal standar akademik
├── README.md                # Dokumentasi utama proyek
├── Route_Finder.py          # Kode sumber utama aplikasi CLI (Executable)
└── Rough_Flowchart.md       # Diagram alir visual terstruktur (Notasi Mermaid / Draw.io)
```

---

## Prasyarat Sistem

- **Sistem Operasi:** Windows 10/11, Linux (Ubuntu/Debian/Fedora), atau macOS.
- **Bahasa Pemrograman:** Python versi **3.10** ke atas (menggunakan fitur sintaksis `match-case` pada modul *routing* menu).
- **Pustaka Eksternal:** **Tidak ada** (Hanya menggunakan modul bawaan: `os`, `sys`, `typing`).

---

## Panduan Penggunaan

### 1. Kloning Repositori
Buka terminal / PowerShell dan jalankan perintah berikut:

```bash
git clone https://github.com/Luxionis/Router-Finder-Kecerdasan-Tiruan.git
cd Router-Finder-Kecerdasan-Tiruan
```

### 2. Menjalankan Aplikasi
Jalankan file program langsung melalui interpreter Python:

```bash
python Route_Finder.py
```

### 3. Navigasi Menu
Setelah aplikasi berjalan, antarmuka terminal akan menyajikan opsi berikut:
- Ketik `1` lalu tekan `ENTER` untuk menjalankan **Simulasi Rute Statis**.
- Ketik `2` lalu tekan `ENTER` untuk membuka **Kalkulator Rute Dinamis**.
- Ketik `3` lalu tekan `ENTER` untuk menampilkan **Profil & Identitas Kelompok**.
- Ketik `0` lalu tekan `ENTER` untuk **Keluar** dari aplikasi.

---

## Studi Kasus & Pembahasan Logika

### Topologi Graf Statis
Pada Mode 1 (Studi Kasus), didefinisikan sebuah graf berarah dengan himpunan simpul $V = \{A, B, C, D, E, F\}$ dan konfigurasi bobot sisi $E$ sebagai berikut:

- $A \to B = 4$
- $A \to C = 6$
- $B \to C = 2$
- $B \to D = 9$
- $B \to F = 2$
- $C \to D = 8$
- $D \to E = 9$
- $F \to B = 2$

### Hasil Komputasi
Pencarian rute terpendek dari simpul **A** menuju simpul **E** menghasilkan lintasan optimal:

$$\mathbf{A \to B \to D \to E}$$

Dengan total bobot: **22**

**Rincian akumulasi bobot lintasan:**
1. Segmen $A \to B$ : Bobot = $4$ (Akumulasi: $4$)
2. Segmen $B \to D$ : Bobot = $9$ (Akumulasi: $13$)
3. Segmen $D \to E$ : Bobot = $9$ (Akumulasi: $22$)

*(Sebagai perbandingan, rute alternatif $A \to C \to D \to E$ berjarak $6 + 8 + 9 = 23$, dan rute $A \to B \to C \to D \to E$ berjarak $4 + 2 + 8 + 9 = 23$).*

### Contoh Tabel Tracing
Berikut adalah cuplikan output matriks evaluasi jarak yang dihasilkan program pada setiap iterasi:

```text
================================================================================
         TABEL TRACING PEMBARUAN JARAK TERPENDEK (ALGORITMA DIJKSTRA)
================================================================================
-----------------------------------------------------------------------------------------------------------------------
| Langkah | Node Aktif     | Visited (S)            |    A     |    B     |    C     |    D     |    E     |    F     |
-----------------------------------------------------------------------------------------------------------------------
| L-0     | -              | {}                     |    0     |   inf    |   inf    |   inf    |   inf    |   inf    |
| L-1     | A              | {A}                    |    0*    |   4(A)   |   6(A)   |   inf    |   inf    |   inf    |
| L-2     | B              | {A, B}                 |    0*    |    4*    |   6(A)   |  13(B)   |   inf    |   6(B)   |
| L-3     | C              | {A, B, C}              |    0*    |    4*    |    6*    |  13(B)   |   inf    |   6(B)   |
| L-4     | F              | {A, B, C, F}           |    0*    |    4*    |    6*    |  13(B)   |   inf    |    6*    |
| L-5     | D              | {A, B, C, F, D}        |    0*    |    4*    |    6*    |   13*    |  22(D)   |    6*    |
| L-6     | E              | {A, B, C, F, D, E}     |    0*    |    4*    |    6*    |   13*    |   22*    |    6*    |
-----------------------------------------------------------------------------------------------------------------------
Keterangan Simbol:
  *    : Simpul telah masuk ke himpunan permanen S (jarak optimal terkonfirmasi).
 (X)   : Predecessor rute sementara yang melalui simpul X.
  inf  : Belum terjangkau dari simpul awal (jarak tak hingga).
```

---

## Ketahanan Sistem & Penanganan Kasus Khusus

Program telah diuji secara komprehensif terhadap berbagai kondisi batas (*edge cases*):

| Kondisi Kasus Batas | Penanganan oleh Program | Hasil / Respon Sistem |
|:---|:---|:---|
| **Titik Asal == Titik Tujuan** | Terdeteksi di awal sebelum iterasi | Mengembalikan rute `[Start]`, total bobot `0`, status sukses. |
| **Simpul Tujuan Tidak Terjangkau** | Deteksi sisa simpul bernilai `inf` | Status `UNREACHABLE`, rute `-`, total bobot `inf`. |
| **Input Bobot Negatif ($w < 0$)** | Pengecekan pada fungsi validasi sisi | Menolak input, memunculkan pesan error, meminta masukan ulang. |
| **Input Karakter pada Angka** | Blok `try-except ValueError` | Program tidak *crash*, menampilkan peringatan format bilangan bulat. |
| **Input String Kosong / Spasi** | Sanitasi `.strip()` & cek *null* | Meminta masukan ulang tanpa menghentikan eksekusi. |
| **Interupsi Terminal (Ctrl+C / EOF)** | Tangkap `KeyboardInterrupt` / `EOFError` | Keluar secara aman (*graceful degradation*) tanpa trace error kotor. |

---

## Dokumen Pendukung

Untuk analisis mendalam dan kelengkapan laporan, repositori ini menyertakan:
- **[`Pseudocode.txt`](Pseudocode.txt)**: Rincian notasi algoritma prosedural formal dari seluruh modul fungsi.
- **[`Rough_Flowchart.md`](Rough_Flowchart.md)**: Diagram alir alur kerja lengkap (bernotasi Mermaid yang kompatibel dengan Draw.io).

