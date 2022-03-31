import datetime,re,flask_excel,os
from flask.helpers import send_file
from flask import Flask,render_template,url_for,request,redirect,flash
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager, UserMixin, login_user, current_user, logout_user, login_required
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from waitress import serve

delta = datetime.timedelta(hours=5,minutes=30)

userFormat=".{5,10}"
emailFormat=".{,}@.{,}"
phoneFormat="[0-9]{10}"
passwordFormat=".{5,20}"

qriousStart=datetime.datetime(2022,3,1,0,1,0)-delta
qriousEnd=datetime.datetime(2022,4,3,23,59,0)-delta

anticodingStart=datetime.datetime(2022,3,1,0,1,0)-delta
anticodingEnd=datetime.datetime(2022,4,3,23,59,0)-delta

datageddonStart=datetime.datetime(2022,3,21,15,0,0)-delta
datageddonEnd=datetime.datetime(2022,4,21,17,0,0)-delta

from questions import *

app=Flask(__name__,static_url_path='/static')
app.config['SECRET_KEY'] = 'you-cant-guess'
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://'+(os.environ.get('DATABASE_URL') or 'postgres://qjscrmnbgmznfi:91d33d6885f353f69643dda8745a2d5a058598890f249cb47d8553dacfe49a69@ec2-54-205-183-19.compute-1.amazonaws.com:5432/dos75t9cbjsi7')[11:]
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['RATELIMIT_APPLICATION'] = "4/second;12/minute"
app.config['UPLOAD_FOLDER'] = 'static/uploads' 
db=SQLAlchemy(app)
bcrypt=Bcrypt(app)
flask_excel.init_excel(app)
login_manager=LoginManager(app)
limiter = Limiter(app,key_func=get_remote_address)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@login_manager.unauthorized_handler
def unauthorized_callback():
    flash("You have not logged in","fail")
    return redirect(url_for('home'))

class User(db.Model,UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(10), unique=True, nullable=False)
    email = db.Column(db.String(50), unique=True, nullable=False)
    phone = db.Column(db.String(10), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)
    stage = db.Column(db.Integer, default=0)
    recentTime = db.Column(db.DateTime, nullable=False, default=datetime.datetime.now)

    def __repr__(self):
        return f"User({self.username} , {self.email} , {self.stage+1} , {self.recentTime})"

    def toList(self):
        return [self.id,self.username,self.email,self.phone,self.stage+1,self.recentTime]

class Files(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String(20), unique=True, nullable=False)
    file = db.Column(db.LargeBinary)
    uploadTime = db.Column(db.DateTime, nullable=False, default=datetime.datetime.now)

@app.errorhandler(429)
def toomanyreq(e):
    if current_user.is_authenticated:
        print(current_user.username+" "+current_user.phone+" "+current_user.email)
    return "<h3>Too many requests!</h3><h1>Chill...</h1><h4>Try again in sometime</h4>", 429

@app.route('/')
def home():
    if current_user.is_authenticated:
        flash("Already Logged In",'success')
        return redirect(url_for('events'))
    return render_template('home.html',userFormat=userFormat,emailFormat=emailFormat,phoneFormat=phoneFormat,passwordFormat=passwordFormat)


@app.route('/register',methods=['POST','GET'])
def register():
    if current_user.is_authenticated:#check if logged in
        flash("Already Logged In",'success')
        return redirect(url_for('events'))

    if request.method == 'POST':#if form submitted
        if not request.form.get('username') or not request.form.get('email') or not request.form.get('password') or not request.form.get('phone'):#if all details not entered
            flash("You Must Enter All Details","fail")
            return redirect(url_for('home'))

        if not re.match(userFormat,request.form.get('username')):#check format
            flash("Username must be 5 to 10 characters long","fail")
            return redirect(url_for('home'))
        if not re.match(passwordFormat,request.form.get('password')):
            flash("Password must be 5 to 20 characters long","fail")
            return redirect(url_for('home'))
        if not re.match(emailFormat,request.form.get('email')):
            flash("Email must be in correct format","fail")
            return redirect(url_for('home'))
        if not re.match(phoneFormat,request.form.get('phone')):
            flash("Enter 10 digit Phone Number","fail")
            return redirect(url_for('home'))

        if User.query.filter_by(username=request.form.get('username')).first():#if user exists
            flash("Username exists, use another or Login",'fail')
            return redirect(url_for('home'))
        elif User.query.filter_by(email=request.form.get('email')).first():
            flash("Email exists, use another or Login",'fail')
            return redirect(url_for('home'))
        elif User.query.filter_by(phone=request.form.get('phone')).first():
            flash("Phone number exists, use another or Login",'fail')
            return redirect(url_for('home'))
        else:#create new user
            hashed_password = bcrypt.generate_password_hash(request.form.get('password')).decode('utf-8')
            user = User(username=request.form.get('username'),email=request.form.get('email'),
                        phone=request.form.get('phone'),password=hashed_password)
            db.session.add(user)
            db.session.commit()
            flash("Account Created Successfully!",'success')
            login_user(user)
            return redirect(url_for('events'))
    flash("Enter Details First","fail")
    return redirect(url_for('home'))


@app.route('/login',methods=['POST','GET'])
def login():
    if current_user.is_authenticated:#if logged in
        flash("Already Logged In",'success')
        return redirect(url_for('events'))

    if request.method == 'POST':#if form submitted
        if not request.form.get('username') or not request.form.get('password'):#if all details not entered
            flash("You Must Enter All Details","fail")
            return redirect(url_for('home'))

        if not re.match(userFormat,request.form.get('username')):#check format
            flash("Username must be 5 to 10 characters long","fail")
            return redirect(url_for('home'))
        if not re.match(passwordFormat,request.form.get('password')):
            flash("Password must be 5 to 20 characters long","fail")
            return redirect(url_for('home'))

        user = User.query.filter_by(username=request.form.get('username')).first()
        if user and bcrypt.check_password_hash(user.password, request.form.get('password')):#if user exists
            login_user(user)
            flash("Logged In Successfully",'success')
            return redirect(url_for('events'))
        else:#if user does not exist
            flash("Username/Password does not match, try again or Register",'fail')
            return redirect(url_for('home'))

    flash("Enter Details First","fail")
    return redirect(url_for('home'))


@app.route('/events',methods=['POST','GET'])
@login_required
def events():
    return render_template('events.html',name=current_user.username)

@app.route('/questions',methods=['POST','GET'])
@login_required
def questions():
    questions = {**stage1 , **stage2 , **stage3 , **stage4 , **stage5 , **stage6 , **stage7 , **stage8 , **stage9}
    return render_template('questionPage.html',questions=enumerate(questions.items()),
                            stage=current_user.stage,name=current_user.username,leaderboard=getLeaderboard(),
                            length=len(questions))

@app.route('/qrious',methods=['POST','GET'])
@login_required
def qrious():
    if datetime.datetime.now() < qriousStart:
        flash("Event Not Started Yet",'fail')
        return redirect(url_for('events'))
    elif datetime.datetime.now() > qriousEnd:
        flash("Event Has Ended",'fail')
        return redirect(url_for('events'))
    if current_user.stage >= len(questionSet):
        return redirect(url_for('finished'))
    questions = questionSet[current_user.stage]
    answers = answerSet[current_user.stage]
    if request.method == 'POST':
        for index in range(len(questions)):
            if not request.form.get(f"question-{index+1}"):
                flash("You must attempt all questions",'fail')
                return redirect(url_for('qrious'))
            elif request.form.get(f"question-{index+1}") != answers[index]:
                flash("One(or more) of the answers is wrong",'fail')
                return redirect(url_for('qrious'))
        current_user.stage = current_user.stage+1
        current_user.recentTime = datetime.datetime.now()
        if current_user.stage < len(questionSet)-1:
            flash(f"Stage {current_user.stage} cleared!",'success')
        db.session.commit()
        return redirect(url_for('qrious'))
    return render_template('questionPage.html',questions=enumerate(questions.items()),
                            stage=current_user.stage,name=current_user.username,leaderboard=getLeaderboard(),
                            length=len(questions))


@app.route('/robots.txt',methods=['GET'])
@login_required
def robot():
    return send_file('static/robots.txt')

@app.route('/n1c3.html',methods=['GET'])
@login_required
def n1c3():
    return 'FLAG{THE-BOTS-ARE-HERE}</h1></body></html>'

@app.route('/api',methods=['GET'])
def api():
    if not (request.args.get('query') and request.args.get('stage') and request.args.get('questionNum')):
        return '<h4>BAD REQUEST</h4><p>EXPECTING ARGUMENTS query, stage, questionNum</p>'
    elif request.args.get('query')=='flag' and request.args.get('stage')==apistage:
        if request.args.get('questionNum')=='1':
            return 'FLAG{MY-FIRST-QUERY}'
        elif request.args.get('questionNum')=='2':
            if request.headers.get('User-Agent') == 'CSABrowser':
                return 'FLAG{SECRET-AGENT-QUERY}'
            else:
                return '<h4>Detected browser: '+request.headers.get('User-Agent')+'</h4><p>Try again using CSABrowser</p>'

    return '<h4>Wrong Query Values</h4><p>Try Something Else</p>'

@app.route('/anticoding',methods=['POST','GET'])
@login_required
def anticoding():
    if datetime.datetime.now() < anticodingStart:
        flash("Event Not Started Yet",'fail')
        return redirect(url_for('events'))
    elif datetime.datetime.now() > anticodingEnd:
        flash("Event Has Ended",'fail')
        return redirect(url_for('events'))
    if request.method == 'POST':
        for i in range(1,4):
            f=request.files[f"question-{i}"]
            if f and f.filename[-2:]=='.c':
                f.save(f"static/submissions/anticoding/{current_user.username}_{i}.c")

        flash("Submitted!",'success')
                
    return render_template('anticoding.html',name=current_user.username)

@app.route('/datageddon',methods=['GET'])
@login_required
def datageddon():
    if datetime.datetime.now() < datageddonStart:
        flash("Event Not Started Yet",'fail')
        return redirect(url_for('events'))
    elif datetime.datetime.now() > datageddonEnd:
        flash("Event Has Ended",'fail')
        return redirect(url_for('events'))
    if request.method == 'POST':
        f=request.files["question"]
        if f and f.filename[-4:]=='.csv':
            f.save(f"static/submissions/datageddon/{current_user.username}.csv")
            flash("Submitted!",'success')
        else:
            flash("Upload CSV File",'fail')
                
    return render_template('datageddon.html',name=current_user.username)
        

@app.route('/export',methods=['GET'])
@login_required
def export():
    if current_user.username == 'admin':
        return flask_excel.make_response_from_array([['No','Username','Email','Phone','Stage','Time']]+[x.toList() for x in User.query.all()],file_type="csv",file_name="userlist")
    else:
        flash("Not Allowed",'fail')
        return redirect(url_for('home'))

@app.route('/congrats')
@login_required
def finished():
    if current_user.stage < len(questionSet):
        flash("You have not completed the test",'fail')
        return redirect(url_for('qrious'))
    return render_template("congrats.html",leaderboard=getLeaderboard(),name=current_user.username)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash("Logged Out Successfully",'success')
    return redirect(url_for('home'))

@app.route('/reset/<stage>')
@login_required
def reset(stage):
    if current_user.username == 'admin':
        current_user.stage = int(stage)-1
        current_user.recentTime = datetime.datetime.now()
        db.session.commit()
    else:
        flash("Not Allowed",'fail')
    return redirect(url_for('qrious'))

def getLeaderboard():
    users = User.query.order_by(User.stage.desc(),User.recentTime).limit(10)
    leaderboard = []
    for i,user in enumerate(users):
        stage = f"Stage {user.stage}"
        if user.stage >= len(questionSet):
            #stage = "Finished"
            pass
        elif user.stage == 0:
            stage = "Started"
        time=str((datetime.datetime.now()-user.recentTime).days)
        time+=" day ago" if time[0]=='1' else " days ago"
        if time[0]=='0':
            time = str(int((datetime.datetime.now()-user.recentTime).seconds/3600))+" hours ago"
        if time[0]=='0':
            time = str(int((datetime.datetime.now()-user.recentTime).seconds/60))+" minutes ago"
        if time[0]=='0':
            time = str(int((datetime.datetime.now()-user.recentTime).seconds))+" seconds ago"
        leaderboard.append('<td>{}</td><td>: {} ,</td><td>{}</td>'.format(user.username,stage,time))
    return leaderboard

if __name__ == '__main__':
    #app.run(debug=False,host='0.0.0.0',port=int(os.environ.get('PORT', 5000)))    #local network with debug
    app.run(debug=True)                    #locl machine with debug
    #serve(app,host='0.0.0.0',port=5000)     #for hosting