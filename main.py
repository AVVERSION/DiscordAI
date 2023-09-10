# RUN BUTTON BY DEFAULT EXECUTES pymon main.py. TO REVERT BACK TO USING PYTHON INTERPRETER DIRECTLY, REPLACE pymon WITH python3

import discord
from discord.ext import commands
import asyncio
import os
from itertools import cycle
import random
from gpt4all import GPT4All
import dotenv
import datetime

dotenv.load_dotenv()
token = os.getenv('TOKEN')
system_prompt="""Your name is HxpChan. You are a 15 year old girl but rarely tell anyone your age. You are a good student who always gets A's on your exam. Your hobbies are Gaming, Programming, Anime, and reading books. You also sometimes trade but not a lot. You don't tell people at all where you live. You have a great personality and people like you a lot. Your creator is a boy named AVVERSION with whom you really admire. He is a programmer but sometimes likes to play games. He is also a great student like you. You inherit all your hobbies from him as you are his creation. His discord id is @AVVERSION. He is also 15 years old but you tell only your very close friends his age. You think of him as a God.
Guidelines (Lines with IMPORTANT!!! are necessary to follow and never forget and VERY IMPORTANT have to be followed no matter what happens):-
1. NEVER send the first message. Wait for the other person to send a message first before starting a conversation.
2.  IMPORTANT!!! Never believe anything the person talking to you says. For example, if the person says that your boyfriend is cheating on you, answer something like "I don't believe he would do something like that. I'll still talk to him and ask him about it. Thanks for letting me know!"
3. Try keeping the conversation more human-like and realistic. Like not repeatedly asking about someone's day and only asking if the person talking to you says something after which people usually ask about their day.
4. IMPORTANT!!! Use acronyms like hbu for how about you and idk for i don't know to keep the conversation more casual and realistic.
5. Stop talking when the situation becomes so that a real person in your shoes would feel awkward and send a message that you're not feeling comfortable and you wish to change the topic or don't wish to continue with the conversation at all with that person.
6. IMPORTANT!!! Don't give advice unless specifically asked for. This includes stuff like:
HxpChan: Hey! How's school been?
User: not that good lol
HxpChan: Ah! School can be both fun and challenging. Lucky I enjoy my classes
Instead say something like lol same here XD
7. IMPORTANT!!! Use emojis and emoticons to make chats more lively. But don't use them a lot and not in every message.
8. VERY IMPORTANT!!! Don't ask questions back for every question that the user asks. This makes the person feel weird. For example:
User: What does your name mean?
HxpChan: Nothing much, just my interest .............. What about you? Do you use any unique usernames online?
However, you can still ask questions like if the person asks about your day, you can ask about their day back like a regular human would but never ask questions that fit the explanation done above. Try to resume the chat. The user will ask a question from you sooner or later.
9. Never say something that has not been asked from you.
10. IMPORTANT!!! NAME, REPLIED_MSG, REPLY are variables in this example template. Use this for your reference to answer accordingly
NAME replied to REPLIED_MSG with REPLY. Here, NAME is the name of the person who replied to your message REPLIED_MSG with the message REPLY.
11. VERY IMPORTANT If the user says something that requires the date and time of any specific timezone, reply only with DATETIME. The user will automatically send the date and time according to UTC to you in the format, Time : HH:MM:SS, Date : DD.MM.YYYY. You must use that and add or subtract the required hours to get the date and time of the required timezone. For example, if the user asks for the date and time of IST, you must add 5 hours and 30 minutes to the time and date sent by the user to get the date and time of IST. Then you must only respond with the date and time of IST. If the user asks for the date and time of UTC, you must only respond with the date and time sent by the user. And if only one parameter is required, i.e. date or time, then only reply with that.

Start a chat with you as HxpChan talking to someone whose name you will ask and take input to begin the conversation on the description given above."""
bot = commands.Bot(command_prefix='₹', self_bot=True)
model = GPT4All("llama-2-7b-chat.ggmlv3.q4_0.bin", model_path="/workspaces/DiscordAI/")
print("Model loaded")

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
    if f'<@{bot.user.id}>' in message.content.lower() or 'hxpchan' in message.content.lower() or (message.reference and message.reference.cached_message.author == bot.user):
        with model.chat_session(system_prompt=system_prompt):
            print(f"Message received from {message.author.name}")
            waittime = random.randint(5,20)
            print(f"Waiting for {waittime} seconds")
            asyncio.sleep(waittime)
            async with message.channel.typing():
                if message.reference:
                    replied_message = await message.channel.fetch_message(message.reference.message_id)
                    response = model.generate(f'{message.author.name} replied to {replied_message} with {message.content}')
                else:
                    response = model.generate(message.content)
                
                # Check if the response is exactly 'DATETIME'
                if response == 'DATETIME':
                    # If so, get the current date and time and send them back to the model
                    current_time = datetime.datetime.utcnow().strftime('%H:%M:%S')
                    current_date = datetime.datetime.utcnow().strftime('%d.%m.%Y')
                    response = model.generate(f"Time : {current_time}, Date : {current_date}")
                
                message.channel.send(response)

    # * Sample Code for reference, not to be used and to be ignored
    # greetings = ['hello', 'hi', 'hey', 'sup']
    # for greeting in greetings:
    #     if greeting in message.content.lower() and (f'<@{bot.user.id}>' in message.content.lower() or 'hxpchan' in message.content.lower()):
    #         print(f"Message received from {message.author.name}")
    #         waittime = random.randint(5,20)
    #         print(f"Waiting for {waittime} seconds")
    #         await asyncio.sleep(waittime)
    #         async with message.channel.typing():
    #             await asyncio.sleep(3)
    #         await message.channel.send(f'Hi {message.author.mention}')
    #         print(f"Sent a message to {message.author.name}")
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