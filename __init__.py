"""
4GraphAnalysis Plugin for PyMOL
Author: David Foutch
Contact: dfoutch@analysisandinformatics.org
Version: 1.0
Description: A PyMOL plugin for graph analysis of protein structures.
"""

from pymol.plugins import addmenuitemqt
from .my_plugin import get_protein_name  # Import get_protein_name from my_plugin.py
from . import main_window  # Import main_window from the current package

def __init_plugin__(app=None):
    addmenuitemqt('4GraphAnalysis', run_my_plugin)

def run_my_plugin():
    main_window.show_window()

