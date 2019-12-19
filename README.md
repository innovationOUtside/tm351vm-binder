# tm351vm-binder
See if we can generate a Binder/repo2docker build of the TM351 VM

Open to Notebook homepage: [![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/innovationOUtside/tm351vm-binder/master)

Open to OpenRefine: [![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/innovationOUtside/tm351vm-binder/master?urlpath=openrefine)

Open to Jupyterlab: [![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/innovationOUtside/tm351vm-binder/master?urlpath=lab)

The TM351 Virtual Machine was originally developed as a vagrant launched VirtualBox Lunix virtual machine to support the Open University distance learning course *TM351 Data Management and Analysis*.

This build packages eveything within a single container.

The virtual machine includes:

- Jupyter notebooks
- lots of preinstalled Python packages
- OpenRefine
- a Postgres database server
- a mongo database server

This repository is an attempt to get something similar running in MyBinder...

A Github Action is also used to build releases using `repo2docker` and puch the resulting container to Docker Hub.

The container can be found as `ousefuldemos/tm351-binderised:latest`.

The Jupyter notebook server runs on the default port 8888.

The container can be launched directly using [`containds`](https://containds.com/), the desktop app for running notebook containers and a personal, local Binder service. Select a new image and search for `tm351`; the `ousefuldemos/tm351-binderised` image is the one you want. When prompted, select the "standard" launch route, NOT the 'Try to start Jupyter notebook' route.
