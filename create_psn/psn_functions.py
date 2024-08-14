from PyQt5.QtWidgets import QApplication, QMainWindow, QCheckBox, QHBoxLayout, \
    QVBoxLayout, QGroupBox, QRadioButton, QPushButton, QButtonGroup, \
    QGridLayout, QDialog, QTextEdit, QDialogButtonBox, QWidget, QLabel

import pymol 
import tempfile
import os

def show_pymol_objects_dialog(self):
    dialog = QDialog(self)
    dialog.setWindowTitle("Loaded PyMOL Objects")
    layout = QVBoxLayout()

    text_edit = QTextEdit()
    text_edit.setReadOnly(True)

    # Get the list of loaded PyMOL objects
    objects = pymol.cmd.get_object_list()

    if objects:
        text_edit.setText("\n".join(objects))
    else:
        text_edit.setText("No PyMOL objects loaded.")

    layout.addWidget(text_edit)

    button_box = QDialogButtonBox(QDialogButtonBox.Ok)
    button_box.accepted.connect(dialog.accept)
    layout.addWidget(button_box)

    dialog.setLayout(layout)
    dialog.exec()

def convert_object_to_cif(self):

    # Get the list of all objects in the session
    objects = pymol.cmd.get_object_list()

    # Assuming we want to save the first object in the list
    object_name = objects[0] if objects else None

    if object_name:
        # Get the system temporary directory
        temp_dir = tempfile.gettempdir()

        # Define the path for the output PDB file
        output_pdb_path = os.path.join(temp_dir, f"{object_name}.pdb")

        # Save the object as a PDB file
        pymol.cmd.save(output_pdb_path, object_name)

        # Define the path for the output CIF file
        output_cif_path = os.path.join(temp_dir, f"{object_name}.cif")

        # Convert the PDB file to a CIF file
        pymol.cmd.load(output_pdb_path)
        pymol.cmd.save(output_cif_path, object_name)

        # Print the paths of the saved files
        print(f"Object saved as PDB file: {output_pdb_path}")
        print(f"Object converted and saved as CIF file: {output_cif_path}")
    else:
        print("No objects found in the current PyMOL session.")
