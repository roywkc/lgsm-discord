# Work with Python 3.6
import random
import asyncio
import aiohttp
import json
import subprocess
import discord
import time
import psutil
import configparser
from discord import Game
from discord.ext.commands import Bot

def dict_factory(cursor, row):
    d = {}
    for idx,col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d

config = configparser.RawConfigParser()
config.read('config.ini')

BOT_PREFIX = (config.get('DEFAULT','BOT_PREFIX'))
TOKEN = config.get('DEFAULT','DISCORD_TOKEN')  # Get at discordapp.com/developers/applications/me
GAMESERVER = config.get('DEFAULT','GAMESERVER')

client = Bot(command_prefix=BOT_PREFIX)

playing = []

for value in config.get('DEFAULT','PLAYING').split(','):
    playing.append(value)

allowed = []

for value in config.get('DEFAULT','ALLOWED').split(','):
    allowed.append(value)

remove_from_output = ['[K','32m','[0m', '93m', '36m', '92m', '\\x1b', '94m']

def directcommand(command):
    #if command == 'details':
    #    command = 'postdetails'

    #elif command == 'update':
    #    command = 'force-update'

    try:
        print('inside directcommand')
        output = subprocess.run('/home/'+GAMESERVER+'/'+GAMESERVER+' "'+command+'"', shell=True,stdout=subprocess.PIPE,universal_newlines=True)
        output = str(output.stdout)
        for t in remove_from_output:
            output = output.replace(t,'')
        return output
    except expression as identifier:
        return "Command encountered an error."

def is_command(m):
    return m.content.startswith(BOT_PREFIX)


@client.command(pass_context=True, name="start")
async def start_command(context):
    if str(context.message.channel) in allowed:
        await context.send("Starting.. this may take a minute or two..")
        print('Content: ['+str(context.message.content[1:])+'] Author: ['+str(context.message.author)+'] Channel: ['+str(context.message.channel)+']')
        output = directcommand("start")
        await context.send(output)
    else:
        await client.say("The channel ("+str(context.message.channel)+") does not have permission to run commands. Please refrain from trying.")


@client.command(pass_context=True, name="stop")
async def stop_command(context):
    if str(context.message.channel) in allowed:
        print('Content: ['+str(context.message.content[1:])+'] Author: ['+str(context.message.author)+'] Channel: ['+str(context.message.channel)+']')
        await context.send("Stopping.. this may take a minute or two..")
        output = directcommand("stop")
        await context.send(output)
    else:
        await client.say("The channel ("+str(context.message.channel)+") does not have permission to run commands. Please refrain from trying.")

@client.command()
async def restart(context):
    if str(context.message.channel) in allowed:
        print('Content: ['+str(context.message.content[1:])+'] Author: ['+str(context.message.author)+'] Channel: ['+str(context.message.channel)+']') 
        await context.send("Restarting.. this may take a minute or two..")
        output = directcommand("restart")
        await context.send(output)
    else:
        await client.say("The channel ("+str(context.message.channel)+") does not have permission to run commands. Please refrain from trying.")

@client.command()
async def details(context):
    if str(context.message.channel) in allowed:
        print('Content: ['+str(context.message.content[1:])+'] Author: ['+str(context.message.author)+'] Channel: ['+str(context.message.channel)+']')
        output = directcommand("details")
        
        await context.send(output.split("Command-line Parameters")[1]) # we pass the context so we can have all the commands in help

    else:
        await context.send("The channel ("+str(context.message.channel)+") does not have permission to run commands. Please refrain from trying.")

@client.command(pass_context=True, name="update")
async def update_command(context):
    await client.delete_message(context.message)
    if str(context.message.channel) in allowed:
        print('Content: ['+str(context.message.content[1:])+'] Author: ['+str(context.message.author)+'] Channel: ['+str(context.message.channel)+']')
        output = directcommand("update")
        await context.send(output) # we pass the context so we can have all the commands in help
    else:
        await client.say("The channel ("+str(context.message.channel)+") does not have permission to run commands. Please refrain from trying.")

@client.command()
async def botstats(context):
    process = psutil.Process()
    msg = "Bot stats\nCPU: "+str(process.cpu_percent())+"%\nRam: "+str(process.memory_percent())+"%"
    await context.send(msg)


@client.command(name="joke", pass_context=True)
async def joke(context):
    jokes = [
        "I can't wait to see the sunset in your hole",
        "Big Booties never looked the same",
        "The emporium finds your penis lacking",
        "Julian is not funny",
        "Have you met... Daniel from Talon?",
        "Khurram hangs out with dead rats",
        "Dave and Billy needs more Nords",
        "Ruben hunts for tentacles, thats why his house is on the water",
        "Put the nood in your mouth. NOW!"
            ]
    await context.send(jokes[random.randint(0,len(jokes))])


@client.event
async def on_command_error(ctx, error):
        if isinstance(error, discord.ext.commands.errors.CommandNotFound): # or discord.ext.commands.errors.CommandNotFound as you wrote
                    await ctx.send("The Raven could not understand that command")

@client.event
async def on_ready():
    print("We are connected and running as "+GAMESERVER+"!")
    print("---"+str(len(playing))+" now playing options.")
    print("---"+str(len(allowed))+" allowed channel(s)")

async def change_presence_loop():
    await client.wait_until_ready()
    await asyncio.sleep(4)
    while not client.is_closed:
        now_playing = random.choice(playing)
        print("Now Playing: "+now_playing)
        await client.change_presence(game=Game(name=now_playing))
        await asyncio.sleep(60*60) # change every hour

client.loop.create_task(change_presence_loop())
client.run(TOKEN)
