from openai import OpenAI
# Define the parameters for the getCurrentWeather function

question_to_user_description = (
    "Your question to user."
    "e.g. \"Sympy module isn't installed. Would you like me to install it from the console?\""
    "or \"There was a syntax error, would you like me to give it another try?\""
)

ask_user_params = {
    "type": "object",
    "properties": {
        "question_to_user": {"type": "string", "description": question_to_user_description},
    },
    "required": ["question_to_user"],
}

get_user_input_function = {
    "name": "getUserInput",
    "description": "Get user input",
    "parameters": ask_user_params,
}

remark_to_user_param_description = (
    "A short and witty status update to the user."
    "e.g. \"Installing sympy module\""
    "or \"Trying again\""
    "or \"Flattery will get you everywhere!\""
)

status_update_params = {
    "type": "object",
    "properties": {
        "short_remark": {"type": "string", "description": remark_to_user_param_description},
    },
}

status_update_function = {
    "name": "statusUpdate",
    "description": "Send a status update to the user.",
    "parameters": status_update_params,
}

code_param_description = (
    "The code to execute."
    "for example a very simple line of code: \"import sympy\"",
    "or \"print('Hello World')\""
    "or an arbitrary number of lines of code:"
    """# Import necessary libraries
import numpy as np
import matplotlib.pyplot as plt

# Generate some data
x = np.linspace(0, 10, 100)
y = np.sin(x)

# Plot the data
plt.plot(x, y)
plt.xlabel('X axis')
plt.ylabel('Y axis')
plt.title('Sine Wave')
plt.show()
"""
)
execute_console_code_params = {
    "type": "object",
    "properties": {
        "code": {"type": "string", "description": code_param_description},
    },
    "required": ["code"],
}

execute_console_code_function_description = (
    "Use this to send code to be automatically executed in the console."
    "The code should be sent exactly as it would be typed into the console."
    "It can be a single line of code, or multiple lines of code."
    "The user is in a VR environment and has no access to the console. User can only see the code and the output."
    "It therefore needs to be well formatted and ready to run."
)

execute_console_code_function = {
    "name": "executeConsoleCode",
    "description": execute_console_code_function_description,
    "parameters": execute_console_code_params,
}
write_code_to_file_description = (
    "Use this to write python modules"
    "The code should be sent exactly as it would appear in the file."
)
write_python_code_to_file_params = {
    "type": "object",
    "properties": {
        "filename": {"type": "string", "description": "The relative filename to write the code to. e.g. \"my_file.py\""},
        "code": {"type": "string", "description": code_param_description},
    },
    "required": ["filename", "code"],
}
write_code_to_file_function = {
    "name": "writeCodeToFile",
    "description": write_code_to_file_description,
    "parameters": write_python_code_to_file_params,
}

code_assistant_tools = [
    {"type": "function", "function": get_user_input_function},
    {"type": "function", "function": execute_console_code_function},
    {"type": "function", "function": write_code_to_file_function},
    {"type": "function", "function": status_update_function}
]

instructions = ("You are a Python console expert. Back in the days, they would have called you a console hot dogger. "
                     "When the user requests for something to be done, reply with a json containing a short witty response, "
                     "and then exactly the code you would put in a python console to do it.")

code_assistant_config = {
    "name": "Python Console Hot Dogger",
    "instructions": instructions,
    "model": "gpt-4-1106-preview",
    "tools": code_assistant_tools,
}
    


# Create the assistant
#assistant = client.beta.assistants.create(**code_assistant_config)

# Now 'assistant' holds the created assistant
