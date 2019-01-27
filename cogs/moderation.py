import discord
import datetime
import asyncio
import json
import random

from discord.ext import commands
from random import randint
from datetime import datetime

seconds_in_unit = {"s": 1, "m": 60, "h": 3600, "d": 86400, "w": 604800} # Gives us the seconds per unit used for timed mutes.
def convertToSeconds(timeduration):
    return int(timeduration[:-1]) * seconds_in_unit[timeduration[-1]]

client = discord.Client()

class Moderation(object):
    def __init__(self, bot):
        self.bot = bot

    # Mute command
    @commands.command(pass_context=True)
    @commands.has_permissions(manage_roles=True)
    async def mute(self, ctx, user: discord.Member, timeduration, *, reason="No reason specified"):
        # Specify  what role your adding. In this case its the muted role since we're muting/unmuting the user
        role = discord.utils.get(user.server.roles, name = "Muted")
        # Send it to the logs
        log_channel = discord.utils.get(ctx.message.server.channels, name = 'public-mod-logs')
        userID = (user.id)
        embed = discord.Embed(title="Member Muted", color = 0xB760F3)
        embed.add_field(name="Member", value="{} ".format(user) + "(<@{}>)".format(userID), inline=True)
        embed.add_field(name="Mod", value="{}".format(ctx.message.author), inline=True)
        embed.add_field(name="Duration", value=timeduration, inline=True)
        embed.add_field(name="Reason", value="{}".format(reason), inline=True)
        embed.set_thumbnail(url=user.avatar_url)
        await self.bot.send_message(log_channel, embed=embed)
        #await self.bot.send_message(ctx.message.channel, embed=embed)
        await self.bot.add_roles(user, role)
        print("muted")
        await self.bot.delete_message(ctx.message)

        theTime = convertToSeconds("{}".format(timeduration)) #convert our time argument to seconds
        print(theTime)
        await asyncio.sleep(int(theTime)) # pass the seconds to asyncio.sleep
        try:
            await self.bot.remove_roles(user, role)
            print("unmuted")
        except:
            pass

    @mute.error
    async def mute_error(self, error, ctx):
        if isinstance(error, discord.ext.commands.BadArgument):
            userID = (ctx.message.author.id)
            botMessage = await self.bot.send_message(ctx.message.channel,"<@%s>: **Sorry, I couldn't find this user**" % (userID))
            await self.bot.delete_message(ctx.message)        
            await asyncio.sleep(5)
            try:
                await self.bot.delete_message(botMessage)
            except:
                pass
        
        elif isinstance(error, discord.ext.commands.MissingRequiredArgument):
            userID = (ctx.message.author.id)
            await self.bot.send_message(ctx.message.author,"<@%s>: **Missing Required Argument.** Ex:```!mute @user 2h```" % (userID))
            await self.bot.delete_message(ctx.message)
        elif isinstance(error, discord.ext.commands.CheckFailure):
            userID = (ctx.message.author.id)
            await self.bot.send_message(ctx.message.author,"<@%s>: **You don't have permission to perform this action**" % (userID))
            await self.bot.delete_message(ctx.message)

    # Unmute command
    @commands.command(pass_context=True)
    @commands.has_permissions(manage_roles=True)
    async def unmute(self, ctx, user: discord.Member):
        # Specify  what role you're removing. In this case its the muted role since we're unmuting the user
        role = discord.utils.get(user.server.roles, name = "Muted")
        # Send it to the logs
        log_channel = discord.utils.get(ctx.message.server.channels, name = 'public-mod-logs')
        userID = (user.id)
        embed = discord.Embed(title="Member Unmuted", color = 0x563F65)
        embed.add_field(name="Member", value="{} ".format(user) + "(<@{}>)".format(userID), inline=True)
        embed.add_field(name="Mod", value="{}".format(ctx.message.author), inline=True)
        embed.set_thumbnail(url=user.avatar_url)

        await self.bot.send_message(log_channel, embed=embed)
        #await self.bot.send_message(ctx.message.channel, embed=embed)
        await self.bot.remove_roles(user, role)
        await self.bot.delete_message(ctx.message)

    @unmute.error
    async def unmute_error(self, error, ctx):
        if isinstance(error, discord.ext.commands.BadArgument):
            userID = (ctx.message.author.id)
            botMessage = await self.bot.send_message(ctx.message.channel,"<@%s>: **Sorry, I couldn't find this user**" % (userID))
            await self.bot.delete_message(ctx.message)        
            await asyncio.sleep(5)
            try:
                await self.bot.delete_message(botMessage)
            except:
                pass
        
        elif isinstance(error, discord.ext.commands.CheckFailure):
            userID = (ctx.message.author.id)
            await self.bot.send_message(ctx.message.author,"<@%s>: **You don't have permission to perform this action**" % (userID))
            await self.bot.delete_message(ctx.message)

    @commands.command(pass_context=True)
    @commands.has_permissions(ban_members=True)
    async def info(self, ctx, user: discord.Member):
        embed = discord.Embed(title="{}'s Info".format(user.name), description="Here's what I found.", color=0x00cda1)
        embed.add_field(name="Username", value=user, inline=True)
        embed.add_field(name="ID", value=user.id, inline=True)
        embed.add_field(name="Status", value=user.status, inline=True)
        embed.add_field(name="Highest Role", value=user.top_role)

        userMade = user.created_at
        userMade2 = userMade.strftime("%B %d, %Y %I:%M %p")
        embed.add_field(name="Created", value="{}".format(userMade2))

        userJoin = user.joined_at
        userJoin2 = userJoin.strftime("%B %d, %Y %I:%M %p")
        embed.add_field(name="Joined", value="{}".format(userJoin2))

        embed.set_thumbnail(url=user.avatar_url)
        embed.set_footer(text="Requested by {}".format(ctx.message.author))
        embed.timestamp = datetime.utcnow()
        await self.bot.say(embed=embed)
        print("User's info requested")
        await self.bot.delete_message(ctx.message)


    @info.error
    async def info_error(self, error, ctx):
        if isinstance(error, discord.ext.commands.BadArgument):
            userID = (ctx.message.author.id)
            botMessage = await self.bot.send_message(ctx.message.channel,"<@%s>: **Sorry, I couldn't find this user**" % (userID))
            await self.bot.delete_message(ctx.message)        
            await asyncio.sleep(5)
            try:
                await self.bot.delete_message(botMessage)
            except:
                pass
        
        elif isinstance(error, discord.ext.commands.CheckFailure):
            userID = (ctx.message.author.id)
            await self.bot.send_message(ctx.message.author,"<@%s>: **You don't have permission to perform this action**" % (userID))
            await self.bot.delete_message(ctx.message)




    @commands.command(pass_context=True)
    @commands.has_permissions(ban_members=True) 
    async def ban(self, ctx, user: discord.Member, *, reason: str = "No reason specified"):
        log_channel = discord.utils.get(ctx.message.server.channels, name = 'public-mod-logs')
        userID = (user.id) 
        embed = discord.Embed(title="Member Banned", color = 0xD82626)
        embed.add_field(name="Member", value="{} ".format(user) + "(<@{}>)".format(userID), inline=True)
        embed.add_field(name="Mod", value="{}".format(ctx.message.author), inline=True)
        embed.add_field(name="Reason", value="{}".format(reason), inline=False)
        embed.set_thumbnail(url=user.avatar_url)
        embed.timestamp = datetime.utcnow()

        #await self.bot.send_message(discord.Object(id=log_channel), embed=embed)
        await self.bot.send_message(log_channel, embed=embed)
        await self.bot.ban(user)
        await self.bot.delete_message(ctx.message)
    
    @ban.error
    async def ban_error(self, error, ctx):
        if isinstance(error, discord.ext.commands.BadArgument):
            userID = (ctx.message.author.id)
            botMessage = await self.bot.send_message(ctx.message.channel,"<@%s>: **Sorry, I couldn't find this user**" % (userID))
            await self.bot.delete_message(ctx.message)        
            await asyncio.sleep(5)
            try:
                await self.bot.delete_message(botMessage)
            except:
                pass
        
        elif isinstance(error, discord.ext.commands.CheckFailure): # Message to the user if they don't have perms
            userID = (ctx.message.author.id)
            await self.bot.send_message(ctx.message.author,"<@%s>: **You don't have permission to perform this action**" % (userID))
            await self.bot.delete_message(ctx.message)


    @commands.command(pass_context=True, aliases=["rule"])
    @commands.has_permissions(ban_members=True)
    async def addrule(self, ctx, ruleN, *, ruleT):
        r = randint(0, 0xFFFFFF)

        rule_channel = discord.utils.get(ctx.message.server.channels, name = 'rules')
        embed = discord.Embed(title = "Rule #{}".format(ruleN), description="{}".format(ruleT), colour=discord.Colour(r))
        await self.bot.send_message(rule_channel, embed=embed)
        await self.bot.delete_message(ctx.message)
            
    @addrule.error
    async def addrule_error(self, error, ctx):
        if isinstance(error, discord.ext.commands.MissingRequiredArgument):
            userID = (ctx.message.author.id)
            await self.bot.send_message(ctx.message.author,"<@%s>: **Missing Required Argument.** Ex:```!addrule 1 The text goes here```" % (userID))
            await self.bot.delete_message(ctx.message)





def setup(bot):
    bot.add_cog(Moderation(bot))