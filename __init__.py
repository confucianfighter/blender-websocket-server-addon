
bl_info = {
    "name": "WebSocket Addon",
    "blender": (3, 6, 5),
    "category": "WebSockets",
    "description": (
        "Addon to handle WebSocket communications. Send and receive via bpy, but also has a panel for convenience. "
        "All async operations and threading are handled for you. \n"
        "Usage:\n"
        "import websocket_addon\n"
        "websocket_addon.server.start_server()\n\n"
        "# The server runs in the background and keeps a queue. It dequeues messages one at a time and calls and waits\n"
        "# for your function to handle them each time.\n"
        "# They are passed to you as unparsed strings. You can parse them however you like.\n"
        "# Your callback function will be passed a string.\n\n"
        "websocket_addon.set_message_received_callback('your_callback_function')\n\n"
        "def your_callback_function(message):\n"
        "    print('Received message:', message)\n"
        "    data = json.loads(message)\n"
        "    # Do something with the data\n"
        "    message = 'Your response'\n"
        "    websocket_addon.server.enqueue_message(message)"
    ),
    "author": "Daylan Nance",
    "version": (0,0,1)
}

import bpy
from . import server
from . import server_panel
import sys

# class SetMessageCallbackOperator(bpy.types.Operator):
#     """Operator to set the message received callback function
#     This is not currently in use but the code is preserved for future use"""
#     bl_idname = "wss.set_message_callback"
#     bl_label = "Set Message Callback"
#     callback_function_name: bpy.props.StringProperty

#     def execute(self, context):
#         # Set the callback function
#         # Ensure that the function name exists in bpy.app.driver_namespace
#         if self.callback_function_name in bpy.app.driver_namespace:
#             context.scene.websocket_message_callback = self.callback_function_name
#         else:
#         return {'FINISHED'}

# // Create an event that can be subscred to


def register():
    if __name__ != "websocket_addon":
        sys.modules["websocket_addon"] = sys.modules[__name__]
    server.register()
    server_panel.register()
    #bpy.utils.register_class(SetMessageCallbackOperator)
    
def unregister():
    server.unregister()
    server_panel.unregister()
    #bpy.utils.uregister_class(SetMessageCallbackOperator)

    
if __name__ == "__main__":
    register()
