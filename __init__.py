
bl_info = {
    "name": "WebSocket Addon",
    "blender": (3, 6, 5),
    "category": "WebSockets",
    "description": "Addon to handle WebSocket communications. Send and recieve via bpy, but also has a panel for convenience.",
    "author": "Daylan Nance",
    "version": (0,0,1)
}

import bpy
from . import server
from . import server_panel



def register():
    server.register()
    server_panel.register()
    
def unregister():
    server.unregister()
    server_panel.unregister()
    
if __name__ == "__main__":
    register()
