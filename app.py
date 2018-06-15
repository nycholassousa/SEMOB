from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:656993@localhost/flask_semob'
db = SQLAlchemy(app)


class Vehicle(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    brand = db.Column(db.String(50), nullable=False)
    model = db.Column(db.String(50), nullable=False)
    plate = db.Column(db.String(50), unique=True, nullable=False)
    date = db.Column(db.DateTime(), nullable=False)
    reason = db.Column(db.String(50), nullable=False)
    situation = db.Column(db.Boolean, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True)

    def __init__(self, brand, model, plate, reason):
        self.brand = brand
        self.model = model
        self.plate = plate
        self.date = datetime.datetime.utcnow()
        self.reason = reason
        self.situation = True


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(30), nullable=False)
    admin = db.Column(db.Boolean, nullable=False)
    vehicles = db.relationship('Vehicle', backref='user', lazy=True, nullable=True)

    def __init__(self, name, email, password):
        self.name = name
        self.email = email
        self.password = password


# Home Page
@app.route('/')
def index():
    return render_template('index.html')

# Create Vehicle Page
@app.route('/add_vehicle')
def add_vehicle():
    return render_template('add_vehicle.html')

# Create User Page
@app.route('/create_user')
def create_user():
    return render_template('create_user.html')

# POST User Method
@app.route('/api/post/user', methods=['POST'])
def post_user():
    user = User(request.form['name'], request.form['email'], request.form['password'])
    db.session.add(user)
    db.session.commit()
    return redirect(url_for('index'))

# POST Vehicle Method
@app.route('/api/post/vehicle', methods=['POST'])
def post_vehicle():
    vehicle = Vehicle(request.form['brand'], request.form['model'], request.form['plate'], request.form['reason'])
    db.session.add(vehicle)
    db.session.commit()
    return redirect(url_for('index'))


# GET Vehicle Info Method
@app.route('/api/get/vehicle/<plate>', methods=['GET'])
def get_vehicle(plate):
    vehicle = Vehicle.query.filter_by(plate=plate).first()
    return render_template('vehicle_info.html', vehicle=vehicle)


if __name__ == '__main__':
    app.debug = True
    app.run()
