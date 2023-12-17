import json
import traceback
import bpy
import bmesh
from . import geometry_exporter


y = 1
def execute_user_code(code):
    return ""
    try:
        # You might want to set up a safe environment for exec
        # to prevent security issues or unwanted access
        local_vars = {}
        exec(code, globals(), local_vars)
        # Assuming the user code stores its result in a variable 'output'
        return {"status": "success", "result": local_vars.get("output")}
    except Exception as e:
        # Capture any errors
        return {"status": "error", "error": str(e), "traceback": traceback.format_exc()}

