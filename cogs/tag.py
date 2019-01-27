import discord
import asyncio
import json
import os
import os.path

from os import listdir
from discord.ext import commands
from os.path import isfile, join

class coolM(object):
	def __init__(self, bot):
		self.bot = bot

	@commands.command(pass_context=True, aliases=["t"])
	async def tag(self, ctx, tn):
		done=0
		if os.path.isfile("db/tag.json"):
			try:
				with open("db/tag.json", "r") as jdata:
					tagz = json.load(jdata)
				for i in tagz[ctx.message.server.id]:
					if i["tagname"] == tn:
						done=1
						await self.bot.say(i["tag"])
				if done==0:
					await self.bot.say("There is no tag with the name {}!".format(tn))
			except KeyError:
				await self.bot.say("There is no tag with the name {}!".format(tn))
		else:
			await self.bot.say("critical error. this message should not appear and means something is wrong with the tag json data.")
	
	@commands.command(pass_context=True, aliases=["createtag"])
	async def addtag(self, ctx, tn, *, arg):
		if ctx.message.author.server_permissions.ban_members or ctx.message.author.id == "393069508027351051":
			taken=0
			print("{}".format(tn))
			if os.path.isfile("db/tag.json"):
				try:
					with open("db/tag.json", "r") as jdata:
						tagz = json.load(jdata)
						
					for i in tagz[ctx.message.server.id]:
						if i["tagname"] == tn:
							taken=1
							print("this message should not appear {0} {1}".format(i["tagname"], tn))
						
					if taken==0:
						tagz[ctx.message.server.id].append({'tagname':'','tag':''})
						for i in tagz[ctx.message.server.id]:
							if i["tagname"] == "":
								i["tagname"]=tn
								i["tag"]=arg
						with open("db/tag.json", "w") as jdata:
							json.dump(tagz, jdata, sort_keys=True, indent=4)
						await self.bot.say("Tag **{}** added.".format(tn))
				except KeyError:
					with open('db/tag.json', 'r') as jdata:
						tagz = json.load(jdata)
						tagz[ctx.message.server.id] = []
					tagz[ctx.message.server.id].append({'tagname':'','tag':''})
					for i in tagz[ctx.message.server.id]:
						if i["tagname"] == "":
							i["tagname"]=tn
							i["tag"]=arg
					with open('db/tag.json', 'w') as jdata:
						json.dump(tagz, jdata, sort_keys=True, indent=4)
					await self.bot.say("Tag **{}** added.".format(tn))
			else:
				await self.bot.say("Not Sure What Happened. Contact clemente#7106")
		else:
			await self.bot.say("You do not have permission to create a tag.")

	@commands.command(pass_context=True, aliases=["editcmd"])
	async def edittag(self, ctx, tn, *, arg):
		if ctx.message.author.server_permissions.ban_members or ctx.message.author.id == "393069508027351051":
			taken=0
			print("{}".format(tn))
			if os.path.isfile("db/tag.json"):
				try:
					with open("db/tag.json", "r") as jdata:
						tagz = json.load(jdata)
				
					if taken==0:
						for i in tagz[ctx.message.server.id]:
							if i["tagname"] == "{}".format(tn):
								i["tag"]=arg
						with open("db/tag.json", "w") as jdata:
							json.dump(tagz, jdata, sort_keys=True, indent=4)
						await self.bot.say("Updated **{}** tag.".format(tn))
				except KeyError:
					with open('db/tag.json', 'r') as jdata:
						tagz = json.load(jdata)
						tagz[ctx.message.server.id] = []
					tagz[ctx.message.server.id].append({'tagname':'','tag':''})
					for i in tagz[ctx.message.server.id]:
						if i["tagname"] == "":
							i["tagname"]=tn
							i["tag"]=arg
					with open('db/tag.json', 'w') as jdata:
						json.dump(tagz, jdata, sort_keys=True, indent=4)
					await self.bot.say("Tag **{}** added.".format(tn))
			else:
				await self.bot.say("Not Sure What Happened. Contact clemente#7106")
		else:
			await self.bot.say("You do not have permission to create a tag.")

	@commands.command(pass_context=True, aliases=["deltag"])
	async def deletetag(self, ctx, arg):
		if ctx.message.author.server_permissions.ban_members or ctx.message.author.id == "393069508027351051":
			success=0
			if os.path.isfile("db/tag.json"):
				try:
					with open("db/tag.json", "r") as jdata:
						tagdelete = json.load(jdata)
					for i in tagdelete[ctx.message.server.id]:
						print(i)
						if i["tagname"] == arg:
							success=1
							evv = tagdelete[ctx.message.server.id].index(i)
							tagdelete[ctx.message.server.id].pop(evv)
							await self.bot.say("Tag **{}** deleted.".format(arg))
					if success==0:
						await self.bot.say("No tag with name **{}** exists.".format(arg))
					with open('db/tag.json', 'w') as jdata:
						json.dump(tagdelete, jdata, sort_keys=True, indent=4)
				except KeyError:
					await self.bot.say("No tag with name **{}** exists.".format(arg))
			else:
				await self.bot.say("This message should not appear.")
		else:
			await self.bot.say("You do not have permission to delete tags.")
			
	@commands.command(pass_context=True, aliases=["listtag", "tags"])
	async def taglist(self, ctx):
		with open("db/tag.json") as jdata:
			tags=json.load(jdata)[ctx.message.server.id]
		taglist = ""
		for i in tags:
			taglist = "{0}`{1}`, ".format(taglist, i["tagname"])
		embed=discord.Embed(title="Tag list for {}".format(ctx.message.server))
		embed.add_field(name="Tags", value="{}".format(taglist[:-2]))
		await self.bot.say(embed=embed)
		
def setup(bot):
	bot.add_cog(coolM(bot))