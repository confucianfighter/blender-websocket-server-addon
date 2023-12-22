from asyncio import wait
from openai import OpenAI
import json
import io
import struct
import pydub
from . import openai_tools_params
from openai_tools_params import code_assistant_config

client = OpenAI()
thread_id = None


def text_completion():
    completion = client.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=[
        {"role": "system", "content": "You are a poetic assistant, skilled in explaining complex programming concepts with creative flair."},
        {"role": "user", "content": "Compose a poem that explains the concept of recursion in programming."}
    ]
    )

    print(completion.choices[0].message)
def assistant_code_request(data) -> str:
    global thread_id
    data = parse_assistant_code_request(data)
    if(data['status'] == "error"):
        return json.dumps(data)
    
    user_request = data['user_request']
    # if user request length is less than 3, return a message saying that the request is too short
    if(len(user_request) < 3):
        message = {"status": "error",
            "type":"code_assistant_reply",
            "short_remark":  "Your request is too short. Please try again.",
            "stderr": "",
            "code": "",
            "caught_exception": "false",
            "result": ""
        }
        return json.dumps(message)
    #user_request = "print 'Wow, you really are a python console hot dogger' to the screen.))"
    instructions = ("You are a Python console expert. Back in the days, they would have called you a console hot dogger. "
                     "When the user requests for something to be done, reply with a json containing a short witty response, "
                     "and then exactly the code you would put in a python console to do it. Reply only with json. Here is an example: "
                     "User requests \"print('hello world to the screen')\". Your response would be "
                     "{\"short_remark\": \"No problem\", \"code\": \"print('hello world')\"}"
                     "The json will be auto parsed and executed by the client.")
    
    assistant = create_assistant(instructions=instructions);# create assistant
    if(assistant['status'] == "error"):
        return json.dumps(assistant)
    assistant = assistant['assistant']
    
    try:
        if(thread_id != None):
            thread = client.beta.threads.retrieve(thread_id)
        else:               
            thread = client.beta.threads.create()
            thread_id = thread.id
    except Exception as e:
        raise RuntimeError("Error creating assistant thread:\n" + str(e))
    
    try: 
        message = client.beta.threads.messages.create(
            thread_id=thread.id,
            role="user",
            content=user_request
        )
    except Exception as e:
        raise RuntimeError("Error creating assistant message:\n" + str(e))
    
    try:
        run = client.beta.threads.runs.create(
            thread_id=thread.id,
            assistant_id=assistant.id,
        )
    except Exception as e:
        raise RuntimeError("Error creating assistant run:\n" + str(e))
    
    try:
        run = client.beta.threads.runs.retrieve(
            thread_id=thread.id,
            run_id=run.id
        )
    except Exception as e:
        raise RuntimeError("Error retrieving assistant run status:\n" + str(e))
    
    while run.status != "completed":
        wait(1)
        try:
            run = client.beta.threads.runs.retrieve(
                thread_id=thread.id,
                run_id=run.id
            )
        except Exception as e:
            raise RuntimeError("Error retrieving assistant run status in the polling loop:\n" + str(e))
    
    try:
        messages = client.beta.threads.messages.list(
            thread_id=thread.id
        )
    except Exception as e:
        raise RuntimeError("Got a message back but error parsing assistant messages:\n" + str(e))
    
    try:
        first_message = messages.data[0] 
    except Exception as e:
        raise RuntimeError("Got a message back but messages.data[0] wasn't there:\n" + str(e))
    # Accessing the first element in the data list
    
    try:
        first_message_text = first_message.content[0].text.value  # Assuming the structure matches your output
    except Exception as e:
        raise RuntimeError("Messages.data[0] was there but first_message.content[0].text.value wasn't there:\n" + str(e))
    
    first_message_text = strip_md_formatting(first_message_text)
    print(first_message_text)
    if(first_message_text == ""):
        # send code assistant reply failed message
        message = {"status": "error",
            "type":"code_assistant_reply",
            "short_remark":  "Failed to parse code assistant JSON, Please try again.",
            "stderr": "",
            "code": "",
            "caught_exception": "false",
            "result": ""
        }
    message_json = json.loads(first_message_text)
    short_remark = message_json['short_remark']
    code = message_json['code']
    message = {"status": "success",
        "type":"code_assistant_reply",
        "short_remark":  short_remark,
        "stderr": "",
        "code": code,
        "caught_exception": "false",
        "result": ""
    }
    try:
        message = json.dumps(message)
    except Exception as e:
        raise RuntimeError("Everything went through fine, but error converting assistant_code_reply to json:\n" + str(e))
    
    print(message)
    return message    # return message

def create_tool_using_assistant():
    try:
        assistant = client.beta.assistants.create(
            **code_assistant_config
        )
    except Exception as e:
        details = f"Error creating assistant: {e}\nThis happened during a code assitant request."
        return {
            "status": "error",
            "type":"code_assistant_reply",
            "short_remark":  "Failed to create code assistant, AI are like humans. Just try again.",
            "stderr": details,
            "code": "",
            "caught_exception": "false",
            "result": ""
        }
    return {
        "status": "success",
        "assistant": assistant
    }

def create_assistant(instructions = ""):
    try:
        assistant = client.beta.assistants.create(
            name="Python Console Hot Dogger",
            instructions=instructions,
            tools=[{"type": "code_interpreter"}],
            model="gpt-4-1106-preview"
        )
    except Exception as e:
        details = f"Error creating assistant: {e}\nThis happened during a code assitant request."
        return {
            "status": "error",
            "type":"code_assistant_reply",
            "short_remark":  "Failed to create code assistant, AI are like humans. Just try again.",
            "stderr": details,
            "code": "",
            "caught_exception": "false",
            "result": ""
        }
    return {
        "status": "success",
        "assistant": assistant
    }

def parse_assistant_code_request(json_string):
    try:
        # Parse the JSON string into a dictionary
        data = json.loads(json_string)
        # add a status key to the dictionary
        data['status'] = "success"
        return data
    except json.JSONDecodeError as e:
        details = f"Error parsing JSON string: {e}.\nString was: {json_string}"
        data = {"status": "error",
            "type":"code_assistant_reply",
            "short_remark":  "Failed to parse code assistant request, Please try again.",
            "stderr": details,
            "code": "",
            "caught_exception": "false",
            "result": ""
        }
        return data
    
def strip_md_formatting(text):
    stripped_text = ""
    if text.startswith("```json"):
        # Strip the Markdown code block syntax
        stripped_text = text.strip("```json\n").rstrip("```")
        print("Text started with json markdown, stripping it")
    else:
        print("Text did not start with json markdown, not stripping it")

    if text.endswith("```"):
        stripped_text = stripped_text.rstrip("```")
        print("Text ended with json markdown, stripping it")
        
    else:
        print("Text did not end with json markdown, not stripping it")
    # Parse the JSON
    try:
        data = json.loads(stripped_text)
        print("JSON string parses correctly, passing it on as a string.", data)
    except json.JSONDecodeError as e:
        print("Failed to decode JSON:", e)
        return ""
    
    return stripped_text
    
def speech_to_text(data):
    # convert wav_file bytes string to a file object
    # wav_file = bytes(wav_file)
    # wav_file = io.BytesIO(wav_file)
    # open text.wav file
    
    data = json.loads(data)
    # frame_rate = data['frame_rate']
    # channels = data['channels']
    # sample_width = data['sample_width']
    # samples = data['raw_bytes']
    # audio_bytes = b''.join(struct.pack('f', sample) for sample in samples)

    # Save the bytes to a WAV file in memory
    wav_io = io.BytesIO()
    # wav_io.write(audio_bytes)
    # wav_io.seek(0)

    # Load this 'file' into PyDub
    # audio_segment = pydub.AudioSegment.from_file(wav_io, format="wav")

    # # Convert to the format required by the speech-to-text service
    # # For example, for Google's API, you need LINEAR16 PCM format
    # audio_segment = audio_segment.set_frame_rate(frame_rate).set_channels(channels).set_sample_width(sample_width)
    # audio_data = audio_segment.raw_data

    wav_file = open("C:\\Users\\Daylan\\AppData\\Roaming\\Blender Foundation\\Blender\\4.0\\scripts\\addons\\blender-websocket-server-addon\\speech_sample.wav", "rb")
    try:
        transcript = client.audio.transcriptions.create(
            model="whisper-1", 
            file=wav_file,
        )
    except Exception as e:
        
        raise RuntimeError("Error sending to openai:\n" + e)
        
    text = transcript.text
    print(text)
    print(f"👍👍👍👍👍👍👍👍👍👍👍")
    print(text)
    print(text)
    message = {"status": "success",
        "type":"speech_to_text_reply",
        "text": text,
        "stdout": text,
        "stderr": "",
        "caught_exception": "false",
        "result": ""
    }
    return json.dumps(message)
    