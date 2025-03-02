# from selenium import webdriver
# from selenium.webdriver.common.by import By
# from selenium.webdriver.chrome.service import Service
# from selenium.webdriver.chrome.options import Options
# from webdriver_manager.chrome import ChromeDriverManager
# from dotenv import dotenv_values
# import os
# import mtranslate as mt

# # Load environment variables from .env file
# env_vars = dotenv_values(".env")

# # Get input language setting from the environment variable
# input_language = env_vars.get("InputLanguage", "en")

# # Define HTML code for speech recognition interface
# HtmlCode = """<!DOCTYPE html>
# <html lang="en">
# <head>
#     <title>Speech Recognition</title>
# </head>
# <body>
#     <button id="start" onclick="startRecognition()">Start Recognition</button>
#     <button id="end" onclick="stopRecognition()">Stop Recognition</button>
#     <p id="output"></p>
#     <script>
#         const output = document.getElementById('output');
#         let recognition;

#         function startRecognition() {
#             recognition = new webkitSpeechRecognition() || new SpeechRecognition();
#             recognition.lang = '';
#             recognition.continuous = true;

#             recognition.onresult = function(event) {
#                 const transcript = event.results[event.results.length - 1][0].transcript;
#                 output.textContent += transcript;
#             };

#             recognition.onend = function() {
#                 recognition.start();
#             };
#             recognition.start();
#         }

#         function stopRecognition() {
#             recognition.stop();
#             output.innerHTML = "";
#         }
#     </script>
# </body>
# </html>"""

# # Replace the language setting in the HTML code with input language from env
# HtmlCode = str(HtmlCode).replace(
#     "recognition.lang = '';", f"recognition.lang = '{input_language}';"
# )

# # write the modified code to a file
# with open(r"Data\Voice.html", "w") as f:
#     f.write(HtmlCode)

# # Get current working directory
# curr_dir = os.getcwd()

# # Generate file path for HTML file
# Link = f"{curr_dir}/data/Voice.html"

# # Set Chrome options for the WebDriver.
# chrome_options = Options()
# user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.142.86 Safari/537.36"
# chrome_options.add_argument(f"user-agent={user_agent}")
# chrome_options.add_argument("--use-fake-ui-for-media-stream")
# chrome_options.add_argument("--use-fake-device-for-media-stream")
# chrome_options.add_argument("--headless=new")

# # Initialize the Chrome WebDriver using the ChromeDriverManager.
# service = Service(ChromeDriverManager().install())
# driver = webdriver.Chrome(service=service, options=chrome_options)

# # Define the path for temporary files.
# TempDirPath = rf"{curr_dir}/frontend/Files"


# # Function to set the assistant's status by writing it to a file.
# def set_assistant_status(status):
#     with open(rf"{TempDirPath}/Status.data", "w", encoding="utf-8") as file:
#         file.write(status)


# def query_modifier(query):
#     if not query.strip():  # Handle empty input
#         return ""

#     new_query = query.lower().strip()
#     query_words = new_query.split()

#     question_words = {
#         "how",
#         "what",
#         "who",
#         "when",
#         "where",
#         "why",
#         "which",
#         "whose",
#         "whom",
#         "can",
#         "what's",
#         "where's",
#         "how's",
#     }

#     auxiliary_verbs = {
#         "is",
#         "are",
#         "am",
#         "was",
#         "were",
#         "do",
#         "does",
#         "did",
#         "can",
#         "could",
#         "will",
#         "would",
#         "shall",
#         "should",
#         "may",
#         "might",
#         "must",
#         "have",
#         "has",
#         "had",
#     }

#     # Check if the first word suggests a question
#     is_question = query_words[0] in question_words or query_words[0] in auxiliary_verbs

#     # Ensure proper punctuation at the end
#     if new_query[-1] in [".", "?", "!"]:
#         new_query = new_query[:-1]  # Remove existing punctuation

#     new_query += "?" if is_question else "."

#     return new_query.capitalize()


# def universal_translator(text):
#     english_translation = mt.translate(text, "en", "auto")
#     return english_translation.capitalize()


# # Function to translate text into English using mtranslate Library
# def speech_recognition():

#     # open the HTML file in browser
#     driver.get("file:///" + Link)

#     # start speech recogniition by clicking the start button
#     driver.find_element(by=By.ID, value="start").click()

#     while True:
#         try:
#             # get the recognized text from HTML output element
#             text = driver.find_element(by=By.ID, value="output").text

#             if text:
#                 # stop recognition by clicking the stop button
#                 driver.find_element(by=By.ID, value="end").click()

#                 # if the input language is English, return the modified query
#                 if input_language.lower() == "en" or "en" in input_language.lower():
#                     return query_modifier(text)
#                 else:
#                     set_assistant_status("Translating...")
#                     return query_modifier(universal_translator(text))

#         except Exception as e:
#             pass


# # main execuion block
# if __name__ == "__main__":
#     while True:
#         # continuously perform speech recognition and print the recognized text
#         text = speech_recognition()
#         print(text)


from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from dotenv import dotenv_values
import os
import mtranslate as mt

# Load environment variables from .env file
env_vars = dotenv_values(".env")

# Get input language setting from the environment variable
input_language = env_vars.get("InputLanguage", "en")

# Define HTML code for speech recognition interface
HtmlCode = """<!DOCTYPE html>
<html lang="en">
<head>
    <title>Speech Recognition</title>
</head>
<body>
    <button id="start" onclick="startRecognition()">Start Recognition</button>
    <button id="end" onclick="stopRecognition()">Stop Recognition</button>
    <p id="output"></p>
    <script>
        const output = document.getElementById('output');
        let recognition;

        function startRecognition() {
            recognition = new webkitSpeechRecognition() || new SpeechRecognition();
            recognition.lang = '';
            recognition.continuous = true;

            recognition.onresult = function(event) {
                const transcript = event.results[event.results.length - 1][0].transcript;
                output.textContent += transcript;
            };

            recognition.onend = function() {
                recognition.start();
            };
            recognition.start();
        }

        function stopRecognition() {
            if (recognition) {
                recognition.stop();
                output.innerHTML = "";
            }
        }
    </script>
</body>
</html>"""

# Replace the language setting in the HTML code with input language from env
HtmlCode = str(HtmlCode).replace(
    "recognition.lang = '';", f"recognition.lang = '{input_language}';"
)

# Create Data directory if it doesn't exist
os.makedirs("Data", exist_ok=True)

# write the modified code to a file
with open(r"Data\Voice.html", "w") as f:
    f.write(HtmlCode)

# Get current working directory
curr_dir = os.getcwd()

# Generate file path for HTML file - Fix path separator for cross-platform compatibility
Link = os.path.join(curr_dir, "Data", "Voice.html")

# Set Chrome options for the WebDriver.
chrome_options = Options()
user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.142.86 Safari/537.36"
chrome_options.add_argument(f"user-agent={user_agent}")
chrome_options.add_argument("--use-fake-ui-for-media-stream")
chrome_options.add_argument("--use-fake-device-for-media-stream")
chrome_options.add_argument("--headless=new")

# Initialize the Chrome WebDriver using the ChromeDriverManager.
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=chrome_options)

# Define the path for temporary files with proper path handling
TempDirPath = os.path.join(curr_dir, "frontend", "Files")

# Ensure the temp directory exists
os.makedirs(TempDirPath, exist_ok=True)


# Function to set the assistant's status by writing it to a file.
def set_assistant_status(status):
    status_file = os.path.join(TempDirPath, "Status.data")
    with open(status_file, "w", encoding="utf-8") as file:
        file.write(status)


def query_modifier(query):
    if not query.strip():  # Handle empty input
        return ""

    new_query = query.lower().strip()
    query_words = new_query.split()

    if not query_words:  # Handle case where split results in empty list
        return ""

    question_words = {
        "how",
        "what",
        "who",
        "when",
        "where",
        "why",
        "which",
        "whose",
        "whom",
        "can",
        "what's",
        "where's",
        "how's",
    }

    auxiliary_verbs = {
        "is",
        "are",
        "am",
        "was",
        "were",
        "do",
        "does",
        "did",
        "can",
        "could",
        "will",
        "would",
        "shall",
        "should",
        "may",
        "might",
        "must",
        "have",
        "has",
        "had",
    }

    # Check if the first word suggests a question
    is_question = query_words[0] in question_words or query_words[0] in auxiliary_verbs

    # Ensure proper punctuation at the end
    if new_query and new_query[-1] in [".", "?", "!"]:
        new_query = new_query[:-1]  # Remove existing punctuation

    new_query += "?" if is_question else "."

    return new_query.capitalize()


def universal_translator(text):
    try:
        english_translation = mt.translate(text, "en", "auto")
        return english_translation.capitalize()
    except Exception as e:
        print(f"Translation error: {e}")
        return text.capitalize()  # Return original text if translation fails


# Function to translate text into English using mtranslate Library
def speech_recognition():
    try:
        # open the HTML file in browser
        driver.get("file:///" + Link.replace("\\", "/"))  # Ensure proper URL format

        # start speech recognition by clicking the start button
        driver.find_element(by=By.ID, value="start").click()

        while True:
            try:
                # get the recognized text from HTML output element
                text = driver.find_element(by=By.ID, value="output").text

                if text:
                    # stop recognition by clicking the stop button
                    driver.find_element(by=By.ID, value="end").click()

                    # if the input language is English, return the modified query
                    if input_language.lower() == "en" or "en" in input_language.lower():
                        return query_modifier(text)
                    else:
                        set_assistant_status("Translating...")
                        return query_modifier(universal_translator(text))

            except Exception as e:
                print(f"Recognition loop error: {e}")
                # Small delay to prevent high CPU usage
                import time

                time.sleep(0.1)

    except Exception as e:
        print(f"Speech recognition error: {e}")
        return "Error in speech recognition."


# Main execution block
if __name__ == "__main__":
    try:
        while True:
            # continuously perform speech recognition and print the recognized text
            text = speech_recognition()
            if text:  # Only print non-empty text
                print(text)
    except KeyboardInterrupt:
        # Clean up resources when the program is interrupted
        driver.quit()
        print("Speech recognition terminated.")
    except Exception as e:
        print(f"Main loop error: {e}")
        driver.quit()
