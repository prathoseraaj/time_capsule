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
      const res = await axios.post("/api/store", {
        encryptedMessage: encrypted,
        unlockTime: time,
      });

      setLink(`${window.location.origin}/view/${res.data.id}#${key}`);
    } catch (err) {
      console.error("Error:", err);
      alert("Error storing message");
    }
  };

  return (
    <div className="h-[100vh] w-full bg-black text-white flex flex-col items-center justify-center p-4">
      <form
        onSubmit={handleSubmit}
        className="flex flex-col gap-3 w-full max-w-md"
      >
        <textarea
          rows="5"
          placeholder="Enter your secret message"
          value={message}
          onChange={(e) => setMessage(e.target.value)}
          className="p-2 bg-black border border-white text-white w-full rounded resize-none"
        />
        <input
          type="datetime-local"
          value={unlockTime}
          onChange={(e) => setUnlockTime(e.target.value)}
          className="p-2 border border-white bg-black text-white w-full rounded appearance-none focus:outline-none"
        />

        <button
          type="submit"
          className="p-2 border border-white text-white rounded hover:bg-white hover:text-black transition"
        >
          Create Capsule
        </button>
      </form>

      {link && (
        <div className="mt-4 text-center">
          <p className="mb-1">Save this link:</p>
          <a
            href={link}
            target="_blank"
            rel="noreferrer"
            className="break-all underline"
          >
            {link}
          </a>
        </div>
      )}
    </div>
  );
}

export default App;
