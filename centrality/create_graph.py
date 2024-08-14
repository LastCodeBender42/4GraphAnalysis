import os
import subprocess
import sys
import tempfile
import pymol
import networkx as nx
import pandas as pd

def create_ring_graph():
    object_list = pymol.cmd.get_object_list()
    if not object_list:
        QMessageBox.warning(main_window, "Error", "No protein loaded.")
        return

    protein_name = object_list[0]
    tmp_dir = tempfile.gettempdir()
    cif_file_path = os.path.join(tmp_dir, f"{protein_name}.cif_ringEdges")
    pdb_file_path = os.path.join(tmp_dir, f"{protein_name}.pdb")

    tsv_file = cif_file_path

    # Read the tab-separated file into a DataFrame
    df = pd.read_csv(tsv_file, sep='\t')

    df2 = df[df['NodeId1'].str.contains('^A:') & (df['NodeId2'].str.contains('^A:'))].copy()
    df2['source'] = df2['NodeId1'].str.extract(r'(\d+)').astype(int)
    df2['target'] = df2['NodeId2'].str.extract(r'(\d+)').astype(int)
    ring_df = df2[['source','target']].copy()

    graph = ring_df
    G = nx.Graph()
    for index, row in graph.iterrows():
        G.add_edge(row['source'], row['target'])
    return G