# Basic WebSocket Interaction

This portion of the project demonstrates a simple interaction using WebSockets in Python. In this example, a WebSocket server is created to echo back any message it receives from a client.

## How it Works:

### Server Setup:
- The WebSocket server is implemented using Python and the `websockets` library.
- It listens for incoming connections on localhost, port 8765.

### Client Setup:
- The WebSocket client is also written in Python and uses the `websockets` library.
- It connects to the WebSocket server running on localhost, port 8765.

### Interaction:
- The client sends a message ("Hello, WebSocket Server!") to the server.
- The server receives the message and echoes it back to the client.
- The client receives the echoed message and prints it to the console.

## Running the Example:

### Start the Server:
1. Open a terminal window.
2. Navigate to the directory containing `websocket_server.py`.
3. Run the command: `python websocket_server.py`.

### Run the Client:
1. Open another terminal window.
2. Navigate to the directory containing `websocket_client.py`.
3. Run the command: `python websocket_client.py`.

### Observe Output:
- You should see the client sending a message to the server and receiving the echoed message back.

## Conclusion:

This basic interaction demonstrates the simplicity and power of WebSockets for real-time communication between clients and servers. Feel free to explore and modify the code to deepen your understanding of WebSockets in Python.
