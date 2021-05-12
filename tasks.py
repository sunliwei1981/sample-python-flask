#!/usr/bin/python3
# -*- coding: utf-8 -*-
# author:sunliwei1981
# date:10/05/2021


from celery import Celery
from flask_mail import Message
from application import app, mail


def make_celery(app):
    celery = Celery(app.import_name,
                    backend=app.config['CELERY_RESULT_BACKEND'],
                    broker=app.config['CELERY_BROKER_URL'])
    celery.conf.update(app.config)
    return celery


celery = make_celery(app)


@celery.task
def send_mail(subject, recipients, body):
    message = Message(subject=subject, recipients=recipients, body=body, charset="utf-8")
    mail.send(message)
