#!/usr/bin/python3
# -*- coding: utf-8 -*-
# author:sunliwei1981
# date:10/05/2021


from application import app
from flask import Blueprint, make_response, current_app, g
from flask_restful.utils import PY3
from json import dumps
from flask_restful import Api

from app.controllers.route_index import route_index
from app.resources.Login import Login


# below are restful resources
restful_api = Blueprint('restful_api', __name__)


@restful_api.before_request
def before_request():
    """User authentication"""
    # do authentication here
    user = "authenticated user"
    g.user = user


api = Api(restful_api)


@api.representation('application/json')
def output_json(data, code, headers=None):
    """wrap the restful response json body, add status and message fields, if it does not have one"""

    if 'status' not in data:
        data = {
            'status': 1,
            'message': 'OK',
            'data': data
        }

    settings = current_app.config.get('RESTFUL_JSON', {})

    # If we're in debug mode, and the indent is not set, we set it to a
    # reasonable value here.  Note that this won't override any existing value
    # that was set.  We also set the "sort_keys" value.
    if current_app.debug:
        settings.setdefault('indent', 4)
        settings.setdefault('sort_keys', not PY3)

    # always end the json dumps with a new line
    dumped = dumps(data, **settings) + "\n"
    resp = make_response(dumped, code)
    resp.headers.extend(headers or {})
    return resp


# register all restful apis here
api.add_resource(Login, '/login/')


# register all routes here
app.register_blueprint(route_index, url_prefix="/")
app.register_blueprint(restful_api, url_prefix="/resources")
