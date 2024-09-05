# -*- coding:utf-8 -*- 
# author = 'denishuang'
from __future__ import unicode_literals
import os, ssl, email
import logging
import smtplib
from logging.handlers import SMTPHandler
from app import app, DEBUG
from email.message import EmailMessage

PROJECT = os.environ.get('PROJECT', '')
LOG_FILE = os.environ.get('LOG_FILE')

app.config['MAIL_SERVER'] = os.environ.get('MAIL_SERVER')
app.config['MAIL_PORT'] = 465
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
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


class SSLSMTPHandler(SMTPHandler):
    def emit(self, record):
        """
        Override emit method to use smtplib.SMTP_SSL for sending emails.
        """
        try:
            port = self.mailport
            if not port:
                port = smtplib.SMTP_SSL_PORT  # 默认 SSL 端口 465
            smtp = smtplib.SMTP_SSL(self.mailhost, port)
            content = self.format(record)
            msg = EmailMessage()
            msg['From'] = self.fromaddr
            msg['To'] = ','.join(self.toaddrs)
            msg['Subject'] = self.getSubject(record)
            msg['Date'] = email.utils.localtime()
            msg.set_content(content)

            if self.username:
                print(smtp.login(self.username, self.password))
            smtp.send_message(msg)
            smtp.quit()
        except Exception:
            self.handleError(record)

    def getSubject(self, record: logging.LogRecord) -> str:
        s = record.message.replace('\n', ' ')[:255]
        s = f'[ERROR]{PROJECT}:{s}'
        if record.exc_text:
            t = record.exc_text.strip().split('\n')[-1][:255]
            s = f'{s}:{t}'
        return s


def add_mail_handler():
    mail_handler = SSLSMTPHandler(
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
