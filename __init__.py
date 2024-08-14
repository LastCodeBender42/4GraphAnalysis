from pymol.plugins import addmenuitemqt
from .my_plugin import get_protein_name  # Import get_protein_name from my_plugin.py
from . import main_window  # Import main_window from the current package

def __init_plugin__(app=None):
    addmenuitemqt('4GraphAnalysis', run_my_plugin)

def run_my_plugin():
    main_window.show_window()

