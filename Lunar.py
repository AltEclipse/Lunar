import os
import openai
import asyncio
import googletrans
import requests
from bs4 import BeautifulSoup
import discord
from discord.ext import commands
from googletrans import Translator
from rasa.engine import loader
from rasa.engine.storage import ModelStorage
from langdetect import detect
import pyjokes
import rasa.core.run
from rasa.core.agent import Agent
import random

# Setup OpenAI API credentials
openai.api_key = "INPUT_BOT_TOKEN_HERE"
bot_name = "Alteclipse"

# Setup translation API credentials
translator = Translator(service_urls=['translate.google.com'])

# Load Rasa model
model_directory = "./models/nlu"
interpreter = Interpreter.load(model_directory)

# Function to detect the language of the text
def detect_lang(text):
    try:
        return detect(text)
    except Exception as e:
        print(f"Language detection failed: {e}")
        return "unknown"

# Function to translate text to target language
def translate_text(text, target_lang):
    try:
        translation = translator.translate(text, dest=target_lang)
        return translation.text
    except Exception as e:
        print(f"Translation failed: {e}")
        return None

# List of possible responses for different scenarios
greetings = ["Hey there!", "What's up?", "Hello!", "Hiya!"]
goodbyes = ["See ya later!", "Bye for now!", "Catch ya later!", "Goodbye!"]
jokes = ["Why did the tomato turn red? Because it saw the salad dressing!", 
         "Why did the coffee file a police report? It got mugged!", 
         "Why was the math book sad? Because it had too many problems."]
compliments = ["You're looking sharp today!", "Great job!", "I'm impressed!"]

# Function to generate AI response using Rasa
async def generate_response(prompt):
    try:
        # Use the interpreter to parse the user's input and extract intent and entities
        result = interpreter.parse(prompt)
        intent = result["intent"]["name"]
        entities = result["entities"]

        # Use the Rasa model to generate a response based on the extracted intent and entities
        response = await interpreter.parse(prompt)

        # Define personality responses for different intents
        if intent == "greet":
            text = random.choice(greetings)
        elif intent == "goodbye":
            text = random.choice(goodbyes)
        elif intent == "joke":
            text = random.choice(jokes)
        elif intent == "compliment":
            text = random.choice(compliments)
        else:
            text = response[0]["text"]

        return text
    except Exception as e:
        print(f"Failed to generate AI response: {e}")
        return "Sorry, I couldn't understand what you said."

# Event listener for when bot is ready
@client.event
async def on_ready():
    print(f'{bot_name} is ready.')

# Event listener for when bot receives a message
@client.event
async def on_message(message):
    # Ignore messages sent by the bot itself
    if message.author == client.user:
        return

    # Check if bot's name is mentioned in the message
    if client.user.mentioned_in(message):
        # Remove bot's name from the message and remove leading/trailing white space
        prompt = message.content.replace(f"@{bot_name}", "").strip()
        # Generate AI response using Rasa
        response = await generate_response(prompt)
        # Send the response
        await message.channel.send(response)
    elif message.content.startswith("!translate"):
        # Get the target language from the message content
        target_lang = message.content.replace("!translate", "").strip()
        # Get the text to be translated
        text_to_translate = message.content.replace("!translate", "").strip()
        # Detect the language of the text to be translated
        source_lang = detect_lang(text_to_translate)
        # Translate the text to the target language
        translated_text = translate_text(text_to_translate, target_lang)
        # Send the translated text
        await message.channel.send(f"Original ({source_lang}): {text_to_translate}\nTranslated ({target_lang}): {translated_text}")
    elif message.content.startswith("!joke"):
        # Get a joke from the PyJokes library
        joke = pyjokes.get_joke()
        # Send the joke
        await message.channel.send(joke)

# Run the bot
client.run(os.getenv("DISCORD_TOKEN"))
