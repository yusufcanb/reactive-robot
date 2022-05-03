*** Settings ***
Library   reactive_robot/lib.py

*** Tasks ***
Demo Task
    ${topic}=   Get Reactive Robot Topic
    ${payload}=   Get Reactive Robot Payload
    Log  ${topic}
    Log  ${payload}
    Log Variables
