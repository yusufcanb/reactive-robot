from multiprocessing import cpu_count

MAX_WORKER = cpu_count() * 2
EVENT_PAYLOAD_VARIABLE = "REACTIVE_ROBOT_RECEIVED_MSG"
