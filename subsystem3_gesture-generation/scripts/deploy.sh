MODEL_PATH=../networks/Audio2Gestures/

sudo docker build $MODEL_PATH -t wasp-gg
sudo docker run -dit -v ${PWD}/..:/app/wasp wasp-gg