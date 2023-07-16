from typing import List
from session import Session

class User:

    
    #need to make static list of Users shared between all instances of the class? 
    userDict={"Stefanie":"fansensei", "Katelyn":"tarokaite"}



    def __init__(self, username, passwd):
        self.username=username
        self.passwd=passwd
        self.session_list:List[Session]
        User.userDict[username]=passwd
    
    def add_session(self, session:Session):
        self.session_list.append(session)

    def validate_user(usrn, pw):
        if User.userDict.get(usrn)==pw:
            return True
        else:
            return False

    


