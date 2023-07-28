from flask_sqlalchemy import SQLAlchemy
from userclass import User
from datetime import datetime
from application import db
from sqlalchemy.orm import relationship

class Question(db.Model):
    id=db.Column(db.Integer, primary_key=True)
    question=db.Column(db.String(300), nullable=False)
    answer=db.Column(db.String(20), nullable=False)
    date_created=db.Column(db.DateTime, default=datetime.utcnow)
    created_by=db.Column(db.Integer, db.ForeignKey(User.id), nullable=True)
    
    creator=relationship('User', foreign_keys='Question.created_by')
    

    
    
    def __init__(self, question, answer):
        self.question=question
        self.answer=answer
    def set_answer(self, user_ans ):
        self.user_ans=user_ans

    