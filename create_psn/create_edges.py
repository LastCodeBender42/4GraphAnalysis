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

def egde_betweenness():
    graph = create_ring_graph()
    edgebetw = nx.edge_betweenness_centrality(graph, k=None, normalized=True, weight=None, seed=None)
    keys = list(edgebetw.keys())
    values = list(edgebetw.values())
    newdf = pd.DataFrame(keys, columns=['source', 'target'])
    newdf['weight'] = values
    return newdf

def create_edges():
    newdf = egde_betweenness()

    pymol.cmd.color("lightorange", "Chain A")
    pymol.cmd.hide('lines')
    pymol.cmd.show('sticks')

    for i in range(len(newdf)):
        a, b, c = str(newdf.iloc[i, 0]), str(newdf.iloc[i, 1]), str(newdf.iloc[i, 2])
        c = float(c)
        pymol.cmd.bond("chain A and resi " + a + " and name CA", "chain A and resi " + b + " and name CA")
        pymol.cmd.set_bond("stick_radius", 20.0 * c, "chain A and resi " + a + " and name CA", "chain A and resi " + b + " and name CA")
        pymol.cmd.set_bond("stick_color", "red", "chain A and resi " + a + " and name CA", "chain A and resi " + b + " and name CA")
        pymol.cmd.show("sticks", "chain A and resi " + a + " and name CA, chain A and resi " + b + " and name CA")

    pymol.cmd.bg_color("white")

    pymol.cmd.remove("resn HOH")
    pymol.cmd.hide('sticks', '(polymer and not (name ca))')
    pymol.cmd.hide('(not chain A)')