from flask import Flask, request
import pyodbc

app = Flask(__name__)

VERIFY_TOKEN = 'idfvbiunsdxvifidsvhnriesnv'

# Database connection
conn_str = 'DRIVER={ODBC Driver 17 for SQL Server};SERVER=192.168.1.145,1435;DATABASE=Exam;UID=yash;PWD=Sit@321#'

def log_message(timestamp, group_id, user_id, message_id, message_type, message_content, participant_id):
    try:
        conn = pyodbc.connect(conn_str)
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO WhatsAppMessages (timestamp, group_id, user_id, message_id, message_type, message_body, participant_id)
            VALUES (?, ?, ?, ?, ?, ?, ?)''',
            (timestamp, group_id, user_id, message_id, message_type, message_content, participant_id))
        conn.commit()
    except Exception as e:
        print(f"Error inserting message: {e}")
    finally:
        conn.close()

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
        value = data.get('value', {})
        messages = value.get('messages', [])
        for message in messages:
            timestamp = int(message['timestamp'])
            user_id = message.get('from', '')
            message_id = message.get('id', '')
            message_type = message.get('type', '')
            message_content = message.get('text', {}).get('body', '')

            # Assuming no group context in the provided data format
            group_id = ''
            participant_id = ''

            log_message(timestamp, group_id, user_id, message_id, message_type, message_content, participant_id)
    except Exception as e:
        print(f"Error processing message: {e}")

    return 'OK', 200



