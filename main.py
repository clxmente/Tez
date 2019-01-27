import discord
import asyncio
import requests
import os
import os.path
import traceback
import time

from discord.ext import commands
from discord.ext.commands import Bot
from os import listdir
from os.path import isfile, join

bot = commands.Bot(command_prefix='!')
bot.remove_command('help')

owners = ["393069508027351051"]

@bot.event
async def on_ready():
    print ("Launched...")
    print ("My name is " + bot.user.name)
    print ("ID: " + bot.user.id)

@bot.command(pass_context=True)
async def reload(ctx, cogToLoad = None):
    if str(ctx.message.author.id) in owners:
        if cogToLoad == None:
            # Loading
            loadingCogMessage = await bot.say("Loading Cogs")
            for extension in [f.replace('.py', "") for f in listdir("cogs") if isfile(join("cogs", f))]:
                try:
                    if not "__init__" in extension:
                        print("Reloading {}...".format(extension))
                        bot.unload_extension("cogs." + extension)
                        bot.load_extension("cogs." + extension)
                except Exception as e:
                    print("Failed to load cog {}".format(extension))
                    await bot.say("⛔️ | Failed to load cog {}".format(extension))
                    traceback.print_exc()
            await bot.edit_message(loadingCogMessage, "✅ | Cogs have been loaded successfully")

        else:
            try:
                if not "__init__" in cogToLoad:
                    print("Reloading {}...".format(cogToLoad))
                    bot.unload_extension("cogs." + cogToLoad)
                    loadingCogMessage = await bot.say("Loading {}..".format(cogToLoad))
                    bot.load_extension("cogs." + cogToLoad)
                    await bot.edit_message(loadingCogMessage, "✅ | {} has been loaded.".format(cogToLoad))
            except Exception as e:
                print("Failed to load cog {}".format(cogToLoad))
                await bot.say("⛔️ | Failed to load cog {}".format(cogToLoad))
                traceback.print_exc()

    else:
        print("Unauthorized user has attempted to reload modules.. Stopped :)")
        await bot.say("⛔️ | Bot owner only!")

@bot.command(pass_context=True)
@commands.cooldown(1, 7, commands.BucketType.user)
async def ping(ctx):
    time_then = time.monotonic()
    pinger = await bot.send_message(ctx.message.channel, 'Pong | Loading latency..')
    ping = '%.2f' % (1000*(time.monotonic()-time_then))
    embed = discord.Embed(colour=discord.Colour(0xbf99e5))

    embed.add_field(name="Aceruos Ping", value="Ping: **{}ms** ".format(ping))
    await bot.delete_message(pinger)
    await bot.say(embed=embed)
    print("Ping")
    print("--------------------")


bot.run('bot_token_here')


