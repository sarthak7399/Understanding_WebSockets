// Backend is server.py

import "./App.css";
import { useState, useEffect, useCallback } from "react";
import SpeechRecognition, {
    useSpeechRecognition,
} from "react-speech-recognition";
/* global webkitSpeechRecognition */

const App = () => {
    const [webSocket, setWebSocket] = useState(null);
    const [connectionStatus, setConnectionStatus] = useState("Disconnected");
    const [audioQueue, setAudioQueue] = useState([]);
    const [isSendingAudio, setIsSendingAudio] = useState(false);
    const [isPlayingAudio, setIsPlayingAudio] = useState(false);
    const [isRecording, setIsRecording] = useState(false);
    const [audioChunksPlayed, setAudioChunksPlayed] = useState(0);
    const [text, setText] = useState();
    const [noSpeechErrorCount, setNoSpeechErrorCount] = useState(0);

    const { resetTranscript, browserSupportsSpeechRecognition } =
        useSpeechRecognition();

    const sendDataToBackend = useCallback(
        (data) => {
            if (webSocket && data.trim() !== "") {
                webSocket.send(data);
            }
        },
        [webSocket]
    );

    const startListening = useCallback(() => {
        let recognition; // Define recognition variable

        if (!isRecording && !isPlayingAudio && audioQueue.length === 0) {
            try {
                recognition = new webkitSpeechRecognition(); // Initialize recognition
                recognition.lang = "en-IN";
                recognition.onresult = (event) => {
                    const transcript = event.results[0][0].transcript;
                    // console.log("Complete event object:", event);
                    console.log("Transcript:", transcript);
                    setText(transcript);
                    resetTranscript();
                    setIsSendingAudio(false);
                    setNoSpeechErrorCount(0);
                    sendDataToBackend(transcript);
                };
                recognition.onerror = (event) => {
                    // console.error("Speech recognition error:", event.error);
                    // console.log("Error event numbering:", noSpeechErrorCount);
                    if (event.error === "no-speech") {
                        setNoSpeechErrorCount((count) => count + 1); // Increment the 'no-speech' count
                        if (noSpeechErrorCount + 1 > 2) {
                            // Check if it's the third occurrence
                            if (webSocket) {
                                webSocket.close(); // Disconnect the WebSocket
                                console.log(
                                    "WebSocket disconnected due to timeout."
                                );
                            }
                        }
                    } else if (event.error === "aborted") {
                        startListening();
                    }
                };
                recognition.onstart = () => {
                    setIsRecording(true);
                };
                recognition.onend = () => {
                    setIsRecording(false);
                };
                recognition.start();
            } catch (error) {
                console.error("Error starting speech recognition:", error);
            }
        }
    }, [
        isRecording,
        isPlayingAudio,
        audioQueue.length,
        resetTranscript,
        noSpeechErrorCount,
        webSocket,
        sendDataToBackend,
    ]);

    const startWebSocket = useCallback(() => {
        if (!webSocket) {
            const socket = new WebSocket("ws://localhost:8000/ws");

            socket.onopen = () => {
                console.log("WebSocket connection opened.");
                setConnectionStatus("Connected");
                setWebSocket(socket);
                startListening();
            };

            socket.onerror = (event) => {
                console.error("WebSocket error:", event);
                setConnectionStatus("Error");
            };

            socket.onclose = () => {
                console.log("WebSocket connection closed.");
                setConnectionStatus("Disconnected");
                setWebSocket(null);
            };

            socket.onmessage = async (event) => {
                if (event.data !== "LAST_CHUNK") {
                    setAudioQueue((prevQueue) => [...prevQueue, event.data]);
                    setIsSendingAudio(true);
                } else {
                    setIsSendingAudio(false);
                }
            };
        }
    }, [webSocket, startListening]);

    const playAudioChunks = useCallback(() => {
        if (!isPlayingAudio && audioQueue.length > 0) {
            setIsPlayingAudio(true);
            const audio = new Audio();
            const audioBlob = audioQueue[0];
            audio.src = URL.createObjectURL(audioBlob);
            audio.onended = () => {
                setAudioChunksPlayed((prevChunks) => prevChunks + 1);
                setAudioQueue((prevQueue) => prevQueue.slice(1));
                setIsPlayingAudio(false);
                if (audioChunksPlayed === audioQueue.length) {
                    startListening();
                }
            };
            audio.play().catch((error) => {
                console.error("Error playing audio:", error);
                setIsPlayingAudio(false);
            });
        }
    }, [audioQueue, isPlayingAudio, audioChunksPlayed, startListening]);

    useEffect(() => {
        if (!browserSupportsSpeechRecognition) {
            console.error("Speech recognition not supported by this browser.");
        }
    }, [browserSupportsSpeechRecognition]);

    useEffect(() => {
        if (connectionStatus === "Connected") {
            startListening();
        } else {
            SpeechRecognition.stopListening();
            resetTranscript();
        }
    }, [connectionStatus, startListening, resetTranscript]);

    useEffect(() => {
        if (audioQueue.length > 0 && !isPlayingAudio) {
            playAudioChunks();
        }
    }, [audioQueue, isPlayingAudio, playAudioChunks]);

    useEffect(() => {
        if (isSendingAudio) {
            const timeout = setTimeout(() => {
                setIsSendingAudio(false);
            }, 10000);
            return () => clearTimeout(timeout);
        }
    }, [isSendingAudio]);

    return (
        <div className="container">
            <h2>Speech to Text Converter</h2>
            <br />
            <p>
                A React hook that converts speech from the microphone to text
                and makes it available to your React components.
            </p>

            <div className="main-content" onClick={resetTranscript}>
                {text}
            </div>

            <div className="btn-style">
                <button
                    onClick={() => {
                        if (connectionStatus === "Disconnected") {
                            startWebSocket();
                        } else {
                            if (webSocket) {
                                webSocket.close();
                            }
                        }
                    }}
                >
                    {connectionStatus === "Disconnected"
                        ? "Connect"
                        : "Disconnect"}
                </button>
            </div>
        </div>
    );
};

export default App;
