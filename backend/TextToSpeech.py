import pygame
import random
import asyncio
import edge_tts
import os
from dotenv import dotenv_values

# Load environment variables from .env file
env_vars = dotenv_values(".env")
AssistantVoice = env_vars.get("AssistantVoice")


# Asynchronous function to convert text to an audio file
async def text_to_audio(text) -> None:
    file_path = r"Data\speech.mp3"

    # check if file already exists
    if os.path.exists(file_path):
        os.remove(file_path)

    # create the communication object to generate speech
    communicate = edge_tts.Communicate(text, AssistantVoice, pitch="+5Hz", rate="+13%")
    await communicate.save(r"Data\speech.mp3")


# Function to manage text-to-speech (TTS) functionality
def tts(text, func=lambda r=None: True):
    try:
        # Convert text to audio file asynchronously
        asyncio.run(text_to_audio(text))

        # Initialize pygame mixer for audio playback
        pygame.mixer.init()

        # Load the generated speech file into pygame mixer
        pygame.mixer.music.load(r"Data\speech.mp3")
        pygame.mixer.music.play()  # play the audio

        # Loop until the audio is done playing or the function stops
        while pygame.mixer.music.get_busy():
            if func() == False:
                break

            # limit the loop to 10 ticks per second
            pygame.time.Clock().tick(10)

    except Exception as e:
        print(f"Error in TTS: {e}")

    finally:
        try:
            # call the provided function with False to signal the end of TTS
            func(False)
            pygame.mixer.music.stop()
            pygame.mixer.quit()

        except Exception as e:
            print(f"Error in finally block: {e}")


# Function to manage text-to-speech with additional responses for long text
def text_to_speech(text, func=lambda r=None: True):
    data = str(text).split(".")  # split the text by periods into a list of sentences

    responses = [
        "The rest of the result has been printed to the chat screen, kindly check it out sir.",
        "The rest of the text is now on the chat screen, sir, please check it.",
        "You can see the rest of the text on the chat screen, sir.",
        "The remaining part of the text is now on the chat screen, sir.",
        "Sir, you'll find more text on the chat screen for you to see.",
        "The rest of the answer is now on the chat screen, sir.",
        "Sir, please look at the chat screen, the rest of the answer is there.",
        "You'll find the complete answer on the chat screen, sir.",
        "The next part of the text is on the chat screen, sir.",
        "Sir, please check the chat screen for more information.",
        "There's more text on the chat screen for you, sir.",
        "Sir, take a look at the chat screen for additional text.",
        "You'll find more to read on the chat screen, sir.",
        "Sir, check the chat screen for the rest of the text.",
        "The chat screen has the rest of the text, sir.",
        "There's more to see on the chat screen, sir, please look.",
        "Sir, the chat screen holds the continuation of the text.",
        "You'll find the complete answer on the chat screen, kindly check it out sir.",
        "Please review the chat screen for the rest of the text, sir.",
        "Sir, look at the chat screen for the complete answer.",
    ]

    # If the text is very long(more than 4 sentences and 250 characters), add a response message
    if len(data) > 4 and len(text) >= 250:
        tts(" ".join(data[0:2]) + "." + random.choice(responses), func)
    # otherwise just play the whole text
    else:
        tts(text, func)


# Main execution loop
if __name__ == "__main__":
    while True:
        text_to_speech(input("Enter the text: "))


# list of voices available in Edge TTS.txt - https://gist.github.com/BettyJJ/17cbaa1de96235a7f5773b8690a20462
