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
    if PARAMS.get("nb", None) is None:
        if PARAMS.get("agglomeration", None) is None:
            res = db.get_promotion_all()
        else:
            agglo = PARAMS.get("agglomeration", None)
            res = db.get_promotion_agg_all(agg=agglo)
    else:
        nb = PARAMS.get("nb", None)
        agglo = PARAMS.get("agglomeration", None)
        if agglo is None:
            res = db.get_promotion_nb_all(nb=nb)
        else:
            res = db.get_promotion_agg_nb(nb=nb, agg=agglo)
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

### INTERACTION WITH FRONT PAGE

### SECOND PAGE - MAP - QUERIES

### THIRD PAGE - LISTS - QUERIES 