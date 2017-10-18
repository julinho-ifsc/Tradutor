import os, json
import paho.mqtt.client as mqtt
import paho.mqtt.publish as publish
from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/json', methods=['POST'])
def post_json():
    dados = request.get_json()
    lista_de_pontos = []
    for points in dados['points']:
        lista_de_pontos.append(points['rfid'] + '-' + points['action'])
    final = ';'.join(lista_de_pontos)
    publish.single(robot + '/rota', final, hostname=broker)
    return jsonify(message='JSON posted')

# Traduz as msg mqtt para json
def not_empty(string):
    return string != ''

def on_connect(client, userdata, flags, rc):
    client.subscribe(robot + '/#')

def on_message(client, userdata, msg):
    topic = list(filter(not_empty, msg.topic.split('/')))
    print(json.dumps({(topic[1]): str(msg.payload.decode('utf-8'))}))

if __name__ == '__main__':
    try:
        robot = os.environ['ROBOT']
    except:
        robot = 'julinho'
    try:
        broker = os.environ['MQTT_BROKER']
    except:
        broker = 'mqtt.sj.ifsc.edu.br'
    client = mqtt.Client()
    client.on_connect = on_connect
    client.on_message = on_message
    client.connect(broker, 1883, 60)
    client.loop_forever()
    app.run(host='0.0.0.0', port=3000, debug=True)
