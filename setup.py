from setuptools import setup, find_packages

setup(
    name='4GraphAnalysis',
    version='1.0',
    packages=find_packages(),
    install_requires=[
        'PyQt5',
        'pymol',
        'PySide6',
        'plotly'
    ],
    entry_points={
        'pymol.plugins': [
            '4GraphAnalysis = my_plugin.__init__:__init_plugin__',
        ],
    },
)
