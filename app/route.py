from flask import Flask, render_template, request, jsonify, send_from_directory
import paho.mqtt.client as mqtt
import threading
import ssl
from app import app
import os
import json



MQTT_BROKER = "broker.emqx.io"
MQTT_PORT = 8084
MQTT_TOPIC = "/overlay/toggle"

mqtt_client = mqtt.Client(clean_session=True, transport="websockets")


# MQTT Callbacks
def on_connect(client, userdata, flags, rc):
    print("✅ Connected to MQTT broker with result code", rc)
    client.subscribe(MQTT_TOPIC)

def on_message(client, userdata, msg):
    print(f"📨 Message received: {msg.topic} → {msg.payload.decode()}")

def on_disconnect(client, userdata, rc):
    print(f"🔌 Disconnected with result code {rc}")
    if rc != 0:
        print("⚠️ Unexpected disconnect. Reconnecting...")
        try:
            client.reconnect()
        except Exception as e:
            print(f"❌ Reconnect failed: {e}")

# Configure MQTT client
mqtt_client.reconnect_delay_set(min_delay=2, max_delay=10)
mqtt_client.on_connect = on_connect
mqtt_client.on_message = on_message
mqtt_client.on_disconnect = on_disconnect

# TLS Setup using system CA certs (no need for .crt file)
context = ssl.create_default_context()
#context.load_verify_locations('app/certs/broker.emqx.io-ca.crt')
mqtt_client.tls_set_context(context)


# Run MQTT client in a background thread
def mqtt_thread():
    try:
        mqtt_client.connect(MQTT_BROKER, MQTT_PORT, keepalive=60)
        mqtt_client.loop_forever()
    except Exception as e:
        print(f"🚨 MQTT connection failed: {e}")

threading.Thread(target=mqtt_thread, daemon=True).start()


# Flask routes
@app.route('/')
def index():
    return render_template("index.html")

@app.route('/toggle_overlay', methods=['POST'])
def toggle_overlay():
    data = request.json
    current_state = data.get('state')
    message = 'turn_on' if current_state == 'on' else 'turn_off'
    result = mqtt_client.publish(MQTT_TOPIC, message, qos=1)
    print("📤 Publish result:", result)
    return jsonify({"status": "toggled", "new_state": message})


@app.route('/static/<path:path>')
def send_static(path):
    return send_from_directory('static', path)
