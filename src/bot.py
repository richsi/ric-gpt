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
# client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print(f"We have logged in as {client.user}")

def generate_prompt(animal):
    return """Suggest animes to watch based on genre.
Animal: Action
Names: Jujustsu Kaisen
Animal: Slice of life
Names: Your Lie in April
Animal: {}
Names:""".format(
        animal.capitalize()
    )

async def generate_response(message):
    # prompt = f"{message.author.name}: {message.content}\nAI:"
    prompt = generate_prompt(str(message.content))
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        # messages = [
        #     {"role": "system", "content": "You are a helpful assistant."},
        #     {"role": "user", "content": "Who won the world series in 2020?"},
        #     {"role": "assistant", "content": "The Los Angeles Dodgers won the World Series in 2020."},
        #     {"role": "user", "content": "Where was it played?"}
        # ],
        messages = [{"role": "user", "content": str(message.content)}],
        # prompt=prompt,
        max_tokens=1024,
        n=1,
        stop=None,
        temperature=1,
    )
    completion_tokens = response['usage']['completion_tokens']
    prompt_tokens= response['usage']['prompt_tokens']
    total_tokens = response['usage']['total_tokens']
    cost = response['usage']['total_tokens'] * 0.0015
    final_response = "Generated with gpt-3.5-turbo: %s\n %s + %s = %s tokens used ($%s)" % (response.choices[0].message.content.strip(), 
                                                                                            str(completion_tokens), str(prompt_tokens), 
                                                                                            str(total_tokens), 
                                                                                            str(cost))

    return final_response

@client.command(name='chat')
async def chat(ctx):
    # if message.author == client.user:
    #     return
    response = await generate_response(ctx.message)
    await ctx.channel.send(response)

client.run(DISCORD_TOKEN)