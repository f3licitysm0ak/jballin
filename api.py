from typing import List
from flask import Flask, request, render_template, session
from qobject import Question
from flask_sqlalchemy import SQLAlchemy
from application import app,db
from userclass import User
from datetime import datetime





 

qlist:List[Question] = list()
#defining list of type Question + making questions

q1=Question("What is the capital of Japan", "tokyo")
qlist.append(q1)


 


 


#variables to store username and password for making user object later
usrnm=""
pwd=""


#checking method for all questions
def check(text1, ind:int):


   

    if text1.lower()==qlist[ind].answer.lower():

       return True

    else:
       return False  


 

       




 

@app.route('/')
def login():
 
    return render_template("login.html" )#removed second item question=q

 


@app.route('/next', methods=['GET','POST'])
def my_form_post():



    
 
    global qlist

    myIndex:int=session['current_index']

    answer = request.form['text1']
    check(answer, myIndex)

    if check(answer,myIndex):
        s=session['score']
        s=s+1
        session['score']=s
    else:
        x=session['incorrect'] #list of questions which were answered incorrectly
        x.append(qlist[myIndex].question)
        session['incorrect']=x

        a=session['incorrecta'] #list of correct answers to questions which were answered incorrectly
        a.append(qlist[myIndex].answer)
        session['incorrecta']=a

        y=session['incorrect_entries']#list of answers which the user entered that were incorrect
        y.append(answer)
        session['incorrect_entries']=y

        print("Question answered incorrectly:" + str(x))
        print("Correct answer:" + str(a))
        print("User answered:" + str(y))

           


    
 

    

    if myIndex==len(qlist)-1:
         
        
        return render_template("score.html", score=session['score'], numqs=len(qlist))
        

         
    myIndex=myIndex+1
    session['current_index']= myIndex
    

    q=qlist[myIndex].question
    return render_template('home2.html', question=q)
    
@app.route('/start', methods=[ 'POST']) 
def start():
    global qlist



     
    session['current_index']= 0
    session['score']=0

    session['incorrect'] =[]
    session['incorrecta'] = []
    session['incorrect_entries']=[]

    qlist=Question.query.all()
 



    q=qlist[0].question
    return render_template("home2.html", question=q)


@app.route('/home', methods=['POST'])
def validate():
    


    #declared both username and password as global to avoid that error thing lol
    global usrnm
    global pwd

    usrnm = request.form['username']
    pwd = request.form['password']

    if User.validate_user(usrnm,pwd)==True:

        session['username']=usrnm
        print ("User " + session["username"] + " has logged in.")
        return render_template("home.html", message="")
    else:
        return render_template("login.html", error="LOGIN FAILED. Please try again with a different username or password.")
    

#adding new route(s?) for entering questions

@app.route('/qform', methods=['GET'])
def show_form():
    return render_template('create.html')

@app.route('/create' , methods=['POST'])
def add():
    global pq
    global pa

    pq=request.form['propq']
    pa=request.form['propa']

    newq=Question(pq,pa)#creates Question object with pq and pa as question and answer attributes
    db.session.add(newq)
    db.session.commit()#appends newly made question to database
    return render_template("home.html", message="Question successfully created.")
    
#route(s) below for registering new users
@app.route('/register', methods=['POST'])#might need to add get here if it doesnt work
def reg():
    return render_template('register.html')

@app.route('/registered', methods=['POST'])#might need to add get here if it doesnt work
def regd():

    newu=request.form['cusername']
    newp=request.form['cpassword']

    new_user=User(username=newu, passwd=newp)

    db.session.add(new_user)
    db.session.commit()



    return render_template("login.html", error="Account successfully created.")


#(attempted) route to display incorrect answers
@app.route('/view', methods=['POST'])
def display():


    q=session['incorrect']
    an=session['incorrecta']
    e=session['incorrect_entries']

    return render_template("view.html", len=len(qlist), questions=q, you_answered=e, correct_answer=an)







    

@app.route('/logout', methods=['POST'])
def logout():
    return render_template("login.html", error="")



    

 
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)