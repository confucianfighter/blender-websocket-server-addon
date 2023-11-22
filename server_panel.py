import sys
import os

# Assuming your module is in the same directory as your script
import bpy
from . import server

class WebSocketServerPanel(bpy.types.Panel):
    bl_idname = "NODE_PT_websocket_server"
    bl_label = "WSS"
    bl_space_type = 'NODE_EDITOR'
    bl_region_type = 'UI'
    bl_category = 'WebSocket'

    def draw(self, context):
        layout = self.layout
        layout.operator("wss.start_websocket_server")
        layout.operator("wss.stop_websocket_server")
        # Display server messages and status here

# Registration
def register():
    bpy.utils.register_class(WebSocketServerPanel)

def unregister():
    bpy.utils.unregister_class(WebSocketServerPanel)

if __name__ == "__main__":
    register()