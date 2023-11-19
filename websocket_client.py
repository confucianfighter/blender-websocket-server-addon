#import asyncio
#import websockets
#import bpy

#async def websocket_client(stop):
#    uri = "ws://localhost:8765"
#    async with websockets.connect(uri) as websocket:
#        print("Blender sending message")
#        await websocket.send('{"role": "blender"}')
#        while not stop():
#            print("While not stop")
#            await asyncio.sleep(0.1)  # Non-blocking wait
#            # Handle WebSocket communication here

## Global stop flag
#stop_flag = False

## Function to stop the client
#def stop_websocket_client():
#    global stop_flag
#    stop_flag = True

## Asyncio event loop setup
#loop = asyncio.new_event_loop()
#asyncio.set_event_loop(loop)

## Task setup
#task = loop.create_task(websocket_client(lambda: stop_flag))

## Blender timer callback
#def timer_callback():
#    loop.run_until_complete(asyncio.sleep(0.1))
#    if stop_flag:
#        return None  # Stop the timer
#    return 0.1

## Starting the timer
#bpy.app.timers.register(timer_callback)
#import asyncio
#import websockets
#import bpy

#class WebSocketClient:
#    
#    stop_flag=False
#    def __init__(self, uri):
#        self.uri = uri
#        self.websocket = None

#    async def connect(self):
#        print("Trying to connect")
#        self.websocket = await websockets.connect(self.uri)

#    async def receive_messages(self):
#        while not self.stop_flag:
#            print("Waiting to recieve message")
#            message = await self.websocket.recv()
#            print("Received:", message)  # Handle received messages
#        
#    async def send_message(self, message, op):
#        op.report({'INFO'},"Checking if self.websocket")
#        if self.websocket:
#            print("Sending message")
#            await self.websocket.send(message)
#    
#    async def stop(self):
#        self.stop_flag = True
#        
#    async def is_connected(self):
#        return self.websocket is not None and self.websocket.open
## Global WebSocket client instance
#ws_client = WebSocketClient("ws://0.0.0.0:8765")

## Operator for sending messages
#class SendMessageOperator(bpy.types.Operator):
#    """Send a WebSocket Message"""
#    bl_idname = "wm.send_websocket_message"
#    bl_label = "Send WebSocket Message"

#    message: bpy.props.StringProperty(name="Message")

#    def execute(self, context):
#        self.report({'INFO'}, 'Executing send message op')
#        if ws_client is None:
#            self.report({'INFO'}, 'ws_client is None!')
#        if not ws_client.is_connected():
#            self.report({'INFO'}, 'ws_client is not connected!')
#            
#        try:
#            asyncio.run_coroutine_threadsafe(ws_client.send_message(self.message, self), asyncio.get_event_loop())
#            self.report({'INFO'},'NO ERROR DETECTED, message was {self.message}')
#        except:
#            self.report({'INFO'}, 'Run coroutine failed for send op')
#            
#        return {'FINISHED'}
#    
#class StopWSClientOperator(bpy.types.Operator):
#    """Send a WebSocket Message"""
#    bl_idname = "wm.stop_ws_client"
#    bl_label = "Stop the NodeVR Websocket Client"

#    def execute(self, context):
#        print("Stopping WS Client")
#        asyncio.run_coroutine_threadsafe(ws_client.stop(), asyncio.get_event_loop())
#        return {'FINISHED'}

## Register the operator
#def register():
#    bpy.utils.register_class(SendMessageOperator)
#    bpy.utils.register_class(StopWSClientOperator)

#def unregister():
#    bpy.utils.unregister_class(SendMessageOperator)
#    bpy.utils.register_class(StopWSClientOperator)

#if __name__ == "__main__":
#    register()

#    # Start the WebSocket client and listen for messages
#    asyncio.run_coroutine_threadsafe(ws_client.connect(), asyncio.get_event_loop())
#    asyncio.run_coroutine_threadsafe(ws_client.receive_messages(), asyncio.get_event_loop())
#    # Example of sending a message using the operator
#    # bpy.ops.wm.send_websocket_message(message="Hello from Blender")


#import threading
#import queue
#import websockets
#import bpy




#class StopWSClientOperator(bpy.types.Operator):
#    """Send a WebSocket Message"""
#    bl_idname = "wm.stop_ws_client"
#    bl_label = "Stop the NodeVR Websocket Client"

#    def execute(self, context):
#        print("executing stop")
#        print("Stopping WS Client")
#        global stop_flag
#        stop_flag=True
#        return {'FINISHED'}

## Register the operator
#def register():
#    bpy.utils.register_class(SendMessageOperator)
#    bpy.utils.register_class(StopWebsocketClientOperator)

#def unregister():
#    bpy.utils.unregister_class(SendMessageOperator)
#    bpy.utils.register_class(StopWSClientOperator)

## Thread-safe queue for messages
#message_queue = queue.Queue()

## Start WebSocket client thread
#ws_client_thread = WebSocketClientThread("ws://localhost:8765", message_queue)
#ws_client_thread.start()


#def process_messages():
#    while not stop_flag:
#        print("Waiting for message stop flag is")
#        print(stop_flag)
#        if not message_queue.empty():
#            message = message_queue.get()
#            print("message")
#            # Process the message and update the node
#            # Example: update_node_with_message(message)
#            bpy.context.view_layer.update()  # Update the scene

#            # Send a response message
#            # You'll need to implement the response sending logic, possibly using another thread or method

#        return 3  # Continue the timer

## Start the timer to periodically check for messages
#bpy.app.timers.register(process_messages)

# Remember to stop the WebSocket client thread when exiting Blender or when it's no longer needed
# ws_client_thread.stop()

import threading
import queue
import websockets
import asyncio
import bpy

class WebSocketClientThread(threading.Thread):
    def __init__(self, uri):
        threading.Thread.__init__(self)
        self.uri = uri
        self.send_queue = queue.Queue()
        self.receive_queue = queue.Queue()
        self.stop_event = threading.Event()

    async def websocket_client(self):
        async with websockets.connect(self.uri) as websocket:
            await websocket.send('{"role":"blender"}')
            while not self.stop_event.is_set():
                # Send messages if available
                while not self.send_queue.empty():
                    message = self.send_queue.get_nowait()
                    await websocket.send(message)

                # Receive messages
                if websocket.open:
                    try:
                        message = await asyncio.wait_for(websocket.recv(), timeout=0.1)
                        self.receive_queue.put(message)
                    except asyncio.TimeoutError:
                        pass  # No message received

    def enqueue_message(self, message):
        self.send_queue.put(message)

    def get_next_received_message(self):
        if not self.receive_queue.empty():
            return self.receive_queue.get_nowait()
        return None

    def run(self):
        asyncio.new_event_loop().run_until_complete(self.websocket_client())

    def stop(self):
        self.stop_event.set()

def process_websocket_messages():
    global ws_client_thread
    if ws_client_thread is not None:
        ws_client_thread.enqueue_message('{ "role":"blender", "recipient": "unity"}')
        message = ws_client_thread.get_next_received_message()
        if message is not None:
            print("message recieved")
            print(message)
            # Process the received message
            # For example, update something in Blender based on the message

    return 0.1  # Poll every 0.1 seconds

if __name__ == "__main__":
    # Global WebSocket client instance
    ws_client_thread = WebSocketClientThread("ws://0.0.0.0:8765")
    ws_client_thread.start()
    bpy.app.timers.register(process_websocket_messages)
