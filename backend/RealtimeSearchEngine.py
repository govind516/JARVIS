from googlesearch import search
from groq import Groq
from json import load, dump
import datetime
from dotenv import dotenv_values

# Load environment variables from .env file
env_vars = dotenv_values(".env")

# Retrieve username, assistant name, and API Key
Username = env_vars.get("Username")
Assistantname = env_vars.get("Assistantname")
GroqAPIKey = env_vars.get("GroqAPIKey")

# Initialize the Groq client using API Key
client = Groq(api_key=GroqAPIKey)

# Define a system message that provides context to the AI chatbot
System = f"""Hello, I am {Username}, You are a very accurate and advanced AI chatbot named {Assistantname} which has real-time up-to-date information from the internet.
*** Provide Answers In a Professional Way, make sure to add full stops, commas, question marks, and use proper grammar.***
*** Just answer the question from the provided data in a professional way. ***"""

# Attempt to load the chat log from JSON file
try:
    with open(r"Data\Chatlog.json") as f:
        messages = load(f)
except FileNotFoundError:
    with open(r"Data\Chatlog.json", "w") as f:
        dump([], f)


def googlesearch(query):
    results = list(search(query, advanced=True, num_results=5))
    answer = f"The search results for '{query}' are:\n[start]\n"

    for i in results:
        answer += f"Title: {i.title}\nDescription: {i.description}\n\n"

    answer += "[end]"
    print(answer)
    return answer


# Function to clean up answer by removing empty lines
def answer_modifier(answer):
    lines = answer.split("\n")  # Split response into lines
    non_empty_lines = [line for line in lines if line.strip()]  # Remove empty lines
    modified_answer = "\n".join(non_empty_lines)
    return modified_answer


# List of system instructions for chatbot
SystemChatBot = [
    {"role": "system", "content": System},
    {"role": "user", "content": "Hi"},
    {"role": "assistant", "content": "Hello, how can I help you?"},
]


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


# Function to get real-time search and response generation.
def realtime_search_engine(prompt):
    global SystemChatBot, messages

    # Load Chat log from JSON file
    with open(r"Data\Chatlog.json") as f:
        messages = load(f)
    messages.append({"role": "user", "content": f"{prompt}"})

    # Add Google search results to system chatbot messages.
    SystemChatBot.append({"role": "system", "content": googlesearch(prompt)})

    # Add real-time information at the beginning
    messages.insert(0, {"role": "system", "content": realtime_information()})

    # Make request to Groq API
    completion = client.chat.completions.create(
        model="llama3-70b-8192",
        messages=SystemChatBot + messages,
        max_tokens=2048,
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
    SystemChatBot.pop()
    return answer_modifier(answer=answer)


# Main program entry point
if __name__ == "__main__":
    while True:
        prompt = input("Enter Your Question: ")  # Prompt user for a question
        if prompt.lower() in ["exit", "quit"]:
            print("Goodbye!")
            break
        print(realtime_search_engine(prompt))
