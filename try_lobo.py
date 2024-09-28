from flask import Flask, jsonify, request
from pyzabbix import ZabbixMetric, ZabbixSender

app = Flask(__name__)

# Zabbix configuration
ZABBIX_SERVER = "zabbix-server"
ZABBIX_PORT = 10051
ZABBIX_HOST = "nr-server"
ZABBIX_ITEM_KEY = "123123"

# Token de autenticação
AUTH_TOKEN = "AgErI#ArauJo#ZBwebhook"

# Function to send data to Zabbix
def send_data_to_zabbix(data):
    metric = ZabbixMetric(ZABBIX_HOST, ZABBIX_ITEM_KEY, data)
    sender = ZabbixSender(zabbix_server=ZABBIX_SERVER, zabbix_port=ZABBIX_PORT)
    response = sender.send([metric])
    # Extract relevant information from the response
    return {
        "processed": response.processed,
        "failed": response.failed,
        "total": response.total,
        "seconds_spent": response.time
    }

# Função de autenticação baseada em token
def check_auth(token):
    return token == AUTH_TOKEN

# Webhook endpoint to receive data and send it to Zabbix
@app.route('/zabbix-webhook', methods=['POST'])
def receive_webhook():
    auth_header = request.headers.get('Auth')
    if not check_auth(auth_header):
        return jsonify({"status": "error", "message": "Error no token"}), 403
    try:
        webhook_data = request.json
        if webhook_data is None:
            return jsonify({"status": "error", "message": "Nenhum dado fornecido"}), 400
        zabbix_response = send_data_to_zabbix(webhook_data)
        return jsonify({"status": "success", "response": zabbix_response}), 200
    except Exception as e:
        print("Error:", str(e))
        return jsonify({"status": "error", "message": str(e)}), 500

if __name__ == "__main__":
    app.run(port=8000, host="0.0.0.0")