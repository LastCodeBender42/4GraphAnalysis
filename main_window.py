from PyQt5.QtWidgets import QApplication, QMainWindow, QCheckBox, QHBoxLayout, \
    QVBoxLayout, QGroupBox, QRadioButton, QPushButton, QButtonGroup, QProgressBar,\
    QGridLayout, QDialog, QTextEdit, QDialogButtonBox, QWidget, QLabel

from .create_psn import *
from .downloads import *
from .centrality import *

import sys
import webbrowser 
import pymol 

class MainDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle('Python Graph Analysis App')
        
        '''
        Group Box for generating protein structure network
        '''
        psn = QGroupBox('Generate Protein Structure Network:')
        objs = QPushButton('Show PyMOL objects', self)
        objs.clicked.connect(self.show_pymol_objects_dialog)

        convert = QPushButton('Create cif file', self)
        convert.clicked.connect(self.convert_object_to_cif)

        ring = QPushButton('Connect to RING server', self)
        ring.clicked.connect(self.execute_ring_api)

        net = QPushButton('Generate PSN Network', self)
        net.clicked.connect(self.create_edges)

        psn_layout = QVBoxLayout()
        psn_layout.addWidget(objs)
        psn_layout.addWidget(convert)
        psn_layout.addWidget(ring)
        psn_layout.addWidget(net)
        psn.setLayout(psn_layout)
        # ----------------------------------------------------------------

        '''
        GroupBox for selecting the appearance of the network visualization
        '''
        display = QGroupBox('Select Visualization:')
        show_cartoon = QPushButton('Show as cartoon', self)
        show_cartoon.clicked.connect(self.show_as_cartoon)
        show_network = QPushButton('Show as network', self)
        show_network.clicked.connect(self.show_as_network)
        
        display_layout = QVBoxLayout()
        display_layout.addWidget(show_cartoon)
        display_layout.addWidget(show_network)
        display.setLayout(display_layout)
        # ----------------------------------------------------------------

        '''
        Calculates betweenness, closeness, degree, and eigenvector centralities
        and displays the top 25% as weighted vertices
        '''
        grid_box = QGroupBox('Select a Network Centrality:')
        grid_layout = QGridLayout()

        self.checkbox_bc = QCheckBox('Set as network (Betweenness)')
        self.checkbox_cc = QCheckBox('Set as network (Closeness)')
        self.checkbox_dc = QCheckBox('Set as network (Degree)')
        self.checkbox_ec = QCheckBox('Set as network (Eigenvector)')

        self.button_bc = QPushButton('Betweenness centrality', self)
        self.button_bc.clicked.connect(self.button_bc_clicked)
        self.button_cc = QPushButton('Closeness centrality', self)
        self.button_cc.clicked.connect(self.button_cc_clicked)
        self.button_dc = QPushButton('Degree centrality', self)
        self.button_dc.clicked.connect(self.button_dc_clicked)
        self.button_ec = QPushButton('Eigenvector centrality', self)
        self.button_ec.clicked.connect(self.button_ec_clicked)

        grid_layout.addWidget(self.button_bc, 0, 0)
        grid_layout.addWidget(self.checkbox_bc, 0, 1)
        grid_layout.addWidget(self.button_cc, 0, 2)
        grid_layout.addWidget(self.checkbox_cc, 0, 3)
        grid_layout.addWidget(self.button_dc, 1, 0)
        grid_layout.addWidget(self.checkbox_dc, 1, 1)
        grid_layout.addWidget(self.button_ec, 1, 2)
        grid_layout.addWidget(self.checkbox_ec, 1, 3)
        grid_box.setLayout(grid_layout)

        # ----------------------------------------------------------------

        '''
        - Opens a link to a GitHub page that outlines helpful commands in PyMOL terminal
        - Downloads the data to folder on user computer
        - Downloads a dashboard for further investigation
        '''
        help_box = QGroupBox("Guide for customizing the visualization:")
        help_layout = QVBoxLayout()
        help_link = QPushButton("Helpful commands")
        help_link.clicked.connect(self.link_to_github)
        download_data = QPushButton("Download data")
        download_dashboard = QPushButton("Download dashboard")

        '''
        Sets up a progress bar for the initialization and completion of the RING api
        '''
        self.progressBar = QProgressBar(self)
        self.progressBar.setRange(0, 100)
        self.progressBar.setValue(0)

        help_layout.addWidget(help_link)
        help_layout.addWidget(download_data)
        help_layout.addWidget(download_dashboard)
        help_layout.addWidget(self.progressBar)
        help_box.setLayout(help_layout)
        # ----------------------------------------------------------------

        '''
        GUI layout
        '''
        h_layout = QHBoxLayout()
        h_layout.addWidget(psn)
        h_layout.addWidget(display)

        v_layout = QVBoxLayout(self)
        v_layout.addLayout(h_layout)
        v_layout.addWidget(grid_box)
        v_layout.addWidget(help_box)
        # ----------------------------------------------------------------

    def link_to_github(self):
        link_to_github(self)

    def show_pymol_objects_dialog(self):
        show_pymol_objects_dialog(self)

    def convert_object_to_cif(self):
        convert_object_to_cif(self)

    def execute_ring_api(self):
        execute_ring_api(self)

    def create_edges(self):
        create_edges()

    def show_as_network(self):
        pymol.cmd.select('ca_atoms', 'name CA')
        pymol.cmd.show('spheres', 'ca_atoms')
        pymol.cmd.set('sphere_scale', 0.5, 'ca_atoms')
        pymol.cmd.hide('cartoon', 'all')
        pymol.cmd.hide('everything', 'not chain A')

    def show_as_cartoon(self):
        pymol.cmd.hide('spheres','ca_atoms')
        pymol.cmd.show('cartoon','chain A')
    # ----------------------------------------------------------------

    '''
    functions for calculating and visualizing centrality properties
    '''
    def button_bc_clicked(self):
        if not self.checkbox_bc.isChecked():
            color_by_betw()
        else:
            size_by_betw()

    def button_cc_clicked(self):
        if not self.checkbox_cc.isChecked():
            color_by_close()
        else:
            size_by_close()

    def button_dc_clicked(self):
        if not self.checkbox_dc.isChecked():
            color_by_degree()
        else:
            size_by_degree()

    def button_ec_clicked(self):
        if not self.checkbox_ec.isChecked():
            color_by_eigen()
        else:
            size_by_eigen()





def show_window():
    dialog = MainDialog()
    dialog.exec_()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_window = MainDialog()
    main_window.show()
    sys.exit(app.exec())
