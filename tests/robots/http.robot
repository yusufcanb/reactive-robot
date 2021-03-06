*** Settings ***
Library                 RequestsLibrary

*** Tasks ***

Quick Get Request Test
    ${response}=        GET         https://jsonplaceholder.typicode.com/posts/1

Quick Get Request With Parameters Test
    ${response}=    GET  https://jsonplaceholder.typicode.com/posts/1  params=query=ciao  expected_status=200

Quick Get A JSON Body Test
    ${response}=    GET  https://jsonplaceholder.typicode.com/posts/1
    Should Be Equal As Strings    1  ${response.json()}[id]
