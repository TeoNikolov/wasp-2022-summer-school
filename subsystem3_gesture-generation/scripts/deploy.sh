MODEL_PATH=../networks/Audio2Gestures/

docker build $MODEL_PATH -t wasp-gg
docker run -dit -v ${PWD}/..:/app/wasp wasp-gg