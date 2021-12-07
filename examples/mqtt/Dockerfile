FROM robotframework/rfdocker

WORKDIR /opt/service

# project setup
COPY . /opt/service
RUN pip install -r requirements.txt

# reactive-robot setup
RUN pip install reactive-robot

CMD ["python", "-m", "reactive-robot", "serve"]