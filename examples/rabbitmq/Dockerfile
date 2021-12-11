FROM python:3.10-slim

WORKDIR /opt/service

# project setup
COPY . /opt/service
RUN pip install -r requirements.txt

# reactive-robot setup
RUN pip install reactive-robot

CMD ["python3", "-m", "reactive_robot", "serve"]