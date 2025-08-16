from flask import Flask, request, jsonify, send_from_directory
import sqlite3
import uuid
from datetime import datetime
from flask_cors import CORS
import os

app = Flask(__name__, static_folder='../frontend/build', static_url_path='')
CORS(app)
DB = 'message.db'

def init_db():
    with sqlite3.connect(DB) as conn:
        conn.execute('''
            CREATE TABLE IF NOT EXISTS messages (
                id TEXT PRIMARY KEY,
                unlock_time TEXT,
                encrypted TEXT
            )
        ''')
        conn.commit()

init_db()

# Serve React build
@app.route('/')
def serve_react():
    return send_from_directory(app.static_folder, 'index.html')

@app.route('/<path:path>')
def serve_react_static(path):
    if path != "" and os.path.exists(os.path.join(app.static_folder, path)):
        return send_from_directory(app.static_folder, path)
    else:
        return send_from_directory(app.static_folder, 'index.html')

# API: Store message
@app.route('/api/store', methods=['POST'])
def store():
    data = request.get_json()
    message_id = str(uuid.uuid4())
    unlock_time = data.get('unlockTime')
    encrypted = data.get('encryptedMessage')

    with sqlite3.connect(DB) as conn:
        conn.execute("INSERT INTO messages (id, unlock_time, encrypted) VALUES (?, ?, ?)",
                     (message_id, unlock_time, encrypted))
        conn.commit()

    return jsonify({'id': message_id})

# API: View message
@app.route('/view/<message_id>')
def view(message_id):
    with sqlite3.connect(DB) as conn:
        cur = conn.execute("SELECT unlock_time, encrypted FROM messages WHERE id=?", (message_id,))
        row = cur.fetchone()

    if not row:
        return "Message not found.", 404

    unlock_time, encrypted = row
    now = datetime.now()

    try:
        if len(unlock_time) == 16:
            unlock_dt = datetime.strptime(unlock_time, '%Y-%m-%dT%H:%M')
        else:
            unlock_dt = datetime.strptime(unlock_time, '%Y-%m-%dT%H:%M:%S')
    except Exception as e:
        return f"Invalid unlock time format: {e}", 400

    if now < unlock_dt:
        return "Message not yet unlocked.", 403

    # Simpler HTML (from first code)
    return f'''
    <!DOCTYPE html>
    <html>
    <body>
        <div id="output"></div>
        <script src="https://cdnjs.cloudflare.com/ajax/libs/crypto-js/4.1.1/crypto-js.min.js"></script>
        <script>
          const encrypted = "{encrypted}";
          const key = decodeURIComponent(window.location.hash.substring(1));
          const decrypted = CryptoJS.AES.decrypt(encrypted, key).toString(CryptoJS.enc.Utf8);
          document.getElementById('output').innerText = decrypted || "Could not decrypt message";
        </script>
    </body>
    </html>
    '''

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False)
