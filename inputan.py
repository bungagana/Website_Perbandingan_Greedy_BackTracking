#===================== IDENTITAS DEVELOPER =====================
# NAMA : BUNGA LAELATUL MUNA 
# NIM  : 21102010
#===============================================================

#--------------------- LIBRARY ---------------------------------
import streamlit as st
import random
from streamlit_option_menu import option_menu
import networkx as nx
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from graphviz import Digraph
import numpy as np
import time

#### ----- NAVIGATION BAR ---- ####
selected = option_menu(
    menu_title="Perbandingan Algoritma Shortest Path",
    options=["Greedy",  "Backtracking", "Inputan"],
    orientation="horizontal",  # Mengubah orientasi menu menjadi vertikal
    styles={
        "container": {"padding": "0!important", "background-color": "black"},
        "nav-link": {
            "font-size": "15px",
            "font-colour": "white",
            "text-align": "center",
            "margin": "0px",
            "--hover-color": "#eeeee",
        },
        "nav-link-selected": {"background-color": "#696666"},
    },
)

#### ----- SECTION HOME ---- ####
if selected == "Greedy":
    # Definisi matriks jarak antar ruangan
    jarak = [
        [0, 5, 7, 3, float('inf')],  # A: [A, B, C, D, E]
        [5, 0, 4, float('inf'), 3],  # B: [A, B, C, D, E]
        [7, 4, 0, float('inf'), 5],  # C: [A, B, C, D, E]
        [3, float('inf'), float('inf'), 0, 4],  # D: [A, B, C, D, E]
        [float('inf'), float('inf'), 5, 4, 0]  # E: [A, B, C, D, E]
    ]

    # Fungsi untuk memilih ruangan selanjutnya berdasarkan jarak terdekat
    def pilih_ruangan_greedy(ruangan_sekarang, ruangan_tersedia):
        jarak_minimal = float('inf')
        ruangan_selanjutnya = None

        for ruangan in ruangan_tersedia:
            jarak_ruangan = jarak[ruangan_sekarang][ruangan]
            if jarak_ruangan is not None and jarak_ruangan < jarak_minimal:
                jarak_minimal = jarak_ruangan
                ruangan_selanjutnya = ruangan

        return ruangan_selanjutnya

    # Algoritma greedy
    def optimisasi_greedy():
        solusi = [0]  # Ruangan awal A
        jarak_total = 0
        ruangan_sekarang = 0  # Ruangan awal

        ruangan_tersedia = list(range(1, len(jarak)))

        while ruangan_tersedia:
            ruangan_selanjutnya = pilih_ruangan_greedy(ruangan_sekarang, ruangan_tersedia)
            if ruangan_selanjutnya is None:
                break
            solusi.append(ruangan_selanjutnya)
            jarak_total += jarak[ruangan_sekarang][ruangan_selanjutnya]

            ruangan_tersedia.remove(ruangan_selanjutnya)
            ruangan_sekarang = ruangan_selanjutnya

        jarak_total += jarak[ruangan_sekarang][0]  # Kembali ke ruangan A
        solusi.append(0)  # Menambahkan ruangan A ke solusi

        return solusi, jarak_total

    # Menjalankan algoritma greedy
    start_time = time.time()
    solusi_greedy, jarak_greedy = optimisasi_greedy()
    end_time = time.time()
    execution_time = end_time - start_time

    # Menampilkan hasil greedy
    st.header("Hasil Optimasi Greedy:")
    st.caption ("Jika pasien ingin melewati semua ruangan dengan titik awal dari A maka ruangan yang harus dilwati terlebih dulu adalah spt dibawah ini: ")
    st.write([chr(ruangan + ord('A')) for ruangan in solusi_greedy])
    st.write("Jarak Terbaik (Greedy):", jarak_greedy)
    st.write("Waktu Eksekusi:", execution_time, "detik")
    st.markdown("---")


elif selected == "Backtracking":
    # Definisi matriks jarak antar ruangan
    jarak = [
        [0, 5, 7, 3, float('inf')],  # A: [A, B, C, D, E]
        [5, 0, 4, float('inf'), 3],  # B: [A, B, C, D, E]
        [7, 4, 0, float('inf'), 5],  # C: [A, B, C, D, E]
        [3, float('inf'), float('inf'), 0, 4],  # D: [A, B, C, D, E]
        [float('inf'), float('inf'), 5, 4, 0]  # E: [A, B, C, D, E]
    ]
    # Algoritma backtracking
    def optimisasi_backtracking(ruangan_sekarang, ruangan_tersedia, jarak_total, solusi):
        if not ruangan_tersedia:
            jarak_total += jarak[ruangan_sekarang][0]  # Kembali ke ruangan A
            solusi.append(0)  # Menambahkan ruangan A ke solusi
            return jarak_total, solusi

        jarak_minimal = float('inf')
        ruangan_selanjutnya = None

        for ruangan in ruangan_tersedia:
            jarak_ruangan = jarak[ruangan_sekarang][ruangan]
            if jarak_ruangan is not None and jarak_ruangan < jarak_minimal:
                jarak_minimal = jarak_ruangan
                ruangan_selanjutnya = ruangan

        ruangan_tersedia.remove(ruangan_selanjutnya)
        solusi.append(ruangan_selanjutnya)
        jarak_total += jarak[ruangan_sekarang][ruangan_selanjutnya]

        jarak_total, solusi = optimisasi_backtracking(
            ruangan_selanjutnya, ruangan_tersedia, jarak_total, solusi
        )

        return jarak_total, solusi

   # Menjalankan algoritma backtracking
    start_time = time.time()
    solusi_backtracking = []
    jarak_backtracking, solusi_backtracking = optimisasi_backtracking(
        0, list(range(1, len(jarak))), 0, solusi_backtracking
    )
    end_time = time.time()
    execution_time = end_time - start_time

    # Menampilkan hasil backtracking
    st.header("Hasil Optimasi Backtracking:")
    st.caption("Jika pasien ingin melewati semua ruangan dengan titik awal dari A maka ruangan yang harus dilwati terlebih dulu adalah spt dibawah ini: ")
    st.write(['A'] + [chr(ruangan + ord('A')) for ruangan in solusi_backtracking])  # Add 'A' at the beginning of the sequence
    st.write("Jarak Terbaik (Backtracking):", jarak_backtracking)
    st.write("Waktu Eksekusi:", execution_time, "detik")
    st.markdown("---")
    
#========================= INI UNTUK CUSTOM INPUTAN DARI USER ===============================
elif selected == "Inputan":
    st.header("Kalkulasi Optimasi Jarak Antar Ruangan")
    jumlah_ruangan = st.number_input("Masukkan jumlah ruangan:", min_value=1, value=5, step=1)

    jarak = np.zeros((jumlah_ruangan, jumlah_ruangan))
    for i in range(jumlah_ruangan):
        for j in range(i + 1, jumlah_ruangan):
                jarak[i][j] = st.number_input(f"Masukkan jarak antara ruangan {i+1} dan ruangan {j+1}: ")
                jarak[j][i] = jarak[i][j]
                
    # Fungsi untuk memilih ruangan selanjutnya berdasarkan jarak terdekat
    def pilih_ruangan_greedy(ruangan_sekarang, ruangan_tersedia):
        jarak_minimal = float('inf')
        ruangan_selanjutnya = None

        for ruangan in ruangan_tersedia:
            jarak_ruangan = jarak[ruangan_sekarang][ruangan]
            if jarak_ruangan is not None and jarak_ruangan < jarak_minimal:
                jarak_minimal = jarak_ruangan
                ruangan_selanjutnya = ruangan

        return ruangan_selanjutnya

     #============================= ALGO GREEDY ===================================
    def optimisasi_greedy():
        solusi = [0]  # Ruangan awal A
        jarak_total = 0
        ruangan_sekarang = 0  # Ruangan awal

        ruangan_tersedia = list(range(1, jumlah_ruangan))

        while ruangan_tersedia:
            ruangan_selanjutnya = pilih_ruangan_greedy(ruangan_sekarang, ruangan_tersedia)
            if ruangan_selanjutnya is None:
                break
            solusi.append(ruangan_selanjutnya)
            jarak_total += jarak[ruangan_sekarang][ruangan_selanjutnya]

            ruangan_tersedia.remove(ruangan_selanjutnya)
            ruangan_sekarang = ruangan_selanjutnya

        jarak_total += jarak[ruangan_sekarang][0]  # Kembali ke ruangan awal
        solusi.append(0)  # Menambahkan ruangan awal A ke solusi

        return solusi, jarak_total
     # Menjalankan algoritma greedy
    start_time = time.perf_counter()  # Measure execution time after input processing

    solusi_greedy, jarak_greedy = optimisasi_greedy()

    # Calculate execution time
    execution_time_gred = time.perf_counter() - start_time
    
    #============================= ALGO BACKTRACKING ===================================
    def optimisasi_backtracking():
        solusi_terbaik = None
        jarak_terbaik = float('inf')
        ruangan_awal = 0
        ruangan_tersedia = list(range(1, jumlah_ruangan))

        def backtrack(ruangan_sekarang, ruangan_tersedia, solusi, jarak_total):
            nonlocal solusi_terbaik, jarak_terbaik

            if len(ruangan_tersedia) == 0:
                jarak_total += jarak[ruangan_sekarang][ruangan_awal]
                solusi.append(ruangan_awal)

                if jarak_total < jarak_terbaik:
                    solusi_terbaik = solusi.copy()
                    jarak_terbaik = jarak_total

                solusi.pop()
                jarak_total -= jarak[ruangan_sekarang][ruangan_awal]
                return

            for ruangan_selanjutnya in ruangan_tersedia:
                jarak_ruangan = jarak[ruangan_sekarang][ruangan_selanjutnya]
                if jarak_ruangan is not None:
                    solusi.append(ruangan_selanjutnya)
                    ruangan_tersedia.remove(ruangan_selanjutnya)
                    jarak_total += jarak_ruangan

                    backtrack(ruangan_selanjutnya, ruangan_tersedia, solusi, jarak_total)

                    solusi.pop()
                    ruangan_tersedia.append(ruangan_selanjutnya)
                    jarak_total -= jarak_ruangan

        solusi = [ruangan_awal]
        backtrack(ruangan_awal, ruangan_tersedia, solusi, 0)

        return solusi_terbaik, jarak_terbaik

    # # Menjalankan algoritma backtracking
    start_time = time.perf_counter()

    solusi_backtracking, jarak_backtracking = optimisasi_backtracking()

    execution_time_back = time.perf_counter() - start_time
    
    #================================ GRAPH ===========================================
    fig, ax = plt.subplots()
    G = nx.Graph()

    # Tambahkan node ke grafik
    for i in range(jumlah_ruangan):
        G.add_node(i, pos=(random.randint(1, 100), random.randint(1, 100)))

    # Tambahkan edge ke grafik
    for i in range(jumlah_ruangan):
        for j in range(i + 1, jumlah_ruangan):
            if jarak[i][j] > 0:
                G.add_edge(i, j, weight=jarak[i][j])

    # Gambar grafik dengan posisi node
    pos = nx.get_node_attributes(G, "pos")
    nx.draw(G, pos, with_labels=True, node_size=500, font_size=12, node_color="skyblue", edge_color="gray")

    # Gambar jalur rute terpendek
    edge_labels = nx.get_edge_attributes(G, "weight")
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_color="red")

    # Tampilkan grafik
    st.pyplot(fig)
    st.markdown("---")

    
    #===================== Hasil GREEDY ==========================
    st.header("Hasil Optimasi Greedy:")
    st.write("Rute terpendek (Greedy):", solusi_greedy)
    st.write("Jarak terbaik (Greedy):", jarak_greedy)
    st.write("Waktu Eksekusi (s):", execution_time_gred)


    #==================== Hasil BACTRACKING =======================
    st.header("Hasil Optimasi Backtracking:")
    st.write("Rute terpendek (Backtracking):", solusi_backtracking)
    st.write("Jarak terbaik (Backtracking):", jarak_backtracking)
    st.write("Waktu Eksekusi (s):", execution_time_back)