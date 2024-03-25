FROM selenium/standalone-chrome

USER root 

RUN apt-get update && apt-get install -y python3-pip python3-dev && \
    ln -s /usr/bin/python3 /usr/bin/python && \
    pip3 install --upgrade pip

WORKDIR /app

COPY . /app

RUN pip --no-cache-dir install -r requirements.txt

CMD ["python3", "/app.py"]