# tm351vm-binder
See if we can generate a Binder/repo2docker build of the TM351 VM

Open to Notebook homepage: [![Binder](https://gke.mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/innovationOUtside/tm351vm-binder/master)

Open to OpenRefine: [![Binder](https://mybinder.org/badge_logo.svg)](https://gke.mybinder.org/v2/gh/innovationOUtside/tm351vm-binder/master?urlpath=openrefine)

Open to Jupyterlab: [![Binder](https://mybinder.org/badge_logo.svg)](https://gke.mybinder.org/v2/gh/innovationOUtside/tm351vm-binder/master?urlpath=lab)

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

To run the container from the command line on a Mac:

`docker run --name tm351test --rm -d -p 8895:8888 -v "$PWD/notebooks:/home/jovyan/notebooks" -v "$PWD/openrefine_projects:/home/jovyan/openrefine" -e JUPYTER_TOKEN="letmein" ousefuldemos/tm351-binderised:latest`

*(The quotes round the volume mount cope with spaces in the `$PWD` directory path)*
  
This will serve the container on `http://localhost:8895` and share folders from the current directory; login with the token `letmein` or whatever token you set.

On Windows, I think you need to try something like the following [UNTESTED]:

`docker run --name tm351test --rm -d -p 8895:8888 -v c:\tm129share\notebooks:c:\home\jovyan\notebooks -v c:\tm129share\openrefine_projects:c:\home\jovyan\openrefine -e JUPYTER_TOKEN="letmein" ousefuldemos/tm351-binderised:latest`

*If you can help me debug the Windows invocation, that would be really useful. Please post to a new issue.*

In order to access the notebook server via your browser, you will need to find the token used to access the notebook server. Use the one you set and passed in via the `JUPYTER_TOKEN=` assignment in the docker command, or look up the token by running:

`docker exec -it tm351test jupyter notebook list`

This will display something along the lines of:

`Currently running servers:
http://0.0.0.0:8888/?token=dca25d6755dbd2a1c9b346dca3b8c839e44c9271e20bc416 :: /home/jovyan`

Use the token value to log in to the server.

The run command will create a notebooks directory in the directory you issued the run command from, and then share it into the `notebooks` folder that you can see from the notebook server homepage. OpenRefine projects are also shared between your local machine and the container.

Files that exist outside the `/home/joyan/notebooks` and `/home/jovyan/openrefine` directory paths in the container (which is to say, outside the `notebooks` and `openrefine` directories viewable from the notebook server homepage, *will not be shared to your local desktop*.
