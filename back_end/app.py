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
app = Flask("promotion")

# load configuration, fall back on environment
from os import environ as ENV

# will be used later 
from werkzeug.security import generate_password_hash, check_password_hash

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


#
# GET /version
#
# general information about the application
#
@app.route("/version", methods=["GET"])
def get_version():
    # TODO check read permission
    now = db.now()[0][0]
    # BEWARE all requests must commit…
    # TODO automate commit call on all requests
    db.commit()
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

# GET /promotion with filter for number returned and agglomeration
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
    db.commit()
    return jsonify(res)


# GET /commerce with filter for categorie and agglomeration
# different approach than above; we don't treat individual cases
# rather we will do the join anyway 
@app.route("/commerce", methods=["GET"])
def get_commerce():
    cat = PARAMS.get("categorie", '%')
    agglo = PARAMS.get("agglomeration", '%')
    res = db.get_commerce(agg=agglo, cat=cat)
    db.commit()
    return jsonify(res)


### ACCOUNT RELATED QUERIES
@app.route('/client/<int:clid>', methods=["GET"])
def get_client_info(clid):
    # authentication checks required 
    res = db.get_client_info(clid=clid)
    db.commit()
    return jsonify(res)

@app.route('/client/<int:clid>', methods=["PATCH", "PUT"])
def patch_client_info(clid):
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
    db.commit()
    return Response(status=201)


@app.route('/signup', methods=["POST"])
def post_client_info():
    #authentication check that query coming from app?
    clnom, clpnom = PARAMS.get("clnom", None), PARAMS.get("clpnom", None), 
    clemail, aid = PARAMS.get("clemail", None), PARAMS.get("aid", None)
    clmdp = generate_password_hash(PARAMS.get("clmdp", None))
    try: #catch the exception if the client already exists in the database
        db.post_client_info(clnom=clnom, clpnom=clpnom, clemail=clemail, aid=aid, clmdp=clmdp)
        db.commit()
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
        db.commit()
        app.logger.debug(res)
        app.logger.debug(clmdp)
        if check_password_hash(res[0][2], clmdp):
            return jsonify(res[0][0])
        else:
            return Response(status=401)

### INTERACTION WITH FRONT PAGE

### SECOND PAGE - MAP - QUERIES

### THIRD PAGE - LISTS - QUERIES 

### commerce interface

@app.route('/commerce/<int:cid>', methods=["GET"])
def get_commerce_info(cid):
    # authentication checks required 
    res = db.get_commerce_info(cid=cid)
    db.commit()
    return jsonify(res)
#curl -i -X GET http://0.0.0.0:5000/commerce/1


@app.route('/commerce/<int:cid>', methods=["PATCH", "PUT"])
def patch_commerce_info(cid):
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
        db.commit()
        catnom=catnom.split(",")
        for x in catnom:
            db.post_commerce_categorie(catnom=x, cid=cid)
    db.commit()
    return Response(status=201)
#curl -i -X PATCH -d cnom=zara -d cpresentation=casual -d cemail=zara@hotmail.com -d aid=1 -d cmdp=zarapassword -d rue_and_num=270 rue saint jacques -d code_postal=75005 -d url_ext=xyz -d catnom=Textile,Restaurant http://0.0.0.0:5000/commerce/1

@app.route('/commerce', methods=["POST"])
def post_commerce_info():
    #authentication check that query coming from app?
    cnom, cpresentation = PARAMS.get("cnom", None), PARAMS.get("cpresentation", None)
    cemail, aid = PARAMS.get("cemail", None), int(PARAMS.get("aid", None))
    url_ext, code_postal = PARAMS.get("url_ext", None), int(PARAMS.get("code_postal", None))
    rue_and_num = PARAMS.get("rue_and_num", None)
    cmdp = generate_password_hash(PARAMS.get("cmdp", None))
    catnom=PARAMS.get("catnom", None)

    try: #catch the exception if the commerce already exists in the database
        res=db.post_commerce_info(cnom= cnom, cpresentation= cpresentation, cemail= cemail, aid= aid, cmdp= cmdp, rue_and_num= rue_and_num, code_postal= code_postal, url_ext= url_ext, catnom= catnom)
        db.commit()
       # return(repr(res))
        p = int(res[0][0])
        if "catnom" in PARAMS:
            catnom=catnom.split(",")
            for x in catnom:
                db.post_commerce_categorie(catnom=x, cid=p)
                db.commit()
            return jsonify(res[0][0])
    except Exception as e:
        #return str(e)
        return Response(status=400)

