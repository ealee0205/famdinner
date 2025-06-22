# famdinner
## For first usage:
First make sure you are not using the macOS builtin python. Run `which python3` to see that PATH. By default, macOS python builtin will be at `/usr/bin/python` instead of `/user/bin/local/python`

To create the venv, run:
```
python3 -m venv venv
. venv/bin/activate
pip install -U pip
pip install -r requirements.txt
```


To run the flask app in a local port, run:
```
flask --debug --app=famdinner run
```

To set up the db:
```
from famdinner import db, create_app
app=create_app()
with app.app_context():
    db.create_all()
ctx=app.app_context()
ctx.push()
from famdinner import create_admin
create_admin()
ctx.pop()
```