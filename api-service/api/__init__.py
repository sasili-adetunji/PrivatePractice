import os
import datetime
from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Api, Resource, reqparse
from flask_jwt import JWT, jwt_required
from .security import authenticate, identity

# instantiate the app
app = Flask(__name__)

app.secret_key = 'Sasiliyu'
# instantiate the db
db = SQLAlchemy(app)

api = Api(app)
# set config
app_settings = os.getenv('APP_SETTINGS')
app.config.from_object(app_settings)

jwt = JWT(app, authenticate, identity)
patients = []


class Patient(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('address',
        required=True,
        help="This is a required field"
    )
    @jwt_required()
    def get(self, name):
        patient = next(filter(lambda x: x['name'] == name, patients), None)
        return { 'patient ': patient }, 200 if patient else 404

    def post(self, name):
        if next(filter(lambda x: x['name'] == name, patients), None):
            return { 'message': "An patient with name '{}' already exist".format(name)}, 400

        data = Patient.parser.parse_args()
        patient = { 'name': name, 'address': data['address'] }
        patients.append(patient)
        return patient, 201

    def delete(self, name):
        global patients
        patients = list(filter(lambda x: x['name'] != name, patients ))
        return { "message": "The patients '{}' was successfully deleted" .format(name)}, 200

    def put(self, name):
        data = Patient.parser.parse_args()

        patient  = next(filter(lambda x: x['name'] == name, patients), None)
        if patient is None:
            patient = { 'name': name, 'address': data['address']}
            patients.append(patient)
        else:
            patient.update(data)
        return patient

class PatientList(Resource):
    def get(self):
        return { 'patient': patients}

api.add_resource(Patient, '/api/patient/<string:name>')
api.add_resource(PatientList, '/api/patients')

# model
# class User(db.Model):
#     __tablename__ = "users"
#     id = db.Column(db.Integer, primary_key=True, autoincrement=True)
#     username = db.Column(db.String(128), nullable=False)
#     email = db.Column(db.String(128), nullable=False)
#     active = db.Column(db.Boolean(), default=True, nullable=False)

#     def __init__(self, username, email):
#         self.username = username
#         self.email = email