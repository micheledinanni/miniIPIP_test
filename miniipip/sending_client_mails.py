import smtplib , os, yaml, threading
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from myproject.logger import logger_file


class ModelEmail():
    subject = None
    text = None
    email = None
    flag = None


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
    def __init__(self, name):
        threading.Thread.__init__(self)
        self.name = name

    def run(self):
        global smtp_session
        try:
            smtp_session = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
            smtp_session.ehlo()
            smtp_session.starttls()
            smtp_session.login(SMTP_USER, SMTP_PSW)
            msg = MIMEMultipart()
            msg['From'] = MAIL_SENDER
            msg['Subject'] = 'My results of the Big 5 personality test'
            msg['To'] = ModelEmail.email
            body = ModelEmail.text
            msg.attach(MIMEText(body, 'plain'))
            text = msg.as_string()
            smtp_session.sendmail(MAIL_SENDER, [MAIL_SENDER, ModelEmail.email], text)
            smtp_session.quit()
            ModelEmail.flag = 1
        except Exception as e:
            error = str(e)
            logger_file(error)
            smtp_session.quit()


def client_send_mail():
    EmailThread1 = EmailThread(name='Sending email')
    EmailThread1.start()
    EmailThread1.join()
    if ModelEmail.flag is 1:
        return 1
    else:
        return 0
