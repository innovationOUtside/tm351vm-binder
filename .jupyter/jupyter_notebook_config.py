# Traitlet configuration file for jupyter-notebook.

c.ServerProxy.servers = {
    'openrefine': {
        'command': ['${CONDA_DIR}/openrefine/openrefine-2.8/refine', '-p', '{port}','-d','/home/jovyan/openrefine'],
        'port': 3333,
        'timeout': 120,
        'launcher_entry': {
            'enabled': True,
            'icon_path': '$HOME/.jupyter/custom/open-refine-logo.svg',
            'title': 'OpenRefine',
        },
    },
}
