from asyncio import wait
from openai import OpenAI
import json
import io
import struct
import pydub

client = OpenAI()

def text_completion():
    completion = client.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=[
        {"role": "system", "content": "You are a poetic assistant, skilled in explaining complex programming concepts with creative flair."},
        {"role": "user", "content": "Compose a poem that explains the concept of recursion in programming."}
    ]
    )

    print(completion.choices[0].message)
def assistant_code_request(data):
    #data = json.loads(data)
    #user_request = data['user_request']
    user_request = "print('Wow, you really are a python console hot dogger' to the screen.))"
    instructions = ("You are a Python console expert. Back in the days, they would have called you a console hot dogger. "
                     "When the user requests for something to be done, reply with a json containing a short witty response, "
                     "and then exactly the code you would put in a python console to do it. Reply only with json. Here is an example: "
                     "User requests \"print('hello world to the screen')\". Your response would be "
                     "{\"short_response\": \"No problem\", \"code\": \"print('hello world')\"}")
    

    assistant = client.beta.assistants.create(
        name="Python Console Hot Dogger",
        instructions=instructions,
        tools=[{"type": "code_interpreter"}],
        model="gpt-4-1106-preview"
    )
    thread = client.beta.threads.create()
    message = client.beta.threads.messages.create(
        thread_id=thread.id,
        role="user",
        content=user_request
    )
    run = client.beta.threads.runs.create(
        thread_id=thread.id,
        assistant_id=assistant.id,
    )
    run = client.beta.threads.runs.retrieve(
        thread_id=thread.id,
        run_id=run.id
    )
    while run.status != "completed":
        wait(1)
        run = client.beta.threads.runs.retrieve(
            thread_id=thread.id,
            run_id=run.id
        )
        
    messages = client.beta.threads.messages.list(
        thread_id=thread.id
    )
    # message = {"status": "success",
    #     "type":"assistant_code_reply",
    #     "stdout": messages,
    #     "stderr": "",
    #     "code": messages,
    #     "caught_exception": "false",
    #     "result": ""
    # }
    # message = json.dumps(message)
    first_message = messages.data[0]  # Accessing the first element in the data list
    first_message_text = first_message.content[0].text.value  # Assuming the structure matches your output

    print(first_message_text)
    # return message
    
    
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
        "type":"console_return",
        "stdout": text,
        "stderr": "",
        "caught_exception": "false",
        "result": ""
    }
    return json.dumps(message)
    