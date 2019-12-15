# text2speech
This is basically the steps listed on Mozilla's TTS [Released Models](https://github.com/mozilla/TTS/wiki/Released-Models) wiki. The goal is to provide an image with everything you need to turn text into audio using the built-in [server](https://github.com/mozilla/TTS/tree/master/server).

You can run this image from docker using:
~~~~bash
docker run --gpus all -d -p 5002:5002 --tmpfs /tmp kai5263499/text2speech
~~~~

There are 3 ways to send text to the server and recieve a wav file in response:
~~~~bash
curl -s "http://localhost:5002/api/tts?text=This%20is%20my%20text" -o response.wav
curl -s -X POST -d "text=This is my text" "http://localhost:5002/api/tts" -o response.wav
curl -s -F 'file=@localfilename.txt' "http://localhost:5002/api/tts_upload" -o response.wav
~~~~
