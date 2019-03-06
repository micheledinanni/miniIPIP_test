import json, csv
import smtplib, os, yaml, threading
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from pathlib import Path
from myproject.logger import logger_file
from django.utils.crypto import get_random_string
from .models import EmailToken

class Email_token_to_save():
    id = None

class ModelEmail():
    subject = None
    text = None
    email = None
    token = None


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


# SMTP Constants
SMTP_SERVER = email_host()
SMTP_PORT = email_port()
SMTP_USER = email_host_user()
SMTP_PSW = email_host_passwd()

# MAIL Constants
MAIL_SENDER = email_from()


class EmailThread(threading.Thread):
    def __init__(self, name, mail):
        threading.Thread.__init__(self)
        self.name = name
        self.mail = mail

    def run(self):
        global smtp_session
        try:
            smtp_session = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
            smtp_session.ehlo()
            smtp_session.starttls()
            smtp_session.login(SMTP_USER, SMTP_PSW)
            msg = MIMEMultipart()
            msg['From'] = MAIL_SENDER
            msg['Subject'] = ModelEmail.subject
            msg['To'] = self.mail
            body = ModelEmail.text
            msg.attach(MIMEText(body, 'plain'))
            id = get_random_string(length=6)
            text = msg.as_string().format(id)
            Email_token_to_save.id = id
            smtp_session.sendmail(MAIL_SENDER, [MAIL_SENDER, self.mail], text)
            save_for_ajax(1, len(ModelEmail.email))
            smtp_session.quit()
        except Exception as e:
            error = str(e)
            logger_file(error)
            save_for_ajax(0, len(ModelEmail.email))
            smtp_session.quit()


def running():
    for email in ModelEmail.email:
        EmailThread1 = EmailThread(name='Sending email to{0}'.format(email), mail=email)
        EmailThread1.start()
        EmailThread1.join()
        q = EmailToken(id_test=Email_token_to_save.id,email=email)
        q.save()


def save_for_ajax(value, number_of_emails):
    with open('myproject/ajax_files/status.json', 'r')as f:
        data = json.load(f)
        if value is 1:
            data["number_of_emails_sent"] = data["number_of_emails_sent"] + 1
        else:
            data["number_of_not_sent_emails"] = data["number_of_not_sent_emails"] + 1
    with open('myproject/ajax_files/status.json', 'w') as write:
        values = {"number_of_emails_sent": data["number_of_emails_sent"],
                  "number_of_total_emails": number_of_emails,
                  "number_of_not_sent_emails": data["number_of_not_sent_emails"]}
        json.dump(values, write)
        f.close()
        write.close()



