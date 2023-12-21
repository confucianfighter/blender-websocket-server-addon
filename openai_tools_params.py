from openai import OpenAI
# Define the parameters for the getCurrentWeather function

get_current_weather_params = {
    "type": "object",
    "properties": {
        "location": {"type": "string", "description": "The city and state e.g. San Francisco, CA"},
        "unit": {"type": "string", "enum": ["c", "f"]}
    },
    "required": ["location"]
}

# Define the getCurrentWeather function
get_current_weather_function = {
    "name": "getCurrentWeather",
    "description": "Get the weather in location",
    "parameters": get_current_weather_params
}

# Define the parameters for the getNickname function
get_nickname_params = {
    "type": "object",
    "properties": {
        "location": {"type": "string", "description": "The city and state e.g. San Francisco, CA"}
    },
    "required": ["location"]
}

# Define the getNickname function
get_nickname_function = {
    "name": "getNickname",
    "description": "Get the nickname of a city",
    "parameters": get_nickname_params
}

# Define the tools (functions)
tools = [
    {"type": "function", "function": get_current_weather_function},
    {"type": "function", "function": get_nickname_function}
]

# Define the assistant
assistant_config = {
    "instructions": "You are a weather bot. Use the provided functions to answer questions.",
    "model": "gpt-4-1106-preview",
    "tools": tools
}

# Create the assistant
assistant = client.beta.assistants.create(**assistant_config)

# Now 'assistant' holds the created assistant
