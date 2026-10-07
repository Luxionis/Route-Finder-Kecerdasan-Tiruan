# DOKUMEN ROUGH FLOWCHART PROGRAM OPTIMASI RUTE (ALGORITMA DIJKSTRA)
**File Sumber:** `Route_Finder.py`  
**Mata Kuliah:** Kecerdasan Tiruan (I)  
**Dosen Pengampu:** I Nyoman Prayana Trisna, S.Kom., M.Cs.  
**Kelompok 6:**
- Nyoman Gede Adi Mahardika (2405551062)
- Ida Bagus Dalem Werda Adnyana (2505551131)
- Tyo Putra Kharinata (2405551162)
- Cornel Asmara Noya Oleona (2505551164)

---

## 1. Flowchart Utama Program (`main()`)

Flowchart ini menggambarkan siklus hidup aplikasi utama dari mulai inisialisasi, pembersihan terminal, tampilan menu interaktif, seleksi opsi (*match-case*), hingga terminasi program.

```mermaid
flowchart TD
    classDef startEnd fill:#d4edda,stroke:#28a745,stroke-width:2px,color:#155724;
    classDef process fill:#d1ecf1,stroke:#17a2b8,stroke-width:2px,color:#0c5460;
    classDef decision fill:#fff3cd,stroke:#ffc107,stroke-width:2px,color:#856404;
    classDef io fill:#e2e3e5,stroke:#6c757d,stroke-width:2px,color:#383d41;
    classDef subproc fill:#e7daff,stroke:#6f42c1,stroke-width:2px,color:#321f59;

    Start([Mulai / Program Start]):::startEnd --> Init[Inisialisasi Encoding & Definisi Konstanta Graf Statis]:::process
    Init --> ClearScreen[Bersihkan Layar / clear_screen]:::process
    ClearScreen --> DisplayMenu[/"Tampilkan Welcoming / Main Menu"/]:::io
    DisplayMenu --> InputMenu[/"Input Pilihan Menu [0-3]"/]:::io
    InputMenu --> ValidateChoice{"Validasi Input Integer [0, 1, 2, 3]?"}:::decision

    ValidateChoice -- "Tidak Valid (Error)" --> ShowErrMenu[/"Tampilkan Pesan Error Validasi"/]:::io
    ShowErrMenu --> InputMenu

    ValidateChoice -- "Valid" --> MatchCase{"Pilihan Menu (Match-Case)"}:::decision

    MatchCase -- "Opsi 1" --> CallUC1[["Panggil: run_hardcoded_simulation()"]]:::subproc
    MatchCase -- "Opsi 2" --> CallUC2[["Panggil: run_dynamic_calculator()"]]:::subproc
    MatchCase -- "Opsi 3" --> CallUC3[["Panggil: show_author_menu()"]]:::subproc
    MatchCase -- "Opsi 0" --> CallExit[["Panggil: show_goodbye_menu()"]]:::subproc

    CallUC1 --> PauseMain[/"Tekan ENTER untuk Lanjut / pause_screen()"/]:::io
    CallUC2 --> PauseMain
    CallUC3 --> PauseMain

    PauseMain --> ClearScreen

    CallExit --> Terminate([Selesai / Exit]):::startEnd
```

---

## 2. Flowchart Sub-Proses: Use Case 1 (Simulasi Graf Statis)

Menggambarkan eksekusi otomatis pencarian rute terpendek dari simpul **A** ke simpul **E** menggunakan graf *predefined* 6 simpul: `A, B, C, D, E, F`.

```mermaid
flowchart TD
    classDef startEnd fill:#d4edda,stroke:#28a745,stroke-width:2px,color:#155724;
    classDef process fill:#d1ecf1,stroke:#17a2b8,stroke-width:2px,color:#0c5460;
    classDef decision fill:#fff3cd,stroke:#ffc107,stroke-width:2px,color:#856404;
    classDef io fill:#e2e3e5,stroke:#6c757d,stroke-width:2px,color:#383d41;
    classDef subproc fill:#e7daff,stroke:#6f42c1,stroke-width:2px,color:#321f59;

    Sub1Start([Mulai: run_hardcoded_simulation]):::startEnd --> ClearScr1[Bersihkan Layar Terminal]:::process
    ClearScr1 --> DisplayInfo1[/"Tampilkan Info Studi Kasus & Bobot Sisi Statis"/]:::io
    DisplayInfo1 --> LoadStatic["Load HARDCODED_GRAPH & Titik Awal: 'A', Titik Tujuan: 'E'"]:::process
    LoadStatic --> ExecDijkstra1[["Eksekusi: run_dijkstra(graph, 'A', 'E', nodes)"]]:::subproc
    ExecDijkstra1 --> ShowTable1[/"Cetak Tabel Tracing Langkah demi Langkah"/]:::io
    ShowTable1 --> ShowResult1[/"Cetak Hasil Akhir: Rute Terpendek & Rincian Segmen"/]:::io
    ShowResult1 --> Sub1End([Kembali ke Menu Utama]):::startEnd
```

---

## 3. Flowchart Sub-Proses: Use Case 2 (Kalkulator Rute Dinamis)

Menggambarkan alur interaktif saat pengguna menginput jumlah simpul, matriks bobot sisi keluar per simpul, penentuan simpul awal dan akhir, hingga kalkulasi Dijkstra.

```mermaid
flowchart TD
    classDef startEnd fill:#d4edda,stroke:#28a745,stroke-width:2px,color:#155724;
    classDef process fill:#d1ecf1,stroke:#17a2b8,stroke-width:2px,color:#0c5460;
    classDef decision fill:#fff3cd,stroke:#ffc107,stroke-width:2px,color:#856404;
    classDef io fill:#e2e3e5,stroke:#6c757d,stroke-width:2px,color:#383d41;
    classDef subproc fill:#e7daff,stroke:#6f42c1,stroke-width:2px,color:#321f59;

    Sub2Start([Mulai: run_dynamic_calculator]):::startEnd --> ClearScr2[Bersihkan Layar Terminal]:::process
    ClearScr2 --> InputN[/"Input Jumlah Simpul N (2 - 26)"/]:::io
    InputN --> CheckN{"Valid Integer & 2 <= N <= 26?"}:::decision
    CheckN -- "Tidak" --> ErrN[/"Tampilkan Pesan Error Jumlah Simpul"/]:::io --> InputN
    CheckN -- "Ya" --> GenLabels["Generate Label Simpul: A, B, C, ... sebanyak N"]:::process

    GenLabels --> InitGraph["Inisialisasi Adjacency List Kosong: custom_graph"]:::process

    InitGraph --> LoopU{"Untuk Setiap Node u dalam nodes"}:::decision
    LoopU -- "Selesai Semua Node" --> ShowSummary[/"Tampilkan Ringkasan Struktur Graf (display_graph_summary)"/]:::io

    LoopU -- "Node u Aktif" --> LoopV{"Untuk Setiap Node v != u"}:::decision
    LoopV -- "Selesai Semua v" --> LoopU

    LoopV -- "Pasangan (u, v)" --> InputW[/"Input Bobot Sisi u -> v (ENTER / '0' jika tidak ada koneksi)"/]:::io
    InputW --> CheckW{"Valid non-negatif integer (>= 0)?"}:::decision
    CheckW -- "Tidak (Negatif / Huruf)" --> ErrW[/"Tampilkan Pesan Error Bobot"/]:::io --> InputW
    CheckW -- "Ya: Bobot > 0" --> SaveEdge["Simpan: custom_graph[u][v] = bobot"]:::process --> LoopV
    CheckW -- "Ya: Bobot == 0 / ENTER" --> SkipEdge["Abaikan Sisi (Tidak Terhubung)"]:::process --> LoopV

    ShowSummary --> InputStart[/"Input Titik Awal (Start Node)"/]:::io
    InputStart --> CheckStart{"Node ada dalam daftar simpul?"}:::decision
    CheckStart -- "Tidak" --> ErrStart[/"Error: Simpul tidak ditemukan"/]:::io --> InputStart
    CheckStart -- "Ya" --> InputEnd[/"Input Titik Tujuan (End Node)"/]:::io

    InputEnd --> CheckEnd{"Node ada dalam daftar simpul?"}:::decision
    CheckEnd -- "Tidak" --> ErrEnd[/"Error: Simpul tidak ditemukan"/]:::io --> InputEnd
    CheckEnd -- "Ya" --> ExecDijkstra2[["Eksekusi: run_dijkstra(custom_graph, start, end, nodes)"]]:::subproc

    ExecDijkstra2 --> ShowTable2[/"Cetak Tabel Tracing Langkah demi Langkah"/]:::io
    ShowTable2 --> ShowResult2[/"Cetak Hasil Akhir & Rincian Rute"/]:::io
    ShowResult2 --> Sub2End([Kembali ke Menu Utama]):::startEnd
```

---

## 4. Flowchart Detail: Algoritma Dijkstra & Tracing (`run_dijkstra`)

Flowchart ini memodelkan logika komputasi inti Dijkstra, pengelolaan himpunan *unvisited/visited*, relaksasi tetangga, pencatatan jejak langkah (*tracing table*), hingga rekonstruksi rute mundur melalui *predecessor*.

```mermaid
flowchart TD
    classDef startEnd fill:#d4edda,stroke:#28a745,stroke-width:2px,color:#155724;
    classDef process fill:#d1ecf1,stroke:#17a2b8,stroke-width:2px,color:#0c5460;
    classDef decision fill:#fff3cd,stroke:#ffc107,stroke-width:2px,color:#856404;
    classDef io fill:#e2e3e5,stroke:#6c757d,stroke-width:2px,color:#383d41;
    classDef subproc fill:#e7daff,stroke:#6f42c1,stroke-width:2px,color:#321f59;

    DijkStart([Mulai: run_dijkstra]):::startEnd --> InitVectors["Inisialisasi distances[all] = inf<br>predecessors[all] = None<br>distances[start] = 0<br>unvisited = all_nodes<br>visited_sequence = []"]:::process

    InitVectors --> CheckSameStart{"Apakah start_node == end_node?"}:::decision
    CheckSameStart -- "Ya (Edge Case)" --> RetSame["Catat Langkah 0 (Jarak = 0)<br>path = [start_node]<br>total_distance = 0"]:::process --> ReturnResult([Return Hasil & Tracing]):::startEnd

    CheckSameStart -- "Tidak" --> LogStep0["Catat Langkah 0 (Inisialisasi ke trace_records)"]:::process
    LogStep0 --> LoopUnvisited{"Apakah unvisited masih memiliki elemen?"}:::decision

    LoopUnvisited -- "Kosong" --> Reconstruct["Rekonstruksi Lintasan Mundur"]:::process

    LoopUnvisited -- "Masih Ada Elemen" --> FindMin["Cari node dalam unvisited dengan distances[node] terkecil<br>(Tie-breaker alfabetis)"]:::process
    FindMin --> CheckReach{"Apakah min_dist == inf?"}:::decision
    CheckReach -- "Ya (Sisa node tak terjangkau)" --> Reconstruct

    CheckReach -- "Tidak" --> MarkVisited["current_node = node terpilih<br>Hapus current_node dari unvisited<br>Tambahkan current_node ke visited_sequence"]:::process

    MarkVisited --> NeighborLoop{"Untuk setiap (neighbor, weight) keluar dari current_node"}:::decision

    NeighborLoop -- "Tetangga dalam unvisited" --> CalcTentative["tentative_dist = distances[current_node] + weight"]:::process
    CalcTentative --> CheckRelax{"Apakah tentative_dist < distances[neighbor]?"}:::decision
    CheckRelax -- "Ya" --> RelaxUpdate["distances[neighbor] = tentative_dist<br>predecessors[neighbor] = current_node<br>Catat Log: Nilai Diperbarui"]:::process --> NeighborLoop
    CheckRelax -- "Tidak" --> RelaxKeep["Catat Log: Nilai Tetap (>=)"]:::process --> NeighborLoop

    NeighborLoop -- "Tetangga sudah di visited (S)" --> SkipPerm["Catat Log: Sudah permanen (Dilewati)"]:::process --> NeighborLoop

    NeighborLoop -- "Selesai Semua Tetangga" --> RecordTrace["Simpan Snapshot ke trace_records:<br>(Langkah, Node Aktif, Visited S, Vektor Jarak, Catatan Relaksasi)"]:::process

    RecordTrace --> CheckGoal{"Apakah current_node == end_node?"}:::decision
    CheckGoal -- "Ya (Target Tercapai)" --> Reconstruct
    CheckGoal -- "Tidak" --> LoopUnvisited

    Reconstruct --> CheckFound{"Apakah distances[end_node] != inf?"}:::decision
    CheckFound -- "Ya (Rute Ditemukan)" --> TraceBack["Telusuri predecessors dari end_node ke start_node<br>Balikkan list lintasan (Reverse path)<br>total_distance = distances[end_node]"]:::process --> ReturnResult
    CheckFound -- "Tidak (Unreachable)" --> SetUnreached["path = []<br>total_distance = inf<br>is_found = False"]:::process --> ReturnResult
```

---

## 5. Flowchart Validasi Input Foolproof (`try-except` Pattern)

Menggambarkan arsitektur pertahanan program agar kebal terhadap kesalahan ketik (*anti-crash*).

```mermaid
flowchart TD
    classDef startEnd fill:#d4edda,stroke:#28a745,stroke-width:2px,color:#155724;
    classDef process fill:#d1ecf1,stroke:#17a2b8,stroke-width:2px,color:#0c5460;
    classDef decision fill:#fff3cd,stroke:#ffc107,stroke-width:2px,color:#856404;
    classDef io fill:#e2e3e5,stroke:#6c757d,stroke-width:2px,color:#383d41;

    ValStart([Mulai: Blok Input]):::startEnd --> LoopWhile["Perulangan while True:"]:::process
    LoopWhile --> TryBlock["Blok try: Baca input string mentah"]:::process
    TryBlock --> CheckEmpty{"Apakah string kosong?"}:::decision
    CheckEmpty -- "Ya" --> ErrEmpty[/"Cetak Error: Input tidak boleh kosong"/]:::io --> LoopWhile
    CheckEmpty -- "Tidak" --> ParseInt["Konversi tipe data ke integer"]:::process

    ParseInt --> CheckBounds{"Apakah dalam batas valid (min & max)?"}:::decision
    CheckBounds -- "Di luar rentang" --> ErrBounds[/"Cetak Error: Nilai di luar rentang"/]:::io --> LoopWhile
    CheckBounds -- "Sesuai rentang" --> ReturnVal([Return Nilai Valid]):::startEnd

    ParseInt -. "Gagal konversi (ValueError)" .-> CatchVal["Blok except ValueError:"]:::process
    CatchVal --> ErrType[/"Cetak Error: Input harus berupa angka bulat"/]:::io --> LoopWhile

    TryBlock -. "Interupsi Ctrl+C / EOF" .-> CatchInterrupt["Blok except (KeyboardInterrupt, EOFError):"]:::process
    CatchInterrupt --> HandleInterrupt[/"Cetak Info: Operasi dibatalkan/default value"/]:::io --> ReturnVal
```

---

## 6. Tabel Referensi Simbol Standar (Draw.io Notation)

| Simbol Bentuk (Draw.io) | Notasi Mermaid | Nama Standar | Fungsi dalam Program |
| :--- | :--- | :--- | :--- |
| **Oval / Pill** | `([Text])` | *Terminator* | Menandai titik awal (*Start*) dan akhir (*End/Return*) suatu alur fungsi. |
| **Persegi Panjang** | `[Text]` | *Process* | Operasi inisialisasi, komputasi variabel, relaksasi jarak, atau pembaruan status. |
| **Belah Ketupat** | `{"Text?"}` | *Decision* | Percabangan logika kondisi (`if-else`, `match-case`, batas nilai, dan pengecekan elemen). |
| **Jajaran Genjang** | `[/"Text"/]` | *Input / Output* | Interaksi pengguna terminal: pembacaan input keyboard dan pencetakan tabel/string. |
| **Persegi Berlapis** | `[["Text"]]` | *Subroutine / Predefined Process* | Pemanggilan fungsi modular eksternal (misal pemanggilan algoritma Dijkstra). |

---
*Dokumen ini disusun untuk mempermudah pemetaan visual ke dalam aplikasi diagram seperti Draw.io, Lucidchart, atau Microsoft Visio.*

