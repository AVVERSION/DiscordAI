# RUN BUTTON BY DEFAULT EXECUTES pymon main.py. TO REVERT BACK TO USING PYTHON INTERPRETER DIRECTLY, REPLACE pymon WITH python3

import discord
from discord.ext import commands
import asyncio
import os
from itertools import cycle
import random

token = os.environ['TOKEN']
bot = commands.Bot(command_prefix='₹', self_bot=True)

# Define a list of statuses for the bot to cycle through
statuses = cycle([
    discord.Game(name="with your feelings"),
    discord.Game(name="with your mom"),
    discord.Game(name="with your dad"),
    discord.Game(name="with your life")
])

@bot.event
async def on_ready():
    botname = bot.user.name.capitalize()
    print("-" * 60, end="\n")
    print(f'Logged in as {botname}')
    while True:
        status = next(statuses)
        await bot.change_presence(status=discord.Status.idle, activity=status)
        await asyncio.sleep(30)

# Creating a command that listens for messages and replies with Hi and pings the person when someone says Hello while pinging the bot
@bot.event
async def on_message(message):
    greetings = ['hello', 'hi', 'hey', 'sup']
    for greeting in greetings:
        if greeting in message.content.lower() and (f'<@{bot.user.id}>' in message.content.lower() or 'hxpchan' in message.content.lower()):
            print(f"Message received from {message.author.name}")
            waittime = random.randint(5,20)
            print(f"Waiting for {waittime} seconds")
            await asyncio.sleep(waittime)
            async with message.channel.typing():
                await asyncio.sleep(3)
            await message.channel.send(f'Hi {message.author.mention}')
            print(f"Sent a message to {message.author.name}")
    await bot.process_commands(message)

# Creating command which accepts incoming friend requests after 60 seconds and Dms the person who sent the request after 8 seconds
@bot.event
async def on_friend_request(request):
    print(f"Incoming friend request from {request.user.name}")
    await asyncio.sleep(60)
    print(f"Accepting friend request from {request.user.name}")
    await request.accept()
    await asyncio.sleep(8)
    await request.user.send(f'Hi {request.user.name}!')

bot.run(token)