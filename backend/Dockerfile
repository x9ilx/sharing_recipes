FROM python:3.9
WORKDIR /app

COPY requirements.txt .

RUN apt update
RUN dpkg --configure -a && apt install -y python3

RUN pip install -r /app/requirements.txt --no-cache-dir

COPY . .

RUN chmod +x /app/start_server.sh

CMD "/app/start_server.sh"
