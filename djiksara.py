"""
Copyright (c) 2024 Wisnu Hidayat
All rights reserved.

This source code is licensed under proprietary license and is protected by copyright law.
Unauthorized copying, redistribution or use of this file, via any medium is strictly prohibited.
Written by Wisnu Hidayat <231240001422>
"""

import networkx as nx
import matplotlib.pyplot as plt
import numpy as np
from datetime import datetime
import matplotlib.patches as patches
import sys
import hashlib
import getpass

class DijkstraVisualizer:
    def __init__(self):
        self.__author__ = "Wisnu Hidayat"
        self.__copyright__ = "Copyright (c) 2024, All rights reserved."
        self.__nim__ = "231240001422"
        self.__version__ = "1.0.0"
        self.__hash__ = self._generate_hash()
    
    def _generate_hash(self):
        return hashlib.sha256(f"{self.__author__}{self.__nim__}".encode()).hexdigest()
    
    def _verify_access(self):
        if self._generate_hash() != self.__hash__:
            raise ValueError("Unauthorized access detected!")
        return True
    
    def _buat_visualisasi_dijkstra(self, start_node, end_node):
        # Konfigurasi matplotlib
        plt.rcParams['figure.facecolor'] = 'white'
        plt.rcParams['axes.facecolor'] = 'white'
        plt.rcParams['axes.grid'] = False
        
        # Membuat figure dengan ukuran yang lebih sesuai
        fig = plt.figure(figsize=(15, 8))
        gs = fig.add_gridspec(1, 2, width_ratios=[1.2, 0.8], wspace=0.3)
        ax1 = fig.add_subplot(gs[0])
        ax2 = fig.add_subplot(gs[1])
        
        # Membuat graf
        G = nx.Graph()
        nodes = range(16)
        G.add_nodes_from(nodes)
        
        edges = [
            (0, 1, 5), (0, 2, 2), (0, 3, 4),
            (1, 5, 9), (2, 4, 8), (2, 7, 5),
            (3, 6, 1), (4, 7, 5), (5, 10, 6),
            (6, 9, 11), (7, 8, 10), (8, 11, 15),
            (9, 11, 10), (10, 12, 8), (11, 14, 7),
            (12, 14, 3), (13, 14, 9), (14, 15, 10)
        ]
        G.add_weighted_edges_from(edges)
        
        # Mencari jalur
        shortest_path = nx.dijkstra_path(G, start_node, end_node, weight='weight')
        shortest_distance = nx.dijkstra_path_length(G, start_node, end_node, weight='weight')
        all_paths = list(nx.all_simple_paths(G, start_node, end_node))
        path_distances = [(p, sum(G[p[i]][p[i+1]]['weight'] for i in range(len(p)-1))) for p in all_paths]
        path_distances.sort(key=lambda x: x[1])
        
        # Mengatur layout graf dengan posisi yang lebih terstruktur
        pos = nx.spring_layout(G, k=1, iterations=100, seed=42)  # Menambahkan seed untuk konsistensi
        
        # Menggambar edges
        nx.draw_networkx_edges(G, pos, ax=ax1, edge_color='lightgray', 
                              style='dashed', width=1, alpha=0.5)
        
        # Menggambar jalur terpendek
        path_edges = list(zip(shortest_path, shortest_path[1:]))
        nx.draw_networkx_edges(G, pos, ax=ax1, edgelist=path_edges, 
                              edge_color='red', width=2)
        
        # Menyiapkan warna dan ukuran node
        node_colors = ['red' if n == start_node else 'green' if n == end_node 
                      else 'orange' if n in shortest_path else 'lightblue' for n in G.nodes()]
        node_sizes = [600 if n in [start_node, end_node] else 
                     500 if n in shortest_path else 400 for n in G.nodes()]
        
        # Menggambar nodes
        nx.draw_networkx_nodes(G, pos, ax=ax1, node_color=node_colors,
                              node_size=node_sizes, edgecolors='white')
        
        # Menambahkan label node
        nx.draw_networkx_labels(G, pos, ax=ax1, font_size=8,
                              font_weight='bold', font_color='black')
        
        # Menambahkan label edge
        edge_labels = nx.get_edge_attributes(G, 'weight')
        nx.draw_networkx_edge_labels(G, pos, edge_labels, ax=ax1,
                                    font_size=7)
        
        # Mengatur judul
        ax1.set_title("Visualisasi Algoritma Dijkstra\n" +
                     f"Jalur Terpendek dari Node {start_node} ke Node {end_node}",
                     pad=20, size=12)
        
        # Menyiapkan informasi dengan header baru
        info_text = [
            "WISNU HIDAYAT - 231240001422",
            "="*40,
            "\nPENJELASAN WARNA",
            "● Merah     : Node Awal",
            "● Hijau     : Node Akhir",
            "● Orange    : Node Jalur",
            "● Biru      : Node Lain",
            "— Merah     : Jalur Terpendek",
            "-- Abu-abu  : Jalur Alternatif",
            "\nINFORMASI RUTE",
            f"Start  : Node {start_node}",
            f"Target : Node {end_node}",
            f"Nodes  : {len(G.nodes())}",
            f"Edges  : {len(G.edges())}",
            "\nJALUR TERPENDEK",
            f"Path   : {' → '.join(map(str, shortest_path))}",
            f"Jarak  : {shortest_distance} unit",
            "\nDETAIL RUTE"
        ]
        
        # Menambahkan detail rute
        for i in range(len(shortest_path)-1):
            weight = G[shortest_path[i]][shortest_path[i+1]]['weight']
            info_text.append(f"[{shortest_path[i]} → {shortest_path[i+1]}] = {weight} unit")
        
        # Menambahkan alternatif rute
        info_text.extend(["\nALTERNATIF RUTE"])
        for idx, (path, dist) in enumerate(path_distances[1:4], 1):
            info_text.append(f"{idx}. {' → '.join(map(str, path))} ({dist} unit)")
        
        # Menambahkan garis penutup tanpa credit
        info_text.extend(["\n" + "="*40])
        
        # Menampilkan informasi
        ax2.text(0.05, 0.95, '\n'.join(info_text), 
                 va='top', family='monospace', fontsize=9,
                 transform=ax2.transAxes)
        ax2.axis('off')
        
        plt.tight_layout()
        plt.show()
        return G
    
    def visualize(self, start_node=0, end_node=15):
        try:
            if self._verify_access():
                return self._buat_visualisasi_dijkstra(start_node, end_node)
        except Exception as e:
            print(f"Error: {str(e)}")
            return None

def main():
    try:
        visualizer = DijkstraVisualizer()
        visualizer.visualize(0, 15)
    except Exception as e:
        print(f"Error: Unauthorized access!")
        sys.exit(1)

if __name__ == "__main__":
    main()
