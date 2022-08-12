<style type="text/css" rel="stylesheet">
	.indent {
		color: red;
	}
</style>

# Subsystem 3: Gesture Generation

## Installation Instructions

### Setting up the Docker environment
The gesture generation subsystem implements a single gesture model called `Audio2Gestures`. This model is located in `./networks/Audio2Gestures/`, and is maintained in a separate [GitHub repository](https://github.com/teonikolov/Speech_driven_gesture_generation_with_autoencoder/tree/GENEA_2022) (a fork of the [original repository](https://github.com/genea-workshop/Speech_driven_gesture_generation_with_autoencoder/tree/GENEA_2022)). This model has an integration with Docker to automate the process of setting up a working environment, in which the model can be trained and used to predict gestures from raw audio.

The script `./scripts/deploy.sh` runs the necessary commands to leverage the Docker integration of the gesture model. The script first builds a Docker image by setting up a guest OS and collecting necessary dependencies, followed by deploying a Docker container in which the gesture model is encapsulated. In addition, the folder `./subsystem3_gesture-generation/` is mounted to `/app/wasp/` in the container's filesystem, so that pre-processed dataset files inside `./dataset/`, and pre-trained models inside `./models/`, can be accessed from within the Docker container. The model needs these files to predict gestures.

Set up the Docker environment as such:

1. Make sure you have Docker [installed on your machine](https://docs.docker.com/get-docker/) and that it is running.
3. `cd ./scripts/` and call either:
	- `bash ./deploy.sh --gpu` if you have a CUDA-enabled GPU and drivers on your computer
	- `bash ./deploy.sh` if you do not have a CUDA-enabled GPU and drivers on your computer
4. Wait for Docker to set up the environment and deploy the container. This could take a while, so why not check this cool [fluid simulator](https://paveldogreat.github.io/WebGL-Fluid-Simulation/) out in the meantime?

### Interacting with the gesture model

If everything went well, you will now have a Docker container with the gesture model, running in the background. You can verify that this is the case by running `docker ps` in your shell, and searching for a container whose `IMAGE` says `"wasp-gg"`. To interact with the gesture model, open a shell inside the Docker container by running

&nbsp;&nbsp;&nbsp;&nbsp;`docker exec -it <container_ID> /bin/bash`

in your shell, replacing `<container_ID>` with the ID of the container, which you can find with the `docker ps` command.

To predict gestures, you can use the supplied `./scripts/batch_jobs.py` script, located in `/app/wasp/scripts/` inside the Docker container. Navigate to the location with `cd /app/wasp/scripts/` and invoke the script with Python:

&nbsp;&nbsp;&nbsp;&nbsp;`python batch_jobs.py --predict --pipeline_dir "../../example_scripts/pipeline.py"`

where `--predict` indicates that we wish to predict gestures, and `--pipeline_dir` points to the location of the `pipeline.py` script that is responsible for invoking lower-level scripts when running the gesture model. With the current implementation of the `batch_jobs.py` script, raw audio files from `./dataset/demo/` will be used to predict gestures, whose BVH data will be output to `./dataset/100/output/`.

---

notes
indicate mounted dir, and specify paths and directories in relation to that dir (that is, once we get in docker container, we do not leave it when dealing with files)
