# -*- coding:utf-8 -*- 
# author = 'denishuang'
from __future__ import unicode_literals
import os
import logging
from logging.handlers import SMTPHandler
from app import app, DEBUG

PROJECT = os.environ.get('PROJECT', '')
LOG_FILE = os.environ.get('LOG_FILE')

app.config['MAIL_SERVER'] = os.environ.get('MAIL_SERVER')
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
# app.config['MAIL_PORT'] = 465
# app.config['MAIL_USE_TLS'] = False
# app.config['MAIL_USE_SSL'] = True
app.config['MAIL_USERNAME'] = os.environ.get('MAIL_USERNAME')
app.config['MAIL_PASSWORD'] = os.environ.get('MAIL_PASSWORD')
app.config['ADMINS'] = os.environ.get('ADMINS', '').split(',')


def add_file_handler():
    file_handler = logging.FileHandler(LOG_FILE)
    file_handler.setLevel(logging.ERROR)
    file_handler.setFormatter(logging.Formatter(
        '%(asctime)s %(levelname)s: %(message)s '
        '[in %(pathname)s:%(lineno)d]'
    ))
    app.logger.addHandler(file_handler)


class XSMTPHandler(SMTPHandler):

    def getSubject(self, record: logging.LogRecord) -> str:
        ls = record.msg.split('\n')
        head = ls[0][:255]
        return f'[ERROR]{PROJECT}:{head}'


def add_mail_handler():
    mail_handler = XSMTPHandler(
        mailhost=(app.config['MAIL_SERVER'], app.config['MAIL_PORT']),
        fromaddr=app.config['MAIL_USERNAME'],
        toaddrs=app.config['ADMINS'],
        subject=f'[ERROR]{PROJECT}',
        credentials=(app.config['MAIL_USERNAME'], app.config['MAIL_PASSWORD'])
    )
    mail_handler.setLevel(logging.DEBUG if DEBUG else logging.ERROR)

    mail_handler.setFormatter(logging.Formatter(
        """
        Message type:       %(levelname)s
        Location:           %(pathname)s:%(lineno)d
        Module:             %(module)s
        Function:           %(funcName)s
        Time:               %(asctime)s
    
        Message:
    
        %(message)s
        """
    ))
    app.logger.addHandler(mail_handler)


if app.config['MAIL_SERVER']:
    add_mail_handler()

if LOG_FILE:
    add_file_handler()
