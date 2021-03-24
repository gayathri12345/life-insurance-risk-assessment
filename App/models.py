from App import db
from flask_login import UserMixin


class User(UserMixin,db.Model):
    id=db.Column(db.Integer, primary_key=True)
    username=db.Column(db.String(15),unique=True)
    email=db.Column(db.String(15),unique=True)
    password=db.Column(db.String(80))

    def __repr__(self):
    	return "<Username :{} and email id: {}>".format(self.username,self.email)