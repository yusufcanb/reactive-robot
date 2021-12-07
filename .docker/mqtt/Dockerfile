FROM eclipse-mosquitto:latest

COPY mosquitto.conf /mosquitto/config/mosquitto.conf


EXPOSE 9001 1881 1883
CMD [ "/usr/sbin/mosquitto", "-c", "/mosquitto/config/mosquitto.conf" ]