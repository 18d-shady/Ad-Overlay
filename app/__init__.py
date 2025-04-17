import ssl
from flask import Flask
from flask_mqtt import Mqtt

app = Flask(__name__)

# SSL Context Setup
context = ssl.create_default_context()
context.load_verify_locations('app/certs/broker.emqx.io-ca.crt')

print(ssl.OPENSSL_VERSION)

# MQTT Config
app.config['MQTT_BROKER_URL'] = 'broker.emqx.io'
app.config['MQTT_BROKER_PORT'] = 8084
app.config['MQTT_KEEPALIVE'] = 60
app.config['MQTT_TLS_ENABLED'] = True
app.config['MQTT_TLS_CONTEXT'] = context
app.config['MQTT_TRANSPORT'] = 'websockets'

mqtt_client = Mqtt(app)
