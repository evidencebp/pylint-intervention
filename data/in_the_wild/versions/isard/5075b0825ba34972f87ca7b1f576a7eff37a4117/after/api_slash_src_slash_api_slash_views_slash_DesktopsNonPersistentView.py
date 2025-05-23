# Copyright 2017 the Isard-vdi project authors:
#      Josep Maria Viñolas Auquer
#      Alberto Larraz Dalmases
# License: AGPLv3

import json
import logging as log
import os
import sys
import time
import traceback
from uuid import uuid4

from flask import request

#!flask/bin/python
# coding=utf-8
from api import app

from ..libv2.api_exceptions import Error
from ..libv2.quotas import Quotas

quotas = Quotas()

from ..libv2.api_desktops_nonpersistent import ApiDesktopsNonPersistent

desktops = ApiDesktopsNonPersistent()

from .decorators import allowedTemplateId, has_token, is_admin, ownsDomainId


@app.route("/api/v3/desktop", methods=["POST"])
@has_token
def api_v3_desktop_new(payload):
    try:
        user_id = payload["user_id"]
        template_id = request.form.get("template", type=str)
    except:
        raise Error(
            "bad_request", "New desktop bad body data", traceback.format_stack()
        )

    if user_id == None or template_id == None:
        raise Error(
            "bad_request", "New desktop missing body data", traceback.format_stack()
        )

    allowedTemplateId(payload, template_id)

    # Leave only one nonpersistent desktop from this template
    desktops.DeleteOthers(user_id, template_id)

    # So now we have checked if desktop exists and if we can create and/or start it
    return (
        json.dumps({"id": desktops.New(user_id, template_id)}),
        200,
        {"Content-Type": "application/json"},
    )


@app.route("/api/v3/desktop/<desktop_id>", methods=["DELETE"])
@has_token
def api_v3_desktop_delete(payload, desktop_id):

    ownsDomainId(payload, desktop_id)
    desktops.Delete(desktop_id)
    return json.dumps({}), 200, {"Content-Type": "application/json"}
