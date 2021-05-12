#!/usr/bin/python3
# -*- coding: utf-8 -*-
# author:sunliwei1981
# date:10/05/2021


from flask import Blueprint, json, render_template, Response, request
from application import db

route_index = Blueprint("route_index", __name__)


@route_index.route("/", methods=["GET"])
def index():
    # do something
    return render_template("index.html")


