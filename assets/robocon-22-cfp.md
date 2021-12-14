**Title**

Reactive Robot - Fastest way to turn Robot Framework projects into event-driven services

--------------------

**Abstract**

With microservices, we see that event-driven designs find more applications in information systems.
The `reactive-robot` project aims to integrate robots into event-driven systems with minimal effort.

------------------------

**Description**

Nowadays, many modern application designs are event-driven and
this architecture enables minimal coupling, which makes it a good option for distributed applications.

Robot Framework is really powerful tool for automation and with Reactive Robot project any Robot Framework
project can turn into event-driven services with built-in connectors for widely used message producers
like Kafka, RabbitMQ or MQTT brokers to build effective and flexible automation services.

Reactive Robot project aims to minimize the effort of service creation using single definition file with YAML format 
called `reactive-robot.yaml`. This definition file contains all information about the service like which message producer
to connect or what is the host and port of the producer. Also, the definition file contains list of bindings which is 
connect the topics to robot files. With this method, message that come from certain topic triggers the execution of 
the robot file with event message assigned to pre-defined variable named `REACTIVE_ROBOT_INCOMING_MSG`.

-----------------------------

