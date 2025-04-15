from flask import Flask
from flask_mqtt import Mqtt

app = Flask(__name__)

# MQTT Configuration
app.config['MQTT_BROKER_URL'] = 'broker.emqx.io'
app.config['MQTT_TRANSPORT'] = 'websockets'
app.config['MQTT_BROKER_PORT'] = 8084
app.config['MQTT_TLS_ENABLED'] = True
app.config['MQTT_KEEPALIVE'] = 60


mqtt_client = Mqtt(app)

from app import route


#app.run(debug=True, use_reloader=True)