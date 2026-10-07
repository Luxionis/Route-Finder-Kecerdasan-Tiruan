import os
import sys
from typing import Any, Dict, List, Optional, Set, Tuple

# Konfigurasi encoding stdout untuk kompatibilitas lintas terminal Windows & Unix
if sys.stdout.encoding and sys.stdout.encoding.lower() not in ("utf-8", "utf8"):
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass

WELCOMING_MENU_STR = """========================================================
        SELAMAT DATANG DI PROGRAM OPTIMASI RUTE
========================================================
Program ini dirancang untuk mencari rute terpendek antar
titik menggunakan Algoritma Dijkstra dengan validasi ketat.

Fitur-fitur utama:
  [1] Simulasi Rute Statis (Sesuai Studi Kasus A ke E)
  [2] Kalkulator Rute Dinamis (Input Titik Kustom)
  [3] Profil Kelompok
  [0] Keluar
========================================================"""

AUTHOR_MENU_STR = """========================================================
                 PROFIL & IDENTITAS AUTHOR
========================================================
  Mata Kuliah    : Kecerdasan Tiruan (I)
  Dosen Pengampu : I Nyoman Prayana Trisna, S.Kom., M.Cs.

  Kelompok 6:
  - Nyoman Gede Adi Mahardika    (2405551062)
  - Ida Bagus Dalem Werda Adnyana (2505551131)
  - Tyo Putra Kharinata          (2405551162)
  - Cornel Asmara Noya Oleona    (2505551164)
========================================================"""

GOODBYE_MENU_STR = """========================================================
       TERIMA KASIH TELAH MENGGUNAKAN PROGRAM KAMI
========================================================
Semoga kalkulator rute ini bermanfaat untuk Anda.
Sampai jumpa kembali!"""

# Data Graf Statis (Predefined 6-node Graph) sesuai studi kasus
# Simpul: A, B, C, D, E, F
# Bobot edge: A-B=4, A-C=6, B-C=2, B-D=9, B-F=2, C-D=8, D-E=9, F-B=2
HARDCODED_NODES: List[str] = ["A", "B", "C", "D", "E", "F"]
HARDCODED_GRAPH: Dict[str, Dict[str, int]] = {
    "A": {"B": 4, "C": 6},
    "B": {"C": 2, "D": 9, "F": 2},
    "C": {"D": 8},
    "D": {"E": 9},
    "E": {},
    "F": {"B": 2},
}

def clear_screen() -> None:
    """
    Membersihkan layar terminal console.
    Menggunakan perintah 'cls' untuk sistem operasi Windows (nt)
    dan 'clear' untuk sistem operasi berbasis Unix/Linux/macOS.
    """
    os.system("cls" if os.name == "nt" else "clear")


def pause_screen(prompt_text: str = "\nTekan [ENTER] untuk melanjutkan...") -> None:
    """
    Menghentikan eksekusi sementara hingga pengguna menekan tombol ENTER.
    Dilengkapi penanganan exception agar program tidak crash jika terjadi interupsi.

    Args:
        prompt_text (str): Pesan jeda yang ditampilkan kepada pengguna.
    """
    try:
        input(prompt_text)
    except (KeyboardInterrupt, EOFError):
        pass


# FUNGSI VALIDASI INPUT (FOOLPROOF VALIDATION)
def get_valid_menu_choice(allowed_choices: List[int]) -> int:
    """
    Meminta dan memvalidasi input pilihan menu dari pengguna.
    Menggunakan perulangan while True dan blok try-except untuk mencegah crash.

    Args:
        allowed_choices (List[int]): Daftar integer pilihan yang diperbolehkan.

    Returns:
        int: Nilai pilihan menu yang valid.
    """
    while True:
        try:
            raw_input = input("Pilih menu [0-3]: ").strip()
            if not raw_input:
                print("\n[ERROR] Pilihan tidak boleh kosong! Silakan masukkan angka.")
                continue
            choice = int(raw_input)
            if choice not in allowed_choices:
                allowed_str = ", ".join(str(c) for c in allowed_choices)
                print(f"\n[ERROR] Pilihan '{choice}' di luar jangkauan! Pilihan yang tersedia: [{allowed_str}].")
                continue
            return choice
        except ValueError:
            allowed_str = ", ".join(str(c) for c in allowed_choices)
            print(f"\n[ERROR] Input harus berupa bilangan bulat! Masukkan salah satu dari: [{allowed_str}].")
        except (KeyboardInterrupt, EOFError):
            print("\n\n[INFO] Input terinterupsi. Memilih keluar (0)...")
            return 0


def get_valid_integer(prompt_str: str, min_val: Optional[int] = None, max_val: Optional[int] = None) -> int:
    """
    Meminta dan memvalidasi input bilangan bulat dari pengguna dengan rentang tertentu.

    Args:
        prompt_str (str): Kalimat prompt yang ditampilkan.
        min_val (Optional[int]): Batas minimum yang diizinkan (inklusif).
        max_val (Optional[int]): Batas maksimum yang diizinkan (inklusif).

    Returns:
        int: Nilai bilangan bulat yang telah tervalidasi.
    """
    while True:
        try:
            raw_input = input(prompt_str).strip()
            if not raw_input:
                print("\n[ERROR] Input tidak boleh kosong! Silakan masukkan bilangan bulat.")
                continue
            val = int(raw_input)
            if min_val is not None and val < min_val:
                print(f"\n[ERROR] Nilai minimal yang diizinkan adalah {min_val}! Silakan coba lagi.")
                continue
            if max_val is not None and val > max_val:
                print(f"\n[ERROR] Nilai maksimal yang diizinkan adalah {max_val}! Silakan coba lagi.")
                continue
            return val
        except ValueError:
            print("\n[ERROR] Input harus berupa bilangan bulat (integer)! Huruf atau simbol tidak diizinkan.")
        except (KeyboardInterrupt, EOFError):
            print("\n\n[INFO] Input terinterupsi. Silakan masukkan nilai kembali.")


def get_valid_edge_weight(u: str, v: str) -> int:
    """
    Meminta bobot edge antara node u ke node v.
    Menolak bobot negatif. Jika menekan ENTER atau menginput '0', dianggap tidak terhubung (bobot 0).

    Args:
        u (str): Node sumber.
        v (str): Node tujuan.

    Returns:
        int: Nilai bobot edge (0 jika tidak ada koneksi, atau integer positif).
    """
    while True:
        try:
            prompt = f"  Bobot edge {u} -> {v} [ENTER/'0' jika tidak terhubung]: "
            raw_input = input(prompt).strip()
            if raw_input == "" or raw_input == "0":
                return 0
            val = int(raw_input)
            if val < 0:
                print(f"  [ERROR] Bobot tidak boleh negatif ({val})! Algoritma Dijkstra mensyaratkan bobot >= 0.")
                continue
            return val
        except ValueError:
            print("  [ERROR] Input tidak valid! Masukkan angka bulat non-negatif atau tekan ENTER/0.")
        except (KeyboardInterrupt, EOFError):
            print("\n  [INFO] Input terinterupsi. Silakan coba lagi.")


def get_valid_node(prompt_str: str, available_nodes: List[str]) -> str:
    """
    Meminta dan memvalidasi input nama node dari daftar node yang tersedia.
    Mendukung pengetikan case-insensitive (misal huruf kecil otomatis menjadi kapital).

    Args:
        prompt_str (str): Teks prompt yang ditampilkan ke pengguna.
        available_nodes (List[str]): Daftar nama node yang sah dalam graf.

    Returns:
        str: Nama node yang valid (uppercase).
    """
    nodes_str = ", ".join(available_nodes)
    while True:
        try:
            raw_input = input(prompt_str).strip().upper()
            if not raw_input:
                print(f"\n[ERROR] Input tidak boleh kosong! Node yang tersedia: {nodes_str}.")
                continue
            if raw_input not in available_nodes:
                print(f"\n[ERROR] Node '{raw_input}' tidak terdaftar! Pilih salah satu dari: {nodes_str}.")
                continue
            return raw_input
        except (KeyboardInterrupt, EOFError):
            print("\n\n[INFO] Input terinterupsi. Silakan pilih kembali.")


def generate_node_labels(num_nodes: int) -> List[str]:
    """
    Menghasilkan label nama node berupa huruf alfabet kapital (A, B, C, ...).

    Args:
        num_nodes (int): Jumlah node yang ingin digenerate (2-26).

    Returns:
        List[str]: List nama node (misal ['A', 'B', 'C', 'D']).
    """
    return [chr(ord("A") + i) for i in range(num_nodes)]


# IMPLEMENTASI ALGORITMA TRACING
def run_dijkstra(
    graph: Dict[str, Dict[str, int]],
    start_node: str,
    end_node: str,
    all_nodes: List[str]
) -> Dict[str, Any]:
    """
    Menjalankan Algoritma Dijkstra untuk mencari rute terpendek dan
    mencatat langkah demi langkah (step-by-step tracing) untuk pembuatan tabel.

    Args:
        graph (Dict[str, Dict[str, int]]): Representasi adjacency list graf.
        start_node (str): Node awal pencarian.
        end_node (str): Node tujuan pencarian.
        all_nodes (List[str]): Daftar seluruh node yang ada di dalam graf.

    Returns:
        Dict[str, Any]: Kamus berisi hasil rute terpendek, total bobot,
                        dan catatan tracing tiap langkah iterasi.
    """
    # Inisialisasi jarak ke semua node sebagai tak hingga (infinity)
    distances: Dict[str, float] = {node: float("inf") for node in all_nodes}
    # Inisialisasi predecessor (simpul pendahulu) untuk rekonstruksi rute
    predecessors: Dict[str, Optional[str]] = {node: None for node in all_nodes}
    
    # Jarak ke node awal adalah 0
    distances[start_node] = 0
    
    # Himpunan node yang belum dikunjungi (unvisited)
    unvisited: Set[str] = set(all_nodes)
    # Himpunan node yang telah permanen dikunjungi (S)
    visited_sequence: List[str] = []
    
    # List untuk menyimpan rekam jejak setiap iterasi (tracing table records)
    trace_records: List[Dict[str, Any]] = []

    # Penanganan edge case jika start_node == end_node
    if start_node == end_node:
        trace_records.append({
            "step": 0,
            "selected_node": start_node,
            "visited_set": [start_node],
            "distances": distances.copy(),
            "predecessors": predecessors.copy(),
            "relaxations": ["Titik asal sama dengan titik tujuan (Jarak = 0)"]
        })
        return {
            "path": [start_node],
            "total_distance": 0,
            "trace_records": trace_records,
            "final_distances": distances,
            "predecessors": predecessors,
            "is_found": True
        }

    # Snapshot Langkah 0: Inisialisasi Awal
    trace_records.append({
        "step": 0,
        "selected_node": "-",
        "visited_set": [],
        "distances": distances.copy(),
        "predecessors": predecessors.copy(),
        "relaxations": [f"Inisialisasi jarak awal: Node {start_node} = 0, Node lainnya = inf"]
    })

    step_counter = 0

    # Perulangan utama Dijkstra
    while unvisited:
        # Cari node dalam unvisited dengan jarak terkecil
        # Gunakan tie-breaker alfabetis (distances[node], node) untuk determinisme
        candidates = [(distances[node], node) for node in unvisited]
        min_dist, current_node = min(candidates, key=lambda x: (x[0], x[1]))

        # Jika jarak terkecil adalah tak hingga, berarti sisa node tidak terjangkau
        if min_dist == float("inf"):
            break

        step_counter += 1
        unvisited.remove(current_node)
        visited_sequence.append(current_node)

        relaxation_notes: List[str] = []

        # Relaksasi sisi-sisi (edges) tetangga yang terhubung dari current_node
        neighbors = graph.get(current_node, {})
        for neighbor, weight in sorted(neighbors.items()):
            if neighbor in unvisited:
                tentative_dist = distances[current_node] + weight
                if tentative_dist < distances[neighbor]:
                    old_dist_str = "inf" if distances[neighbor] == float("inf") else str(distances[neighbor])
                    distances[neighbor] = tentative_dist
                    predecessors[neighbor] = current_node
                    relaxation_notes.append(
                        f"Relaksasi ke {neighbor}: {old_dist_str} -> {tentative_dist} (via {current_node})"
                    )
                else:
                    relaxation_notes.append(
                        f"Relaksasi ke {neighbor}: {tentative_dist} >= {distances[neighbor]} (tetap {distances[neighbor]})"
                    )
            elif neighbor in visited_sequence:
                relaxation_notes.append(
                    f"Pemeriksaan ke {neighbor}: Sudah permanen di himpunan S (dilewati)"
                )

        if not neighbors:
            relaxation_notes.append(f"Node {current_node} tidak memiliki sisi keluar.")

        # Rekam status langkah iterasi ini
        trace_records.append({
            "step": step_counter,
            "selected_node": current_node,
            "visited_set": list(visited_sequence),
            "distances": distances.copy(),
            "predecessors": predecessors.copy(),
            "relaxations": relaxation_notes
        })

        # Jika node tujuan telah dikunjungi dan dipastikan optimal, hentikan pencarian
        if current_node == end_node:
            break

    # Rekonstruksi rute terpendek dari predecessor
    is_found = distances[end_node] != float("inf")
    path: List[str] = []
    
    if is_found:
        curr: Optional[str] = end_node
        while curr is not None:
            path.append(curr)
            curr = predecessors[curr]
        path.reverse()
        total_distance = distances[end_node]
    else:
        path = []
        total_distance = float("inf")

    return {
        "path": path,
        "total_distance": total_distance,
        "trace_records": trace_records,
        "final_distances": distances,
        "predecessors": predecessors,
        "is_found": is_found
    }


# FUNGSI VISUALISASI HASIL & TABEL TRACING
def display_tracing_table(trace_records: List[Dict[str, Any]], all_nodes: List[str]) -> None:
    """
    Menampilkan tabel matriks tracing langkah demi langkah Algoritma Dijkstra
    sesuai standar format pengujian akademik.

    Args:
        trace_records (List[Dict[str, Any]]): Rekaman tiap langkah iterasi.
        all_nodes (List[str]): Daftar semua node pada graf.
    """
    print("\n" + "=" * 80)
    print("         TABEL TRACING PEMBARUAN JARAK TERPENDEK (ALGORITMA DIJKSTRA)")
    print("=" * 80)

    # Menentukan lebar kolom
    col_step = 6
    col_node = 14
    col_visited = max(20, min(30, len(all_nodes) * 3 + 4))
    node_col_width = 8

    # Header Tabel
    header = (
        f"| {'Langkah':<{col_step}} "
        f"| {'Node Aktif':<{col_node}} "
        f"| {'Visited (S)':<{col_visited}} |"
    )
    for n in all_nodes:
        header += f" {n:^{node_col_width}} |"
    
    separator = "-" * len(header)
    print(separator)
    print(header)
    print(separator)

    # Baris data per iterasi
    for record in trace_records:
        step_str = f"L-{record['step']}"
        selected = record["selected_node"]
        visited_nodes = record["visited_set"]
        visited_str = "{" + ", ".join(visited_nodes) + "}"
        if len(visited_str) > col_visited:
            visited_str = visited_str[: col_visited - 3] + "..."

        row_str = (
            f"| {step_str:<{col_step}} "
            f"| {selected:<{col_node}} "
            f"| {visited_str:<{col_visited}} |"
        )

        for n in all_nodes:
            d = record["distances"][n]
            pred = record["predecessors"][n]
            is_perm = n in visited_nodes

            if d == float("inf"):
                val_str = "inf"
            else:
                d_int = int(d) if d.is_integer() else d
                if pred is not None and not is_perm:
                    val_str = f"{d_int}({pred})"
                elif is_perm:
                    val_str = f"{d_int}*"
                else:
                    val_str = f"{d_int}"

            row_str += f" {val_str:^{node_col_width}} |"

        print(row_str)

    print(separator)
    print("Keterangan Simbol Tabel:")
    print("  *    : Node telah menjadi anggota himpunan S (jarak berstatus permanen/optimal).")
    print(" (X)   : Simpul pendahulu (predecessor) rute sementara melalui node X.")
    print("  inf  : Jarak tak hingga (node belum dapat dijangkau dari titik awal).")
    print("=" * 80)

    # Menampilkan rincian relaksasi setiap langkah
    print("\nRINCIAN LOG PROSES RELAKSASI TIAP LANGKAH:")
    print("-" * 80)
    for record in trace_records:
        step_title = f"Langkah {record['step']} (Node: {record['selected_node']})"
        print(f"[{step_title}]")
        for note in record["relaxations"]:
            print(f"  * {note}")
    print("-" * 80)


def display_path_result(
    start_node: str,
    end_node: str,
    path: List[str],
    total_distance: float,
    graph: Dict[str, Dict[str, int]]
) -> None:
    """
    Menampilkan kesimpulan hasil akhir pencarian rute terpendek dan rincian per segmen jalur.

    Args:
        start_node (str): Node awal.
        end_node (str): Node tujuan.
        path (List[str]): Urutan node rute terpendek.
        total_distance (float): Total bobot/jarak rute.
        graph (Dict[str, Dict[str, int]]): Adjacency list graf untuk lookup bobot edge.
    """
    print("\n" + "=" * 80)
    print("                       HASIL AKHIR PENCARIAN RUTE")
    print("=" * 80)
    print(f"  Titik Awal (Start)       : {start_node}")
    print(f"  Titik Tujuan (End)       : {end_node}")

    # Edge Case: Start sama dengan End
    if start_node == end_node:
        print(f"  Status                   : SUKSES (Titik Awal == Titik Tujuan)")
        print(f"  Rute Terpendek           : {start_node}")
        print(f"  Total Bobot / Jarak      : 0")
        print(f"  Catatan                  : Titik asal dan tujuan adalah simpul yang sama.")
        print("=" * 80)
        return

    # Edge Case: Rute tidak ditemukan
    if total_distance == float("inf") or not path:
        print(f"  Status                   : TIDAK DITEMUKAN RUTE (UNREACHABLE)")
        print(f"  Rute Terpendek           : -")
        print(f"  Total Bobot / Jarak      : inf (Tak Terhingga)")
        print(f"  Catatan                  : Tidak ada lintasan yang menghubungkan node '{start_node}' ke '{end_node}'.")
        print("=" * 80)
        return

    # Rute berhasil ditemukan
    path_str = " -> ".join(path)
    total_int = int(total_distance) if total_distance.is_integer() else total_distance
    print(f"  Status                   : SUKSES DITEMUKAN")
    print(f"  Rute Terpendek           : {path_str}")
    print(f"  Total Bobot / Jarak      : {total_int}")
    print("\n  Rincian Lintasan Segmen per Segmen:")
    
    cumulative_cost = 0
    for idx in range(len(path) - 1):
        u = path[idx]
        v = path[idx + 1]
        weight = graph.get(u, {}).get(v, 0)
        cumulative_cost += weight
        print(f"    Segmen {idx + 1}: {u} -> {v}  |  Bobot = {weight:<3}  |  Akumulasi Jarak = {cumulative_cost}")

    print("=" * 80)


def display_graph_summary(graph: Dict[str, Dict[str, int]], all_nodes: List[str]) -> None:
    """
    Menampilkan matriks bobot dan daftar relasi graf yang telah diinput pengguna.

    Args:
        graph (Dict[str, Dict[str, int]]): Graf dalam format adjacency list.
        all_nodes (List[str]): Seluruh node dalam graf.
    """
    print("\n" + "=" * 60)
    print("           RINGKASAN STRUKTUR GRAF & BOBOT")
    print("=" * 60)
    print("Daftar Hubungan Berbobot:")
    edge_count = 0
    for u in all_nodes:
        connections = graph.get(u, {})
        for v, w in sorted(connections.items()):
            print(f"  * {u} -> {v} : Bobot = {w}")
            edge_count += 1
    if edge_count == 0:
        print("  (Tidak ada koneksi/edge antar node yang terhubung)")
    print(f"Total Simpul (Nodes): {len(all_nodes)} | Total Busur (Edges): {edge_count}")
    print("=" * 60)


# FUNGSI MENU & ROUTING
def show_welcoming_menu() -> None:
    """Menampilkan Welcoming Menu ke layar terminal."""
    print(WELCOMING_MENU_STR)


def show_main_menu() -> None:
    """Menampilkan Main Menu dengan membersihkan layar terlebih dahulu."""
    clear_screen()
    show_welcoming_menu()


def show_menu() -> None:
    """Alias dari show_main_menu() sesuai dengan konvensi penamaan fungsi."""
    show_main_menu()


def show_author_menu() -> None:
    """Menampilkan Author / Identity Menu ke layar terminal."""
    clear_screen()
    print(AUTHOR_MENU_STR)
    pause_screen()


def show_goodbye_menu() -> None:
    """Menampilkan Goodbye Menu saat keluar dari aplikasi."""
    clear_screen()
    print(GOODBYE_MENU_STR)


def run_hardcoded_simulation() -> None:
    """
    Menjalankan Use Case 1: Simulasi Rute Statis dari node A ke node E
    berdasarkan graf 6 node (A, B, C, D, E, F) yang telah ditentukan.
    """
    clear_screen()
    print("=" * 80)
    print("       USE CASE 1: SIMULASI RUTE STATIS (STUDI KASUS PREDEFINED A KE E)")
    print("=" * 80)
    print("Deskripsi Permasalahan:")
    print("  Diberikan sebuah graf 6 simpul (A, B, C, D, E, F) dengan bobot relasi berikut:")
    print("    * A -> B = 4 | A -> C = 6")
    print("    * B -> C = 2 | B -> D = 9 | B -> F = 2")
    print("    * C -> D = 8")
    print("    * D -> E = 9")
    print("    * F -> B = 2")
    print("\n  Target Simulasi: Mencari rute optimal dari Node 'A' ke Node 'E'.")
    print("=" * 80)

    # Eksekusi Algoritma Dijkstra
    result = run_dijkstra(
        graph=HARDCODED_GRAPH,
        start_node="A",
        end_node="E",
        all_nodes=HARDCODED_NODES
    )

    # Tampilkan Tabel Tracing dan Hasil
    display_tracing_table(result["trace_records"], HARDCODED_NODES)
    display_path_result(
        start_node="A",
        end_node="E",
        path=result["path"],
        total_distance=result["total_distance"],
        graph=HARDCODED_GRAPH
    )

    pause_screen()


def run_dynamic_calculator() -> None:
    """
    Menjalankan Use Case 2: Kalkulator Rute Dinamis dengan input simpul kustom,
    input matriks bobot antar simpul, penentuan titik awal dan akhir,
    serta komputasi rute Dijkstra dengan visualisasi tabel tracing.
    """
    clear_screen()
    print("=" * 80)
    print("          USE CASE 2: KALKULATOR RUTE DINAMIS (KUSTOMISASI GRAF)")
    print("=" * 80)
    print("Langkah 1: Masukkan jumlah simpul (node) yang ingin dibuat.")
    print("           Contoh: Input 4 akan otomatis menghasilkan simpul A, B, C, D.")
    print("-" * 80)

    # Validasi jumlah node (minimal 2 simpul, maksimal 26 simpul A-Z)
    num_nodes = get_valid_integer(
        prompt_str="Masukkan jumlah node (2 - 26): ",
        min_val=2,
        max_val=26
    )

    custom_nodes = generate_node_labels(num_nodes)
    print(f"\n[INFO] Simpul yang berhasil dibuat ({num_nodes}): {', '.join(custom_nodes)}")

    print("\n" + "-" * 80)
    print("Langkah 2: Masukkan bobot sisi (edge) antar semua pasangan simpul.")
    print("           Tekan tombol ENTER atau masukkan '0' jika dua simpul tidak terhubung.")
    print("           Bobot harus berupa bilangan bulat positif (>= 0).")
    print("-" * 80)

    # Inisialisasi adjacency dictionary untuk graf dinamis
    custom_graph: Dict[str, Dict[str, int]] = {node: {} for node in custom_nodes}

    # Iterasi meminta input bobot untuk seluruh pasangan simpul (u -> v, u != v)
    for u in custom_nodes:
        print(f"\n>> Konfigurasi edge keluar dari Node [{u}]:")
        for v in custom_nodes:
            if u == v:
                continue
            weight = get_valid_edge_weight(u, v)
            if weight > 0:
                custom_graph[u][v] = weight

    # Tampilkan ringkasan graf yang berhasil dibentuk
    clear_screen()
    print("=" * 80)
    print("                     GRAF DINAMIS BERHASIL DIBENTUK")
    print("=" * 80)
    display_graph_summary(custom_graph, custom_nodes)

    print("\nLangkah 3: Tentukan Titik Awal (Start Node) dan Titik Tujuan (End Node).")
    print("-" * 80)
    start_node = get_valid_node(
        prompt_str=f"Masukkan Titik Awal ({', '.join(custom_nodes)}): ",
        available_nodes=custom_nodes
    )
    end_node = get_valid_node(
        prompt_str=f"Masukkan Titik Tujuan ({', '.join(custom_nodes)}): ",
        available_nodes=custom_nodes
    )

    # Eksekusi Algoritma Dijkstra pada Graf Dinamis
    result = run_dijkstra(
        graph=custom_graph,
        start_node=start_node,
        end_node=end_node,
        all_nodes=custom_nodes
    )

    # Tampilkan Tabel Tracing dan Hasil Akhir
    display_tracing_table(result["trace_records"], custom_nodes)
    display_path_result(
        start_node=start_node,
        end_node=end_node,
        path=result["path"],
        total_distance=result["total_distance"],
        graph=custom_graph
    )

    pause_screen()


# ENTRY POINT UTAMA APLIKASI
def main() -> None:
    """
    Fungsi kontrol utama program CLI yang mengelola siklus menu
    dan memanfaatkan match-case statement (Python 3.10+) untuk routing.
    """
    while True:
        show_main_menu()
        choice = get_valid_menu_choice([1, 2, 3, 0])

        # Flow control menggunakan fitur match-case (Python 3.10+)
        match choice:
            case 1:
                run_hardcoded_simulation()
            case 2:
                run_dynamic_calculator()
            case 3:
                show_author_menu()
            case 0:
                show_goodbye_menu()
                break
            case _:
                print("\n[ERROR] Pilihan menu tidak valid!")
                pause_screen()


if __name__ == "__main__":
    main()