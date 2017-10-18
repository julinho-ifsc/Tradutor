import os
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

if __name__ == '__main__':
    try:
        robot = os.environ['ROBOT']
    except:
        robot = 'julinho'

    try:
        broker = os.environ['MQTT_BROKER']
    except:
        broker = 'mqtt.sj.ifsc.edu.br'

    app.run(host='0.0.0.0', port=3000, debug=True)
