#!/usr/bin/python3
# -*- coding: utf-8 -*-
# author:sunliwei1981
# date:10/05/2021


from gevent import monkey
monkey.patch_all()

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import socket
from flask_socketio import SocketIO
from flask_mail import Mail


db = SQLAlchemy()
mail = Mail()
socketio = SocketIO(async_mode=None)
cors = CORS()


class Application(Flask):
    def __init__(self, import_name):
        super(Application, self).__init__(import_name)
        if socket.gethostname() == "production_host_name":
            self.config.from_pyfile('config/production_setting.py')
        else:
            self.config.from_pyfile('config/dev_setting.py')
        self.config['SECRET_KEY'] = 'my_secret_key'
        db.init_app(self)
        mail.init_app(self)        
        socketio.init_app(self,
                          message_queue='redis://127.0.0.1:6379/2',
                          logger=True,
                          engineio_logger=self.logger,
                          cors_allowed_origins="*",
                          debug=self.config["DEBUG"]
                          )
        cors.init_app(self)


app = Application(__name__)
