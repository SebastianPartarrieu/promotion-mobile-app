#! /usr/bin/env python3
import re  # will be useful
import anodb  # type: ignore
import jwt
from werkzeug.security import generate_password_hash, check_password_hash
from os import environ as ENV
import secrets
import os
from werkzeug.utils import secure_filename
import imghdr
from flask import Flask, jsonify, request, Response, session, render_template, send_from_directory
import datetime as dt
import logging as log
import base64
from geopy import Nominatim


log.basicConfig(level=log.INFO)

from geopy import Nominatim
started = dt.datetime.now()

# get running version information
with open("VERSION") as VERSION:
    branch, commit, date = VERSION.readline().split(" ")

# start flask service
from flask import Flask, jsonify, request, Response
import imghdr
#from PIL install Image
from werkzeug.utils import secure_filename
import os
import secrets
import hashlib 
import time

app = Flask("promotion")

# load configuration, fall back on environment

# added imports - token based auth and hash for password storage

if "APP_CONFIG" in ENV:
    app.config.from_envvar("APP_CONFIG")
    CONF = app.config  # type: ignore
else:
    CONF = ENV  # type: ignore

# create $database connection and load queries
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

# Tests for authentication based on JWT (Json Web tokens)

if CONF.get("SECRET_KEY", False):
    global SECRET_KEY
    SECRET_KEY = CONF["SECRET_KEY"]  # for JWTs


def encode_auth_token(user_id, user_type='client'):
    '''
    Generates the Auth token (string).
    Given a user_id, return token
    '''
    try:
        if user_type == 'client':
            payload = {
                # or no expiration at all
                'exp': dt.datetime.utcnow() + dt.timedelta(days=365, seconds=5),
                'iat': dt.datetime.utcnow(),
                'sub': user_id,
                'ust': user_type
            }
        else:
            payload = {
                # or no expiration at all
                'exp': dt.datetime.utcnow() + dt.timedelta(days=7, seconds=5),
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
        # user_id and type (client, commerce, ...)
        return payload['sub'], payload['ust']
    except jwt.ExpiredSignatureError:
        return 'Signature Expired. Please log in again!'
    except jwt.InvalidTokenError:
        return 'Invalid token. Please log in again.'


def is_authorized(auth_token, user_id, user_type='client'):
    '''
    Given an auth_token and a user_id tells whether the token is one of a
    specific user_type and is valid.
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

def convert_address_to_geolocation(code_postal, rue_and_num, aid):
    '''
    code_postal: int
    rue_and_num: str
    aid: int, id of agglomeration

    Returns
    location.latitude:float
    location.longitude:float
    '''
    agglo = db.fetch_agglo_from_aid(aid=aid)
    db.commit()
    locator = Nominatim(user_agent ="myGeocoder")
    complete_address = rue_and_num + ',' + str(agglo[0][0]) + ',' + str(code_postal)
    location = locator.geocode(complete_address)
    return location.latitude, location.longitude
    

def is_authorized_no_id(auth_token, user_type='commerce', check_active=True):
    '''
    Given an auth_token and user_type returns whether the token is valid
    and of a specific user_type. Returns user_id.
    If check_active True then function checks if user account is active. If not returns false.
    '''
    if auth_token == '':
        False
    elif decode_auth_token(auth_token) == 'Signature Expired. Please log in again!':
        return False
    elif decode_auth_token(auth_token) == 'Invalid token. Please log in again.':
        return False
    else:
        user_id_received, user_type_received = decode_auth_token(auth_token)
        if str(user_type_received) != user_type:
            return False
        else:
            if check_active: #only useful to check if all other tests pass
                if user_type == 'commerce':
                    status = db.check_commerce_active(cid=user_id_received)
                    db.commit()
                elif user_type == 'client':
                    status = db.check_client_active(clid=user_id_received)
                    db.commit()
                if status[0][0]:
                    return user_id_received
                else:
                    return False
            else:
                return user_id_received


#
# GET /version
#
# general information about the application
#
@app.route('/')
def index():
    return render_template('page_principale.html')

@app.route('/login/commerce')
def logincommerce_html():
    return render_template('login.html')

@app.route('/logout/commerce')
def logoutcommerce_html():
    return render_template('logout.html')

@app.route('/commercemon-compte')
def mon_compte():
    return render_template('comptetest.html')

@app.route('/addPromotion')
def add_promotion():
    return render_template('addPromotion.html')

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

# FRONT PAGE QUERIES

# GET /promotion with filter for number returned, agglomeration and categories


@app.route("/promotion", methods=["GET"])
def get_promotion():
    cat = PARAMS.get("categorie", '%')
    agglo = PARAMS.get("agglomeration", '%')
    nb = PARAMS.get("nb", 100)  # arbitraire
    cat = cat.split(',')
    if len(cat) == 1:
        res = db.get_promotion(agg=agglo, nb=nb, cat=cat[0])
    else:
        res = []
        for x in cat:
            res.append(db.get_promotion(agg=agglo, nb=nb, cat=x))
    return jsonify({'resultat':res})


# GET /commerce with filter for categorie and agglomeration
@app.route("/commerce", methods=["GET"])
def get_commerce():
    cat = PARAMS.get("categorie", '%')
    agglo = PARAMS.get("agglomeration", '%')
    search = PARAMS.get("search", '%')
    res = db.get_commerce(agg=agglo, cat=cat, search=search)
    for i, element in enumerate(res):
        current_id = element[0]
        img_paths = db.get_commerce_image(cid=current_id) #path, rank, imid
        element = list(element)
        element.append(list(img_paths))
        res[i] = element    
    return jsonify({'resultat': res})

# INTERACTION WITH FRONT PAGE


@app.route('/promotion/<int:pid>', methods=["GET"])
def get_promotion_info(pid):
    res = db.get_promotion_info(pid=pid)
    return jsonify({'resultat': res})

# ACCOUNT RELATED QUERIES


@app.route('/myclient', methods=["GET"])
def get_client_info():
    auth_token = PARAMS.get("token", '')
    clid = is_authorized_no_id(auth_token, user_type='client')
    if clid:
        res = db.get_client_info(clid=clid)
        return jsonify({'resultat': res})
    else:
        return Response(status=401)


@app.route('/myclient', methods=["PATCH", "PUT"])
def patch_client_info():
    auth_token = PARAMS.get("token", '')
    clid = is_authorized_no_id(auth_token, user_type='client')
    if clid:
        clnom, clpnom = PARAMS.get("clnom", None), PARAMS.get("clpnom", None)
        clemail, aid = PARAMS.get("clemail", None), PARAMS.get("aid", None)
        if clnom is not None:
            db.patch_client_nom(clnom=clnom, clid=clid)
        if clpnom is not None:
            db.patch_client_pnom(clpnom=clpnom, clid=clid)
        if clemail is not None:
            db.patch_client_clemail(clemail=clemail, clid=clid)
        if aid is not None:
            db.patch_client_aid(aid=aid, clid=clid)
        return Response(status=201)
    else:
        return Response(status=401)


@app.route('/signup', methods=["POST"])
def post_client_info():
    clnom, clpnom = PARAMS.get("clnom", None), PARAMS.get("clpnom", None),
    clemail, aid = PARAMS.get("clemail", None), PARAMS.get("aid", None)
    clmdp = generate_password_hash(PARAMS.get("clmdp", None))
    try:  # catch the exception if the client already exists in the database
        if not re.match("[^@]+@[^@]+\.[^@]+", clemail):
            return jsonify({'is_registered': False, 'error': 'e-mail wrong format'}), 400
        else: 
            res = db.post_client_info(
                clnom=clnom,
                clpnom=clpnom,
                clemail=clemail,
                aid=aid,
                clmdp=clmdp)
            return jsonify({'is_registered': True}), 201
    except BaseException:
        return jsonify({'is_registered': False}), 400


@app.route('/login', methods=["GET"])
def check_client_get_clid():
    clemail, clmdp = PARAMS.get('clemail', None), PARAMS.get('clmdp', None)
    if (clemail is None) or (clmdp is None):
        return jsonify({'is_logged_in' : False}), 401
    else:
        res = list(db.fetch_login_client(clemail=clemail))
        status = db.check_client_active(clid=res[0][0]) #active check with clid
        if len(res) == 0:
            return jsonify({'is_logged_in': False}), 401
        elif check_password_hash(res[0][2], clmdp):
            if status[0][0]:
                return jsonify({'is_logged_in': True, 'token': encode_auth_token(res[0][0], user_type='client')}), 200
            else:
                return jsonify({'is_logged_in': False}), 401
        else:
            return jsonify({'is_logged_in': False}), 401

@app.route('/myclient', methods=['DELETE'])
def delete_client_info():
    auth_token = PARAMS.get('token', None)
    clid = is_authorized_no_id(auth_token, user_type='client')
    if clid:
        db.invalidate_client_account(clid=int(clid))
        # something to invalidate tokens perhaps? No need. Check if user account valid on queries
        return Response(status=200)
    else:
        return Response(status=401)


@app.route('/mycommerce/promotions', methods=['POST'])
def fetch_promotion_of_commerce():
    auth_token = PARAMS.get("token", None)
    cid = is_authorized_no_id(auth_token, user_type='commerce')
    if cid:
        res = db.fetch_promotion_of_commerce(cid=int(cid))
        return jsonify(res)
    else:
        return jsonify({'status': 'error 400', 'message': 'Something went wrong!'})


# COMMERCE INTERFACE

# no real authentication and authorization needed here as clients will
# access this all the time
@app.route('/commerce/<int:cid>', methods=["GET"])
def get_commerce_info(cid):
    res = db.get_commerce_info(cid=cid)
    return jsonify(res)
# curl -i -X GET http://0.0.0.0:5000/commerce/1


def upload_picture(uploaded_file):
    filename = secure_filename(uploaded_file.filename)
    if filename != '':
        file_ext = os.path.splitext(filename)[1].lower()
        if file_ext not in app.config['UPLOAD_EXTENSIONS'] or \
                file_ext != validate_image(uploaded_file.stream):
            return "Invalid image", 400
        filename=hashlib.md5((secrets.token_hex(8) + str(round(time.time() * 1000))).encode('utf-8')).hexdigest() + file_ext
        return filename


@app.route('/mycommerce', methods=["PATCH", "PUT"])
def patch_commerce_info():
    auth_token = PARAMS.get("token", "")
    cid = is_authorized_no_id(auth_token, user_type='commerce')
    if cid:
        cid = int(cid)
        cnom, cpresentation = PARAMS.get(
            "cnom", None), PARAMS.get(
            "cpresentation", None)
        cemail, aid = PARAMS.get("cemail", None), PARAMS.get("aid", None)
        url_ext, code_postal = PARAMS.get(
            "url_ext", None), PARAMS.get(
            "code_postal", None)
        rue_and_num = PARAMS.get("rue_and_num", None)
        catnom = PARAMS.get("catnom", None)
        # catnom=Restaurant,Textile
        temp_aid = db.fetch_aid_from_commerce(cid=cid)
        if cnom is not None:
            db.patch_commerce_nom(cnom=cnom, cid=cid)
        if cpresentation is not None:
            db.patch_commerce_cpresentation(
                cpresentation=cpresentation, cid=cid)
        if cemail is not None:
            db.patch_commerce_cemail(cemail=cemail, cid=cid)
        if aid is not None:
            db.patch_commerce_aid(aid=aid, cid=cid)
            temp_aid = aid
        if url_ext is not None:
            db.patch_commerce_url_ext(url_ext=url_ext, cid=cid)
        if (code_postal is not None) or (rue_and_num is not None):
            prev_code_postal = db.fetch_code_postal_from_cid(cid=cid)[0][0]
            prev_rue_and_num = db.fetch_rue_and_num_from_cid(cid=cid)[0][0]
            if code_postal is not None:
                prev_code_postal = code_postal
                db.patch_commerce_code_postal(code_postal=code_postal, cid=cid)
            if rue_and_num is not None:
                prev_rue_and_num = rue_and_num
                db.patch_commerce_rue_and_num(rue_and_num=rue_and_num, cid=cid)
            latitude, longitude = convert_address_to_geolocation(code_postal=prev_code_postal,
                                                        rue_and_num=prev_rue_and_num,
                                                        aid=temp_aid)
            db.patch_commerce_lat_long(cid=cid, latitude=latitude, longitude=longitude)
        if catnom is not None:
            db.delete_commerce_categorie(cid=cid)
            catnom = catnom.split(",")
            for x in catnom:
                db.post_commerce_categorie(catnom=x, cid=cid)
        return Response(status=201)
    else:
        return Response(status=401)

@app.route('/signupcommerce', methods=["POST"])
def post_commerce_info():
    cnom, cpresentation = PARAMS.get(
        "cnom", None), PARAMS.get(
        "cpresentation", None)
    cemail, aid = PARAMS.get("cemail", None), PARAMS.get("aid", None)
    url_ext, code_postal = PARAMS.get("url_ext", None), PARAMS.get("code_postal", None)
    rue_and_num = PARAMS.get("rue_and_num", None)
    cmdp = generate_password_hash(PARAMS.get("cmdp", None))
    #cmdp=PARAMS.get("cmdp", None)
    catnom = PARAMS.get("catnom", None)

    latitude, longitude = convert_address_to_geolocation(code_postal=code_postal,
                                                        rue_and_num=rue_and_num,
                                                        aid=aid)

    try:  # catch the exception if the commerce already exists in the database
        res = db.post_commerce_info(cnom=cnom,
                                    cpresentation=cpresentation,
                                    cemail=cemail, aid=int(aid),
                                    cmdp=cmdp, rue_and_num=rue_and_num,
                                    code_postal=code_postal, url_ext=url_ext,
                                    latitude=latitude,
                                    longitude=longitude)

        p = int(res[0][0])
        if catnom is not None:
            catnom = catnom.split(",")
            for x in catnom:
                db.post_commerce_categorie(catnom=x, cid=p)
            return jsonify({'status': 'ok'}), 201
        else:
            return jsonify({'status': 'ok'}), 201
    except Exception as e:
        # return str(e)
        return jsonify({'status': 'error 400', 'message': 'something went wrong!'}), 400



@app.route('/logincommerce', methods=["POST"])
def check_commerce_get_cid():
    cemail, cmdp = PARAMS.get('cemail', None), PARAMS.get('cmdp', None)
    if (cemail is None) or (cmdp is None):
        return jsonify({"status" : "error", "message" : "Invalid email or password"})
        #return jsonify(Response(status=400))
        
    else:
        res = list(db.fetch_login_commerce(cemail=cemail))
        if len(res) == 0:
            return jsonify({"status" : "error", "message" : "Invalid email or password"}), 401
        elif check_password_hash(res[0][2], cmdp):
            status = db.check_commerce_active(cid=res[0][0])
        #elif cmdp==res[0][2]:
            if status[0][0]:
                dict_new = {
                    "status" : "ok",
                    "token" : encode_auth_token(res[0][0], user_type='commerce')
                }
                return jsonify(dict_new), 200
            else:
                return jsonify({"status" : "error", "message" : "Invalid email or password"}), 401
        else:
            return jsonify({"status" : "error", "message" : "Invalid email or password"}), 401
        

@app.route('/mycommerce', methods=['DELETE'])
def delete_commerce_info():
    auth_token = PARAMS.get('token', None)
    cid = is_authorized_no_id(auth_token, user_type='commerce')
    if cid:
        db.invalidate_commerce_account(cid=int(cid))
        #Expire token somehow
        #We also have to handle cascading deletions on other tables of the db
        return Response(status=200)
    else:
        return Response(status=401)

@app.route('/promotion', methods=["POST"])
def post_promotion():
    #Getting info of promotion from HTTP request
    pdescription = PARAMS.get('pdescription', None)
    tdebut = PARAMS.get('tdebut', None) #maybe check for right format and better default option
    tfin = PARAMS.get('tfin', None)
    #Authorization check
    auth_token = PARAMS.get("token", '')
    cid_token = is_authorized_no_id(auth_token, user_type="commerce")
    if cid_token:
        try: #catch the exception if promotion info isn't adequate
            res = db.post_promotion(pdescription=pdescription,
                              tdebut=tdebut,
                              tfin=tfin,
                              cid=int(cid_token))
            p = int(res[0][0])
            return jsonify(p), 201
        except Exception as e:
            return Reponse(status=400)
    else:
        return Response(status=401)

@app.route('/promotion/<int:pid>', methods=['PATCH', 'PUT'])
def patch_promotion(pid):
    pdescription = PARAMS.get('pdescription', None)
    tdebut = PARAMS.get('tdebut', None) #maybe check for right format and better default option
    tfin = PARAMS.get('tfin', None)
    #Authorization check
    auth_token = PARAMS.get("token", '')
    cid_token = is_authorized_no_id(auth_token, user_type="commerce")
    cid_associated_to_pid = db.fetch_cid_of_pid(pid=pid)
    #check if commerce token is valid
    if cid_token:
        #check if commerce is modifying its own promotion
        if int(cid_associated_to_pid[0][0]) != int(cid_token):
            return Response(status=401)
        else:
            if pdescription is not None:
                db.patch_promotion_pdescription(pid=pid, pdescription=pdescription)
            if tdebut is not None:
                db.patch_promotion_tdebut(pid=pid, tdebut=tdebut)
            if tfin is not None:
                db.patch_promotion_tfin(pid=pid, tfin=tfin)
            return Response(status=201)
    else:
        return Response(status=401)

# ADMIN INTERFACE

# Perhaps only one initially created admin account?


'''def gen_thumbnail(filename):
    """ Generate thumbnail image
    """
    height = width = 200
    original = Image.open(os.path.join(app.config['UPLOAD_PATH_PROMOTION'], filename))
    thumbnail = original.resize((width, height), Image.ANTIALIAS)
    thumbnail.save(os.path.join(app.config['UPLOAD_PATH_PROMOTION'], 'thumb_'+filename))'''

# validate that it is an image

def validate_image(stream):
    header = stream.read(512)
    stream.seek(0)
    format = imghdr.what(None, header)
    if not format:
        return None
    return '.' + (format if format != 'jpeg' else 'jpg')


def f_update_image(nameFolder, id, databaseFunction, uploaded_file, ranksFunction):
    filename=upload_picture(uploaded_file)
    uploaded_file.save(os.path.join(app.config[nameFolder], filename))
    #gen_thumbnail(filename, 'UPLOAD_PATH_PROMOTION')
    res=ranksFunction(id)
    res= databaseFunction(filename, str(res[0][0]), id)
    db.commit()
    return res


def f_delete_images(nameFolder, id, databaseFunction):
    res = databaseFunction(id)
    for imgname in res:
        os.remove(os.path.join(app.config[nameFolder], imgname[0]))
    return "", 204


@app.route('/promotion/<int:pid>/image', methods=['POST'])
def upload_image(pid):
    uploaded_file = request.files['file']
    # Authorization checks
    auth_token = PARAMS.get("token", '')
    cid_associated_to_pid = db.fetch_cid_of_pid(pid=pid)
    cid_token = is_authorized_no_id(auth_token, user_type='commerce')
    #check if commerce token is valid
    if cid_token:
        #check if commerce is modifying own image
        if int(cid_associated_to_pid[0][0]) != int(cid_token):
            return Response(status=401)
        else:
            try:
                res = f_update_image(
                    'UPLOAD_PATH_PROMOTION',
                    pid,
                    lambda x, y, z: db.post_promotion_image(filename=x,
                                                            ranks=y,
                                                            pid=z),
                    uploaded_file,
                    lambda x: db.get_rank_last_image_promotion(pid=x)) 
                return jsonify(res)
            except Exception as e:
                return Response(status=400)       
    else:
        return Response(status=401)
# to delete all images of a promotion


@app.route('/promotion/<int:pid>/images', methods=['DELETE'])
def delete_images(pid):
    # Authorization checks
    auth_token = PARAMS.get("token", '')
    cid_associated_to_pid = db.fetch_cid_of_pid(pid=pid)
    cid_token = is_authorized_no_id(auth_token, user_type='commerce')
    #check if commerce token is valid
    if cid_token:
        #check if commerce is modifying own image
        if int(cid_associated_to_pid[0][0]) != int(cid_token):
            return Response(status=401)
        else:
            f_delete_images(
                'UPLOAD_PATH_PROMOTION',
                pid,
                lambda x: db.post_promotion_image(
                    pid=x))
    else:
        return Response(status=401)

def dupcheck(x):
   for elem in x:
      if x.count(elem) > 1:
         return True
      return False

@app.route('/promotion/<int:pid>/image', methods=['PUT','PATCH'])
def change_rank(pid):
    #imageRanks is a list containing image with its rank, i.e. [['image1',1],['image1',2]]
    imageImid = (PARAMS.get('imageImid')).split(",")
    imageRanks = (PARAMS.get('imageRanks')).split(",")
    if dupcheck(imageImid) or dupcheck(imageRanks):
        return Response(status=400)
    ##imageRanks=list(PARAMS.get("imageRanks",None))
    for i in range(len(imageRanks)):
        res = db.change_promotion_filename_image(imid=imageImid[i], ranks=imageRanks[i],pid=pid)
    return '', 204


@app.route('/promotion/<int:pid>/image', methods=['GET'])
def get_images(pid):
    res = db.get_promotion_image(pid=pid)
    return jsonify(res)


@app.route('/promotion/<int:pid>/image', methods=['DELETE'])
def delete_image(pid):
    # Authorization checks
    auth_token = PARAMS.get("token", '')
    cid_associated_to_pid = db.fetch_cid_of_pid(pid=pid)
    cid_token = is_authorized_no_id(auth_token, user_type='commerce')
    #check if commerce token is valid
    if cid_token:
        #check if commerce is modifying own image
        if int(cid_associated_to_pid[0][0]) != int(cid_token):
            return Response(status=401)
        else:
            imageImid = PARAMS.get("imageImid", None)
            res=db.delete_promotion_image(pid=pid, imid=imageImid)
            os.remove(os.path.join(app.config['UPLOAD_PATH_PROMOTION'], res))
            return "", 204
    else:
        return Response(status=401)


@app.route('/commerce/image', methods=['POST'])
def upload_commerce_image():
    uploaded_file = request.files['inpFile']
    auth_token = PARAMS.get("token", None)
    #return repr(uploaded_file.read())
    #return jsonify(upload_file.filename)
    #return uploaded_file.filename
    
    cid = is_authorized_no_id(auth_token, user_type='commerce')
    if cid:
        try:
            res = f_update_image('UPLOAD_PATH_COMMERCE', cid, lambda x, y, z: db.post_commerce_image(imgname=x,ranks=y,cid=z),
                            uploaded_file ,
                            lambda x: db.get_rank_last_image_commerce(cid=x) )         
            return jsonify(res)
        except Exception as e:
            return jsonify("Dfkjn")
            return Response(status=400)
    else:
        return Response(status=401)


#to delete all images of a commerce
@app.route('/commerce/image', methods=['DELETE'])
def delete_commerce_images(cid):
    #Authorization checks 
    auth_token = PARAMS.get("token", '')
    cid = is_authorized_no_id(auth_token, user_type='commerce')
    if cid:
        f_delete_images(
            'UPLOAD_PATH_COMMERCE',
            cid,
            lambda x: db.post_commerce_image(
                cid=x))
    else:
        return Response(status=401)

@app.route('/commerce/<int:cid>/image', methods=['PUT', 'PATCH'])
def change_rank_commerce(cid):
    #imageRanks is a list containing image with its rank, i.e. [['image1',1],['image1',2]]
    imageImid = (PARAMS.get('imageImid')).split(",")
    imageRanks = (PARAMS.get('imageRanks')).split(",")
    if dupcheck(imageImid) or dupcheck(imageRanks):
        return Response(status=400)
    ##imageRanks=list(PARAMS.get("imageRanks",None))
    for i in range(len(imageRanks)):
        res=db.change_commerce_filename_image(Imid=imageImid[i], ranks=imageRanks[i],cid=cid)
        db.commit()
    return '', 204


@app.route('/get/commerce/image', methods=['POST', 'GET'])
def get_images_commerce():
    auth_token = PARAMS.get("token", None)
    cid = is_authorized_no_id(auth_token, user_type='commerce')
    res = db.get_commerce_image(cid=cid)
    return jsonify(res)


@app.route('/commerce/<int:cid>/image', methods=['DELETE'])
def delete_image_commerce(cid):
    #Authorization checks 
    auth_token = PARAMS.get("token", '')
    if is_authorized(auth_token, user_id=cid, user_type='commerce'):
        imageImid = PARAMS.get("imageImid", None)
        res=db.delete_commerce_image(cid=cid, imid=imageImid)
        os.remove(os.path.join(app.config['UPLOAD_PATH_COMMERCE'], res))
        return "",204
    else:
        return Response(status=401)

@app.route('/template/commerceImage/<path:path>')
def send_pic(path):
    return send_from_directory('templates/commerceImage', path)

@app.route('/commerceImage/<path:path>')
def send_pic_commerce(path):
    return send_from_directory('commerceImage', path)

@app.route('/commerce/verify', methods=["PATCH"])
def verify():
    imgname = PARAMS.get("imgname", None)
    db.verify_image(imgname=imgname)
    return "", 204