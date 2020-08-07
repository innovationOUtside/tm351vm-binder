# Traitlet configuration file for jupyter-notebook.
from os import environ

# TO DO: this should be loaded in from a file (.openrefine_version)
# Or we change the path to a neutral one?
OPENREFINE_VERSION=3.3

c.ServerProxy.servers = {
    'openrefine': {
        'command': [f'{environ["CONDA_DIR"]}/openrefine/openrefine-{OPENREFINE_VERSION}/refine', '-p', '{port}','-d',f'{environ["HOME"]}/openrefine'],
        'port': 3333,
        'timeout': 120,
        'launcher_entry': {
            'enabled': True,
            'icon_path': f'{environ["CONDA_DIR"]}/.jupyter/custom/open-refine-logo.svg',
            'title': 'OpenRefine',
        },
    },
}
