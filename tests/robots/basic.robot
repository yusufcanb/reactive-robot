*** Settings ***
Library   reactive_robot/lib.py

*** Tasks ***
Demo Task
    ${payload}=   Get Reactive Robot Payload
    Log To Console  ${payload}
    Log Variables
