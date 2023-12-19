from openai import OpenAI
import json
import io

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
    
def speech_to_text(wav_file):
    # convert wav_file bytes string to a file object
    # wav_file = bytes(wav_file)
    # wav_file = io.BytesIO(wav_file)
    # open text.wav file
    wav_file = open("C:\\Users\\Daylan\\AppData\\Roaming\\Blender Foundation\\Blender\\4.0\\scripts\\addons\\blender-websocket-server-addon\\test.wav", "rb")
    try:
        transcript = client.audio.transcriptions.create(
            model="whisper-1", 
            file=wav_file
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
    