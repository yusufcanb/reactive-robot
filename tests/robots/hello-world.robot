*** Settings ***
Library                 RequestsLibrary
Library                 Process
Suite Setup              Log to Console           ${TEST_VAR}

*** Variable ***
${PORT}                 1234
${CMD}                  docker images

*** Tasks ***

Quick Get Request Test
      Log           ${TEST_VAR}
      ${result} =	Run Process  ${CMD}  shell=True  timeout=1min  on_timeout=continue
      Log           ${result.stdout}