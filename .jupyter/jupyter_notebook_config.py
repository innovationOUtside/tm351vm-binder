# Traitlet configuration file for jupyter-notebook.
from os import environ

c.ServerProxy.servers = {
    'openrefine': {
        'command': [f'{environ["CONDA_DIR"]}/openrefine/openrefine-2.8/refine', '-p', '{port}','-d',f'{environ["HOME"]}/openrefine'],
        'port': 3333,
        'timeout': 120,
        'launcher_entry': {
            'enabled': True,
            'icon_path': f'{environ["CONDA_DIR"]}/.jupyter/custom/open-refine-logo.svg',
            'title': 'OpenRefine',
        },
    },
}
