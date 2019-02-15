# mini-IPIP test
The mini-IPIP test has been developed to identify the personality of Apache developers, based on this following paper:</h5>
```bash
Donnellan MB, Oswald FL, Baird BM, Lucas RE(2006). The mini-IPIP scales: tiny-yet-effective measures 
of the Big Five factors of personality. DOI: 10.1037/1040-3590.18.2.192
```

## 1. Cloning
```bash
$ git clone https://github.com/micheledinanni/miniIPIP_test.git
```
## 2. DB Configuration 
Edit the following configuration file:
* `myproject/cfg/config.yml` - sqlite database configuration 
```yaml
sqlite:
  host: localhost
  user: root
  passwd: ****
  db: db.sqlite3
```
## 3. Initial email configuration
Edit the following configuration file:
* `myproject/cfg/config.yml` - Initial sending email, with setting of host, host user,host port and host password.
                               It has been used the server smtp 'Amazon SES'
```yaml
email:
   email_from: 'collab.uniba@gmail.com'
   email_host: 'secret'
   email_host_user: "secret"
   email_host_passwd: "secret"
   email_port: secret
```
## 4. Change admin password
To change the admin password go into website and paste after website name:
* `/admin`
Check 'Change Password' on top right,insert previous password and insert your new password.
You can take the default password from: 
* ` myproject/cfg/config.yml`

```yaml
django-admin-default-credentials:
  username: admin
  passwd: collab-uniba
```  
Then save your changes.
## 5. Send email into admin
To match the token created for every user, use this syntax into the text of email:
* `your-url-site/miniipip?id={0}`
It is automatically associated a token to take the test.

## 6. Information
```yaml
Every e-mail in the admin is sent every 9 seconds
`The display of the progress to sending emails can be viewed every 10 seconds 
  (the page updates automatically every 10 seconds).
You will see a progress bar and a message to know on-time the sending-progress. 
```
--------------------------------------------------------------------------------------------------------------------------------
## Installation guide
```bash
1. $ git clone https://github.com/micheledinanni/miniIPIP_test.git 
2. cd miniIPIP_test
3. virtualenv venv --no-site-packages
4. source venv/Scripts/activate
5. pip install -r requirements.txt
6. Edit file config.yml into this source myproject/cfg/
7. python manage.py runserver (optionally add port)
```

