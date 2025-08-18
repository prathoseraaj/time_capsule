# Dead Note - Time Capsule (.onion Edition)

A secure, time-locked message application for the Tor network. Users can encrypt messages, set an unlock time, and share a unique link (with decryption key) over Tor. The message can only be decrypted after the specified time.  
**Perfect for privacy-focused, anonymous, and time-delayed communication on the dark web.**

---

## Disclaimer

- **For demonstration/educational use only.** There is no warranty or guarantee of privacy, security, or anonymity.
- This tool is not intended for, nor should it be used for, any illegal or malicious activity.
- The developers and maintainers of this project are not responsible for any misuse or consequences resulting from the use of this software.
- Always thoroughly review, audit, and understand the code before deploying or using it for sensitive or production purposes.
- Using this project does not guarantee complete anonymity or security; users are responsible for their own operational security (OpSec) and privacy practices.

---

## 🌐 .onion Deployment

- This project is designed to run as a hidden service on the Tor network.
- You must have `tor` installed and configured to expose your Flask server as a `.onion` address.
- See [`onion.txt`](server/onion.txt) for getting server's configured .onion address.

---

## Features

- **AES Encryption in Browser**: Message is encrypted client-side. Key never sent to the server.
- **Time-lock**: Set a date and time after which the message can be unlocked.
- **.onion Link Sharing**: Only those with the exact link (including the key fragment) can view & decrypt.
- **No Accounts, No Logs**: Simple, privacy-first design.
- **SQLite storage**: Minimal and portable.

---

## Directory Structure

```
.
├── client/
│   ├── dist/           
│   ├── src/            
│   ├── public/
│   └── ...
├── server/
│   ├── app.py         
│   ├── requirements.txt
│   ├── build/
│   └── onion.txt       
```

---

## Quick Start

### 1. Build the Frontend

```sh
cd client
npm install
npm run build
```

- This creates `client/dist/` for Flask to serve.

### 2. Setup the Backend

```sh
cd server
python3 -m venv venv
source venv/bin/activate  
pip install -r requirements.txt
```

### 3. Configure Tor Hidden Service

- Ensure `tor` is installed and running.
- Edit your `torrc` (often at `/etc/tor/torrc` or `C:\Users\<User>\AppData\Roaming\tor\torrc`):

    ```
    HiddenServiceDir /path/to/hidden_service/
    HiddenServicePort 80 127.0.0.1:5000
    ```

- Restart tor: `sudo systemctl restart tor`
- Your `.onion` address will appear in `/path/to/hidden_service/hostname` — copy it to `server/onion.txt` for your reference.

### 4. Start Flask Server

```sh
cd server
source venv/bin/activate
python app.py
```
- Flask runs on `127.0.0.1:5000` (as configured for Tor hidden service).

---

## Usage

1. **Visit your .onion site** in Tor Browser: `http://<your-onion-address>.onion`
2. **Enter a secret message** and a future unlock datetime.
3. **Get a unique link** (includes message ID and AES key in the URL hash).
4. **Send the link** to your recipient (over Tor or other secure channels).
5. **Recipient visits the link** after the unlock time to decrypt the message in their browser.

---

## How it Works

- **Encryption**: Uses `crypto-js` AES in the browser. The key is generated client-side; server only stores encrypted data.
- **Unlock Time**: Message is only viewable after chosen datetime (server-enforced).
- **Security**: The decryption key is present only in the URL hash (`#`), which is never sent to the server.
- **Privacy**: No accounts, no IP logging, no plaintext message stored.

---

## File Reference

- `client/src/App.jsx` — React component for message form & link generation
- `server/app.py` — Flask API and static file serving
- `server/onion.txt` — Your generated .onion address

---

## Requirements

- Python 3.x
- Node.js & npm
- Tor

---

## Example .onion Deployment Flow

1. Build frontend (`client/dist/`)
2. Start Flask backend (`server/app.py`)
3. Configure Tor to map your `.onion` address to Flask (`127.0.0.1:5000`)
4. Access via Tor Browser: `http://<your-onion-address>.onion`

---      