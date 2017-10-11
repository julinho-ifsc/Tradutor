# FLASK
print 'Carregando .. 25% ... 50% .... 100% vamos com tudo traduzir este codigooooooooooo'
import paho.mqtt.client as mqtt
from flask import Flask, request
import json
import paho.mqtt.publish as publish

app = Flask(__name__)

@app.route("/json", methods=['POST'])
def postJson():
    dados = request.get_json()
    lista_de_pontos = []
    for points in dados['points']:
        lista_de_pontos.append(points['rfid'] + '-' + points['action'])
    final = ';'.join(lista_de_pontos)
    
    print final
    publish.single("julinho/rota", final, hostname="mqtt.sj.ifsc.edu.br")
    return 'JSON posted'
app.run(host='0.0.0.0', port=3000, debug=True)

#Traduz as msg mqtt para json 

def not_empty(str):
    return str != ''

def on_connect(client, userdata, flags, rc):
    client.subscribe("julinho/#")

def on_message(client, userdata, msg):
    topic = filter(not_empty, msg.topic.split('/'))  #split transforma em lista, separados   # ex, nesse caso julinho/sos ficaria ['julinho', 'sos']
    print(json.dumps({(topic[1]): int((msg.payload))}))        

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

client.connect("iot.eclipse.org", 1883, 60)
client.loop_forever()