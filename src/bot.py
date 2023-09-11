import os
import openai
import discord
from dotenv import load_dotenv
from discord.ext import commands

load_dotenv()

BOT_PREFIX = "!"
DISCORD_TOKEN = os.getenv("DISCORD_API_KEY")
openai.api_key = os.getenv("OPENAI_API_KEY")

#Specify intent
intents = discord.Intents.default()
intents.members = True

#Create client
client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print(f"We have logged in as {client.user}")

# @client.command(name = "chat")
# async def chat(message):




client.run(DISCORD_TOKEN)