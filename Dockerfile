FROM ubuntu
FROM python:3.11

WORKDIR /mumble-ai-bot

COPY requirements.txt .
COPY ./src .

RUN pip install -r requirements.txt

RUN apt-get -y update
RUN apt-get -y install espeak
RUN apt-get -y install openssl
RUN apt-get -y install ffmpeg
RUN apt-get -y install libopus0

CMD ["python", "./mumblebot.py"]










