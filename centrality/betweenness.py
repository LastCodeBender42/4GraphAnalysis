import networkx as nx 
from pymol import cmd
import pandas as pd
import tempfile

from .create_graph import *

def color_by_betw():
    G = create_ring_graph()
    betwcentr = nx.betweenness_centrality(G)
    sorted_data = dict(sorted(betwcentr.items()))
    bcvalues = pd.DataFrame(list(sorted_data.items()), columns=['key', 'value'])
    bcvalues = bcvalues[bcvalues['key'] != 100]

    bcvalues_sorted = bcvalues.sort_values(by='value', ascending=False)
    top_percent_count = int(0.4 * len(bcvalues_sorted))
    top_bc_vals = bcvalues_sorted.head(top_percent_count)

    pymol.cmd.color("white", "Chain A")

    for index, row in top_bc_vals.iterrows():
        i = str(index)
        j = int(row['key'])
        k = float(row['value']) / top_bc_vals['value'].max()
        color_name = "col" + i
        pymol.cmd.set_color(color_name, [1.00 - k, 1.00 - k, 1.00])
        pymol.cmd.color(color_name, 'resi ' + str(j) + ' and chain A')

    pymol.cmd.hide('spheres', 'ca_atoms')
    pymol.cmd.show('cartoon', 'chain A')

def size_by_betw():
    G = create_ring_graph()
    betwcentr = nx.betweenness_centrality(G)
    sorted_data = dict(sorted(betwcentr.items()))
    bcvalues = pd.DataFrame(list(sorted_data.items()), columns=['key', 'value'])
    bcvalues = bcvalues[bcvalues['key'] != 100]

    bcvalues_sorted = bcvalues.sort_values(by='value', ascending=False)
    top_percent_count = int(0.4 * len(bcvalues_sorted))
    top_bc_vals = bcvalues_sorted.head(top_percent_count)

    pymol.cmd.color("white", "Chain A")

    pymol.cmd.select('ca_atoms', 'name CA')
    pymol.cmd.show('spheres', 'ca_atoms')
    pymol.cmd.set('sphere_scale', 0.4, 'ca_atoms')
    pymol.cmd.hide('cartoon', 'all')
    pymol.cmd.color("white", "Chain A")
    
    bcvalues_dict = dict(zip(top_bc_vals['key'], top_bc_vals['value']))
    scale_factor = 1.0  # You can adjust this factor as needed

    max_bc_factor = max(bcvalues_dict.values())
    min_bc_factor = min(bcvalues_dict.values())

    for resn, bc_factor in bcvalues_dict.items():
        scaled_size = scale_factor * (bc_factor - min_bc_factor) / (max_bc_factor - min_bc_factor + 1e-6)
        pymol.cmd.set('sphere_scale', scaled_size, f'resi {resn} and name CA and chain A')

    pymol.cmd.hide("everything","not Chain A")

    for index, row in top_bc_vals.iterrows():
    	i = str(index)
    	j = int(row['key'])
    	k = float(row['value']) / top_bc_vals['value'].max()
    	color_name = "col" + i
    	pymol.cmd.set_color(color_name, [1.00 - k, 1.00 - k, 1.00])
    	pymol.cmd.color(color_name, 'resi ' + str(j) + ' and name CA and chain A')

    
   


