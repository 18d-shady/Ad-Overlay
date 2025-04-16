from flask import Flask
from flask_mqtt import Mqtt
import ssl

app = Flask(__name__)

# MQTT Broker Config
app.config['MQTT_BROKER_URL'] = 'broker.emqx.io'
app.config['MQTT_BROKER_PORT'] = 8084  # WSS (TLS over WebSocket)
app.config['MQTT_USERNAME'] = ''       # optional
app.config['MQTT_PASSWORD'] = ''       # optional
app.config['MQTT_KEEPALIVE'] = 60
app.config['MQTT_TLS_ENABLED'] = True
app.config['MQTT_TRANSPORT'] = 'websockets'

# Create secure TLS context (correctly for Windows)
context = ssl.create_default_context()
context.check_hostname = True
context.verify_mode = ssl.CERT_REQUIRED
context.set_ciphers('DEFAULT:@SECLEVEL=1')  # Optional fix for older brokers
app.config['MQTT_TLS_CONTEXT'] = context

mqtt_client = Mqtt(app)

from app import route
