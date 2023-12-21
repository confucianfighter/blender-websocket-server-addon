import json
import traceback
import bpy
import bmesh
from . import geometry_exporter
import sys
import io


y = 1
def execute_user_code(code):
    old_stdout = sys.stdout
    old_stderr = sys.stderr
    new_stdout = io.StringIO()
    new_stderr = io.StringIO()
    sys.stdout = new_stdout
    sys.stderr = new_stderr
    try:
        # You might want to set up a safe environment for exec
        # to prevent security issues or unwanted access
        local_vars = {}
        exec(code, globals(), local_vars)
        # Assuming the user code stores its result in a variable 'output'
        return {"status": "success",
            "type":"console_return",
            "stdout": new_stdout.getvalue(),
            "stderr": new_stderr.getvalue(),
            "caught_exception": "false",
            "result": local_vars.get('output', None)
        }
    except Exception as e:
        # Capture any errors
        return {
            "type": "console_return",
            "stdout": new_stdout.getvalue(),
            "stderr": str(e),
            "caught_exception": "true",
            "status": "error", 
            "error": str(e), "traceback": traceback.format_exc()
        }
    finally:
        sys.stdout = old_stdout
        sys.stderr = old_stderr
        new_stdout.close()
        new_stderr.close()

