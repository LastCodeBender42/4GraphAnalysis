import networkx as nx 
from pymol import cmd
import pandas as pd
import tempfile

from .create_graph import *

def color_by_eigen():
    G = create_ring_graph()
    eigencentr = nx.eigenvector_centrality(G, max_iter=1000, tol=1e-6)
    sorted_data = dict(sorted(eigencentr.items()))
    ecvalues = pd.DataFrame(list(sorted_data.items()), columns=['key', 'value'])
    ecvalues = ecvalues[ecvalues['key'] != 100]

    ecvalues_sorted = ecvalues.sort_values(by='value', ascending=False)
    top_percent_count = int(0.4 * len(ecvalues_sorted))
    top_ec_vals = ecvalues_sorted.head(top_percent_count)

    pymol.cmd.color("white", "Chain A")

    for index, row in top_ec_vals.iterrows():
        i = str(index)
        j = int(row['key'])
        k = float(row['value']) / top_ec_vals['value'].max()
        color_name = "col" + i
        pymol.cmd.set_color(color_name, [1.00, 1.00, 1.00 - k])
        pymol.cmd.color(color_name, 'resi ' + str(j) + ' and chain A')

    pymol.cmd.hide('spheres', 'ca_atoms')
    pymol.cmd.show('cartoon', 'chain A')

def size_by_eigen():
    G = create_ring_graph()
    eigencentr = nx.eigenvector_centrality(G, max_iter=1000, tol=1e-6)
    sorted_data = dict(sorted(eigencentr.items()))
    ecvalues = pd.DataFrame(list(sorted_data.items()), columns=['key', 'value'])
    ecvalues = ecvalues[ecvalues['key'] != 100]

    ecvalues_sorted = ecvalues.sort_values(by='value', ascending=False)
    top_percent_count = int(0.4 * len(ecvalues_sorted))
    top_ec_vals = ecvalues_sorted.head(top_percent_count)

    pymol.cmd.color("white", "Chain A")

    pymol.cmd.select('ca_atoms', 'name CA')
    pymol.cmd.show('spheres', 'ca_atoms')
    pymol.cmd.set('sphere_scale', 0.4, 'ca_atoms')
    pymol.cmd.hide('cartoon', 'all')
    pymol.cmd.color("white", "Chain A")
    
    ecvalues_dict = dict(zip(top_ec_vals['key'], top_ec_vals['value']))
    scale_factor = 1.0  # You can adjust this factor as needed

    max_ec_factor = max(ecvalues_dict.values())
    min_ec_factor = min(ecvalues_dict.values())

    for resn, ec_factor in ecvalues_dict.items():
        scaled_size = scale_factor * (ec_factor - min_ec_factor) / (max_ec_factor - min_ec_factor + 1e-6)
        pymol.cmd.set('sphere_scale', scaled_size, f'resi {resn} and name CA and chain A')

    pymol.cmd.hide("everything","not Chain A")

    for index, row in top_ec_vals.iterrows():
        i = str(index)
        j = int(row['key'])
        k = float(row['value']) / top_ec_vals['value'].max()
        color_name = "col" + i
        pymol.cmd.set_color(color_name, [1.00, 1.00, 1.00 - k])
        pymol.cmd.color(color_name, 'resi ' + str(j) + ' and name CA and chain A')


