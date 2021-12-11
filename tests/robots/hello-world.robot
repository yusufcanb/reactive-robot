*** Settings ***
Library                 RequestsLibrary
Library                 Process
Suite Setup             Log to Console           ${REACTIVE_ROBOT_RECEIVED_MSG}

*** Variable ***
${PORT}                 1234
${CMD}                  docker images

*** Tasks ***

Quick Get Request Test
      Log           ${REACTIVE_ROBOT_RECEIVED_MSG}
      ${result} =	Run Process  ${CMD}  shell=True  timeout=1min  on_timeout=continue
      Log           ${result.stdout}