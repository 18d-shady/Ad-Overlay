from flask import Flask
from flask_mqtt import Mqtt
import ssl

app = Flask(__name__)

# MQTT Broker Config
app.config['MQTT_BROKER_URL'] = 'broker.emqx.io'  # Broker URL
app.config['MQTT_BROKER_PORT'] = 8084
app.config['MQTT_KEEPALIVE'] = 60
app.config['MQTT_TLS_ENABLED'] = True  
app.config['MQTT_TRANSPORT'] = 'websockets'


mqtt_client = Mqtt(app)

from app import route
