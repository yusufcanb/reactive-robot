*** Settings ***

Library   reactive_robot/lib.py

*** Tasks ***
Package should have a keyword named <<Get Reactive Robot Payload>> 
    Keyword Should Exist    Get Reactive Robot Payload    


Package should have a keyword named <<Get Reactive Robot Topic>>
    Keyword Should Exist    Get Reactive Robot Topic
