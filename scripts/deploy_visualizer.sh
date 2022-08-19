#!/bin/bash

VISUALIZER_PATH=../subsystem4_visualization/GENEA_Visualizer/celery-queue/
sudo docker build $VISUALIZER_PATH -f $VISUALIZER_PATH/Dockerfile-standalone -t visualizer
sudo docker run -dit -v ${PWD}/../data:/app/wasp/data -v ${PWD}/../scripts:/app/wasp/scripts visualizer