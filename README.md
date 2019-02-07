# Mini-Ipip test
This test has been developed to identify the personality of Apache developers, based on this following paper:</h5>
```bash
Donnellan MB1, Oswald FL, Baird BM, Lucas RE(2006). The mini-IPIP scales: tiny-yet-effective measures 
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
* `myproject/cfg/config.yml` - initial email to sending and password
```yaml
email:
  email_from: "collab.uniba@gmail.com"
  passwd: ****
```
## 4. Change admin password
To change the admin password go into website and paste after website name:
* `/admin`
```
Check 'Change Password' on top right,insert previous password
(you can take it from '/myproject/cfg/config.yml')and insert your new password.
Then save your changes.
```
##### Notice that the username is 'admin'
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
