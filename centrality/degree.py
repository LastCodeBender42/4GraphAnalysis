import networkx as nx 
from pymol import cmd
import pandas as pd
import tempfile

from .create_graph import *

def color_by_degree():
    G = create_ring_graph()
    degrcentr = nx.degree_centrality(G)
    sorted_data = dict(sorted(degrcentr.items()))
    dcvalues = pd.DataFrame(list(sorted_data.items()), columns=['key', 'value'])
    dcvalues = dcvalues[dcvalues['key'] != 100]

    dcvalues_sorted = dcvalues.sort_values(by='value', ascending=False)
    top_percent_count = int(0.4 * len(dcvalues_sorted))
    top_dc_vals = dcvalues_sorted.head(top_percent_count)

    pymol.cmd.color("white", "Chain A")

    for index, row in top_dc_vals.iterrows():
        i = str(index)
        j = int(row['key'])
        k = float(row['value']) / top_dc_vals['value'].max()
        color_name = "col" + i
        pymol.cmd.set_color(color_name, [1.00 - k, 1.00, 1.00 - k])
        pymol.cmd.color(color_name, 'resi ' + str(j) + ' and chain A')

    pymol.cmd.hide('spheres', 'ca_atoms')
    pymol.cmd.show('cartoon', 'chain A')

def size_by_degree():
    G = create_ring_graph()
    degrcentr = nx.degree_centrality(G)
    sorted_data = dict(sorted(degrcentr.items()))
    dcvalues = pd.DataFrame(list(sorted_data.items()), columns=['key', 'value'])
    dcvalues = dcvalues[dcvalues['key'] != 100]

    dcvalues_sorted = dcvalues.sort_values(by='value', ascending=False)
    top_percent_count = int(0.4 * len(dcvalues_sorted))
    top_dc_vals = dcvalues_sorted.head(top_percent_count)

    pymol.cmd.color("white", "Chain A")

    pymol.cmd.select('ca_atoms', 'name CA')
    pymol.cmd.show('spheres', 'ca_atoms')
    pymol.cmd.set('sphere_scale', 0.4, 'ca_atoms')
    pymol.cmd.hide('cartoon', 'all')
    pymol.cmd.color("white", "Chain A")
    
    dcvalues_dict = dict(zip(top_dc_vals['key'], top_dc_vals['value']))
    scale_factor = 1.0  # You can adjust this factor as needed

    max_dc_factor = max(dcvalues_dict.values())
    min_dc_factor = min(dcvalues_dict.values())

    for resn, dc_factor in dcvalues_dict.items():
        scaled_size = scale_factor * (dc_factor - min_dc_factor) / (max_dc_factor - min_dc_factor + 1e-6)
        pymol.cmd.set('sphere_scale', scaled_size, f'resi {resn} and name CA and chain A')

    pymol.cmd.hide("everything","not Chain A")

    for index, row in top_dc_vals.iterrows():
        i = str(index)
        j = int(row['key'])
        k = float(row['value']) / top_dc_vals['value'].max()
        color_name = "col" + i
        pymol.cmd.set_color(color_name, [1.00 - k, 1.00, 1.00 - k])
        pymol.cmd.color(color_name, 'resi ' + str(j) + ' and name CA and chain A')


