import asyncio
import json
from .lib import websockets
import bpy
import threading
import queue
import ssl
import os
from . import message_handler
from . import openai_handler




ws_server_thread = None
max_size = 10 * 1024 * 1024

class WebSocketServerThread(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.send_queue = queue.Queue()
        self.receive_queue = queue.Queue()
        self.stop_event = threading.Event()
        self.stop_flag = False
        self.server = None
        self.loop = None
        
    async def websocket_server(self, websocket, path):
        while not self.stop_flag:
            # Receive messages
            try:
                message = await asyncio.wait_for(websocket.recv(), timeout=0.1)
                self.receive_queue.put(message)
            except asyncio.TimeoutError:
                pass  # No message received in the timeout period
            except websockets.exceptions.ConnectionClosedError:
               continue # The connection was closed

            # Send messages if available
            while not self.send_queue.empty():
                message = self.send_queue.get_nowait()
                await websocket.send(message)
        if self.server:
            self.server.close()
            await self.server.wait_closed()
        
        

    def enqueue_message(self, message):
        self.send_queue.put(message)

    def get_next_received_message(self):
        if not self.receive_queue.empty():
            return self.receive_queue.get_nowait()
        return None

    def run(self):
#       #asyncio.set_event_loop(asyncio.new_event_loop())
#        start_server = websockets.serve(self.websocket_server, '0.0.0.0', 8765)
#        asyncio.new_event_loop().run_until_complete(start_server)
#        asyncio.get_event_loop().run_forever()
        url = bpy.context.scene.websocket_server_url
        port = bpy.context.scene.websocket_server_port
        cert_pem = bpy.path.abspath(bpy.context.scene.websocket_ssl_cert)
        key_pem = bpy.path.abspath(bpy.context.scene.websocket_ssl_key)
        use_ssl = cert_pem and key_pem
        if not os.path.isfile(cert_pem):
            print(f"Certificate file not found: {cert_pem}")
        else:
            print(f"📜 cert pem path: {cert_pem}")
        if not os.path.isfile(key_pem):
            print(f"Key file not found: {key_pem}")
        else:
            print(f"🔑 key pem path: {key_pem}")
         
        ssl_context = None
        if use_ssl:  # You can set this flag based on user input or configuration
            ssl_context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
            ssl_context.load_cert_chain(certfile=cert_pem, keyfile=key_pem)
        self.loop = asyncio.new_event_loop()
        asyncio.set_event_loop(self.loop)
        print(f"Starting server at {url}:{port}")
        global max_size
        if use_ssl:
            print("Using SSL")
            start_server = websockets.serve(self.websocket_server, url, port, ssl=ssl_context, max_size=max_size)
        else:
            print("Not using SSL")
            start_server = websockets.serve(self.websocket_server, url, port, max_size=max_size)
        self.server = self.loop.run_until_complete(start_server)
        self.loop.run_forever()

    def stop(self):
        self.stop_flag=True
#        if self.loop.is_running():
#            self.loop.call_soon_threadsafe(self.loop.stop)
#            print("call soon stop")
        # if self.server:
        #     self.loop.run_until_complete(self.server.wait_closed())
        #     print("wait closed")
#        self.loop.close()
        print("Closed the loop from ws_thread.stop()")
        
def process_websocket_messages():
    global ws_server_thread
    if ws_server_thread is not None:
        message = ws_server_thread.get_next_received_message()
        if message is not None:
            # data = parse_json_request(message)
            # if data is None:
            #     #ws_server_thread.enqueue_message("Invalid json_format. Message was: " + message)
            # else:
            #     # execute python code and return either a json string or error message
            #     request_type = data.get('type', None)# Returns 'default_type' if 'type' is not found
            #     if request_type is None:
            #         print("Request missing a type. " + message")
            #         #ws_server_thread.enqueue_message("Request missing a type. " + message)
            #     else:
            #         switch_request(request_type, data)
                    
            # print("Received message:", message)
            # #ws_server_thread.enqueue_message(message)
            
            text_res = message_handler.process_incomming_json_request(json_string = message)
            ws_server_thread.enqueue_message(text_res)
            # Process the received message

    return 0.1  # Poll every 0.1 seconds

def parse_json_request(json_string):
    try:
        # Parse the JSON string into a dictionary
        data = json.loads(json_string)
        return data
    except json.JSONDecodeError:
        return None
    
def switch_request(case, args):
    switch_dict = {
        "add_node": add_node,
        "add_connection": add_connection,
        "remove_connection": remove_connection
    }

    # The get method returns the function associated with the case,
    # or handle_default if the case is not found.
    return switch_dict.get(case, handle_default)(args)

def handle_default(args):
    global ws_server_thread
    print("Request type is not in dictionary")
    if ws_server_thread is not None:
        ws_server_thread.enqueue_message("Request type no in dictionary")
    
def add_node(args):
    global ws_server_thread
    node_id = args.get('bl_idname', 'no kind of node')
    message = f"Recieved message to add a {node_id} node and about to add the node."
    if ws_server_thread is not None:
        ws_server_thread.enqueue_message(message)
    
def add_connection(args):
    pass
def remove_connection(args):
    pass
class StopWebSocketServerOperator(bpy.types.Operator):
    """Stop the WebSocket Server"""
    bl_idname = "wss.stop_websocket_server"
    bl_label = "Stop WebSocket Server"

    def execute(self, context):
        global ws_server_thread
        if ws_server_thread is not None:
            print("Attempting to stop WebSocket Server...")
            ws_server_thread.stop()
             # Ensure the thread has finished
            print("WebSocket Server Stopped")
        else:
            self.report({'INFO'}, "WebSocket Server not running")
        return {'FINISHED'}
    
class StartWebSocketServerOperator(bpy.types.Operator):
    """Start the WebSocket Server"""
    bl_idname = "wss.start_websocket_server"
    bl_label = "Start WebSocket Server"

    def execute(self, context):
        global ws_server_thread
        if True: #ws_server_thread is None:
            print("Attempting to start WebSocket Server...")
             # Ensure the thread has finished
            start_server()
            print("WebSocket Server started")
        else:
            self.report({'INFO'}, "WebSocket Server thread is not None")
        return {'FINISHED'}
# create openai_handler.assistant_code_request operator
class AssistantCodeRequestOperator(bpy.types.Operator):
    """Request code from OpenAI Codex"""
    bl_idname = "wss.code"
    bl_label = "Request code from OpenAI Codex"

    def execute(self, context):
        openai_handler.assistant_code_request(data="")
        return {'FINISHED'}

def register():
    bpy.utils.register_class(StopWebSocketServerOperator)
    bpy.utils.register_class(StartWebSocketServerOperator)
    bpy.app.timers.register(start_server, first_interval=5.0)
    bpy.utils.register_class(AssistantCodeRequestOperator)
    


def unregister():
    bpy.utils.unregister_class(StopWebSocketServerOperator)
    bpy.utils.unregister_class(StartWebSocketServerOperator)
    bpy.utils.unregister_class(AssistantCodeRequestOperator)

def start_server():
    global ws_server_thread
    ws_server_thread = WebSocketServerThread()
    ws_server_thread.start()
    bpy.app.timers.register(process_websocket_messages)
    
if __name__ == "__main__":
    # Global WebSocket server instance
    register()
   
    
    
