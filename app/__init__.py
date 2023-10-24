from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_admin import Admin

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "mysql+pymysql://root:matkhauroot@localhost/doan?charset=utf8mb4"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True
app.config['SECRET_KEY'] = '123456'
db = SQLAlchemy(app=app)
admin = Admin(app=app, name='QUẢN TRỊ', template_mode='bootstrap4')
