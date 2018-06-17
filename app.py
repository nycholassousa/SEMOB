from flask import Flask, render_template, redirect, url_for, request
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm 
from wtforms import StringField, PasswordField, BooleanField, SelectField, SubmitField
from wtforms.validators import InputRequired, Email, Length
from flask_sqlalchemy  import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user

import datetime
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = '123!'
# app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:656993@localhost/flask'
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://xfknaorlqkasws:b13173df128716a8e79e9b54fb2aa782a3f01703819eee70416b515e368ac562@ec2-54-243-235-153.compute-1.amazonaws.com:5432/dbmdf4dpinbe69'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
bootstrap = Bootstrap(app)
db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    email = db.Column(db.String(50), unique=True)
    password = db.Column(db.String(80))
    admin = db.Column(db.Integer)

class Vehicle(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    brand = db.Column(db.String(30))
    model = db.Column(db.String(30))
    plate = db.Column(db.String(7))
    date = db.Column(db.DateTime())
    reason = db.Column(db.String(80))
    situation = db.Column(db.Integer)

    def changeSituation(self, situation):
        self.situation = situation

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class LoginForm(FlaskForm):
    email = StringField('email', validators=[InputRequired(), Length(min=4, max=50)])
    password = PasswordField('password', validators=[InputRequired(), Length(min=8, max=80)])
    remember = BooleanField('remember me')

class RegisterForm(FlaskForm):
    email = StringField('email', validators=[InputRequired(), Email(message='Invalid email'), Length(max=50)])
    name = StringField('name', validators=[InputRequired(), Length(min=4, max=50)])
    password = PasswordField('password', validators=[InputRequired(), Length(min=8, max=80)])

class RegisterVehicle(FlaskForm):
    brand = SelectField(
        'brand',
        choices=[('fiat', 'Fiat'), ('chevrolet', 'Chevrolet'), ('volkswagen', 'Volkswagen'), ('ford', 'Ford')]
    )
    model = SelectField(
        'model',
        choices=[('uno', 'Uno'), ('onix', 'Onix'), ('gol', 'Gol'), ('ka', 'Ka')]
    )
    plate = StringField('plate', validators=[InputRequired(), Length(min=7, max=7)])
    reason = StringField('reason', validators=[InputRequired(), Length(max=80)])

class SearchForm(FlaskForm):
    search_input = StringField('', validators=[InputRequired(), Length(min=7, max=7)])
    submit = SubmitField('Search')

@app.route('/', methods=['POST','GET'])
def index():
    form = SearchForm()

    if form.search_input.data:
        return redirect('/'+form.search_input.data)
    
    return render_template('index.html', form=form)

@app.route('/<plate>')
def show_plate(plate):
    info = Vehicle.query.filter_by(plate=plate).first()
    return render_template('result.html', title = plate, info = info)

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    message = ''

    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user:
            if check_password_hash(user.password, form.password.data):
                login_user(user, remember=form.remember.data)
                return redirect(url_for('dashboard'))

        message = 'Dados invalidos'
        return render_template('login.html', form=form, message=message)

    return render_template('login.html', form=form, message=message)

@app.route('/registerVehicle', methods=['GET', 'POST'])
@login_required
def registerVehicle():
    form = RegisterVehicle()
    message = ''

    if form.validate_on_submit():
        new_vehicle = Vehicle(brand=form.brand.data, model=form.model.data, plate=form.plate.data, date=datetime.datetime.utcnow(), reason=form.reason.data, situation=1)
        db.session.add(new_vehicle)
        db.session.commit()
        return redirect(url_for('dashboard'))

    return render_template('registerVehicle.html', form = form)

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    form = RegisterForm()

    if form.validate_on_submit():
        hashed_password = generate_password_hash(form.password.data, method='sha256')
        new_user = User(name=form.name.data, email=form.email.data, password=hashed_password, admin=1)
        db.session.add(new_user)
        db.session.commit()

        return redirect(url_for('login'))

    return render_template('signup.html', form=form)

@app.route('/flip', methods=['POST'])
def flip():
    vehicle = Vehicle.query.filter_by(id=request.form["flip"]).first_or_404()
    vehicle.situation = 0
    db.session.commit()
    return redirect(url_for('dashboard'))

@app.route('/dashboard')
@login_required
def dashboard():
    vehicles = Vehicle.query.all()
    return render_template('dashboard.html', user=current_user, vehicles=vehicles)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
