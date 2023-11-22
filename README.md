# WebSocket Addon

## Description
Addon to handle WebSocket communications in Blender. It allows sending and receiving messages via bpy and includes a convenient panel. All asynchronous operations and threading are managed internally.

## Usage
The server runs in the background, maintaining a message queue. It dequeues messages one at a time, calling and waiting for your function to handle them. Messages are passed as unparsed strings, which you can parse as needed. Your callback function will receive these messages as a string argument.

```python
import websocket_addon

# Start the WebSocket server
websocket_addon.server.start_server()

# Set the callback function for when a message is received
websocket_addon.set_message_received_callback("your_callback_function")

# Define your callback function
def your_callback_function(message):
    print("Received message:", message)
    data = json.loads(message)  # Parse the message
    # Process the data
    response = "Your response"
    websocket_addon.server.enqueue_message(response)
```

That's it, all threading and async are handled for you. For convenience a websocket tab is included in the node editor properties panel with buttons for starting and restarting.
