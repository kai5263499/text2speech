FROM ubuntu:18.04

LABEL MAINTAINER="Wes Widner <kai5263499@gmail.com>"

EXPOSE 5002

RUN apt-get update && \
    apt-get install -y espeak libsndfile1 wget python3-pip unzip && \
    pip3 install https://github.com/reuben/TTS/releases/download/t2-ljspeech-mold/TTS-0.0.1+b6b513f-py3-none-any.whl

COPY ./server.py /usr/local/lib/python3.6/dist-packages/TTS/server/server.py

ENTRYPOINT [ "/usr/bin/python3 -m TTS.server.server" ]