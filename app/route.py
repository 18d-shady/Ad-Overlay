from flask import Flask, render_template, request, jsonify, send_from_directory
import paho.mqtt.client as mqtt
import threading
import ssl
from app import app
import os
import json


topic = '/overlay/toggle'


def on_connect(client, userdata, flags, rc):
    print("Connected with result code", rc)
    client.subscribe("/overlay/toggle")

def on_message(client, userdata, msg):
    print(f"Message received: {msg.topic} {msg.payload.decode()}")

context = ssl.create_default_context()
context.load_verify_locations('app/certs/broker.emqx.io-ca.crt')

mqtt_client = mqtt.Client(transport="websockets")
mqtt_client.tls_set_context(context)
mqtt_client.on_connect = on_connect
mqtt_client.on_message = on_message

# Run MQTT in background
def mqtt_thread():
    mqtt_client.connect("broker.emqx.io", 8084)
    mqtt_client.loop_forever()

threading.Thread(target=mqtt_thread, daemon=True).start()


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
