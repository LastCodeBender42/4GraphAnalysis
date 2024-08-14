import networkx as nx 
from pymol import cmd
import pandas as pd
import tempfile

from .create_graph import *

def color_by_close():
    G = create_ring_graph()
    closecentr = nx.closeness_centrality(G)
    sorted_data = dict(sorted(closecentr.items()))
    ccvalues = pd.DataFrame(list(sorted_data.items()), columns=['key', 'value'])
    ccvalues = ccvalues[ccvalues['key'] != 100]

    ccvalues_sorted = ccvalues.sort_values(by='value', ascending=False)
    top_percent_count = int(0.4 * len(ccvalues_sorted))
    top_cc_vals = ccvalues_sorted.head(top_percent_count)

    pymol.cmd.color("white", "Chain A")

    for index, row in top_cc_vals.iterrows():
        i = str(index)
        j = int(row['key'])
        k = float(row['value']) / top_cc_vals['value'].max()
        color_name = "col" + i
        pymol.cmd.set_color(color_name, [1.00, 1.00 - k, 1.00 - k])
        pymol.cmd.color(color_name, 'resi ' + str(j) + ' and chain A')

    pymol.cmd.hide('spheres', 'ca_atoms')
    pymol.cmd.show('cartoon', 'chain A')

def size_by_close():
    G = create_ring_graph()
    closecentr = nx.closeness_centrality(G)
    sorted_data = dict(sorted(closecentr.items()))
    ccvalues = pd.DataFrame(list(sorted_data.items()), columns=['key', 'value'])
    ccvalues = ccvalues[ccvalues['key'] != 100]

    ccvalues_sorted = ccvalues.sort_values(by='value', ascending=False)
    top_percent_count = int(0.4 * len(ccvalues_sorted))
    top_cc_vals = ccvalues_sorted.head(top_percent_count)

    pymol.cmd.color("white", "Chain A")

    pymol.cmd.select('ca_atoms', 'name CA')
    pymol.cmd.show('spheres', 'ca_atoms')
    pymol.cmd.set('sphere_scale', 0.4, 'ca_atoms')
    pymol.cmd.hide('cartoon', 'all')
    pymol.cmd.color("white", "Chain A")
    
    ccvalues_dict = dict(zip(top_cc_vals['key'], top_cc_vals['value']))
    scale_factor = 1.0  # You can adjust this factor as needed

    max_cc_factor = max(ccvalues_dict.values())
    min_cc_factor = min(ccvalues_dict.values())

    for resn, cc_factor in ccvalues_dict.items():
        scaled_size = scale_factor * (cc_factor - min_cc_factor) / (max_cc_factor - min_cc_factor + 1e-6)
        pymol.cmd.set('sphere_scale', scaled_size, f'resi {resn} and name CA and chain A')

    pymol.cmd.hide("everything","not Chain A")

    for index, row in top_cc_vals.iterrows():
    	i = str(index)
    	j = int(row['key'])
    	k = float(row['value']) / top_cc_vals['value'].max()
    	color_name = "col" + i
    	pymol.cmd.set_color(color_name, [1.00, 1.00 - k, 1.00 - k])
    	pymol.cmd.color(color_name, 'resi ' + str(j) + ' and name CA and chain A')


