from PyQt5.QtWidgets import QMainWindow, QProgressBar, QMessageBox
import os
import sys
import pymol
import tempfile
from .ring_api import run_ring_api

def get_current_run_config():
    edge_policy = "--best_edge"
    
    seq_sep = '3'
    len_hbond = '5.5'
    len_pica = '7.0'
    len_pipi = '7.0'
    len_salt = '5.0'
    len_ss = '3.0'
    len_vdw = '0.8'

    return {
        "-g": seq_sep,
        "-o": len_salt,
        "-s": len_ss,
        "-k": len_pipi,
        "-a": len_pica,
        "-b": len_hbond,
        "-w": len_vdw,
        "edges": edge_policy
    }

def execute_ring_api(main_window):
    try:
        print("Executing RING API...")

        object_list = pymol.cmd.get_object_list()
        if not object_list:
            QMessageBox.warning(main_window, "Error", "No protein loaded.")
            return

        protein_name = object_list[0]

        if not protein_name:
            QMessageBox.warning(main_window, "Error", "No protein loaded.")
            return

        # Save to a temporary directory as CIF
        tmp_dir = tempfile.gettempdir()
        file_name = f"{protein_name}.cif"
        file_path = os.path.join(tmp_dir, file_name)


        run_config = get_current_run_config()

        main_window.progressBar.show()
        
        def progress_f(p):
            main_window.progressBar.setValue(p)    
        
        run_ring_api(file_path, run_config, tmp_dir, progress_f)

        print("RING API execution complete.")

    except Exception as e:
        QMessageBox.critical(main_window, "Error", f"Failed to execute RING API: {e}")
        print(f"Failed to execute RING API: {e}", file=sys.stderr)

