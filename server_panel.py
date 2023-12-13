import sys
import os
import bpy
from . import server

def update_server_settings(self, context):
    # This function will be called whenever the URL or port properties are updated.
    # You can add logic here to react to the changes, e.g., restart the server.
    scene = context.scene
    server.url = scene.websocket_server_url
    server.port = scene.websocket_server_port

    # Now you can use the url and port values
    # For example, to restart the server with the new settings
    print("Updated server settings: URL =", url, "Port =", port)

class WebSocketServerPanel(bpy.types.Panel):
    bl_idname = "NODE_PT_websocket_server"
    bl_label = "WebSocket Server Settings"
    bl_space_type = 'NODE_EDITOR'
    bl_region_type = 'UI'
    bl_category = 'WebSocket'

    def draw(self, context):
        layout = self.layout
        scene = context.scene

        layout.prop(scene, "websocket_server_url", text="URL")
        layout.prop(scene, "websocket_server_port", text="Port")

        layout.operator("wss.start_websocket_server")
        layout.operator("wss.stop_websocket_server")
        # Add a checkbox for SSL:
        layout.prop(scene, "websocket_ssl")
        # get the value of the checkbox:
        ssl = scene.websocket_ssl
        # if the checkbox is checked, show the cert and key path fields:
        if ssl:
            layout.prop(scene, "websocket_ssl_cert", text="SSL Certificate")
            layout.prop(scene, "websocket_ssl_key", text="SSL Key")
           
        # if the checkbox is not checked, hide the cert and key path fields:
        
        
# Registration
def register():
    bpy.types.Scene.websocket_server_url = bpy.props.StringProperty(
        name = "URL",
        description = "WebSocket server URL",
        default = "localhost",
        update = update_server_settings
    )
    # Add property for cert and key path:
    bpy.types.Scene.websocket_ssl_cert = bpy.props.StringProperty(
        name="SSL Certificate",
        subtype='FILE_PATH',
        description="Path to SSL certificate"
    )
    # add bool property for ssl
    bpy.types.Scene.websocket_ssl = bpy.props.BoolProperty(
        name="SSL",
        description="Use SSL",
        default=False
    )
    bpy.types.Scene.websocket_ssl_key = bpy.props.StringProperty(
        name="SSL Key",
        subtype='FILE_PATH',
        description="Path to SSL key"
    )

    bpy.types.Scene.websocket_server_port = bpy.props.IntProperty(
        name = "Port",
        description = "WebSocket server port",
        default = 8080,
        min = 1,
        max = 65535,
        update = update_server_settings
    )

    bpy.utils.register_class(WebSocketServerPanel)

def unregister():
    bpy.utils.unregister_class(WebSocketServerPanel)
    del bpy.types.Scene.websocket_server_url
    del bpy.types.Scene.websocket_server_port
    del bpy.types.Scene.websocket_ssl_cert
    del bpy.types.Scene.websocket_ssl_key
    del bpy.types.Scene.websocket_ssl

if __name__ == "__main__":
    register()
