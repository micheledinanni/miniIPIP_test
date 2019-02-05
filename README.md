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
To change the admin password go to:
* `/admin`

``
  Check 'Change Password' on top right and insert old password,
  then insert your new password.
``
##### Notice that the user is 'admin'
