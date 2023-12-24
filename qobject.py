from flask_sqlalchemy import SQLAlchemy
from userclass import User
from datetime import datetime
from application import db
from sqlalchemy.orm import relationship
from dataclasses import dataclass

@dataclass
class Question(db.Model):
    id:int=db.Column(db.Integer, primary_key=True)
    question:str=db.Column(db.String(300), nullable=False)
    answer:str=db.Column(db.String(20), nullable=False)
    img:str=db.Column(db.String(500), nullable=False)
    date_created:datetime=db.Column(db.DateTime, default=datetime.utcnow)
    created_by:int=db.Column(db.Integer, db.ForeignKey(User.id), nullable=True)
    
    creator=relationship('User', foreign_keys='Question.created_by')
    

    
    
    def __init__(self, question, answer,img):
        self.question=question
        self.answer=answer
        self.img=img
    def set_answer(self, user_ans ):
        self.user_ans=user_ans

    