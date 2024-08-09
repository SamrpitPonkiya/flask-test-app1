from flask import Flask, request
import pyodbc

app = Flask(__name__)

VERIFY_TOKEN = 'idfvbiunsdxvifidsvhnriesnv'



@app.route("/")
def start():
    return "The APp is running"

@app.route('/whatsapp-webhook', methods=['GET'])
def verify_webhook():
    token_sent = request.args.get("hub.verify_token")
    if token_sent == VERIFY_TOKEN:
        return request.args.get("hub.challenge")
    return 'Invalid verification token', 403

@app.route('/whatsapp-webhook', methods=['POST'])
def webhook():
    data = request.get_json()

    try:
      print(data)
           
    except Exception as e:
        print(f"Error processing message: {e}")

    return 'OK', 200



