build-image:
	docker build -t kai5263499/text2speech .

exec-interactive:
	docker run \
	--gpus all \
	-it --rm \
	-p 5002:5002 \
	--tmpfs /tmp \
	-v ${PWD}/server.py:/usr/local/lib/python3.6/dist-packages/TTS/server/server.py \
	--entrypoint bash \
	kai5263499/text2speech

run-image:
	docker run \
	--gpus all \
	-d \
	-p 5002:5002 \
	--tmpfs /tmp \
	kai5263499/text2speech