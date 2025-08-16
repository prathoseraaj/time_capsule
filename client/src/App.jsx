import React, { useState } from "react";
import CryptoJS from "crypto-js";
import axios from "axios";

function App() {
  const [message, setMessage] = useState("");
  const [unlockTime, setUnlockTime] = useState("");
  const [link, setLink] = useState("");

  const handleSubmit = async (e) => {
    e.preventDefault();

    if (!message || !unlockTime) {
      alert("Fill all fields");
      return;
    }

    const key = CryptoJS.lib.WordArray.random(16).toString();
    const encrypted = CryptoJS.AES.encrypt(message, key).toString();
    const time = unlockTime.length === 16 ? unlockTime + ":00" : unlockTime;
  
    try {
      // Use relative URL - will work with any domain including .onion
      const res = await axios.post("/api/store", {
        encryptedMessage: encrypted,
        unlockTime: time, 
      });

      // Generate link using current origin (will be your .onion address)
      setLink(`${window.location.origin}/view/${res.data.id}#${key}`);
    } catch (err) {
      console.error("Error:", err);
      alert("Error storing message");
    }
  };

  return (
    <div style={{ padding: 20, justifyContent: "center", alignItems: "center" }}>
      <h2>DeadNet - Anonymous Time Capsule</h2>
      <form onSubmit={handleSubmit}>
        <div>
          <textarea
            rows="5"
            cols="50"
            placeholder="Enter your secret message"
            value={message}
            onChange={(e) => setMessage(e.target.value)}
          />
        </div>
        <div>
          Unlock Date & Time:
          <br />
          <input
            type="datetime-local"
            value={unlockTime}
            onChange={(e) => setUnlockTime(e.target.value)}
          />
        </div>
        <button type="submit">Create Capsule</button>
      </form>

      {link && (
        <div style={{ marginTop: 20 }}>
          <b>Save this link to access your message later:</b>
          <br />
          <a href={link} target="_blank" rel="noreferrer">
            {link}
          </a>
        </div>
      )}
    </div>
  );
}

export default App;