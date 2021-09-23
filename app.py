from flask import Flask, jsonify, request, current_app, send_file, render_template, Response
from os import path
import secret as sct
import config as cnf
from lib.account import objAccount
from lib.owner import objOwner
from lib.transaction import objTransaction
from sqlalchemy import create_engine  
from sqlalchemy.orm import sessionmaker

# Initiate the database tables if they don't exist by running the models file
basepath = path.dirname(__file__)
filepath = path.abspath(path.join(basepath, "lib", "models.py"))
exec(open(filepath).read())

# Initialize a database session
db_uri = 'postgresql+psycopg2://'+sct.username+':'+sct.password+'@'+cnf.db_server+'/'+cnf.db_name
db = create_engine(db_uri)
Session = sessionmaker()
Session.configure(bind=db)

session = Session()

# Initialize objects
a = objAccount(session)
o = objOwner(session)
t = objTransaction(session)
app = Flask(__name__, static_folder="static")

# App routes

@app.route("/owners/get", methods=['POST', 'GET'])
def get_owners():
    response = o.get_owners()
   
    return jsonify(response)

@app.route("/accounts/get", methods=['POST'])
def get_accounts():
    request_data = request.get_json()
    name = request_data['name']
    response = o.get_accounts(name)
   
    return jsonify(response)

if __name__ == "__main__":

    app.run(port=5002, debug=True)


