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

from requests import Session
import re
from os import environ as ENV
from typing import Dict, Union, Tuple
import json

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
    r = requests.request(
        method,
        URL + path,
        auth=auth,
        **kwargs)  # type: ignore
    assert r.status_code == status
    if content is not None:
        assert re.search(content, r.text, re.DOTALL) is not None
    return r.text


# def check_api_authorization

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


# FRONT PAGE QUERIES

# GET /promotion with filter for number of promotions returned and for
# agglomeration
def test_1():
    check_api(
        'GET',
        '/promotion',
        200,
        data={
            "nb": 3,
            "agglomeration": "Paris"})
    check_api('GET', '/promotion', 200, data={"agglomeration": "Paris"})
    check_api(
        'GET',
        '/promotion',
        200,
        data={
            "nb": 3,
            "agglomeration": "Caen"})
    check_api('GET', '/promotion', 200, data={"nb": 3})
    check_api('GET', '/promotion', 200)

# GET /commerce with filter for categories and agglomeration


def test_2():
    check_api(
        'GET',
        '/commerce',
        200,
        data={
            "categorie": "restaurant",
            "agglomeration": "Paris"})
    check_api('GET', '/commerce', 200, data={"categorie": "restaurant"})
    check_api('GET', '/commerce', 200, data={"agglomeration": "Paris"})
    check_api('GET', '/commerce', 200)

# GET /promotion/<pid>


def test_3():
    check_api('GET', '/promotion/1', 200)

# ACCOUNT RELATED QUERIES
# Get client info, signup and patch client info

### Authentication and authorization


def test_AA_workflow_client():
    check_api(
        'POST',
        '/signup',
        201,
        data={
            "clnom": "Partarrieu",
            "clpnom": "Sebastian",
            "clemail": "s.a.partarrieu@gmail.com",
            "aid": 3,
            "clmdp": "pass"})
    check_api(
        'POST',
        '/signup',
        400,
        data={
            "clnom": "Partarrieu",
            "clpnom": "Sebastian",
            "clemail": "s.a.partarrieu@gmail.com",
            "aid": 3,
            "clmdp": "pass"})

    response = json.loads(check_api(
        'GET',
        '/login',
        200,
        data={
            "clemail": "s.a.partarrieu@gmail.com",
            "clmdp": "pass"}))
    auth_token = response['token']

    check_api(
        'GET',
        '/login',
        401,
        data={
            "clemail": "s.a.partarrieu@gmail.com",
            "clmdp": "passworddd"})
    # for some reason escape characters are added to the auth_token when we
    # fetch text from response in check_api
    check_api('GET', '/myclient', 200,
              data={'token': auth_token})
    check_api('GET', '/myclient', 401, data={'token': ''})
    check_api('PATCH', '/myclient', 201,
              data={'clpnom': 'Sebby', 'token': auth_token})
    check_api('PUT', '/myclient', 201,
              data={"clnom": "PARTARRIEU", 'token': auth_token})


def test_AA_workflow_commerce():
    check_api('POST', '/signupcommerce', 201, data={'cnom': 'Fromager Saint Louis',
                                                          'cpresentation': 'Vend du fromage de bonne qualité',
                                                          'cemail': 'fromager@fromage.com',
                                                          'code_postal': 75005,
                                                          'rue_and_num': '80 Boulevard Saint-Michel',
                                                          'aid': 1,
                                                          'cmdp': 'dubonfromage', 'catnom': 'Restaurant,Textile'})
    check_api('POST', '/signupcommerce', 400, data={'cnom': 'Fromager Saint Louis',
                                                    'cpresentation': '',
                                                    'url_ext': 'fromager@fromage.com',
                                                    'code_postal': 75005,
                                                    'rue_and_num': '80 Boulevard Saint-Michel',
                                                    'aid': 1,
                                                    'cmdp': 'dubonfromage', 'catnom': 'Restaurant,Textile'})
    check_api('POST', '/signupcommerce', 400, data={'cnom': 'Fromager Saint Louis',
                                                    'cpresentation': '',
                                                    'code_postal': 75005,
                                                    'rue_and_num': '80 Boulevard Saint-Michel',
                                                    'aid': 1,
                                                    'cmdp': 'dubonfromage', 'catnom': 'Restaurant,Textile'})
    response = json.loads(check_api(
        'GET',
        '/logincommerce',
        200,
        data={
            'cemail': 'fromager@fromage.com',
            'cmdp': 'dubonfromage'}))
    auth_token = response['token']
    check_api('PATCH', '/mycommerce', 201,
              data={'cnom': 'Fromager Saint Jacques', 'token': auth_token})
    check_api('PUT', '/mycommerce', 201,
              data={'cpresentation': 'Fromage frais', 'token': auth_token})
    pid = check_api('POST', '/promotion', 201, data={'token': auth_token, 'pdescription': 'Du fromage pas cher', 'tdebut': '2020-01-25', 'tfin': '2020-01-30'})
    check_api('PATCH', '/promotion/'+ str(pid), 201, data={'token': auth_token, 'pdescription':'Du bon fromage', 'tfin': '2020-04-16'})

# Login with email and password


# INTERACTION WITH FRONT PAGE

# SECOND PAGE - MAP - QUERIES

# THIRD PAGE - LISTS - QUERIES

# INTERFACE COMMERCE
def test_6():
    check_api(
        'POST',
        '/signupcommerce',
        201,
        data={
            "cnom": "ZARA1",
            "cpresentation": "voila zara",
            "cemail": "zara1@hotmail.com",
            "aid": 1,
            "cmdp": "zarapassword",
            "rue_and_num": "270 rue saint jacques",
            "code_postal": 75004,
            "url_ext": "xyz",
            "catnom": "Textile,Restaurant"})
    check_api(
        'POST',
        '/signupcommerce',
        400,
        data={
            "cnom": "ZARA1",
            "cpresentation": "voila zara",
            "cemail": "zara1@hotmail.com",
            "aid": 1,
            "cmdp": "zarapassword",
            "rue_and_num": "270 rue saint jacques",
            "code_postal": 75004,
            "url_ext": "xyz",
            "catnom": "Textile,Restaurant"})


def test_7():
    check_api('GET', '/logincommerce', 200, data={"cemail": "zara1@hotmail.com", "cmdp": "zarapassword"})
    check_api('GET', '/logincommerce', 401, data={"cemail": "zara1@hotmail.com", "cmdp": "passworddd"})

def test_8():
    check_api('PATCH','/promotion/1/image',204, data={"imageImid":'1,2', "imageRanks":'2,1'})
    check_api('PATCH','/promotion/1/image',400, data={"imageImid":'1,2', "imageRanks":'1,1'})
