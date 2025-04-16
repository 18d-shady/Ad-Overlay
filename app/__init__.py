from flask import Flask
from flask_mqtt import Mqtt
import ssl
import socket

app = Flask(__name__)

context = ssl.create_default_context()
                    
# MQTT Broker Config
app.config['MQTT_BROKER_URL'] = 'broker.emqx.io'  # Broker URL
app.config['MQTT_BROKER_PORT'] = 8083
app.config['MQTT_KEEPALIVE'] = 60
app.config['MQTT_TLS_ENABLED'] = False
app.config['MQTT_TRANSPORT'] = 'websockets'

def secure_mqtt_socket():
    # Create a raw socket and wrap it with SSLContext
    raw_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    ssl_socket = context.wrap_socket(raw_socket, server_hostname='broker.emqx.io')
    return ssl_socket

mqtt_client = Mqtt(app)


#mqtt_client._mqtt_client.socket = secure_mqtt_socket()

from app import route
