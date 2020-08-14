# tm351vm-binder
See if we can generate a Binder/repo2docker build of the TM351 VM

Open to Notebook homepage: [![Binder](https://gke.mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/innovationOUtside/tm351vm-binder/master)

Open to OpenRefine: [![Binder](https://mybinder.org/badge_logo.svg)](https://gke.mybinder.org/v2/gh/innovationOUtside/tm351vm-binder/master?urlpath=openrefine)

Open to Jupyterlab: [![Binder](https://mybinder.org/badge_logo.svg)](https://gke.mybinder.org/v2/gh/innovationOUtside/tm351vm-binder/master?urlpath=lab)

The TM351 Virtual Machine was originally developed as a vagrant launched VirtualBox Linux virtual machine to support the Open University distance learning course *TM351 Data Management and Analysis*. From 2020J, the module will be distributing the software environment, renamed the *TM351 Virtual Computing Environment (VCE)* via a Docker container.

This build packages eveything within a single Docker container.

The virtual computing environment includes:

- Jupyter notebooks
- lots of preinstalled Python packages
- OpenRefine
- a Postgres database server
- a mongo database server

This repository can be used to launch the environment via a Binderhub service such as MyBinder.

A Github Action is also used to build Docker images using `repo2docker` and then push the resulting container image to Docker Hub.

The container image can be found as `ousefuldemos/tm351-binderised:latest`.

WHen the environment is launched via a container, the Jupyter notebook server tat provides the main user interface runs on the default port 8888.

To get hold of the lastest version of the Docker container image, run the following command from the commandline/command prompt:

`docker pull ousefuldemos/tm351-binderised:latest`

To run the container from the command line on a Mac:

```
# Create a directory for your TM351 work
mkdir -p TM351VCE

# Launch the container with shared directories mounted from your TM351VCE directory
docker run --name tm351_20J --rm -d -p 8351:8888 -v "$PWD/TM351VCE/notebooks:/home/jovyan/notebooks" -v "$PWD/TM351VCE/openrefine_projects:/home/jovyan/openrefine" -e JUPYTER_TOKEN="letmein" ousefuldemos/tm351-binderised:latest
```

*(The quotes round the volume mount cope with spaces in the `$PWD` directory path)*

Rather than using the mounting directories relative to the current directory (`$PWD`) the `docker run` command is run in, we could also specify a mounted directory using an absolute path, such as `"/Users/MyUser/TM351VCE/notebooks:/home/jovyan/notebooks"`.

This will serve the container on `http://localhost:8351` and share folders from the `TM351VCE` folder in the current directory; login with the token `letmein` or whatever token you set.

If you want to update a legacy container to use an updated image, you need to stop and remove/delete the original container and then rerun the `docker run` command:

```
docker stop tm351_20J
docker rm tm351_20J
```
If you do delete the container, shared volume files will be preserved on host and mounted back into the new container, but any changes you made to the initial of the original container, such as installing additional Python packages or making changes to database tables, will be lost.

On Windows, first create a directory `C:\TM351VCE`. Then start the container using a command of the form:

`docker run --name tm351vce --rm -d -p 8351:8888 -v $pwd\notebooks:/home/jovyan/notebooks
 -v $pwd\openrefine_projects:/home/jovyan/openrefine -e JUPYTER_TOKEN="letmein" ousefuldemos/tm351-binderised:latest`
 
You can also specify volume bindings using an absilute path to a directory on the host computer, rather than a path relative to the current directory (`$pwd`) that the `docker run` command is executed in, using a volume mount command of the form `-v c:\TM351VCE\notebooks:c:\home\jovyan\notebooks`.

In order to access the notebook server via your browser, you will need to find the token used to access the notebook server. Use the one you set and passed in via the `JUPYTER_TOKEN=` assignment in the docker command, or look up the token by running:

`docker exec -it tm351_20J jupyter notebook list`

This will display something along the lines of:

`Currently running servers:
http://0.0.0.0:8888/?token=dca25d6755dbd2a1c9b346dca3b8c839e44c9271e20bc416 :: /home/jovyan`

Use the token value to log in to the server.

The run command will create a notebooks directory in the directory you issued the run command from, and then share it into the `notebooks` folder that you can see from the notebook server homepage. OpenRefine projects are also shared between your local machine and the container.

Files that exist outside the `/home/joyan/notebooks` and `/home/jovyan/openrefine` directory paths in the container (which is to say, outside the `notebooks` and `openrefine` directories viewable from the notebook server homepage, *will not be shared to your local desktop*.

The container can also be launched directly using [`containds`](https://containds.com/), the desktop app for running notebook containers and a personal, local Binder service. Select a new image and search for `tm351`; the `ousefuldemos/tm351-binderised` image is the one you want. When prompted, select the "standard" launch route, NOT the 'Try to start Jupyter notebook' route.
