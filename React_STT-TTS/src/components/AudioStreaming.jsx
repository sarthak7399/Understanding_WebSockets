import React, { useState, useRef } from "react";

const AudioStreaming = () => {
  const [isConnected, setIsConnected] = useState(false);
  const [audioChunks, setAudioChunks] = useState([]);
  const audioPlayerRef = useRef(null);

  const connectWebSocket = () => {
    const websocket = new WebSocket("ws://localhost:8000/audio");

    websocket.onopen = () => {
      console.log("WebSocket connection established");
      setIsConnected(true);
    };

    websocket.onmessage = async (event) => {
      const audioData = event.data;
      if (audioData instanceof Blob) {
        setAudioChunks((prevChunks) => [...prevChunks, audioData]);
        if (!audioPlayerRef.current.paused) {
          // If the audio player is already playing, no need to trigger play again
          return;
        }
        playNextChunk(0); // Start playing the chunks from index 0
      }
    };
  };

  const playNextChunk = (index) => {
    if (index >= audioChunks.length) {
      return; // Stop if all chunks have been played
    }
    const audioBlob = audioChunks[index];
    const audioUrl = URL.createObjectURL(audioBlob);
    audioPlayerRef.current.src = audioUrl;
    audioPlayerRef.current.onended = () => {
      playNextChunk(index + 1); // Play the next chunk recursively
    };
    audioPlayerRef.current.play();
  };

  return (
    <div>
      <button onClick={connectWebSocket}>
        {isConnected ? "Connected" : "Connect"}
      </button>
      <audio controls ref={audioPlayerRef}></audio>
    </div>
  );
};

export default AudioStreaming;
