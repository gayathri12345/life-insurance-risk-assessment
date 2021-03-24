from io import TextIOWrapper
from .risk import Risk 
from flask import render_template, request,url_for,redirect,flash
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from .forms import LoginForm, RegisterForm, UploadForm
from .models import User
from App import app,db


#config
login_manager=LoginManager()
login_manager.init_app(app)
login_manager.login_view='login'



@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


@app.route('/')
def root():
    return redirect(url_for('home'))


@app.route('/home')
def home():
    return render_template('home.html')


@app.route('/login',methods=['GET','POST'])
def login():
    form=LoginForm()
    if form.validate_on_submit():
        user=User.query.filter_by(username=form.username.data).first()
        if user:
            if check_password_hash(user.password,form.password.data):
                login_user(user,remember=True)
                return redirect(url_for('predict'))
        
        return render_template('login.html',form=form,error=1)
        #return "<h1>" + 'Logged in successfully' + "</h1>"
    return render_template('login.html',form=form,error=0)


@app.route('/register',methods=['GET','POST'])
def register():
    form=RegisterForm()
    if form.validate_on_submit():
        hashed_password=generate_password_hash(form.password.data,method='sha256')
        new_user=User(username=form.username.data,email=form.email.data,password=hashed_password)
        db.session.add(new_user)
        db.session.commit()

        #need to change
        return '<h1>' + "Registered Successfully" + '</h1>'
    return render_template('register.html',form=form)


@app.route('/predict', methods=['GET', 'POST'])
@login_required
def predict():
    form=UploadForm()
    if form.validate_on_submit():
        csv_file = form.file.data
        csv_file = TextIOWrapper(csv_file, encoding='utf-8')
        r=Risk(csv_file)
        Id,preprocessed_data=r.load_and_preprocess()
        result=r.get_prediction(preprocessed_data)
        r.save(Id,result)
        #return "Done!"   
        return render_template('dashboard.html',form=form,user=current_user.username)

    return  render_template('dashboard.html',form=form,user=current_user.username)



@app.route('/forget_password',methods=['GET','POST'])
def forget_password():
    form=LoginForm()
    if form.validate_on_submit():
        user=User.query.filter_by(username=form.username.data).first()
        if user:
            #update password in database
            hashed_password=generate_password_hash(form.password.data, method='sha256')
            user.password=hashed_password
            db.session.commit()
            #flash("Password has been updated!")
            #return redirect(url_for('login'))

        return render_template('forget_password.html',form=form, error=1)

    return render_template('forget_password.html',form=form,error=0)

import pandas as pd
@app.route('/charts')
def charts():
    data=pd.read_csv('App/static/output/risk.csv')
    a={'Response' : 'Value'}
    a.update(data['Response'].value_counts().to_dict())
    return render_template('charts.html',data=a)
   

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('home'))