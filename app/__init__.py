from flask import Flask
from flask_mqtt import Mqtt

import ssl

context = ssl.create_default_context()

app = Flask(__name__)

# MQTT Configuration
app.config['MQTT_BROKER_URL'] = 'broker.emqx.io'
app.config['MQTT_TRANSPORT'] = 'websockets'
app.config['MQTT_BROKER_PORT'] = 8083
app.config['MQTT_TLS_ENABLED'] = False
app.config['MQTT_KEEPALIVE'] = 60
#app.config['MQTT_TLS_INSECURE'] = False  # Set to True only if you must skip cert checks
#app.config['MQTT_TLS_CONTEXT'] = context


mqtt_client = Mqtt(app)

from app import route


#app.run(debug=True, use_reloader=True)