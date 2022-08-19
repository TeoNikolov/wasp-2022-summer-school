#!/bin/bash

MODEL_PATH=../subsystem3_gesture-generation/networks/Audio2Gestures/
sudo docker build $MODEL_PATH -t wasp-gg
sudo docker run -dit \
	-v ${PWD}/../data:/app/wasp/data \
	-v ${PWD}/../scripts:/app/wasp/scripts \
	-v ${PWD}/../subsystem3_gesture-generation/dataset/:/app/wasp/dataset \
	-v ${PWD}/../subsystem3_gesture-generation/models/:/app/wasp/models \
	wasp-gg