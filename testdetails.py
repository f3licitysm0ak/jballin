from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from userclass import User
from application import db
from dataclasses import dataclass
from testinfo import TestInfo

@dataclass
class TestDetails(db.Model):
    id:int=db.Column(db.Integer, primary_key=True)
    attempt_id=db.Column(db.Integer, db.ForeignKey(TestInfo.id), nullable=False)
    question:str=db.Column(db.String(300), nullable=False)
    answer:str=db.Column(db.String(200), nullable=False)
    user_answered:str=db.Column(db.String(300), nullable=False)

    def __init__(self, attempt_id, question, answer, ua):
        self.attempt_id=attempt_id
        self.question=question
        self.answer=answer
        self.user_answered=ua
