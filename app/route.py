from flask import Flask, render_template, request, jsonify, send_from_directory
from flask_mqtt import Mqtt
from app import mqtt_client, app
import threading
import os
import json


topic = '/overlay/toggle'

# Define the on_connect callback
@mqtt_client.on_connect()
def handle_connect(client, userdata, flags, rc):
    if rc == 0:
        print('Connected successfully')
        mqtt_client.subscribe(topic)
    else:
        print('Bad connection. Code:', rc)

# Define the on_message callback
@mqtt_client.on_message()
def handle_message(client, userdata, msg):
    print(f"Message received: {msg.topic} {msg.payload.decode()}")


@app.route('/')
def index():
    return render_template("index.html")

@app.route('/toggle_overlay', methods=['POST'])
def toggle_overlay():
    data = request.json
    current_state = data.get('state')
    if current_state == 'on':
        result = mqtt_client.publish('/overlay/toggle', 'turn_on')
        print("Publish result:", result)
    else:
        mqtt_client.publish('/overlay/toggle', "turn_off")  # Send message to turn on
        
    return jsonify({"status": "toggled", "new_state": "on" if current_state == 'on' else "off"})


@app.route('/static/<path:path>')
def send_static(path):
    return send_from_directory('static', path)


# Create a directory to store the uploaded images
#uploadFolder = 'images'
#UPLOAD_FOLDER = os.path.join(app.static_folder, uploadFolder)
#print(UPLOAD_FOLDER)
#app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
