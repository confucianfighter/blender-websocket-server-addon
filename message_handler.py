import json
from . import geometry_exporter
from . import execute_websocket_code

def process_incomming_json_request(json_string):
    data = {}
    try:
        # Parse the JSON string into a dictionary
        data = json.loads(json_string)
    except json.JSONDecodeError:
        print("JSON Decode Error")
        return None
    
    if data is None:
        return None
    if data.get('type', None) is None:
        return None
    if data['type'] == "console_code":
        # ultimately the return would be a message back with the script id, perhaps.
        return execute_websocket_code.execute_user_code(data['code'])
    if data['type'] == "add_cube":
        cube_dict = geometry_exporter.add_cube()
        # create a message to send back to the client
        json_dict = {
            "type": "mesh_update",
            "mesh_id": "cube"
        }
        json_dict.update(cube_dict)
        cube_json = json.dumps(json_dict)
        # take the cube_json and send it back to the client
        return cube_json
    