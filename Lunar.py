import os
import openai
import asyncio
import googletrans
import rasa
from discord.ext import commands
from googletrans import Translator
from rasa.engine import loader
from rasa.engine.storage import ModelStorage

# Setup OpenAI API credentials
openai.api_key = "API_KEY_HERE"
bot_name = "INPUT_BOT_NAME_HERE"

# Setup translation API credentials
translator = Translator(service_urls=['translate.google.com'])

# Language detection API
from langdetect import detect

# Setup discord bot
client = commands.Bot(command_prefix="!")

# Load Rasa NLU model
model_path = "./models/nlu"
model_storage = ModelStorage.local(model_path)
trained_model = loader.load(model_storage)

# Create interpreter
interpreter = trained_model.interpreter

# Function to detect the language of the text
def detect_lang(text):
    try:
        return detect(text)
    except:
        return "unknown"

# Function to translate text to target language
def translate_text(text, target_lang):
    try:
        translation = translator.translate(text, dest=target_lang)
        return translation.text
    except:
        return None

# Function to generate AI response using Rasa
async def generate_response(prompt):
    try:
        result = interpreter.parse(prompt)
        intent = result["intent"]["name"]
        entities = result["entities"]
        response = await rasa.core.run.get_response(intent=intent, entities=entities)
        return response["text"]
    except Exception as e:
        print(e)
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
        # Generate a response from the AI
        response = await generate_response(message.content)

        # Send response to the channel
        await message.channel.send(response)
        return

    # Check if message is in a different language and translate it to English
    if detect_lang(message.content) != "en":
        translated_message = translate_text(message.content, "en")
        if translated_message:
            message.content = translated_message
        else:
            await message.channel.send("Sorry, I couldn't translate the message to English.")
            return

    # Generate a response from the AI
    response = await generate_response(message.content)

    # Send response to the channel
    await message.channel.send(response)

# Function to start the bot
async def on_bot_ready():
    print(f'{bot_name} is ready.')

# Command listener for /ping command
@client.command()
async def ping(ctx):
    await ctx.send('Pong!')

# Run the bot
loop = asyncio.get_event_loop()
loop.create_task(client.start("API_KEY_HERE"))
loop.run_until_complete(on_bot_ready())
loop.run_forever()
