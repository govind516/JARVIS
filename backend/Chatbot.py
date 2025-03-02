from groq import Groq
from json import load, dump
import datetime
from dotenv import dotenv_values

#  Load environment variable from .env file
env_vars = dotenv_values(".env")

# Rerieve username, assitant name and API Key
Username = env_vars.get("Username")
Assistantname = env_vars.get("Assistantname")
GroqAPIKey = env_vars.get("GroqAPIKey")

# Initialize the Groq client using API Key
client = Groq(api_key=GroqAPIKey)

# Initialize empty list to store chat messages
messages = []

# Define a system message that provides context to AI chatbot about its role and behaviour
System = f"""Hello, I am {Username}, You are a very accurate and advanced AI chatbot named {Assistantname} which also has real-time up-to-date information from the internet.
*** Do not tell time until I ask, do not talk too much, just answer the question.***
*** Reply in only English, even if the question is in Hindi, reply in English.***
*** Do not provide notes in the output, just answer the question and never mention your training data. ***
"""

# List of system instructions for chatbot
SystemChatBot = [{"role": "system", "content": System}]

# Attempt to load the chat log from JSON file
try:
    with open(r"Data\Chatlog.json") as f:
        messages = load(f)
except FileNotFoundError:
    with open(r"Data\Chatlog.json", "w") as f:
        dump([], f)


# Function to get real-time date and time information
def realtime_information():
    current_date_time = datetime.datetime.now()
    day = current_date_time.strftime("%A")
    date = current_date_time.strftime("%d")
    month = current_date_time.strftime("%B")
    year = current_date_time.strftime("%Y")
    hour = current_date_time.strftime("%H")
    minute = current_date_time.strftime("%M")
    second = current_date_time.strftime("%S")

    # Format information into string
    data = "Please use this real-time information if needed,\n"
    data += f"Day: {day}\nDate: {date}\nMonth: {month}\nYear: {year}\n"
    data += f"Time: {hour} hours :{minute} minutes :{second} seconds.\n"
    return data


# Function to modify chatbot's response for better formatting
def answer_modifier(answer):
    lines = answer.split("\n")  # Split response into lines
    non_empty_lines = [line for line in lines if line.strip()]  # Remove empty lines
    modified_answer = "\n".join(non_empty_lines)
    return modified_answer


# Main chatbot function to handle user queries
def chatbot(query):
    """This  function sends the user's query  to chatbot and returns AI's response."""

    try:
        # Load the existing chat log from JSON file
        with open(r"Data\Chatlog.json") as f:
            messages = load(f)

        messages.append({"role": "user", "content": f"{query}"})

        # Add real-time information at the beginning
        messages.insert(0, {"role": "system", "content": realtime_information()})

        # Make request to Groq API
        completion = client.chat.completions.create(
            model="llama3-70b-8192",
            messages=SystemChatBot + messages,
            max_tokens=1024,
            temperature=0.7,
            top_p=1,
            stream=True,
            stop=None,
        )

        # Initialize empty string to store AI's response
        answer = ""

        # Process the streamed response chunks.
        for chunk in completion:
            if chunk.choices[0].delta.content:
                answer += chunk.choices[0].delta.content

        answer = answer.replace(
            "</s>", ""
        )  # Clean up any unwanted tokens from the response.

        # Append the chatbot's response to the messages list.
        messages.append({"role": "assistant", "content": answer})

        # Save the updated chat log to the JSON file.
        with open(r"Data\ChatLog.json", "w") as f:
            dump(messages, f, indent=4)

        # Return the formatted response.
        return answer_modifier(answer=answer)

    except Exception as e:
        # Handle errors by printing the exception and resetting the chat log.
        print(f"Error: {e}")
        with open(r"Data\ChatLog.json", "w") as f:
            dump([], f, indent=4)
        return "An error occurred. Please try again."  # Retry the query after resetting the log.


# Main program entry point
if __name__ == "__main__":
    while True:
        user_input = input("Enter Your Question: ")  # Prompt user for a question
        if user_input.lower() in ["exit", "quit"]:
            print("Goodbye!")
            break
        print(chatbot(user_input))
