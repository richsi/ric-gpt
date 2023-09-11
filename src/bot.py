import os
import openai
import discord
from dotenv import load_dotenv
from discord.ext import commands

load_dotenv()

DISCORD_TOKEN = os.getenv("DISCORD_API_KEY")
openai.api_key = os.getenv("OPENAI_API_KEY")

#Specify intent
intents = discord.Intents.default()
intents.members = True

#Create client
client = commands.Bot(command_prefix='!', intents = discord.Intents.all())

@client.event
async def on_ready():
    print(f"We have logged in as {client.user}")

async def generate_response(message):
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages = [{"role": "user", "content": str(message.content)}],
        max_tokens=1024,
        n=1,
        stop=None,
        temperature=0.7,
    )
    completion_tokens = response['usage']['completion_tokens']
    prompt_tokens= response['usage']['prompt_tokens']
    total_tokens = response['usage']['total_tokens']
    cost = response['usage']['total_tokens'] * (0.0015 / 1000)
    final_response = "%s\n %s + %s = %s tokens used ($%s)" % (response.choices[0].message.content.strip(), 
                                                                str(prompt_tokens), 
                                                                str(completion_tokens),
                                                                str(total_tokens), 
                                                                str(cost))

    return final_response

@client.command(name='chat')
async def chat(ctx):
    response = await generate_response(ctx.message)
    await ctx.channel.send(response)

client.run(DISCORD_TOKEN)