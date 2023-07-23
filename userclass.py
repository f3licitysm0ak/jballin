from typing import List
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from application import db
 
class User(db.Model):
    id=db.Column(db.Integer, primary_key=True)
    username=db.Column(db.String(200), nullable=False)
    passwd=db.Column(db.String(200), nullable=False) 
    date_created=db.Column(db.DateTime, default=datetime.utcnow)
    is_admin=db.Column(db.Boolean,nullable=False, default=False)



#making function to return database ids
    def __repr__(self):
        return '<User ID: %r>' % self.id

        
    

    def __init__(self, username, passwd):
        self.username=username
        self.passwd=passwd



    def validate_user(usrn, pw):
        u=User.query.filter(User.username==usrn).first()
        if u:
            if u.passwd==pw:
                return True
            else:
                return False
            
        else:
            return False
         
        

    


