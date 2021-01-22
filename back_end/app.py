#! /usr/bin/env python3
import logging as log
log.basicConfig(level=log.INFO)

import datetime as dt
started = dt.datetime.now()

# get running version information
with open("VERSION") as VERSION:
    branch, commit, date = VERSION.readline().split(" ")

# start flask service
from flask import Flask, jsonify, request, Response
import imghdr
#from PIL import Image
from werkzeug.utils import secure_filename
import os
import secrets

app = Flask("promotion")

# load configuration, fall back on environment
from os import environ as ENV

# added imports - token based auth and hash for password storage
from werkzeug.security import generate_password_hash, check_password_hash
import jwt
import re #will be useful

if "APP_CONFIG" in ENV:
    app.config.from_envvar("APP_CONFIG")
    CONF = app.config  # type: ignore
else:
    CONF = ENV  # type: ignore

# create $database connection and load queries
import anodb  # type: ignore
db = anodb.DB(
    CONF["DB_TYPE"], CONF["DB_CONN"], CONF["DB_SQL"], CONF["DB_OPTIONS"]
)

#
# Request parameters as a dict, in json, form or args
#

PARAMS = {}

def set_params():
    global PARAMS
    PARAMS = request.values if request.json is None else request.json

app.before_request(set_params)

def do_commit(res: Response):
    global db
    db.commit()
    return res

app.after_request(do_commit)


#
# AAA: Authentication, Authorization and Audit
#
# Authentication and Audit are rightfully delegated to the web server.
# However, the development server associated to flask (Werkzeug)
# does not know how to do Authentication:-(
# The usual flask solution is to handle it in flask itself,
# which is a poor choice because it is inefficient.
# The work around is that *under testing*, the `LOGIN`
# parameter is accepted as a login claim, and tests can take
# advantage of this.
#
# Sigh.
#
# LOGIN is set through a hook:
#
LOGIN: str = ""

if CONF.get("TESTING", False):
    def set_login():
        assert CONF["TESTING"]
        assert request.remote_user is None
        assert request.environ["REMOTE_ADDR"] == "127.0.0.1"
        global LOGIN
        LOGIN = PARAMS.get("LOGIN", None)
        log.info(f"LOGIN: {LOGIN}")
else:
    def set_login():
        global LOGIN
        LOGIN = request.remote_user

app.before_request(set_login)

### Tests for authentication based on JWT (Json Web tokens)

if CONF.get("SECRET_KEY", False):
    global SECRET_KEY
    SECRET_KEY = CONF["SECRET_KEY"] #for JWTs

def encode_auth_token(user_id, user_type='client'):
    '''
    Generates the Auth token (string).
    Given a user_id, return token
    '''
    try:
        payload = {
            'exp': dt.datetime.utcnow() + dt.timedelta(days=1, seconds=5),
            'iat': dt.datetime.utcnow(),
            'sub': user_id,
            'ust': user_type
        }
        return jwt.encode(
            payload,
            SECRET_KEY,
            algorithm='HS256'
        )
    except Exception as e:
        return e

def decode_auth_token(auth_token):
    '''
    Decodes an auth token which will be sent with http requests from FE
    param: auth_token
    return: integer and string or string
    '''
    try:
        payload = jwt.decode(auth_token, SECRET_KEY, algorithms="HS256")
        return payload['sub'], payload['ust'] #user_id and type (client, commerce, ...)
    except jwt.ExpiredSignatureError:
        return 'Signature Expired. Please log in again!'
    except jwt.InvalidTokenError:
        return 'Invalid token. Please log in again.'

def is_authorized(auth_token, user_id, user_type='client'):
    '''
    Given an auth_token and a user_id tells whether the token is one of a
    client and is valid.
    param: auth_token and user_it(int)
    return: bool
    '''
    if auth_token == '':
        return False
    elif decode_auth_token(auth_token) == 'Signature Expired. Please log in again!':
        return False
    elif decode_auth_token(auth_token) == 'Invalid token. Please log in again.':
        return False
    else:
        user_id_received, user_type_received = decode_auth_token(auth_token)
        if str(user_type_received) != user_type:
            return False
        elif int(user_id_received) != int(user_id):
            return False
        else:
            return True

#
# GET /version
#
# general information about the application
#

@app.route("/version", methods=["GET"])
def get_version():
    # TODO check read permission
    now = db.now()[0][0]
    return jsonify(
        {
            "app": app.name,
            "variant": "anodb",
            "version": 4,
            "db": CONF["DB_TYPE"],
            "started": str(started),
            "user": LOGIN,
            "branch": branch,
            "commit": commit,
            "date": date,
            "now": now,
        }
    )

### FRONT PAGE QUERIES 

# GET /promotion with filter for number returned, agglomeration and categories
@app.route("/promotion", methods=["GET"])
def get_promotion():
    cat = PARAMS.get("categorie", '%')
    agglo = PARAMS.get("agglomeration", '%')
    nb = PARAMS.get("nb", 100) #arbitraire
    cat = cat.split(',')
    if len(cat) == 1:
        res = db.get_promotion(agg=agglo, nb=nb, cat=cat[0])
    else:
        res = []
        for x in cat:
            res.append(db.get_promotion(agg=agglo, nb=nb, cat=x))
    return jsonify(res)


# GET /commerce with filter for categorie and agglomeration
@app.route("/commerce", methods=["GET"])
def get_commerce():
    cat = PARAMS.get("categorie", '%')
    agglo = PARAMS.get("agglomeration", '%')
    res = db.get_commerce(agg=agglo, cat=cat)
    return jsonify(res)

### INTERACTION WITH FRONT PAGE
@app.route('/promotion/<int:pid>', methods=["GET"])
def get_promotion_info(pid):
    res = db.get_promotion_info(pid=pid)
    return jsonify(res)

### ACCOUNT RELATED QUERIES
@app.route('/client/<int:clid>', methods=["GET"])
def get_client_info(clid):
    auth_token = PARAMS.get("token", '')
    if is_authorized(auth_token, user_id=clid, user_type='client'):
        res = db.get_client_info(clid=clid)
        return jsonify(res)
    else:
        return Response(status=401)

@app.route('/client/<int:clid>', methods=["PATCH", "PUT"])
def patch_client_info(clid):
    auth_token = PARAMS.get("token", '')
    if is_authorized(auth_token, user_id=clid, user_type='client'):
        clnom, clpnom = PARAMS.get("clnom", None), PARAMS.get("clpnom", None)
        clemail, aid = PARAMS.get("clemail", None), PARAMS.get("aid", None)
        if clnom != None:
            db.patch_client_nom(clnom=clnom, clid=clid)
        if clpnom != None:
            db.patch_client_pnom(clpnom=clpnom, clid=clid)
        if clemail != None:
            db.patch_client_clemail(clemail=clemail, clid=clid)
        if aid != None:
            db.patch_client_aid(aid=aid, clid=clid)
        return Response(status=201)
    else:
        return Response(status=401)

@app.route('/signup', methods=["POST"])
def post_client_info():
    clnom, clpnom = PARAMS.get("clnom", None), PARAMS.get("clpnom", None), 
    clemail, aid = PARAMS.get("clemail", None), PARAMS.get("aid", None)
    clmdp = generate_password_hash(PARAMS.get("clmdp", None))
    try: #catch the exception if the client already exists in the database
        db.post_client_info(clnom=clnom, clpnom=clpnom, clemail=clemail, aid=aid, clmdp=clmdp)
        return Response(status=201)
    except:
        return Response(status=400)


@app.route('/login', methods=["GET"])
def check_client_get_clid():
    clemail, clmdp = PARAMS.get('clemail', None), PARAMS.get('clmdp', None)
    if (clemail is None) or (clmdp is None):
        return Response(status=400)
    else:
        res = list(db.fetch_login_client(clemail=clemail))
        if len(res) == 0:
            return Response(status=401)
        elif check_password_hash(res[0][2], clmdp):
            return jsonify(encode_auth_token(res[0][0], user_type='client'))
        else:
            return Response(status=401)


### commerce interface

#no real authentication and authorization needed here as clients will access this all the time
@app.route('/commerce/<int:cid>', methods=["GET"])
def get_commerce_info(cid):
    res = db.get_commerce_info(cid=cid)
    return jsonify(res)
#curl -i -X GET http://0.0.0.0:5000/commerce/1


@app.route('/commerce/<int:cid>', methods=["PATCH", "PUT"])
def patch_commerce_info(cid):
    auth_token = PARAMS.get("token", "")
    if is_authorized(auth_token, user_id=cid, user_type='commerce'):
        cnom, cpresentation = PARAMS.get("cnom", None), PARAMS.get("cpresentation", None)
        cemail, aid = PARAMS.get("cemail", None), PARAMS.get("aid", None)
        url_ext, code_postal = PARAMS.get("url_ext", None), PARAMS.get("code_postal", None)
        rue_and_num = PARAMS.get("rue_and_num", None)
        catnom=PARAMS.get("catnom", None)
        ## catnom=Restaurant,Textile
        if cnom != None:
            db.patch_commerce_nom(cnom=cnom, cid=cid)
        if cpresentation != None:
            db.patch_commerce_cpresentation(cpresentation=cpresentation, cid=cid)
        if cemail != None:
            db.patch_commerce_cemail(cemail=cemail, cid=cid)
        if aid != None:
            db.patch_commerce_aid(aid=aid, cid=cid)
        if url_ext != None:
            db.patch_commerce_url_ext(url_ext=url_ext, cid=cid)
        if  code_postal != None:
            db.patch_commerce_code_postal(code_postal=code_postal, cid=cid)
        if rue_and_num != None:
            db.patch_commerce_rue_and_num(rue_and_num=rue_and_num, cid=cid)
        if catnom != None:
            db.delete_commerce_categorie(cid=cid)
            catnom=catnom.split(",")
            for x in catnom:
                db.post_commerce_categorie(catnom=x, cid=cid)
        return Response(status=201)
    else:
        return Response(status=401)

#curl -i -X PATCH -d cnom=zara -d cpresentation=casual -d cemail=zara@hotmail.com -d aid=1 -d cmdp=zarapassword -d rue_and_num=270 rue saint jacques -d code_postal=75005 -d url_ext=xyz -d catnom=Textile,Restaurant http://0.0.0.0:5000/commerce/1

@app.route('/signupcommerce', methods=["POST"])
def post_commerce_info():
    cnom, cpresentation = PARAMS.get("cnom", None), PARAMS.get("cpresentation", None)
    cemail, aid = PARAMS.get("cemail", None), int(PARAMS.get("aid", None))
    url_ext, code_postal = PARAMS.get("url_ext", None), int(PARAMS.get("code_postal", None))
    rue_and_num = PARAMS.get("rue_and_num", None)
    cmdp = generate_password_hash(PARAMS.get("cmdp", None))
    catnom=PARAMS.get("catnom", None)

    try: #catch the exception if the commerce already exists in the database
        res = db.post_commerce_info(cnom=cnom,
                              cpresentation=cpresentation,
                              cemail=cemail, aid=aid,
                              cmdp=cmdp, rue_and_num=rue_and_num,
                              code_postal=code_postal, url_ext=url_ext)
        p = int(res[0][0])
        app.logger.debug(p)
        if catnom is not None:
            catnom=catnom.split(",")
            app.logger.debug(catnom)
            for x in catnom:
                app.logger.debug(x)
                db.post_commerce_categorie(catnom=x, cid=p)
            return  jsonify(p), 201
        else:
            return jsonify(p), 201
    except Exception as e:
        #return str(e)
        return Response(status=400)

@app.route('/logincommerce', methods=["GET"])
def check_commerce_get_cid():
    cemail, cmdp = PARAMS.get('cemail', None), PARAMS.get('cmdp', None)
    if (cemail is None) or (cmdp is None):
        return Response(status=400)
    else:
        res = list(db.fetch_login_commerce(cemail=cemail))
        if len(res) == 0:
            return Response(status=401)
        elif check_password_hash(res[0][2], cmdp):
            return jsonify(encode_auth_token(res[0][0], user_type='commerce'))
        else:
            return Response(status=401)





'''def gen_thumbnail(filename):
    """ Generate thumbnail image
    """
    height = width = 200
    original = Image.open(os.path.join(app.config['UPLOAD_PATH_PROMOTION'], filename))
    thumbnail = original.resize((width, height), Image.ANTIALIAS)
    thumbnail.save(os.path.join(app.config['UPLOAD_PATH_PROMOTION'], 'thumb_'+filename))'''

#validate that it is an image
def validate_image(stream):
    header = stream.read(512)
    stream.seek(0)
    format = imghdr.what(None, header)
    if not format:
        return None
    return '.' + (format if format != 'jpeg' else 'jpg') 

@app.route('/promotion/image/<int:pid>', methods=['POST'])
def upload_image():
    ranks = PARAMS.get("ranks", None)
    uploaded_file = request.files['file']
    filename = secure_filename(uploaded_file.filename)
    if filename != '':
        file_ext = os.path.splitext(filename)[1].lower()
        if file_ext not in app.config['UPLOAD_EXTENSIONS'] or \
            file_ext != validate_image(uploaded_file.stream):
            return "Invalid image", 400
            # Salt and hash the file contents
        filename=secrets.token_hex(8) + file_ext
        uploaded_file.save(os.path.join(app.config['UPLOAD_PATH_PROMOTION'], filename))
        ## add to the database with not verified
        #gen_thumbnail(filename)
        res=db.post_promotion_image(imgname=filename, ranks= ranks, pid=pid)
        return '', 204
    return "Invalide image", 400

#@app.route('/commerce/verify', methods="PATCH")

@app.route('/promotionimage/<int:pid>', methods=['GET'])
def get_image(pid):
    res = db.get_promotion_info(pid=pid)
    return jsonify(res)

@app.route('/promotionimage/<int:pid>', methods=['DELETE'])
def delete_image(pid):
    imgname = PARAMS.get("imgname", None)
    db.delete_promotion_image(pid=pid, imgname=imgname)
    return "",204
