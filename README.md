# WASP Summer School 2022

- [Welcome](#welcome)
- [Installation](#installation)
  * [Prerequisites](#prerequisites)
  * [Cloning the repository](#cloning-the-repository)
  * [Setting up the pipeline](#setting-up-the-pipeline)
  * [Remarks](#remarks)
- [Next steps](#next-steps)

<small><i><a href='http://ecotrust-canada.github.io/markdown-toc/'>Table of contents generated with markdown-toc</a></i></small>


## Welcome

This repository hosts the full pipeline code for the WASP summer school 2022 group assignments. The system contains four major components, with corresponding resources broken down into the following folders:

- Generating text with a text prompt : `./subsystem1_text-generation/`
- Synthesizing speech from text : `./subsystem2_text-to-speech/`
- Generating gesture animations from audio : `./subsystem3_gesture-generation/`
- Visualizing the generated gestures : `./subsystem4_visualization/`
 
In addition, there are two folders in the repository root which are used for storing data files for the pipeline, as well as scripts for running different components of the system. These folders are `./data/` and `./scripts/`, with demo files showing the intended output of the pipeline residing in `./data/demo/`.

## Installation

### Prerequisites

To work with the pipeline, you need to install the following on your machine before continuing with the rest of the setup:

- [git](https://git-scm.com/downloads)
- [Docker Desktop](https://docs.docker.com/get-docker/) v4.7.0 or later
- [Windows Subsystem for Linux](https://docs.microsoft.com/en-us/windows/wsl/install) if on Windows
- [Unreal Engine 4.25.4](https://www.unrealengine.com/en-US/download)

### Cloning the repository

To clone the repository, run this in your shell:

- `git clone https://github.com/TeoNikolov/wasp-2022-summer-school.git`
- `cd wasp-2022-summer-school`

The repository makes of [submodules](https://git-scm.com/book/en/v2/Git-Tools-Submodules) to include code from other repositories into this one without copying over the code files. To set up the submodules, write the following :

- `git submodule update --init`

### Setting up the pipeline

Subsystem 3 and subsystem 4 both use software that can be ran using Docker. This allows the us to easily set up a working environment with all necessary dependencies, minimizing the risk of running into issues during the process. The script `./scripts/deploy.sh` is provided to automate the process of deploying the Dockerized solutions of multiple applications. Run the script like this:

- Make sure Docker Desktop is running!
- `cd ./scripts/`
- `bash ./deploy.sh`

The script will build and deploy several Docker containers, as well as mount relevant folders so that they can be accessed within the containers. This process could take a while, so why not check this cool [fluid simulator](https://paveldogreat.github.io/WebGL-Fluid-Simulation/) out in the meantime?

When ready,  verify that the containers are deployed by running `docker ps` and looking for the following `IMAGE` strings:

- `wasp-gg` (subsystem 3 - Audio2Gestures)
- `visualizer` (subsystem 4 - GENEA_Visualizer)

Also take note of the `CONTAINER ID`, as it will be needed to run some of the scripts in `./scripts/` from within the Docker containers.

### Remarks

- It is possible that some commands fail due to lack of privilege. If this happens, please write `sudo` at the beginning of your commands.
- All file system paths in this document (and documents inside the subsystem folders) are relative to the repository root.

## Next steps

You should now have all relevant software installed, as well as Docker containers set up and running. You are now ready to begin working on your assignments, which you will know more about from the tutorials presented to you during the summer school.

Let us know if you need any help. **Good luck and have fun!**

[Back to top](#wasp-summer-school-2022)
