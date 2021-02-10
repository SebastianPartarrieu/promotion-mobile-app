#! /usr/bin/env python3

# Imports
import re  
import anodb  # type: ignore
import jwt
import secrets
import os
import imghdr
import datetime as dt
import logging as log
import hashlib 
import base64
import time

from os import environ as ENV
from werkzeug.utils import secure_filename
from werkzeug.security import generate_password_hash, check_password_hash
from flask import Flask, jsonify, request, Response, session, render_template, send_from_directory
from geopy import Nominatim

log.basicConfig(level=log.INFO)

started = dt.datetime.now()

# get running version information
with open("VERSION") as VERSION:
    branch, commit, date = VERSION.readline().split(" ")

# start flask service
app = Flask("promotion")

# load configuration, fall back on environment
if "APP_CONFIG" in ENV:
    app.config.from_envvar("APP_CONFIG")
    CONF = app.config  # type: ignore
else:
    CONF = ENV  # type: ignore

# create $database connection and load queries
db = anodb.DB(
    CONF["DB_TYPE"], CONF["DB_CONN"], CONF["DB_SQL"], CONF["DB_OPTIONS"]
)

# Handling PARAMS of the HTTP requests
PARAMS = {}
def set_params():
    '''
    Function to set PARAMS as global variable and assign it.
    '''
    global PARAMS
    PARAMS = request.values if request.json is None else request.json

def do_commit(res: Response):
    '''
    Will be set as a hook to avoid db.commit() in every following function.
    '''
    global db
    db.commit()
    return res

app.before_request(set_params)
app.after_request(do_commit)

# Authentication and authorization will be handled here via JWTs
if CONF.get("SECRET_KEY", False):
    global SECRET_KEY
    SECRET_KEY = CONF["SECRET_KEY"]  # this should stay ONLY in the back-end

########## HELPER FUNCTIONS ##########
#Helper functions for AA
def encode_auth_token(user_id, user_type='client'):
    '''
    Generates the Auth token.

    Args:
        user_id: int corresponding to cid or clid depending on user_type
        user_type: str, either client or commerce

    Output:
        JSON web token: str, encoded payload (exp date, issued at time, user_id, user_type

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
    Decodes auth_token, checking for expiration and token validity.

    Args:
        auth_token: str, JSON Web Token

    Output:
        user_id: int
        user_type: str
        Or string detailing error type.
    '''
    try:
        payload = jwt.decode(auth_token, SECRET_KEY, algorithms="HS256")
        return payload['sub'], payload['ust']
    except jwt.ExpiredSignatureError:
        return 'Signature Expired. Please log in again!'
    except jwt.InvalidTokenError:
        return 'Invalid token. Please log in again.'

def is_authorized(auth_token, user_id, user_type='client'):
    '''
    Authorization function for certain queries. Deprecated.

    Args:
        auth_token: str, JSON Web Token
        user_id: int
        user_type: str

    Output:
        boolean
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
        elif int(user_id_received) != int(user_id): #probably unecessary safeguard
            return False
        else:
            return True

def is_authorized_no_id(auth_token, user_type='commerce', check_active=True):
    '''
    Authorization function for certain queries. 
    Multiple checks before returning id contained within payload.
    
    Args:
        auth_token: str, JSON Web Token
        user_type: str
        check_active: boolean, check if account has not been deactivated 
    
    Output:
        False or user_id
    '''
    if auth_token == '':
        False
    elif decode_auth_token(auth_token) == 'Signature Expired. Please log in again!':
        return False
    elif decode_auth_token(auth_token) == 'Invalid token. Please log in again.':
        return False
    else:
        user_id_received, user_type_received = decode_auth_token(auth_token)
        if str(user_type_received) != user_type: #ensure client with same id as a commerce can't modify commerce info
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
            else: #if a function doesn't need to check account is active, unlikely 
                return user_id_received

#Helper functions for geoencoding
def convert_address_to_geolocation(code_postal, rue_and_num, aid):
    '''
    Everything is in the name.

    Args:
        code_postal: int
        rue_and_num: str
        aid: int, id of agglomeration

    Output:
        location.latitude:float
        location.longitude:float
    '''
    agglo = db.fetch_agglo_from_aid(aid=aid)
    db.commit()
    locator = Nominatim(user_agent ="myGeocoder")
    complete_address = rue_and_num + ',' + str(agglo[0][0]) + ',' + str(code_postal) #270 Rue Saint-Jacques, Paris, 75005
    try:
        location = locator.geocode(complete_address)
        return location.latitude, location.longitude
    except Exception as e:
        return 'address supplied is wrong', ''

#Helper functions for images
def upload_picture(uploaded_file):
    '''
    Implements a number of checks and before uploading image file to database.

    Args:
        uploaded_file: image file .png, .jpeg, .jpg, .gif
    
    Output:
        filename: str
    '''
    filename = secure_filename(uploaded_file.filename)
    if filename != '':
        file_ext = os.path.splitext(filename)[1].lower()
        if file_ext not in app.config['UPLOAD_EXTENSIONS'] or \
                file_ext != validate_image(uploaded_file.stream):
            return "Invalid image", 400
        filename=hashlib.md5((secrets.token_hex(8) + str(round(time.time() * 1000))).encode('utf-8')).hexdigest() + file_ext
        return filename

def validate_image(stream):
    '''
    validatation of the format which should be an image not a text file

    Args: 
        file.stream
    
    Output:
        extension of the file
    '''
    header = stream.read(512)
    stream.seek(0)
    format = imghdr.what(None, header)
    if not format:
        return None
    return '.' + (format if format != 'jpeg' else 'jpg')

def f_update_image(nameFolder, id, databaseFunction, uploaded_file, ranksFunction):
    '''
    save image in the server's folder and the filename in the database for commerce and promotion

    Args:
        path name to save image, pid/cid, function for saving the image in the databse and the folder in the server

    Output:
        imid (id of the image)
    '''
    filename=upload_picture(uploaded_file)
    uploaded_file.save(os.path.join(app.config[nameFolder], filename))
    #gen_thumbnail(filename, 'UPLOAD_PATH_PROMOTION')
    res=ranksFunction(id)
    res= databaseFunction(filename, 1, id)
    db.commit()
    return res

def f_delete_images(nameFolder, id, databaseFunction):
    '''
    delete all images for a promotion of a commerce

    Args: 
        path name to save image, pid/cid, function to delete the image from the database

    Output:
        status

    '''
    try:
        res = databaseFunction(id)
        for imgname in res:
            os.remove(os.path.join(app.config[nameFolder], imgname[0]))
        return "", 204
    except BaseException:
        return "", 400
    

#Actual query handling (finally!)

#General info about the app
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
            "branch": branch,
            "commit": commit,
            "date": date,
            "now": now,
        }
    )


########## CLIENT SIDE QUERIES ##########

@app.route("/promotion", methods=["GET"])
def get_promotion():
    '''
    Getting a bunch of promotion.

    Passed PARAMS:
        categorie: str, 'Restaurant' or 'Textile'
        agglomeration: str, 'Paris'
        nb: int, number of promotions returned

    Response:
        dict['resultat'] contains a list of lists with each sub-list containing:
            p.pid: int, promotion id
            p.pdescription: str, promotion description
            c.cnom: str, the name of commerce who posted the promotion
            p.tdebut: str, start time of promotion YYYY-MM-DD
        dict['images'] contains a list of lists, each sub-list containing image paths: str
        associated to a promotion ordered by rank.
    '''
    cat = PARAMS.get("categorie", '%') #if not present, get promotion in all categories
    agglo = PARAMS.get("agglomeration", '%')
    nb = PARAMS.get("nb", 100)  #arbitraire
    res = db.get_promotion(agg=agglo, nb=nb, cat=cat)
    images = []
    for i, element in enumerate(res):
        current_pid = element[0]
        img_paths = db.get_promotion_image(pid=current_pid)
        img_paths = [tup[0] for tup in img_paths]
        images.append(img_paths)
        element = list(element) #prefer list of lists to list of tuples
        res[i] = element
    return jsonify({'resultat': res, 'images': images})       

@app.route("/commerce", methods=["GET"])
def get_commerce():
    '''
    Getting a bunch of commerce.

    Passed PARAMS:
        categorie: str, 'Restaurant,Textile,Coiffeur'
        agglomeration: str, 'Paris'

    Response:
        dict['resultat'] contains a list of lists with each sub-list containing:
            c.cid: int, commerce id
            c.cnom: str, commerce name
            c.cpresentation: str, description of commerce
            a.anom: str, name of agglomeration 
            c.code_postal: int, postal code of commerce
            c.rue_and_num: str, number and street name  e.g '270 Rue Saint-Jacques'
            c.latitude: int
            c.longitude: int
            c.url_ext: str, url to possible commerce website
        dict['images'] contains a list of lists, each sub-list containing image paths: str
        associated to a commerce ordered by their rank.
    '''
    cat = PARAMS.get("categorie", '%')
    agglo = PARAMS.get("agglomeration", '%')
    search = PARAMS.get("search", '%')
    res = db.get_commerce(agg=agglo, cat=cat, search=search)
    images = []
    for i, element in enumerate(res):
        current_id = element[0]
        img_paths = db.get_commerce_image(cid=current_id) #path, rank, imidn ordered by asc rank
        img_paths = [tup[0] for tup in img_paths]
        element = list(element) #prefer list of lists to list of tuples
        images.append(img_paths)
        res[i] = element
    return jsonify({'resultat': res, 'images': images})

@app.route('/promotion/<int:pid>', methods=["GET"]) #Perhaps useful for commerce side as well
def get_promotion_info(pid):
    '''
    Get information about one promotion

    Passed in url:
        pid: int, id of a promotion

    Response:
        dict['resultat'] contains:
            c.cid: int, id of commerce who posted promotion
            p.pdescription: str, description of promotion
            c.cnom: str, name of commerce
            p.tdebut: str YYYY-MM-DD
            p.tfin: str YYYY-MM-DD
        dict['images'] contains a list of paths to images of this promotion
    '''
    res = db.get_promotion_info(pid=pid)
    images = db.get_promotion_image(pid=pid)
    return jsonify({'resultat': res, 'images': images})
   
#Client account related queries, getting info, login, signup, deletion
@app.route('/myclient', methods=["GET"])
def get_client_info():
    '''
    Get information about the client.

    Passed PARAMS:
        auth_token: str, JSON Web Token

    Response:
        if auth: dict['resultat'] with:
                clnom: str, surname of client
                clpnom: str, name
                clemail: str, email
                aid: int, corresponding to agglomeration
        if not: 401
    '''
    auth_token = PARAMS.get("token", '')
    clid = is_authorized_no_id(auth_token, user_type='client')
    if clid:
        res = db.get_client_info(clid=clid)
        return jsonify({'resultat': res})
    else:
        return Response(status=401)

@app.route('/myclient', methods=["PATCH", "PUT"])
def patch_client_info():
    '''
    Patch information about the client.

    Passed PARAMS:
        auth_token: str, JSON Web Token
        clnom: str, surname of client
        clpnom: str, name
        clemail: str, email
        aid: int, corresponding to agglomeration
    Response:
        201 or 401
    '''
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
    '''
    Sign up for client side front-end.

    Passed PARAMS:
        clnom: str, surname of client, required
        clpnom: str, name, required
        clemail: str, email, required
        aid: int, corresponding to agglomeration, required
        clmdp: str, password will be stored after being hashed, required
    Response:
        dict['is_registered'] containing bool value 
    '''
    clnom, clpnom = PARAMS.get("clnom", None), PARAMS.get("clpnom", None),
    clemail, aid = PARAMS.get("clemail", None), PARAMS.get("aid", None)
    clmdp = generate_password_hash(PARAMS.get("clmdp", None))
    try:  # catch the exception if the client already exists in the database
        if not re.match("[^@]+@[^@]+\.[^@]+", clemail): #check email format
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
    '''
    Login for client side front-end.

    Passed PARAMS:
        clemail: str
        clmdp: str, will be

    Response:
        dict['is_logged_in']: bool
        dict['token']: issued JSON Web Token at login time
        401 if login is false or credentials not given.
    '''
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
    '''
    Deactivating client account via bool in database.

    Passed PARAMS:
        auth_token: str, JSON Web Token
    
    Response:
        200 or 401
    '''
    auth_token = PARAMS.get('token', None)
    clid = is_authorized_no_id(auth_token, user_type='client')
    if clid:
        db.invalidate_client_account(clid=int(clid))
        # something to invalidate tokens perhaps? No need. Check if user account valid on queries
        return Response(status=200)
    else:
        return Response(status=401)

@app.route('/commerce/<int:cid>/promotion', methods=['GET', 'POST'])
def get_promotion_of_commerce_no_token(cid):
    '''
    Get the promotions of a commerce 

    Passed in url:
        cid: int, id of commerce

    Response:
        dict['resultat'] contains list of lists with each sub-list having:
            p.pid: int, id of promotion
            p.pdescription: str, description of promotion
            c.cnom: str, name of commerce
            p.tdebut: str YYYY-MM-DD
            p.tfin: str YYYY-MM-DD
        dict['images'] contains a list of lists with img_paths
    '''
    res = db.fetch_promotion_of_commerce_for_client(cid=int(cid))
    images = []
    for i, element in enumerate(res):
        img_paths = db.get_promotion_image(pid=element[0]) #path, rank, id ordered by start date
        img_paths = [tup[0] for tup in img_paths] #get only image_paths
        images.append(img_paths)
        element = list(element)
        res[i] = element
    return jsonify({'resultat': res, 'images': images})

@app.route('/commerce/<int:cid>', methods=["GET"])
def get_commerce_info(cid):
    '''
    Get information about one commerce.

    Passed in url:
        cid: int
    
    Response:
        dict['resultat'] containing:
            cnom: str
            cpresentation: str
            cemail: str
            url_ext: str
            code_postal: int
            rue_and_num: str
            aid: int for agglomeration
            catnom: str for categories
        dict['images'] with img paths to images of commerce
    '''
    res = db.get_commerce_info(cid=cid)
    images = db.get_commerce_image(cid=cid)
    images = [tup[0] for tup in images]
    return jsonify({'resultat': res, 'images': images})

@app.route('/commerce/information', methods=["POST"])
def get_commerce_info_commerce_side():
    '''
    Get information about one commerce commerce_ side

    Passed in url:
        cid: int
    
    Response:
        dict['resultat'] containing:
            cnom: str
            cpresentation: str
            cemail: str
            url_ext: str
            code_postal: int
            rue_and_num: str
            aid: int for agglomeration
            catnom: str for categories
        dict['images'] with img paths to images of commerce
    '''
    auth_token = PARAMS.get("token", "")
    cid = is_authorized_no_id(auth_token, user_type='commerce')
    if cid:
        res = db.get_commerce_info(cid=cid)
        #images = db.get_commerce_image(cid=cid)
        #images = [tup[0] for tup in images]
        return jsonify(res)
    else:
        return jsonify({'status': 'error 400', 'message': 'Something went wrong!'}), 400

########## COMMERCE SIDE QUERIES ##########

#Sign-up
@app.route('/signupcommerce', methods=["POST"])
def post_commerce_info():
    '''
    Signing up for commerce.

    Passed in PARAMS:
        cnom: str, required
        cpresentation: str, required
        cemail: str, required
        aid: int for agglomeration, required
        url_ext: str
        code_postal: int, required
        rue_and_num: str, required
        cmdp: str, will be stored after being hashed, required
        catnom: str, 'Restaurant,Textile,Coiffeur' format if multiple categories

    Response:
        dict['status'] bool
        dict['message'] str
        201 or 400 
    '''
    cnom = PARAMS.get("cnom", None)
    cpresentation = PARAMS.get("cpresentation", None)
    cemail = PARAMS.get("cemail", None)
    aid = PARAMS.get("aid", None)
    url_ext = PARAMS.get("url_ext", None)
    code_postal = PARAMS.get("code_postal", None)
    rue_and_num = PARAMS.get("rue_and_num", None)
    cmdp = generate_password_hash(PARAMS.get("cmdp", None))
    #cmdp=PARAMS.get("cmdp", None)
    catnom = PARAMS.get("catnom", None)
    latitude, longitude = convert_address_to_geolocation(code_postal=code_postal,
                                                        rue_and_num=rue_and_num,
                                                        aid=aid)

    try:  # catch the exception if the commerce already exists in the database
        if not re.match("[^@]+@[^@]+\.[^@]+", cemail):
            return jsonify({'status': 'error 400', 'message': 'E-mail is wrong format!'}), 400
        else:
            if longitude == '':
                return jsonify({'status': 'error 400', 'message': 'Address is wrong!'}), 400
            res = db.post_commerce_info(cnom=cnom,
                                        cpresentation=cpresentation,
                                        cemail=cemail, aid=int(aid),
                                        cmdp=cmdp, rue_and_num=rue_and_num,
                                        code_postal=code_postal, url_ext=url_ext,
                                        latitude=latitude,
                                        longitude=longitude)

            p = int(res[0][0])
            if catnom is not None:  #to input different categories for commerce in the db
                catnom = catnom.split(",")
                for x in catnom:
                    db.post_commerce_categorie(catnom=x, cid=p)
                return jsonify({'status': 'ok'}), 201
            else:
                return jsonify({'status': 'ok'}), 201
    except Exception as e:
        return jsonify({'status': 'error 400', 'message': 'something went wrong!'}), 400

#Login
@app.route('/logincommerce', methods=["POST", 'GET'])
def check_commerce_get_cid():
    '''
    Login for commerce.

    Passed in PARAMS:
        cemail: str
        cmdp: str

    Response:
        dict['status']: bool
        dict['message']: str
        dict['token']: str, JSON Web Token 
        200 or 401
    '''
    cemail, cmdp = PARAMS.get('cemail', None), PARAMS.get('cmdp', None)
    if (cemail is None) or (cmdp is None):
        return jsonify({"status" : "error", "message" : "Invalid email or password"})
    else:
        res = list(db.fetch_login_commerce(cemail=cemail))
        if len(res) == 0:
            return jsonify({"status" : "error", "message" : "Invalid email or password"}), 401
        elif cmdp==res[0][2]:
        #elif check_password_hash(res[0][2], cmdp):
            status = db.check_commerce_active(cid=res[0][0])
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

#Modify account information      
@app.route('/mycommerce', methods=["PATCH", "PUT"])
def patch_commerce_info():
    '''
    Patch information of a commerce.

    Passed in PARAMS:
        auth_token: str, JSON Web Token
    
    Response:
        201 or 401
    '''
    auth_token = PARAMS.get("token", "")
    cid = is_authorized_no_id(auth_token, user_type='commerce')
    if cid:
        cid = int(cid)
        cnom = PARAMS.get("cnom", None)
        cpresentation = PARAMS.get("cpresentation", None)
        cemail = PARAMS.get("cemail", None)
        aid = PARAMS.get("aid", None)
        url_ext = PARAMS.get("url_ext", None)
        code_postal = PARAMS.get("code_postal", None)
        rue_and_num = PARAMS.get("rue_and_num", None)
        catnom = PARAMS.get("catnom", None)
        # catnom=Restaurant,Textile
        temp_aid = db.fetch_aid_from_commerce(cid=cid) #need to declare temp_aid for new geolocation calculation
        if cnom:
            db.patch_commerce_nom(cnom=cnom, cid=cid)
        if cpresentation:
            db.patch_commerce_cpresentation(
                cpresentation=cpresentation, cid=cid)
        if cemail:
            db.patch_commerce_cemail(cemail=cemail, cid=cid)
        if aid:
            db.patch_commerce_aid(aid=aid, cid=cid)
            temp_aid = aid
        if url_ext:
            db.patch_commerce_url_ext(url_ext=url_ext, cid=cid)
        if (code_postal) or (rue_and_num):
            prev_code_postal = db.fetch_code_postal_from_cid(cid=cid)[0][0]
            prev_rue_and_num = db.fetch_rue_and_num_from_cid(cid=cid)[0][0]
            if code_postal:
                prev_code_postal = code_postal
                db.patch_commerce_code_postal(code_postal=code_postal, cid=cid)
            if rue_and_num:
                prev_rue_and_num = rue_and_num
                db.patch_commerce_rue_and_num(rue_and_num=rue_and_num, cid=cid)
            latitude, longitude = convert_address_to_geolocation(code_postal=prev_code_postal,
                                                        rue_and_num=prev_rue_and_num,
                                                        aid=temp_aid)
            db.patch_commerce_lat_long(cid=cid, latitude=latitude, longitude=longitude)
        if catnom:
            db.delete_commerce_categorie(cid=cid)
            catnom = catnom.split(",")
            for x in catnom:
                db.post_commerce_categorie(catnom=x, cid=cid)
        return jsonify({"status" : "ok", "message" : "changed"}), 200
    else:
        return jsonify({"status" : "error", "message" : "Invalid email or password"}), 401

#Invalidate account
@app.route('/mycommerce', methods=['DELETE'])
def delete_commerce_info():
    '''
    Delete commerce account (Invalidate, actually)

    Passed in PARAMS:
        auth_token: str, JSON Web Token
    
    Response:
        200 or 401
    '''
    auth_token = PARAMS.get('token', None)
    cid = is_authorized_no_id(auth_token, user_type='commerce')
    if cid:
        db.invalidate_commerce_account(cid=int(cid))
        return Response(status=200)
    else:
        return Response(status=401)

#View your promotions
@app.route('/mycommerce/promotions', methods=['POST', 'GET'])
def fetch_promotion_of_commerce():
    '''
    Get the promotions of a commerce via id.

    Passed PARAMS:
        auth_token: str, JSON Web Token
    
    Response:
        if_auth dict containing:
            p.pdescription: str
            c.cnom: str
            p.tdebut: str, YYYY-MM-DD
            p.pid:int
        if not error status and message
    '''
    auth_token = PARAMS.get("token", None)
    cid = is_authorized_no_id(auth_token, user_type='commerce')
    if cid:
        res = db.fetch_promotion_of_commerce(cid=int(cid))
        return jsonify(res)
    else:
        return jsonify({'status': 'error 400', 'message': 'Something went wrong!'}), 400

#Post a promotion
@app.route('/promotion', methods=["POST"])
def post_promotion():
    '''
    Post a promotion from commerce-side front end

    Passed in PARAMS:
        pdescription: str
        tdebut: str, YYYY-MM-DD format
        tfin: str, YYYY-MM-DD format
        auth_token: str, JSON Web Token

    Response:
        dict['status']: bool
        dict['message']: str
        200, 400 or 401 depending on error or success
    '''
    #Getting info of promotion from HTTP request
    pdescription = PARAMS.get('pdescription', None)
    tdebut = PARAMS.get('tdebut', None) #maybe check for right format and better default option
    tfin = PARAMS.get('tfin', None)
    auth_token = PARAMS.get("token", '')
    cid_token = is_authorized_no_id(auth_token, user_type="commerce")
    if cid_token:
        try: #catch the exception if promotion info isn't adequate
            res = db.post_promotion(pdescription=pdescription,
                              tdebut=tdebut,
                              tfin=tfin,
                              cid=int(cid_token))
            p = int(res[0][0])
            return jsonify({"status" : "ok", "pid" :p}), 200        
        except Exception as e:
            return jsonify({"status" : "error", "message" : "Invalid email or password"}), 400
    else:
        return jsonify({"status" : "error", "message" : "Invalid email or password"}), 401
   
#Modify a promotion
@app.route('/promotion/<int:pid>', methods=['PATCH', 'PUT'])
def patch_promotion(pid):
    '''
    Patch a promotion from commerce-side front end

    Passed in PARAMS:
        pdescription: str
        tdebut: str, YYYY-MM-DD format
        tfin: str, YYYY-MM-DD format
        auth_token: str, JSON Web Token

    Response:
        dict['status']: bool
        dict['message']: str
        200, 400 or 401 depending on error or success
    '''
    pdescription = PARAMS.get('pdescription', None)
    tdebut = PARAMS.get('tdebut', None) #maybe check for right format and better default option
    tfin = PARAMS.get('tfin', None)
    auth_token = PARAMS.get("token", '')
    cid_token = is_authorized_no_id(auth_token, user_type="commerce")
    cid_associated_to_pid = db.fetch_cid_of_pid(pid=pid)
    app.logger.debug(cid_associated_to_pid)
    #check if commerce token is valid
    if cid_token:
        #check if commerce is modifying its own promotion
        if int(cid_associated_to_pid[0][0]) != int(cid_token):
            return jsonify({'status': 'error 401', 'message': 'something went wrong!'}), 401
        else:
            if pdescription is not None:
                db.patch_promotion_pdescription(pid=pid, pdescription=pdescription)
            if tdebut is not None:
                db.patch_promotion_tdebut(pid=pid, tdebut=tdebut)
            if tfin is not None:
                db.patch_promotion_tfin(pid=pid, tfin=tfin)
            return jsonify({'status': 'ok', 'message': 'good'}), 201
    else:
        return jsonify({'status': 'error 401', 'message': 'something went wrong!'}), 401

#Delete the promotion
@app.route('/promotion/<int:pid>', methods=["DELETE"])
def delete_promotion_info(pid):
    '''
    Delete promotion information

    Passed in url:
        pid: int
    Passed in PARAMS:
        auth_token: str

    Response:
        str or dict with success of error message.
    '''
    auth_token = PARAMS.get("token", None)
    cid = is_authorized_no_id(auth_token, user_type='commerce')
    if cid:
        res = db.delete_promotion_info(pid=pid)
        return jsonify({'status': 'ok', 'message': 'good'}), 201
    else:
        return jsonify({'status': 'error 400', 'message': 'Something went wrong!'}), 400

##Image handling for commerce interface queries

#post image
@app.route('/promotion/<int:pid>/image', methods=['POST'])
def upload_image(pid):
    '''
    Post an image for a promotion from commerce-side front end

    Passed in url:
        pid: int
    Passed in PARAMS:
        impFile: file
        auth_token: str, JSON Web Token

    Response:
        image id: int
        200, 400 or 401 depending on error or success
    '''
    uploaded_file = request.files['inpFile']
    auth_token = PARAMS.get("token", None)
    cid = is_authorized_no_id(auth_token, user_type='commerce')
    if cid:
        cid_associated_to_pid = db.fetch_cid_of_pid(pid=pid)
        #check if commerce is modifying own image
        if int(cid_associated_to_pid[0][0]) != int(cid):
            return Response(status=401)
        else:
            try:
                res = f_update_image(
                    'UPLOAD_PATH_PROMOTION',
                    pid,
                    lambda x, y, z: db.post_promotion_image(imgname=x,
                                                            ranks=y,
                                                            pid=z),
                    uploaded_file,
                    lambda x: db.get_rank_last_image_promotion(pid=x)) 
                return jsonify(res)
            except Exception as e:
                return Response(status=400)       
    else:
        return Response(status=401)

# Delete images of a promotion
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

#modify an image for a promotion
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
    '''
    Get the images of a promotions of a commerce

    Passed in url:
        pid: int
    
    Response:
        if_auth dict containing:
            image: name fo the image, rank for the order
        if not error status and message
    '''
    res = db.get_promotion_image(pid=pid)
    return jsonify(res)

@app.route('/get/promotion/image', methods=['POST', 'GET'])
def get_images_promotions():
    '''
    Get the images of a promotions of a commerce coomerce-side

    Passed in PARAMS:
        auth_token: str

    Response:
        if_auth dict containing:
            image: name fo the image, rank for the order
        if not error status and message
    '''

    auth_token = PARAMS.get("token", None)
    cid = is_authorized_no_id(auth_token, user_type='commerce')
    res = db.get_promotion_images(cid=cid)
    return jsonify(res)

#delete image fro a promotion
@app.route('/promotion/<int:pid>/image', methods=['DELETE'])
def delete_image(pid):
    '''
    Delete promotion image

    Passed in url:
        pid: int
    Passed in PARAMS:
        auth_token: str

    Response:
        str or dict with success of error message.
    '''

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
    '''
    Post an image for a commerce from commerce-side front end

    Passed in PARAMS:
        impFile: file
        auth_token: str, JSON Web Token

    Response:
        image id: int
        200, 400 or 401 depending on error or success
    '''

    uploaded_file = request.files['inpFile']
    auth_token = PARAMS.get("token", None)
    cid = is_authorized_no_id(auth_token, user_type='commerce')
    if cid:
        try:
            res = f_update_image('UPLOAD_PATH_COMMERCE', cid, lambda x, y, z: db.post_commerce_image(imgname=x,ranks=y,cid=z),
                            uploaded_file ,
                            lambda x: db.get_rank_last_image_commerce(cid=x) )         
            return jsonify(res)
        except Exception as e:
            return jsonify("error")
            return Response(status=400)
    else:
        return Response(status=401)


#to delete all images of a commerce
@app.route('/commerce/image', methods=['DELETE'])
def delete_commerce_images(cid):
    '''
    Delete all images for a commerce

    Passed in PARAMS:
        auth_token: str

    Response:
        str or dict with success of error message.
    '''

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
    '''
    Get the images of a commerce of a commerce commerce-side

    Passed in Params:
        auth_token: str
    
    Response:
  
      images name and ranks 
    '''

    auth_token = PARAMS.get("token", None)
    cid = is_authorized_no_id(auth_token, user_type='commerce')
    res = db.get_commerce_image(cid=cid)
    return jsonify(res)


@app.route('/commerce/<int:cid>/image', methods=['DELETE'])
def delete_image_commerce(cid):
    '''
    Delete an image of a commerce

    Passed in url:
        cid: int
    Passed in PARAMS:
        auth_token: str

    Response:
        str or dict with success of error message.
    '''

    #Authorization checks 
    auth_token = PARAMS.get("token", '')
    if is_authorized(auth_token, user_id=cid, user_type='commerce'):
        imageImid = PARAMS.get("imageImid", None)
        res=db.delete_commerce_image(cid=cid, imid=imageImid)
        os.remove(os.path.join(app.config['UPLOAD_PATH_COMMERCE'], res))
        return "",204
    else:
        return Response(status=401)

########## COMMERCE INTERFACE NAVIGATION ##########

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

@app.route('/informations')
def info():
    return render_template('informations.html')

@app.route('/addPromotion')
def add_promotion():
    return render_template('addPromotion.html')

@app.route('/modifierPromotion')
def modifier_promotion():
    return render_template('modifierPromotion.html')

@app.route('/modifierCommerce')
def modifier_commerce():
    return render_template('modifierCommerce.html')

@app.route('/static/commerceImage/<path:path>')
def send_pic(path):
    return send_from_directory('static/commerceImage', path)

@app.route('/static/promotionImage/<path:path>')
def send_pic_promotions(path):
    return send_from_directory('static/promotionImage', path)

@app.route('/commerceImage/<path:path>')
def send_pic_commerce(path):
    return send_from_directory('commerceImage', path)

@app.route('/commerce/verify', methods=["PATCH"])
def verify():
    imgname = PARAMS.get("imgname", None)
    db.verify_image(imgname=imgname)
    return "", 204