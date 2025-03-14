# Copyright 2017 the Isard-vdi project
# License: AGPLv3

#!flask/bin/python3
# coding=utf-8

import json
import os
import sys
import time
import traceback
from uuid import uuid4

from flask import jsonify, request

from api import app

from ..libv2.api_exceptions import Error
from ..libv2.api_users import ApiUsers, check_category_domain
from ..libv2.log import log

users = ApiUsers()

with open("/version", "r") as file:
    version = file.read()


@app.route("/api/v3", methods=["GET"])
def api_v3_test():
    return (
        json.dumps(
            {"name": "IsardVDI", "api_version": 3.1, "isardvdi_version": version}
        ),
        200,
        {"Content-Type": "application/json"},
    )


@app.route("/api/v3/categories", methods=["GET"])
def api_v3_categories():
    return (
        json.dumps(users.CategoriesFrontendGet()),
        200,
        {"Content-Type": "application/json"},
    )
