
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from application import db
from dataclasses import dataclass

@dataclass 
class User(db.Model):
    id:int=db.Column(db.Integer, primary_key=True)
    username:str=db.Column(db.String(200), nullable=False)
    passwd:str=db.Column(db.String(200), nullable=False) 
    date_created:datetime=db.Column(db.DateTime, default=datetime.utcnow)
    is_admin:bool=db.Column(db.Boolean,nullable=False, default=False)



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
         
        

    


