import discord
import json
import requests
import asyncio
import aiohttp

from discord.ext import commands
from PIL import Image, ImageFont, ImageDraw

class Othercommands(object):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(pass_context=True)
    @commands.cooldown(1, 3, commands.BucketType.user)
    async def fortnite(self, ctx, platform, *, epic_name):
        url = 'https://api.fortnitetracker.com/v1/profile/{}/{}'.format(platform, epic_name)
        headers = {'TRN-Api-Key': 'api-token-here'}
        async with aiohttp.ClientSession() as session: 
            async with session.get(url, headers=headers) as resp:
                req = await resp.json()
        #req = requests.get(url, headers=headers).json() |||| outdated method that blocks event loops? or something? exo told me to change so thx exo
        """with open('api/fortniteapi.json', 'w') as fp:
            json.dump(req, fp, sort_keys=True, indent=4)""" # write to json file
        try:
            image = Image.open("StatsBOT.png") # the template file for the image it creates
            draw = ImageDraw.Draw(image)
            fnt = ImageFont.truetype('/home/solorioeclem164/.local/share/fonts/Evogria_Italic.otf', size=24) # path to font file. I created this to work on Google Cloud VM so your path would be different.
            draw.text(xy=(581,27), text=epic_name, fill=(0,0,0), font=fnt)        

            solo = req["stats"]["p2"]
            soloMatches = int(solo["matches"]["value"])
            soloFM = "{:,}".format(soloMatches)
            soloWins = solo["top1"]["value"]
            fSoloW = int(soloWins)
            fSoloRW = "{:,}".format(fSoloW)
            soloKills = int(solo["kills"]["value"])
            soloKillsFM = "{:,}".format(soloKills)
            soloKD = solo["kd"]["value"]
            soloKPG = solo["kpg"]["value"]
            soloWinP = solo["winRatio"]["value"]
            soloRank = solo["trnRating"]["rank"]
            fRankSoloR = int(soloRank)
            fRankSoloRN = "{:,}".format(fRankSoloR)

            draw.text(xy=(189,283), text=soloFM, fill=(255,255,255), font=fnt)
            draw.text(xy=(62,408), text=fSoloRW, fill=(255,255,255), font=fnt)
            draw.text(xy=(62,525), text=soloKillsFM, fill=(255,255,255), font=fnt)
            draw.text(xy=(62,635), text=soloKPG, fill=(255,255,255), font=fnt) 
            draw.text(xy=(238,408), text=soloWinP, fill=(255,255,255), font=fnt)
            draw.text(xy=(238,525), text=soloKD, fill=(255,255,255), font=fnt) 
            draw.text(xy=(238,635), text=fRankSoloRN, fill=(255,255,255), font=fnt)


            duo = req["stats"]["p10"]
            duoMatches = int(duo["matches"]["value"])
            duoMatchesFM = "{:,}".format(duoMatches)
            duoWins = int(duo["top1"]["value"])
            duoWinsFM = "{:,}".format(duoWins)
            duoKills = int(duo["kills"]["value"])
            duoKillsFM= "{:,}".format(duoKills)
            duoKD = duo["kd"]["value"]
            duoKPG = duo["kpg"]["value"]
            duoWinP = duo["winRatio"]["value"]
            duoRank = int(duo["trnRating"]["rank"])
            duoRankFM = "{:,}".format(duoRank)

            draw.text(xy=(630,283), text=duoMatchesFM, fill=(255,255,255), font=fnt)
            draw.text(xy=(503,408), text=duoWinsFM, fill=(255,255,255), font=fnt)
            draw.text(xy=(503,525), text=duoKillsFM, fill=(255,255,255), font=fnt)
            draw.text(xy=(503,635), text=duoKPG, fill=(255,255,255), font=fnt) 
            draw.text(xy=(679,408), text=duoWinP, fill=(255,255,255), font=fnt)
            draw.text(xy=(679,525), text=duoKD, fill=(255,255,255), font=fnt) 
            draw.text(xy=(679,635), text=duoRankFM, fill=(255,255,255), font=fnt)

            squad = req["stats"]["p9"]
            squadMatches = int(squad["matches"]["value"])
            squadMatchesFM = "{:,}".format(squadMatches)
            squadWins = int(squad["top1"]["value"])
            squadWinsFM = "{:,}".format(squadWins)
            squadKills = int(squad["kills"]["value"])
            squadKillsFM = "{:,}".format(squadKills)
            squadKD = squad["kd"]["value"]
            squadKPG = squad["kpg"]["value"]
            squadWinP = squad["winRatio"]["value"]
            squadRank = int(squad["trnRating"]["rank"])
            squadRankFM = "{:,}".format(squadRank)

            draw.text(xy=(1072,283), text=squadMatchesFM, fill=(255,255,255), font=fnt) # 1047 27
            draw.text(xy=(947,408), text=squadWinsFM, fill=(255,255,255), font=fnt)
            draw.text(xy=(947,525), text=squadKillsFM, fill=(255,255,255), font=fnt)
            draw.text(xy=(947,635), text=squadKPG, fill=(255,255,255), font=fnt) 
            draw.text(xy=(1123,408), text=squadWinP, fill=(255,255,255), font=fnt)
            draw.text(xy=(1123,525), text=squadKD, fill=(255,255,255), font=fnt) 
            draw.text(xy=(1123,635), text=squadRankFM, fill=(255,255,255), font=fnt)
    
            globalMatchesPlayedValue = int(req["lifeTimeStats"][7]["value"])
            globalMatchesPlayedValueFM = "{:,}".format(globalMatchesPlayedValue)
            globalMatchesWonValue = int(req["lifeTimeStats"][8]["value"])
            globalMatchesWonValueFM = "{:,}".format(globalMatchesWonValue)
            globalMatchesWinpercentValue = req["lifeTimeStats"][9]["value"]
            globalKillsValue = int(req["lifeTimeStats"][10]["value"])
            globalKillsValueFM = "{:,}".format(globalKillsValue)
            globalKDValue = req["lifeTimeStats"][11]["value"]

            draw.text(xy=(1047,27), text=globalMatchesPlayedValueFM, fill=(0,0,0), font=fnt) # 1072 283
            draw.text(xy=(165,130), text=globalMatchesWonValueFM, fill=(255,255,255), font=fnt)
            draw.text(xy=(165,208), text=globalKDValue, fill=(255,255,255), font=fnt)
            draw.text(xy=(600,130), text=globalMatchesWinpercentValue, fill=(255,255,255), font=fnt)
            draw.text(xy=(1050,130), text=globalKillsValueFM, fill=(255,255,255), font=fnt)
            draw.text(xy=(600,208), text=squadKPG, fill=(255,255,255), font=fnt)
            image.save('./stats/{}.png'.format(epic_name))
            await self.bot.send_file(ctx.message.channel, './stats/{}.png'.format(epic_name))
            await session.close()

        except KeyError:

            if req["stats"]["p2"] == None: # raises KeyError: 'p2'
                soloFM = "N/A"
                fSoloRW = "N/A"
                soloKillsFM = "N/A"
                soloKPG = "N/A"
                soloWinP = "N/A"
                soloKD = "N/A"
                fRankSoloRN = "N/A"

            """msg = req["error"]
            await self.bot.say(msg + ": **{}**".format(epic_name))"""

    """@fortnite.error
    async def fortnite_error(self, error, ctx): # basically a help command
        if isinstance(error, discord.ext.commands.MissingRequiredArgument):
            embed = discord.Embed(title='Fortnite Help')
            embed.add_field(name="About", value="Fortnite command is used to gather statistics on a fortnite profile. Statistics gathered are from FortniteTracker's API.", inline=False)
            embed.add_field(name="Usage", value="`!fortnite <xbl|pc|psn> <epic_username>`")
            await self.bot.say(embed=embed)"""


def setup(bot):
    bot.add_cog(Othercommands(bot))
