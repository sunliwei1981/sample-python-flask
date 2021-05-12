#!/usr/bin/python3
# -*- coding: utf-8 -*-
# author:sunliwei1981
# date:10/05/2021


from flask_restful import Resource


class Login(Resource):
    def get(self):
        # do login
        return {'func': 'login'}
