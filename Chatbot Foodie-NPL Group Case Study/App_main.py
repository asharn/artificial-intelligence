from flask import session,flash
import pandas as pd
import numpy as np 
from flask import Response
import os 
from flask import Flask, render_template, request, redirect, url_for, send_from_directory,jsonify
import tempfile
import simplejson as j
from rasa_nlu.training_data import load_data
from rasa_nlu.config import RasaNLUModelConfig
from rasa_nlu.model import Trainer
from rasa_nlu.model import Metadata, Interpreter
import json
# Import smtplib for the actual sending function
import smtplib
# Import the email modules we'll need
from flask_mail import Mail, Message
app = Flask(__name__)
app.config.update(
	DEBUG=True,
	#EMAIL SETTINGS
	MAIL_SERVER='smtp.gmail.com',
	MAIL_PORT=465,
	MAIL_USE_SSL=True,
	MAIL_USERNAME = 'dvlpmailsender@gmail.com',
	MAIL_PASSWORD = 'real_password'
	)
mail = Mail(app)   

@app.route('/')
def index():
    return 'Application is working fine.'
    
interpreter = Interpreter.load('./models/nlu/default/restaurantnlu')
@app.route('/nlu_parsing', methods=['POST'])
def transform():
    if request.headers['Content-Type'] == 'application/json':     
        query = request.json.get("utterance")
        results=interpreter.parse(query)
        js = json.dumps(results)
        resp = Response(js, status=200, mimetype='application/json')
        return resp

@app.route('/send-mail', methods=['POST'])
def sendMail():
        if request.headers['Content-Type'] == 'application/json':
                try:
                        recipientEmail = request.json.get("email")
                        restaurants = request.json.get("top-10-restaurants")
                        msg = Message("Top 10 Restaurants !!!",
                                sender="dvlpmailsender@gmail.com",
                                recipients=[recipientEmail])
                        msg.body = restaurants
                        mail.send(msg)
                        return 'Mail sent successfully'
                except Exception as e:
                        return str(e)

if __name__ == '__main__':
    app.run(debug=True)
