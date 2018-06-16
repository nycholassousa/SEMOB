from flask import Flask, render_template, redirect, url_for
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm 
from wtforms import StringField, PasswordField, BooleanField, SelectField
from wtforms.validators import InputRequired, Email, Length
from flask_sqlalchemy  import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user

import datetime

app = Flask(__name__)
app.config['SECRET_KEY'] = '123!'
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:656993@localhost/flask'
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
    admin = db.Column(db.Boolean)

class Vehicle(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    brand = db.Column(db.String(30))
    model = db.Column(db.String(30))
    plate = db.Column(db.String(7))
    date = db.Column(db.DateTime())
    reason = db.Column(db.String(80))
    situation = db.Column(db.Boolean)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class LoginForm(FlaskForm):
    email = StringField('email', validators=[InputRequired(), Length(min=4, max=50)])
    password = PasswordField('password', validators=[InputRequired(), Length(min=8, max=80)])
    remember = BooleanField('remember me')

class RegisterForm(FlaskForm):
    email = StringField('email', validators=[InputRequired(), Email(message='Invalid email'), Length(max=50)])
    name = StringField('name', validators=[InputRequired(), Length(min=4, max=15)])
    password = PasswordField('password', validators=[InputRequired(), Length(min=8, max=80)])

class RegisterVehicle(FlaskForm):
    brand = SelectField(
        'brand',
        choices=[('1', '1'), ('2', '2'), ('3', '3')]
    )
    model = SelectField(
        'model',
        choices=[('1', '1'), ('2', '2'), ('3', '3')]
    )
    plate = StringField('plate', validators=[InputRequired(), Length(max=7)])
    reason = StringField('reason', validators=[InputRequired(), Length(max=80)])

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()

    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user:
            if check_password_hash(user.password, form.password.data):
                login_user(user, remember=form.remember.data)
                return redirect(url_for('dashboard'))

        return '<h1>Invalid email or password</h1>'

    return render_template('login.html', form=form)

@app.route('/registerVehicle', methods=['GET', 'POST'])
def registerVehicle():
    form = RegisterVehicle()
    # form.brand.choices = [(row.ID, row.Name) for row in brand.query.all()]
    # form.model.choices = [(row.ID, row.Name) for row in model.query.all()]

    if form.validate_on_submit():
        new_vehicle = Vehicle(brand=form.brand.data, model=form.model.data, plate=form.plate.data, date=datetime.datetime.utcnow(), reason=form.reason.data, situation=True)
        db.session.add(new_vehicle)
        db.session.commit()
        return 'Vehicle Added'

    return render_template('registerVehicle.html', form=form)

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    form = RegisterForm()

    if form.validate_on_submit():
        hashed_password = generate_password_hash(form.password.data, method='sha256')
        new_user = User(name=form.name.data, email=form.email.data, password=hashed_password, admin=False)
        db.session.add(new_user)
        db.session.commit()

        return '<h1>New user has been created!</h1>'

    return render_template('signup.html', form=form)

@app.route('/dashboard')
@login_required
def dashboard():
    return render_template('dashboard.html', name=current_user.name)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
