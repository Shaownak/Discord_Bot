import os
import discord
import wikipedia
import datetime
import requests
import json
import random
from discord.ext import commands
import youtube_dl
from discord.ext.commands import bot
import asyncio
from random import randint
from replit import db
from keep_alive import keep_alive


os.system('chmod +777 ./ffmpeg')
os.system('./ffmpeg')

my_secret = os.environ['TOKEN']
client = discord.Client()

# sad_words = ["sad","depressed","heartbroken","sorry","unhappy","depressing","angry","cry","miserable"]

# starter_encouragement = [
#   "Cheer up!"
#   "You are the beautiful one"
#   "Hang in there"
#   "You are way better than anything"
#   "You are a great person / bot!"
# ]
def get_quote():
  response = requests.get("http://zenquotes.io/api/random")
  json_data = json.loads(response.text)
  quote = json_data[0]['q'] + "-" + json_data[0]['a']
  return(quote)


@client.event
async def on_ready():
  print('We have logged on as {0.user}'.format(client))


# def search(question):
#   search = wikipedia.summary(question, sentences = 2)
#   return search

@client.event
async def on_member_join(member):
    await member.create_dm()
    await member.dm_channel.send(
        f'Hi {member.name}, welcome to my Discord server!'
    )


# @client.event
# async def on_message(message):
#   idt = client.get_guild(my_secret)

#   if message.author == client.user:
#     return 

#   # if message.content.startswith("!play"):
#   #   song = message.replace("!play", "")
#   #   pywhatkit.playonyt(song)

#   if message.content.startswith("hi"):
#     await message.channel.send("Hello there!We need to talk.") 

#   if message.content.startswith("!How are you?"):
#     await message.channel.send("Better now that you asked.") 

#   if message.content.startswith("!Who are you?"):
#     await message.channel.send("That's a very good question which I don't know.")

#   if message.content.startswith("!users"):
#     await message.channel.send(f"# of members {idt.member_count}")

#   if message.content.startswith("!time"):
#     time = datetime.datetime.now().strftime('%I:%H %p')
#     await message.channel.send(time)




# Playing Music

client = commands.Bot(command_prefix="!")

@client.command()
async def play(ctx, url : str):
    song_there = os.path.isfile("song.mp3")
    try:
        if song_there:
            os.remove("song.mp3")
    except PermissionError:
        await ctx.send("Wait for the current playing music to end or use the 'stop' command")
        return

    voiceChannel = discord.utils.get(ctx.guild.voice_channels, name='General')
    await voiceChannel.connect()
    voice = discord.utils.get(client.voice_clients, guild=ctx.guild)

    ydl_opts = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
    }
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])
    for file in os.listdir("./"):
        if file.endswith(".mp3"):
            os.rename(file, "song.mp3")
    voice.play(discord.FFmpegPCMAudio("song.mp3"))


@client.command()
async def leave(ctx):
    voice = discord.utils.get(client.voice_clients, guild=ctx.guild)
    if voice.is_connected():
        await voice.disconnect()
    else:
        await ctx.send("The bot is not connected to a voice channel.")


@client.command()
async def pause(ctx):
    voice = discord.utils.get(client.voice_clients, guild=ctx.guild)
    if voice.is_playing():
        voice.pause()
    else:
        await ctx.send("Currently no audio is playing.")


@client.command()
async def resume(ctx):
    voice = discord.utils.get(client.voice_clients, guild=ctx.guild)
    if voice.is_paused():
        voice.resume()
    else:
        await ctx.send("The audio is not paused.")


@client.command()
async def stop(ctx):
    voice = discord.utils.get(client.voice_clients, guild=ctx.guild)
    voice.stop()


### Chat

# @client.command
# async def chat(ctx):
#   idt = client.get_guild(my_secret)

#   if ctx.author == client.user:
#     return 

#   # if message.content.startswith("!play"):
#   #   song = message.replace("!play", "")
#   #   pywhatkit.playonyt(song)

#   word = ctx.message.content.split()

#   if word == "Hi":
#     # await message.channel.send("Hello there!We need to talk.")
#     # await client.process.command("Hello there!We need to talk.") 
#     ctx.send("Hello")

#   if word == "!How are you?":
#     # ctx.send("Better now that you asked.")
#     await client.process.command("Better now that you asked.") 

#   if message.content.startswith("!Who are you?"):
#     await message.channel.send("That's a very good question which I don't know.")
#     await client.process.command("That's a very good question which I don't know.")

#   if message.content.startswith("!inspire"):
#     quote = get_quote()
#     await message.channel.send(quote)

#   if any(word in message.content for word in sad_words):
#     await massage.channel.send(random.choice(starter_encouragement))  


#   bot.process.command(message)

#   if message.content.startswith("!users"):
#     await message.channel.send(f"# of members {idt.member_count}")
#     await client.process.command(message)

#   if message.content.startswith("!time"):
#     time = datetime.datetime.now().strftime('%I:%H %p')
#     await message.channel.send(time)
#     await client.process.command(message)
# @client.command()
# async def Hi(ctx):
#   await ctx.channel.send("Hello there! We need to talk.")

# @client.command
# async def How_are_you(ctx):
#   await ctx.channel.send("Hello there! We need to talk.")

# async def Hi(ctx):
#   await ctx.channel.send("Hello there! We need to talk.")



### Wikipedia 

client.remove_command("help")

def wiki_summary(arg):
  definition = wikipedia.summary(arg, sentences=3, chars=1000, auto_suggest=True, redirect=True)
  # definition = wikipedia.summary(arg, sentences=2)
  return definition


@client.command()
async def define(ctx):
    words = ctx.message.content.split()
    important_words = words[1:]
    search = discord.Embed(title="Searching...", description=wiki_summary(important_words), colour=discord.Colour.purple())
    await ctx.send(content=None, embed=search)



### Motivation
@client.command()
async def quote(ctx):
# if message.content.startswith("!inspire"):
    quote = get_quote()
    await ctx.send(quote)


### Userss
# @client.command()
# async def users(ctx):
#   ctx.send(f"# of members {idt.member_count}")


### Time
# @client.command()
# async def time(ctx):
#    time = datetime.datetime.now().strftime('%I:%H %p')
#    ctx.send(time)

  
keep_alive()
client.run(my_secret)

