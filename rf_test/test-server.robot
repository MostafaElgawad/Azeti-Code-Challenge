*** Settings ***
Library  RequestsLibrary

*** Variables ***
${URL}            http://server:80

*** Test Cases ***
Asking for 'life;universe;everything' give us 42
    [Documentation]  This test case sends a GET request {life;universe;everything} to the /answer endpoint and checks the response is 42.
    # Implement a proper test that will:
    # - Send a GET request to the server, on the resource `/answer`, with
    # the following value on the `search` parameter: life;universe;everything
    # - Ensure the server replied with 200 error code
    # - Ensure the server replied 42
    # Create Session    server    ${URL}
    ${body}=    Create Dictionary    search=life;everything;universe
    ${response}=    GET    ${URL}/answer    params=${body}    expected_status=200
    Should Be Equal As Strings    ${response.text}    42

Asking for something else give us unknown
    # Implement a proper test that will:
    # - Send a GET request to the server, on the resource `/answer`, with
    # the following value on the `search` parameter: the truth
    # - Ensure the server replied with 404 error code
    # - Ensure the server replied unknown
    # Note: You can also ask other things, but we don't think it will be able
    # to give a good answer.
