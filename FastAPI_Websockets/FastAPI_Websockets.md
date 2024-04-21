# FastAPI WebSockets Example

This example demonstrates how to create a WebSocket server using FastAPI and interact with it using both Python and HTML/CSS.

## Python Files:

### websocket_server.py:

This file contains the implementation of a WebSocket server using FastAPI. It defines a WebSocket route `/ws` where clients can connect to send and receive messages.

### websocket_client.py:

This file contains the implementation of a WebSocket client using Python. It connects to the WebSocket server implemented in `websocket_server.py`, sends messages, and receives echoed messages back from the server.

## HTML/CSS File:

### websocket_client.html:

This file contains a simple HTML page with an input field and a button. It uses JavaScript to establish a WebSocket connection with the server and send messages entered by the user. The received messages from the server are displayed in a list format.

## Flow:

1. Start the WebSocket server by running `uvicorn websocket_server:app --reload` in the terminal.
2. To test the Python WebSocket client, run `python websocket_client.py` in another terminal window. Enter messages when prompted, and observe the echoed messages received from the server.
3. Type "exit" in the Python client to quit the application.
4. Open the `websocket_client.html` file in a web browser. This will establish a WebSocket connection with the server.
5. Enter a message in the input field and click the "Send" button. The message will be sent to the server.
6. The server will echo back the message, and the echoed message will be displayed on the web page.

This setup demonstrates the bidirectional communication between a WebSocket server implemented with FastAPI and clients using both Python and HTML/CSS.
