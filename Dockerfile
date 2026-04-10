FROM python:3.10-slim

WORKDIR /app
RUN apt-get update && apt-get install -y git wget pv jq python3-dev ffmpeg mediainfo
COPY . .
RUN pip3 install -r requirements.txt

CMD python3 main.py
