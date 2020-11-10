from flask import Flask, render_template, request, redirect,jsonify
from flask_restful import Resource, Api
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
import os

app = Flask(__name__)
api = Api(app)

basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] =os.environ.get('DATABASE_URL') or 'sqlite:///' + os.path.join(basedir, 'mydatabase.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

ma=Marshmallow(app)

class Users(db.Model):
    id = db.Column(db.Integer, 
                          primary_key=True)
    first_name = db.Column(db.String)
    last_name = db.Column(db.String)

    def __init__(self,first_name,last_name):
        self.first_name=first_name
        self.last_name=last_name


class userSchema(ma.Schema):
  class Meta:
    fields = ('id', 'first_name', 'last_name')

# Init schema
user_schema = userSchema()
users_schema = userSchema(many=True)

# Create a user
@app.route('/new', methods=['POST'])
def add_user():
  name = request.json['first_name']
  lastname = request.json['last_name']


  new_user =Users(name,lastname )

  db.session.add(new_user)
  db.session.commit()

  return user_schema.jsonify(new_user)

# Get All users
@app.route('/user', methods=['GET'])
def get_users():
  all_users = Users.query.all()
  result = users_schema.dump(all_users)
  return jsonify(result)

# Get Single user
@app.route('/user/<id>', methods=['GET'])
def get_user(id):
  user = Users.query.get(id)
  return user_schema.jsonify(user)

# Update the user
@app.route('/user/<id>', methods=['PUT'])
def update_user(id):
  user = Users.query.get(id)

  name = request.json['first_name']
  lastname = request.json['last_name']


  user.last_name = name
  user.first_name = lastname


  db.session.commit()

  return user.jsonify(user)

# Delete User
@app.route('/user/<id>', methods=['DELETE'])
def delete_user(id):
  user = User.query.get(id)
  db.session.delete(user)
  db.session.commit()

  return user_schema.jsonify(user)

# Run Server
if __name__ == '__main__':
  app.run(debug=True)
