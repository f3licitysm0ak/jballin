from typing import List
from flask import Flask, request, render_template
from qobject import Question
from userclass import User

app = Flask(__name__)

#defining list of type Question + making questions

q1=Question("What is the capital of Japan", "tokyo")
q2=Question("What is the capital of Miyagi", "sendai")
q3=Question("Which prefecture is Ghibli Park located in? Answer in Hiragana.", "あいち")
q4=Question("Where did kawara soba originate from? Answer in Hiragana.", "かがわ")
q5=Question("Which prefecture is Yuzuru Hanyu from?", "miyagi")
qlist:List[Question] = list()
qlist.append(q1)
qlist.append(q2)
qlist.append(q3)
qlist.append(q4)
qlist.append(q5)

i=0 #to keep track of current question
score=0#score of questions correct

#made variables to store username and password for making user object later
usrnm=""
pwd=""


#checking method for all questions
def check(text1):
   global i
   global score
   if text1.lower()==qlist[i].answer:
       score+=1
 

@app.route('/')
def home():
    q=qlist[i].question
    return render_template('login.html', question=q)


@app.route('/next', methods=['GET','POST'])
def my_form_post():
    global i
    global score


    answer = request.form['text1']
    check(answer)
    

    if i==4:
        print ("score print")
        i=0
        return ("<html>Your score is " + str(score) + "/5. Thanks for playing!</html>")
    else:
        i = i + 1
        print("next question, i = " + str(i))
        q=qlist[i].question
        print("calling render_template")
        return render_template('home2.html', question=q)

@app.route('/start', methods=['POST'])
def start():
    q=qlist[i].question

    #declared both username and password as global to avoid that error thing lol
    global usrnm
    global pwd

    usrnm = request.form['username']
    pwd = request.form['password']

    if User.validate_user(usrnm,pwd)==True:
        return render_template("home2.html", question=q)
    else:
        return render_template("login.html", error="LOGIN FAILED. Please try again with a different username or password.")
    

@app.route('/logout', methods=['POST'])
def logout():
    return render_template("login.html", error="")



    

 
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)