# tm351vm-binder

Repo for defining and building the TM351 Virtual Computing Enviornment (VCE) Docker image.

This README is *not intended* to play the role of a software installation guide; the official software installation guide will be distributed as part of the course materials via the OU VLE.

However, some guidance on installing and using the TM351 VCE locally and on remote hosts, as well as acessing TM351 VCE services from a VS Code editor is available from the [wiki](https://github.com/innovationOUtside/tm351vm-binder/wiki).

----


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

The container image as built from this repository can be found as `ousefuldemos/tm351-binderised:latest` and should be regarded as *unofficial* and *bleeding edge*!

The following command is used in the build process to build, tag and release containers:
```
docker pull ousefuldemos/tm351-binderised:latest && docker image tag ousefuldemos/tm351-binderised:latest ousefulcoursecontainers/ou-tm351:current && docker push ousefulcoursecontainers/ou-tm351:current
```

The actual Docker image released to students and ALs for 2020J  will be named most likely as `ousefulcoursecontainers/ou-tm351:current` (we may also explore a per-presentation tagging strategy).

When the environment is launched via a container, the Jupyter notebook server that provides the main user interface runs inside the container on the default port 8888.

## Installation

To run the TM351 virtual computing environment on your own computer, you will first need to [download and install Docker](https://docs.docker.com/get-docker/).

To get hold of the latest version of the Docker container image as built from releases from this repository, run the following command from the commandline/command prompt:

`docker pull ousefuldemos/tm351-binderised:latest`

The anticipated image for TM351 2020J can be obtained by running the command: `docker pull ousefulcoursecontainers/ou-tm351:current`

To run the container from the command line on a Mac:

```
# Create a directory for your TM351 work
mkdir -p /Users/MyUser/TM351VCE

# Change directory to your TM351VCE directory
cd /Users/MyUser/TM351VCE

# Launch the container with shared directories mounted from your TM351VCE directory
docker run --name tm351vce --rm -d -p 8351:8888 -v "$PWD/TM351VCE/notebooks:/home/jovyan/notebooks" -v "$PWD/TM351VCE/openrefine_projects:/home/jovyan/openrefine" -e JUPYTER_TOKEN="letmein" ousefuldemos/tm351-binderised:latest
```

*(The quotes round the volume mount cope with spaces in the `$PWD` directory path)*

Rather than using the mounting directories relative to the current directory (`$PWD`) the `docker run` command is run in, we could also specify a mounted directory using an absolute path, such as `"/Users/MyUser/TM351VCE/notebooks:/home/jovyan/notebooks"`.

This will serve the container on `http://localhost:8351` and share folders from the `TM351VCE` folder in the current directory; login with the token `letmein` or whatever token you set.

If you want to update a legacy container to use an updated image, you need to stop and remove/delete the original container and then rerun the `docker run` command:

```
docker stop tm351vce
docker rm tm351vce
```
If you do delete the container, shared volume files will be preserved on host and mounted back into the new container, but any changes you made to the initial of the original container, such as installing additional Python packages or making changes to database tables, will be lost.

On Windows, first create a directory `C:\Users\MyUser\TM351VCE`. In the command prompt, change directory to your `C:\Users\MyUser\TM351VCE` directory and start the container using a command of the form:

`docker run --name tm351vce -d -p 35180:8888 -v $pwd\notebooks:/home/jovyan/notebooks -v $pwd\openrefine_projects:/home/jovyan/openrefine -e JUPYTER_TOKEN="letmein" ousefuldemos/tm351-binderised:latest`
 
You can also specify volume bindings using an absolute path to a directory on the host computer, rather than a path relative to the current directory (`$pwd`) that the `docker run` command is executed in, using a volume mount command of the form `-v c:\Users\MyUser\TM351VCE\notebooks:/home/jovyan/notebooks`.

In order to access the notebook server via your browser, you will need to find the token used to access the notebook server. Use the one you set and passed in via the `JUPYTER_TOKEN=` assignment in the docker command, or look up the token by running:

`docker exec -it tm351vce jupyter notebook list`

This will display something along the lines of:

`Currently running servers:
http://0.0.0.0:8888/?token=dca25d6755dbd2a1c9b346dca3b8c839e44c9271e20bc416 :: /home/jovyan`

Use the token value to log in to the server.

The run command will create a notebooks directory in the directory you issued the run command from, and then share it into the `notebooks` folder that you can see from the notebook server homepage. OpenRefine projects are also shared between your local machine and the container.

Files that exist outside the `/home/jovyan/notebooks` and `/home/jovyan/openrefine` directory paths in the container (which is to say, outside the `notebooks` and `openrefine` directories viewable from the notebook server homepage, *will not be shared to your local desktop*.

The container can also be launched directly using [`containds`](https://containds.com/), the desktop app for running notebook containers and a personal, local Binder service. Select a new image and search for `tm351`; the `ousefuldemos/tm351-binderised` image is the one you want. When prompted, select the "standard" launch route, NOT the 'Try to start Jupyter notebook' route.
