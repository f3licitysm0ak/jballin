from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from userclass import User
from application import db
from dataclasses import dataclass

@dataclass
class TestInfo(db.Model):
    id:int=db.Column(db.Integer, primary_key=True)
    user_id=db.Column(db.Integer,db.ForeignKey(User.id), nullable=False)
    date_taken:datetime=db.Column(db.DateTime, default=datetime.utcnow)
    score=db.Column(db.Integer, nullable=False) #this is just the raw score, ex. if 30/60 then score=30
    numqs=db.Column(db.Integer, nullable=False)#total number of questions in the test at that time(hopefully)
    
    


    def __init__(self, user_id, score, numqs):
     
        self.user_id=user_id
        self.score=score
        self.numqs=numqs


    def getscore(self):
        return self.score
        

    def getdate(self):
        return self.date_taken
        

    def getnumqs(self):
        return self.numqs
        

   
        