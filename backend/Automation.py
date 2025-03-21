from AppOpener import close, open as appopen
from webbrowser import open as webopen
from pywhatkit import search, playonyt
from dotenv import dotenv_values
from bs4 import BeautifulSoup
from rich import print
from groq import Groq
import webbrowser
import subprocess
import requests
import keyboard
import asyncio
import os

# Load environment variables from .env file
env_vars = dotenv_values(".env")
GroqAPIKey = env_vars.get("GroqAPIKey")

# Define CSS classes for parsing specific elements in HTML content.
classes = [
    "zCubwf",
    "hgKElc",
    "LTKOO sY7ric",
    "Z0LcW",
    "gsrt vk_bk FzvWSb YwPhnf",
    "pclqee",
    "tw-Data-text tw-text-small tw-ta",
    "IZ6rdc",
    "O5uR6d LTKOO",
    "vLzY6d",
    "webanswers-webanswers_table__webanswers-table",
    "dDoNo ikb4bB gsrt",
    "sXLaOe",
    "LWkfKe",
    "VQF4g",
    "qV3Wpe",
    "kno-rdesc",
    "SPZz6b",
]

# Define a user-agent for making web requests.
user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.75 Safari/537.36"

# Initialize the Groq client with the API key.
client = Groq(api_key=GroqAPIKey)

# Predefined professional responses for user interactions.
professional_responses = [
    "Your satisfaction is my top priority; feel free to reach out if there's anything else I can help you with.",
    "I'm at your service for any additional questions or support you may need—don't hesitate to ask.",
]

# List to store chatbot messages.
messages = []

# System message to provide context to the chatbot.
SystemChatBot = [
    {
        "role": "system",
        "content": f"Hello, I am {os.environ.get('Username', 'a chatbot')}, You're a content writer. You have to write content like letters, articles, and responses.",
    }
]


def google_search(topic):
    search(topic)
    return True


def content(topic):

    # Nested function to open a file in Notepad
    def open_notepad(file):
        default_text_editor = "notepad.exe"
        subprocess.Popen([default_text_editor, file])

    # Nested function to generate content using AI chatbot
    def content_writer_ai(prompt):
        messages.append({"role": "user", "content": f"{prompt}"})

        completion = client.chat.completions.create(
            model="deepseek-r1-distill-llama-70b",
            messages=SystemChatBot + messages,
            max_tokens=2048,
            temperature=0.7,
            top_p=1,
            stream=True,
            stop=None,
        )

        answer = ""

        for chunk in completion:
            if chunk.choices[0].delta.content:
                answer += chunk.choices[0].delta.content

        answer = answer.replace("</s>", "")
        messages.append({"role": "assistant", "content": answer})
        return answer

    topic_clean = topic.replace("Content", "")
    content_by_ai = content_writer_ai(topic_clean)

    with open(
        rf"Data\{topic_clean.lower().replace(' ','')}.txt", "w", encoding="utf-8"
    ) as file:
        file.write(content_by_ai)
        file.close()

    open_notepad(rf"Data\{topic_clean.lower().replace(' ','')}.txt")
    return True


def yt_search(topic):
    url4search = f"https://www.youtube.com/results?search_query={topic}"
    webbrowser.open(url4search)
    return True


def play_yt(query):
    playonyt(query)
    return True


# Function to open an Application or relevant webpage
def open_app(app, session=requests.session()):
    # Known websites dictionary for direct access
    known_websites = {
        "instagram": "https://www.instagram.com/",
        "facebook": "https://www.facebook.com/",
        "twitter": "https://twitter.com/",
        "youtube": "https://www.youtube.com/",
        "linkedin": "https://www.linkedin.com/",
        "github": "https://github.com/",
        "reddit": "https://www.reddit.com/",
        "pinterest": "https://www.pinterest.com/",
        "snapchat": "https://www.snapchat.com/",
        "tiktok": "https://www.tiktok.com/",
        "gmail": "https://mail.google.com/",
        "netflix": "https://www.netflix.com/",
        "spotify": "https://open.spotify.com/",
        "discord": "https://discord.com/app",
        "whatsapp": "https://web.whatsapp.com/",
        "canva": "https://www.canva.com/",
        # Add more as needed
    }

    app = app.strip().lower()  # Normalize the app name

    # Attempts to open the app locally
    try:
        appopen(app, match_closest=True, output=True, throw_error=True)
        return True

    except Exception as e:
        print(f"Error opening application: {e}")

        # Check if it's a known website for direct access
        if app in known_websites:
            print(f"Opening {app} website directly")
            webopen(known_websites[app])
            return True

        # Keep your existing web scraping logic as a fallback
        # Nested function to extract links from HTML content
        def extract_links(html):
            if html is None:
                return []

            soup = BeautifulSoup(html, "html.parser")

            # Try multiple selectors to find links
            all_links = []

            # Original method
            links1 = soup.find_all("a", {"jsname": "UWckNb"})
            all_links.extend(links1)

            # Try for main search results
            for css_class in ["yuRUbf", "g", "rc", "r"]:
                results = soup.find_all("div", class_=css_class)
                for result in results:
                    link_tag = result.find("a")
                    if link_tag:
                        all_links.append(link_tag)

            # If still no links, try a more general approach
            if not all_links:
                all_links = soup.find_all(
                    "a",
                    href=lambda href: href
                    and href.startswith("http")
                    and "google" not in href,
                )

            return [link.get("href") for link in all_links if link.get("href")]

        # Nested function to perform Google Search and retrieve HTML
        def search_google(query):
            url = f"https://www.google.com/search?q={query}"
            headers = {"User-Agent": user_agent}
            response = session.get(url, headers=headers)

            if response.status_code == 200:
                return response.text
            else:
                print(f"Failed to retrieve search results for {query}.")
            return None

        # Try direct URL construction if not a known website
        if "." not in app:  # If it doesn't already contain a domain
            print(f"Trying direct URL for {app}")
            direct_url = f"https://www.{app}.com"
            webopen(direct_url)
            return True

        # Last resort: use your existing search logic
        html = search_google(
            app + " official site"
        )  # Add "official site" to improve results

        if html:
            links = extract_links(html)
            print(links)
            if links:  # Check if links list is not empty
                link = links[0]  # extract first link from search results
                print(f"Opening {link}...")
                webopen(link)
                return True
            else:
                # If no links were found, try a direct search
                webopen(f"https://www.google.com/search?q={app}")
                return True

        return False


# Function to close an application
def close_app(app):
    if "chrome" in app:
        pass
    else:
        try:
            close(app, match_closest=True, output=True, throw_error=True)
            return True
        except:
            return False


# Function to execute 'System-level' Commands
def system(command):

    def mute():
        keyboard.press_and_release("volume mute")

    def unmute():
        keyboard.press_and_release("volume mute")

    def volume_up():
        keyboard.press_and_release("volume up")

    def volume_down():
        keyboard.press_and_release("volume down")

    if command == "mute":
        mute()
    elif command == "unmute":
        unmute()
    elif command == "volume up":
        volume_up()
    elif command == "volume down":
        volume_down()

    return True


# Asynchronous function to translate and execute user commands.
async def translate_and_execute(commands: list[str]):

    funcs = []

    for command in commands:
        if command.startswith("open"):
            if "open it" in command:
                pass
            elif "open file" == command:
                pass
            else:
                fun = asyncio.to_thread(open_app, command.removeprefix("open"))
                funcs.append(fun)

        elif command.startswith("general"):
            pass

        elif command.startswith("realtime"):
            pass

        elif command.startswith("close"):
            fun = asyncio.to_thread(close_app, command.removeprefix("close"))
            funcs.append(fun)

        elif command.startswith("play"):
            fun = asyncio.to_thread(play_yt, command.removeprefix("play"))
            funcs.append(fun)

        elif command.startswith("content"):
            fun = asyncio.to_thread(content, command)
            funcs.append(fun)

        elif command.startswith("google search"):
            fun = asyncio.to_thread(
                google_search, command.removeprefix("google search")
            )
            funcs.append(fun)

        elif command.startswith("youtube search"):
            fun = asyncio.to_thread(yt_search, command.removeprefix("youtube search"))
            funcs.append(fun)

        elif command.startswith("system"):
            fun = asyncio.to_thread(system, command.removeprefix("system"))
            funcs.append(fun)

        else:
            print(f"No Function Found For {command}")

    results = await asyncio.gather(*funcs)

    for result in results:
        if isinstance(result, str):
            yield result
        else:
            yield result


# Asynchronous function to automate command execution
async def automation(commands: list[str]):

    async for result in translate_and_execute(commands):
        pass

    return True
