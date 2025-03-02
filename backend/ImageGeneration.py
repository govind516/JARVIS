import asyncio
from random import randint
from PIL import Image
import requests
from time import sleep
import os
from dotenv import dotenv_values

env_vars = dotenv_values(".env")
HuggingFaceAPIKey = env_vars.get("HuggingFaceAPIKey")

if not HuggingFaceAPIKey:
    raise ValueError("Hugging Face API key not found. Make sure it's set in .env.")


# Function to open and display images based on given prompt
def open_images(prompt):
    folder_path = r"Data"
    prompt = prompt.replace(" ", "_")

    files = [f"{prompt}{i}.jpg" for i in range(1, 5)]

    for jpg_file in files:
        image_path = os.path.join(folder_path, jpg_file)

        try:
            img = Image.open(image_path)
            print(f"Opening image: {image_path}")
            img.show()
            sleep(1)
        except IOError:
            print(f"Error opening image: {image_path}")


# API details for Hugging Face stable diffusion model
API_URL = "https://api-inference.huggingface.co/models/stabilityai/stable-diffusion-xl-base-1.0"
headers = {"Authorization": f"Bearer {HuggingFaceAPIKey}"}


# Async function to send a query to the Hugging Face API
async def query(payload):
    response = await asyncio.to_thread(
        requests.post, API_URL, headers=headers, json=payload
    )
    return response.content


# Async function to generate images based on the given prompt
async def generate_images_async(prompt: str):
    tasks = []

    # Create 4 image generation tasks
    for _ in range(4):
        payload = {
            "inputs": f"{prompt}, quality=4K, sharpness=maximum, Ultra High details, high resolution, seed = {randint(0, 1000000)}"
        }

        task = asyncio.create_task(query(payload))
        tasks.append(task)

    # Wait for all tasks to complete
    image_bytes_list = await asyncio.gather(*tasks)

    # save the generated images to files
    for i, image_bytes in enumerate(image_bytes_list):
        with open(rf"Data\{prompt.replace(' ','_')}{i+1}.jpg", "wb") as f:
            f.write(image_bytes)


# Wrapper function to generate and open images
def generate_images(prompt: str):
    asyncio.run(generate_images_async(prompt))
    open_images(prompt)
    return True


# Main loop to monitor for image generation requests
while True:
    try:
        # Read the status and prompt from the data file
        with open(r"frontend\Files\ImageGeneration.data", "r") as f:
            data: str = f.read()

        prompt, status = data.split(",")

        if status == "True":
            print("Generating Images ...")
            image_status = generate_images(prompt=prompt)

            # reset status in file after generating images
            with open(r"frontend\Files\ImageGeneration.data", "w") as f:
                f.write(f"{prompt},False")

        else:
            sleep(1)

    except Exception as e:
        pass
