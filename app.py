from flask import Flask,render_template,redirect,request,session,url_for,jsonify
import random 
import requests
from flask_sqlalchemy import SQLAlchemy
import os 

URL = "https://qboxlink.000webhostapp.com/confirm.php"


app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('GG')
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL')
db = SQLAlchemy(app)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer,primary_key = True)
    ename = db.Column(db.String(200),unique = True)
    hostel = db.Column(db.String(200),unique = False)

db.create_all()


@app.route('/',methods = ['POST','GET'])
def otp_check():
    if not session:
        if request.method == "POST":
            opt = request.form['OTP']
            print(opt)
            print(session['temp_otp'])
            if int(opt) == int(session['temp_otp']):
                session['s'] = 1
                return redirect('/find')
            else:
                session.pop('tname',None)
                session.pop('s',None)
                session.pop('temp_otp',None)
                return render_template('index.html',err = "Wrong OTP!")
        else:
            return render_template('index.html',err="")
    else:
        return redirect('/find')

@app.route('/sendotp',methods = ['POST','GET'])
def sendotp():
    data ={ "data":"###"}
    mail = request.args['tname']
    d = mail.split("@")
    print(d)
    if d[1] == "srmist.edu.in" or d[0] == "sahiljena46":
        otp = random.randint(1000,9999)
        print(otp)
        data = { "data":"Sent"}
        # defining a params dict for the parameters to be sent to the API 
        PARAMS = {
            'to': mail,
            'hash' : otp
                } 
        # sending get request and saving the response as response object 
        r = requests.get(url = URL, params = PARAMS) 
        session['temp_otp'] = otp
        session['s'] = 0
        session['tname'] = mail
        return jsonify(data)
    else:
        data = {"data":"Please use mail id with the domain 'srmits.edu.in' only"}
        return jsonify(data)

@app.route('/find',methods = ['POST','GET'])
def find():
    if session:
        user = User.query.filter_by(ename = session['tname']).first()
        myhostel = ""
        fellow = []
        if user is not None:
            myhostel = user.hostel
            fellow_q = User.query.filter_by(hostel = myhostel).all()
            for i in range(0,len(fellow_q)):
                e = fellow_q[i].ename
                h = fellow_q[i].hostel
                r=[e,h]
                fellow.append(r)
            if len(fellow) == 1:
                fellow = []
            print(fellow)
            return render_template('sus.html',fellow = fellow ,tname = session['tname'],myhostel = myhostel)
        if request.method == "POST":
            user = User.query.filter_by(ename = session['tname']).first()
            if user is None:
                ename = session['tname']
                hostel_name = request.form['hname']
                hostel_num = request.form['hnum']
                hostel = hostel_name +" "+str(hostel_num)

                user=User(ename = ename, hostel = hostel)
                db.session.add(user)
                db.session.commit()
                return redirect('/find')
        return render_template('sus.html', tname = session['tname'],myhostel= myhostel)
    else:
        return redirect('/')

