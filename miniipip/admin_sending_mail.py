import smtplib
import time
import os
import yaml
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


def email_from():
    with open(os.path.join("myproject", "cfg", "config.yml"), "r") as ymlfile:
        cfg = yaml.load(ymlfile)
        email = cfg['email'].__getitem__('email_from')
    return email


def email_host():
    with open(os.path.join("myproject", "cfg", "config.yml"), "r") as ymlfile:
        cfg = yaml.load(ymlfile)
        host = cfg['email'].__getitem__('email_host')
    return host


def email_host_user():
    with open(os.path.join("myproject", "cfg", "config.yml"), "r") as ymlfile:
        cfg = yaml.load(ymlfile)
        host_user = cfg['email'].__getitem__('email_host_user')
    return host_user


def email_host_passwd():
    with open(os.path.join("myproject", "cfg", "config.yml"), "r") as ymlfile:
        cfg = yaml.load(ymlfile)
        host_passwd = cfg['email'].__getitem__('email_host_passwd')
    return host_passwd


def email_port():
    with open(os.path.join("myproject", "cfg", "config.yml"), "r") as ymlfile:
        cfg = yaml.load(ymlfile)
        host_port = cfg['email'].__getitem__('email_port')
    return host_port


def main_send_email(subject, text_sending, email):
    from_address = email_from()
    to_address = email
    subject = subject
    msg = MIMEMultipart()
    msg['From'] = email_from()
    msg['To'] = email
    msg['Subject'] = "Mini-IPIP: {}".format(subject)

    body = text_sending

    msg.attach(MIMEText(body, 'plain'))
    try:
        server = smtplib.SMTP(email_host(), email_port())
        server.starttls()
        server.login(email_host_user(), email_host_passwd())
        text = msg.as_string()
        server.sendmail(from_address, to_address, text)
        time.sleep(9)
        server.quit()
        return 1
    except Exception:
        return 0
