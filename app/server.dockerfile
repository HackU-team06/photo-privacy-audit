FROM tiangolo/uvicorn-gunicorn-fastapi:python3.10

RUN apt-get update && apt-get upgrade -y &&\
    apt-get install -y libgl1-mesa-dev &&\
    apt-get clean && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY ./requirements.txt /app/requirements.txt
RUN pip install -r /app/requirements.txt

COPY . /app
