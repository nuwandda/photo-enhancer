FROM nvidia/cuda:11.8.0-cudnn8-runtime-ubuntu22.04

ARG DEBIAN_FRONTEND=noninteractive

WORKDIR /usr/app

RUN apt-get update
RUN apt-get install python3.10 -y
RUN apt-get install python-is-python3 -y
RUN apt-get install pip -y
RUN apt-get install git -y
RUN apt-get install git-lfs
RUN apt-get install curl -y
RUN apt-get install ffmpeg -y
RUN apt-get install wget

COPY requirements.txt /usr/app/requirements.txt
RUN pip install --upgrade pip
RUN pip install -r requirements.txt
RUN pip install typing-extensions==4.9.0 --upgrade
ENV ENHANCE_METHOD='gfpgan'
ENV BACKGROUND_ENHANCEMENT='True'
ENV UPSCALE=2
COPY . .

CMD ["uvicorn", "app:app", "--proxy-headers", "--host", "0.0.0.0", "--port", "80", "--workers", "3"]