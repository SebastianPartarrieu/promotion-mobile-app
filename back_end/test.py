#! /usr/bin/env python3
#
# Test against a running local kiva server, including expected failures.
#
# The test assumes some initial data and resets the database
# to the initial state, so that it can be run several times
# if no failure occurs.
#
# The test could initialiaze some database, but I also want to
# use it against a deployed version and differing databases,
# so keep it light.

import re
from os import environ as ENV
from typing import Dict, Union, Tuple

# local flask server test by default
URL = ENV.get('APP_URL', 'http://0.0.0.0:5000')

# real (or fake) authentication
ADMIN, WRITE, READ, NONE = 'promotion', 'calvin', 'hobbes', 'moe'
AUTH: Dict[str, Union[str, None]] = {}
if 'APP_AUTH' in ENV:
    # we are running with a real server with authentication
    for up in ENV['APP_AUTH'].split(','):
        user, pw = up.split(':', 2)
        AUTH[user] = pw
    real_auth = True
else:
    # else we assume 3 test users
    AUTH[ADMIN] = None
    AUTH[WRITE] = None
    AUTH[READ] = None
    AUTH[NONE] = None
    real_auth = False

# reuse connections…
from requests import Session
requests = Session()

#
# Convenient function to send an http request and check the result with a re
#
# Note: the "login" parameter special handling allows to run auth tests on a
# local server without actual authentication. By default, ADMIN is assumed, use
# None to skip auth.
#
# check_api(method: str,         # 'GET', 'POST', 'PUT', 'PATCH', 'DELETE'
#           path: str,           # '/some/url'
#           status: int,         # 200, 201, 204, 400, 401, 403, 404…
#           content: str,        # regexpr to match: r'\[.*\]', r'"calvin"'…
#           login: str,          # auth: login=ADMIN (defaut), WRITE or READ
#           data: Dict[str,str], # http parameters: data={"id": "calvin, …}
#           json: Dict[str,str]) # json parameters: json={"id": "hobbes", …}
#
# Examples:
#
#    check_api("PUT", "/store", 405)
#    check_api("GET", "/store", 200, r'"hobbes"')
#    check_api("POST", "/store", 201, data={"key": "Roméo", "val": "Juliette"})
#    check_api("POST", "/store", 201, json={"key": "Roméo", "val": "Juliette"})
#    check_api("DELETE", "/store", 204)
#
def check_api(method: str, path: str, status: int, content: str = None,
              login: str = ADMIN, **kwargs):
    # work around Werkzeug inability to handle authentication transparently
    auth: Union[Tuple[str, Union[str, None]], None] = None
    if login is not None:
        if real_auth:
            # real http server which handles authentication
            auth = (login, AUTH[login])
        else:
            # test against local http server, apply work around
            if 'json' in kwargs:
                kwargs['json']['LOGIN'] = login
            elif 'data' in kwargs:
                kwargs['data']['LOGIN'] = login
            else:
                kwargs['data'] = {'LOGIN': login}
    else:
        auth = None
    r = requests.request(method, URL + path, auth=auth,
                         **kwargs)  # type: ignore
    assert r.status_code == status
    if content is not None:
        assert re.search(content, r.text, re.DOTALL) is not None
    return r.text

# sanity check
def test_sanity():
    assert re.match(r"https?://", URL)
    assert ADMIN in AUTH
    assert WRITE in AUTH
    assert READ in AUTH
    assert NONE in AUTH

# /whatever # BAD URI
def test_whatever():
    check_api('GET', '/whatever', 404)
    check_api('POST', '/whatever', 404)
    check_api('DELETE', '/whatever', 404)
    check_api('PUT', '/whatever', 404)
    check_api('PATCH', '/whatever', 404)

# /version
def test_version():
    # only GET is implemented
    check_api('GET', '/version', 200, '"promotion"', login=ADMIN)
    check_api('GET', '/version', 200, '"promotion"', login=WRITE)
    check_api('GET', '/version', 200, '"promotion"', login=READ)
    # check_api('GET', '/version', 403, '"kiva"', login=NONE)
    check_api('POST', '/version', 405)
    check_api('DELETE', '/version', 405)
    check_api('PUT', '/version', 405)
    check_api('PATCH', '/version', 405)


### FRONT PAGE QUERIES 

# GET /promotion with filter for number of promotions returned and for agglomeration
def test_1():
    check_api('GET', '/promotion', 200, data={"nb": 3, "agglomeration": "Paris"})
    check_api('GET', '/promotion', 200, data={"agglomeration": "Paris"})
    check_api('GET', '/promotion', 200, data={"nb": 3, "agglomeration": "Caen"})
    check_api('GET', '/promotion', 200, data={"nb": 3})
    check_api('GET', '/promotion', 200)

# GET /client
#def test_2():
 #   check_api('GET', '/client', 200, data={})

### ACCOUNT RELATED QUERIES

### INTERACTION WITH FRONT PAGE

### SECOND PAGE - MAP - QUERIES

### THIRD PAGE - LISTS - QUERIES 