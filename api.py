from typing import List
from flask import Flask, request, render_template, session, flash, redirect, request, url_for
from qobject import Question
from flask_sqlalchemy import SQLAlchemy
from application import app,db
from userclass import User
from datetime import datetime
from dateutil import tz #to set appropriate timezone
from dataclasses import dataclass
from testinfo import TestInfo
from testdetails import TestDetails





 






 


 


#variables to store username and password for making user object later
usrnm=""
pwd=""


#checking method for all questions
def check(text1, ind:int):


   
    qlist=session['qlist']
    print(ind)
    print(qlist[ind])
    if text1.lower()==qlist[ind]['answer'].lower():

       return True

    else:
       return False  


 

       




 

@app.route('/')
def login():
 
    return render_template("login.html" )#removed second item question=q



@app.route('/next', methods=['GET','POST'])
def my_form_post():



    
 
    qlist=session['qlist']

    myIndex:int=session['current_index']

    answer = request.form['text1']
    check(answer, myIndex)

   
    if check(answer,myIndex):
        s=session['score']
        s=s+1
        session['score']=s

    x=session['incorrect'] #labeled as incorrect but actually ALL questions in the current session
    x.append(qlist[myIndex]['question'])
    session['incorrect']=x
    

    a=session['incorrecta'] #list of correct answers to ALL questions in current session(mislabeled)
    a.append(qlist[myIndex]['answer'])
    session['incorrecta']=a

    y=session['incorrect_entries']#list of answers which the user entered that were incorrect
    y.append(answer)
    session['incorrect_entries']=y


    print("Question answered:" + str(x))
    print("Correct answer:" + str(a))
    print("User answered:" + str(y))

           


    
 

    

    if myIndex==len(qlist)-1:
         
        new_test=TestInfo(session['userid'], session['score'], len(qlist), session['weeknum'])

        db.session.add(new_test)#adding the info of the test that was just taken to testinfo(date and score only as of now)
        db.session.flush()
        #db.session.commit()
        


        db.session.refresh(new_test) 
        attempt_id=new_test.id
        print('attempt id:' + str(attempt_id))
        q=session['incorrect']
        a=session['incorrecta']
        ue=session['incorrect_entries'] #retrieving all the users entries (not just entries to incorrectly answered questions, name is misleading) for the current session
        
        for i in range(len(q)):
            t=TestDetails(attempt_id,q[i],a[i],ue[i])
            db.session.add(t)

        db.session.commit()

            
        
        return render_template("score.html", score=session['score'], numqs=len(qlist), attempt_id=attempt_id )
        

         
    myIndex=myIndex+1
    session['current_index']= myIndex
    

    q=qlist[myIndex]['question']
    i=qlist[myIndex]['img']
    return render_template('home2.html', question=q, image=i)
    
@app.route('/start', methods=['POST']) 
def start():
    qlist:List[Question] = list()
    #defining list of type Question + making questions
    
    week_num = request.form['week']

    
    session['current_index']= 0
    session['score']=0

    session['incorrect'] =[]
    session['incorrecta'] = []
    session['incorrect_entries']=[]

    session['weeknum']=week_num
    

    qlist=Question.query.filter_by(weeknum=week_num).all() #retrieving the questions from the database which are from the selected week

    session['qlist']=qlist
 



    q=qlist[0].question
    return render_template("home2.html", question=q)

@app.route('/loginuser', methods=['POST'])
def login_user():

    usrnm = request.form['username']
    pwd = request.form['password']

    u=User.validate_user(usrnm,pwd)

    if u is not None:

        session['username']=u.username
        session['userid']=u.id

        print ("User " + session["username"] + " has logged in.")
        return redirect('/home')
        
    else:
        return render_template("login.html", error="LOGIN FAILED. Please try again with a different username or password.")

@app.route('/home', methods=['GET'])
def home():
    from_zone = tz.tzutc()
    to_zone = tz.tzlocal()



    usrnm=session['username']
    id=session['userid']
    if id:
        #make a list of past attempts so far here
        testlist:List[TestInfo] = list()
        testlist=TestInfo.query.filter(TestInfo.user_id==id).all() #Trying to fetch only tests whose user id matches the current user's id
        if testlist:
            for t in testlist:
                t.date_taken=t.date_taken.replace(tzinfo=from_zone)
                t.date_taken=t.date_taken.astimezone(to_zone)
    
            return render_template("home.html", user=usrnm, len=len(testlist), attempts=testlist)
        else:
            return render_template("home.html", user=usrnm, len=0, attempts=[])
    else:
        return render_template("login.html", error="LOGIN FAILED. Please try again with a different username or password.")
    

#adding new route(s?) for entering questions

@app.route('/qform', methods=['GET'])
def show_form():
    return render_template('create.html')

@app.route('/create' , methods=['POST'])
def add():
    
    wn=request.form['week']
    pq=request.form['propq']
    pa=request.form['propa']
    img=request.form['image']

    newq=Question(pq,pa,img,wn)#creates Question object with pq and pa as question and img and weeknum
    newq.set_creator(session['userid']) #setting creator to whoever is currently logged in 
    db.session.add(newq)
    db.session.commit()#appends newly made question to database
    flash('Question successfully created.')
    return redirect('/home')

    
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


#route to display incorrect answers
@app.route('/view', methods=['POST','GET'])
def display():


    '''q=session['incorrect']
    an=session['incorrecta']
    e=session['incorrect_entries']'''

    attempt_id = request.form['attempt_id']
    test_info=TestInfo.query.filter_by(id=attempt_id).all()
    test_details=TestDetails.query.filter_by(attempt_id=attempt_id).all()
    

    return render_template("view.html", len=len(test_details), testdetails=test_details)







    

@app.route('/logout', methods=['GET','POST'])
def logout():
    return render_template("login.html", error="")



    

 
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)