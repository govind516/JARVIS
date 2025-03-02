from frontend.GUI import (
    gui,
    set_assistant_status,
    show_text_to_screen,
    TempDirPath,
    set_microphone_status,
    answer_modifier,
    query_modifier,
    get_microphone_status,
    get_assistant_status,
)

from backend.Model import first_layer_dmm
from backend.RealtimeSearchEngine import realtime_search_engine
from backend.Automation import automation
from backend.SpeechToText import speech_recognition
from backend.Chatbot import chatbot
from backend.TextToSpeech import text_to_speech
from dotenv import dotenv_values
from asyncio import run
from time import sleep
import subprocess
import threading
import json
import os

# Load environment variable from .env file
env_vars = dotenv_values(".env")

# Retrieve Username, assistant name
Username = env_vars.get("Username")
Assistantname = env_vars.get("Assistantname")

default_message = f"""{Username} : Hello {Assistantname}, How are you ?
{Assistantname} : Welcome {Username}, I am doing well. How may I help you?"""

subprocesses = []
functions = [
    "open",
    "close",
    "play",
    "system",
    "content",
    "google search",
    "youtube search",
]


# Function to display default chats if no previous chat present
def show_default_chat():
    with open("Data/ChatLog.json", "r", encoding="utf-8") as file:
        if len(file.read()) < 5:
            with open(f"{TempDirPath}\Database.data", "w", encoding="utf-8") as file:
                file.write("")
            with open(f"{TempDirPath}\Database.data", "w", encoding="utf-8") as file:
                file.write(default_message)


def read_chatlog_json():
    with open("Data/ChatLog.json", "r", encoding="utf-8") as file:
        return json.load(file)


def chatlog_integration():
    chatlog_data = read_chatlog_json()
    formatted_chatlog = ""

    for entry in chatlog_data:
        if entry["role"] == "user":
            formatted_chatlog += f"{Username}: {entry['content']}\n"
        elif entry["role"] == "assistant":
            formatted_chatlog += f"{Assistantname}: {entry['content']}\n"

    formatted_chatlog = formatted_chatlog.replace("User", Username + " ")
    formatted_chatlog = formatted_chatlog.replace("Assistant", Assistantname + " ")

    with open(f"{TempDirPath}\Database.data", "w", encoding="utf-8") as file:
        file.write(answer_modifier(formatted_chatlog))


def show_chat_on_gui():
    file = open(f"{TempDirPath}\Database.data", "r", encoding="utf-8")
    data = file.read()

    if len(str(data)) > 0:
        lines = data.split("\n")
        result = "\n".join(lines)
        file.close()
        file = open(f"{TempDirPath}\Responses.data", "w", encoding="utf-8")
        file.write(result)
        file.close()


def initial_execution():
    set_microphone_status("False")
    show_text_to_screen("")
    show_default_chat()
    chatlog_integration()
    show_chat_on_gui()


initial_execution()


def main_execution():
    task_execution = False
    image_execution = False
    image_generation_query = ""

    set_assistant_status("Listening...")
    query = speech_recognition()
    show_text_to_screen(f"{Username} : {query}")
    set_assistant_status("Thinking...")
    decision = first_layer_dmm(query)

    print("")
    print(f"\nDecision: {decision}\n")
    print("")

    general_query = any([i for i in decision if i.startswith("general")])
    realtime_query = any([i for i in decision if i.startswith("realtime")])

    merged_query = " and ".join(
        [
            " ".join(i.split()[1:])
            for i in decision
            if i.startswith("general") or i.startswith("realtime")
        ]
    )

    for queries in decision:
        if "generate" in queries:
            image_generation_query = str(queries)
            image_execution = True

    for queries in decision:
        if task_execution == False:
            if any(queries.startswith(func) for func in functions):
                run(automation(list(decision)))
                task_execution = True

    if image_execution == True:
        with open(r"frontend\Files\ImageGeneration.data", "w") as file:
            file.write(f"{image_generation_query},True")
        try:
            p1 = subprocess.Popen(
                ["python", r"backend\ImageGeneration.py"],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                stdin=subprocess.PIPE,
                shell=False,
            )
            subprocesses.append(p1)
        except Exception as e:
            print(f"Error starting ImageGeneration.py: {e}")

    if general_query and realtime_query or realtime_query:
        set_assistant_status("Searching...")
        answer = realtime_search_engine(query_modifier(merged_query))
        show_text_to_screen(f"{Assistantname} : {answer}")
        set_assistant_status("Answering...")
        text_to_speech(answer)
        return True
    else:
        for queries in decision:
            if "general" in queries:
                set_assistant_status("Thinking...")
                query_final = queries.replace("general ", "")
                answer = chatbot(query_modifier(query_final))
                show_text_to_screen(f"{Assistantname} : {answer}")
                set_assistant_status("Answering...")
                text_to_speech(answer)
                return True

            elif "realtime" in queries:
                set_assistant_status("Searching...")
                query_final = queries.replace("realtime ", "")
                answer = realtime_search_engine(query_modifier(query_final))
                show_text_to_screen(f"{Assistantname} : {answer}")
                set_assistant_status("Answering...")
                text_to_speech(answer)
                return True

            elif "exit" in queries:
                answer = "Okay, Bye!"
                show_text_to_screen(f"{Assistantname} : {answer}")
                set_assistant_status("Answering...")
                text_to_speech(answer)
                os._exit(1)


def first_thread():
    while True:
        curr_status = get_microphone_status()

        if curr_status == "True":
            main_execution()
        else:
            ai_status = get_assistant_status()

            if "Available..." in ai_status:
                sleep(0.1)
            else:
                set_assistant_status("Available...")


def second_thread():
    gui()


if __name__ == "__main__":
    threading.Thread(target=first_thread, daemon=True).start()
    second_thread()
