import os, json
import paho.mqtt.publish as publish
from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/json', methods=['POST'])
def post_json():
    data = json.loads(request.data)

    points = data['points']
    points_list = []

    for point in points:
        points_list.append(point['rfid'] + '-' + point['action'])

    message = ';'.join(points_list)
    publish.single(robot + '/rota', message, hostname=broker)

    return jsonify(message='JSON posted')

if __name__ == '__main__':
    robot = os.getenv('ROBOT', 'julinho')
    broker = os.getenv('MQTT_BROKER', 'nuvem2.sj.ifsc.edu.br')
    env = os.getenv('PYTHON_ENV', 'development')
    debug = False if env == 'production' else True

    app.run(host='0.0.0.0', port=3000, debug=debug)
