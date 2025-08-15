from flask import Flask, request, jsonify
import sqlite3
import uuid
from datetime import datetime

app = Flask(__name__)
DB = 'message.db'

def init_db():
    with sqlite3.connect(DB) as conn:
        conn.execute('''CREATE TABLE IF NOT EXISTS messages (
            id TEXT PRIMARY KEY,
            unlock_time TEXT,
            encrypted TEXT''')
@app.route('/store',methods=['POST'])
def store():
    data = request.get_json()
    message_id = str(uuid.uuid4())
    unlock_time = data.get('unlockTime')
    encrypted = data.get('encryptedMessage')

    with sqlite3.connect(DB) as conn:
        conn.execute("INSERT INTO messages (id, unlock_time, encrypted) VALUES (?, ?, ?)",
                     (message_id, unlock_time, encrypted))

    return jsonify({ 'id': message_id })

@app.route('/view/<message_id>')
def view(message_id):
    with sqlite3.connect(DB) as conn:
        cur = conn.execute("SELECT unlock_time, encrypted FROM messages WHERE id=?", (message_id,))
        row = cur.fetchone()

    if not row:
        return "Message not found.", 404

    unlock_time, encrypted = row
    now = datetime.utcnow()

    try:
        unlock_dt = datetime.strptime(unlock_time, '%Y-%m-%dT%H:%M')
    except Exception:
        return "Invalid unlock time format.", 400

    if now < unlock_dt:
        return "Message not yet unlocked.", 403
    return f'''
    <h3>Encrypted Message</h3>
    <p>Use the key from the URL hash (#key) to decrypt this message client-side.</p>
    <pre id="ciphertext">{encrypted}</pre>
    <textarea id="output" rows="10" cols="50"></textarea>

    <script src="https://cdnjs.cloudflare.com/ajax/libs/crypto-js/4.1.1/crypto-js.min.js"></script>
    <script>
      const encrypted = document.getElementById('ciphertext').innerText;
      const key = decodeURIComponent(window.location.hash.substring(1));
      const decrypted = CryptoJS.AES.decrypt(encrypted, key).toString(CryptoJS.enc.Utf8);
      document.getElementById('output').value = decrypted || "[Wrong key or corrupt message]";
    </script>
    '''

if __name__ == '__main__':
    init_db()
    app.run(host='127.0.0.1', port=5000)