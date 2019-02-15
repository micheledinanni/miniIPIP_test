import csv
import json
import smtplib, time, os, yaml, threading
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from pathlib import Path
from django.utils.crypto import get_random_string


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
BCC = [email_from()]

class EmailThread(threading.Thread):
    def __init__(self, name):
        threading.Thread.__init__(self)
        self.name = name

    def run(self):
        global smtp_session
        clean_file_json()
        Path('myproject/ajax_files/data.csv').touch()
        msg = MIMEMultipart()
        msg['From'] = MAIL_SENDER
        msg['Subject'] = ModelEmail.subject
        body = ModelEmail.text
        msg.attach(MIMEText(body, 'plain'))
        try:
            smtp_session = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
            smtp_session.ehlo()
            smtp_session.starttls()
            smtp_session.login(SMTP_USER, SMTP_PSW)
            for mail in ModelEmail.email:
                id = get_random_string(length=6)
                text = msg.as_string().format(id)
                msg['To'] = mail
                smtp_session.sendmail(MAIL_SENDER,[mail,BCC],text)
                save_into_file(mail, id)
                save_for_ajax(1, len(ModelEmail.email))
                time.sleep(9)
        except Exception:
            save_for_ajax(0, len(ModelEmail.email))
            smtp_session.quit()
            return 0
        smtp_session.quit()


def running():
    EmailThread1 = EmailThread(name='Sending email')
    EmailThread1.start()
    EmailThread1.join()


def save_into_file(email, token):
    with open('myproject/ajax_files/data.csv', 'a') as csvfile:
        fieldnames = ['email', 'token', 'send']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerow({'email': email, 'token': token})
        csvfile.close()


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


def clean_file_json():
    with open('myproject/ajax_files/status.json', 'w') as f:
        data = {"number_of_emails_sent": 0,
                "number_of_total_emails": 0,
                "number_of_not_sent_emails": 0}
        json.dump(data, f)
        f.close()
