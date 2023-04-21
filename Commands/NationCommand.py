import random
import disnake
from disnake.ext import commands
import Utils.Utils as Utils

class NationCommand(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.slash_command()
    async def nation(
        self, 
        inter
    ):
        pass

    @nation.sub_command(description = "Provides general info about a nation")
    async def search(
        self,
        inter: disnake.ApplicationCommandInteraction,
        nation: str = commands.Param(description = "Nation's name, leave blank for a random choice", default = ""),
        server: str = commands.Param(description = "Server name, defaults to Aurora", default = "aurora", choices = ["aurora", "nova"])
    ):
        commandString = f"/nation search nation: {nation} server: {server}"
        try:
            if nation == "":
                allNationsLookup = Utils.Lookup.lookup(server, endpoint = "nations")
                nation = random.choice(allNationsLookup["allNations"])
            nationsLookup = Utils.Lookup.lookup(server, endpoint = "nations", name = nation)
        except:
            embed = Utils.Embeds.error_embed(value = "Check if you wrote a parameter incorrectly or if the server is currently offline", type = "userError", footer = commandString)

            await inter.send(embed = embed, ephemeral = True)
            return
        
        try:
            locationUrl = f"https://earthmc.net/map/{server}/?zoom=4&x={nationsLookup['spawn']['x']}&z={nationsLookup['spawn']['z']}"

            embed = Utils.Embeds.embed_builder(title = f"`{nationsLookup['strings']['nation']}`", description = nationsLookup["strings"]["board"], footer = commandString, author = inter.author)

            embed.add_field(name = "King", value = nationsLookup["strings"]["king"], inline = True)
            embed.add_field(name = "Capital", value = nationsLookup["strings"]["capital"], inline = True)
            embed.add_field(name = "Location", value = f"[Open Dynmap]({locationUrl})", inline = True)   

            embed.add_field(name = "Residents", value = nationsLookup["stats"]["numResidents"], inline = True)
            embed.add_field(name = "Town Blocks", value = nationsLookup["stats"]["numTownBlocks"], inline = True)
            embed.add_field(name = "Balance", value = f"{nationsLookup['stats']['balance']}G", inline = True)

            embed.add_field(name = "Towns", value = nationsLookup["stats"]["numTowns"], inline = True)
            embed.add_field(name = "Founded", value = f"<t:{round(nationsLookup['timestamps']['registered'] / 1000)}:R>", inline = True)                  
            embed.add_field(name = "Status", value = f"• `Open` — {nationsLookup['status']['isOpen']}\n• `Public` — {nationsLookup['status']['isPublic']}\n• `Neutral` — {nationsLookup['status']['isNeutral']}", inline = True)

            await inter.send(embed = embed, ephemeral = False)

        except:
            embed = Utils.Embeds.error_embed(value = "If it is not evident that the error was your fault, please report it", footer = commandString)

            await inter.send(embed = embed, ephemeral = True)

    @nation.sub_command(description = "View all the residents of a specified nation")
    async def reslist(
        self,
        inter: disnake.ApplicationCommandInteraction,
        nation: str = commands.Param(description = "Nation's name"),
        server: str = commands.Param(description = "Server name, defaults to Aurora", default = "aurora", choices = ["aurora", "nova"])
    ):
        commandString = f"/nation reslist nation: {nation} server: {server}"
        try:
            nationsLookup = Utils.Lookup.lookup(server, endpoint = "nations", name = nation)
        except:
            embed = Utils.Embeds.error_embed(value = "Check if you wrote a parameter incorrectly or if the server is currently offline", type = "userError", footer = commandString)

            await inter.send(embed = embed, ephemeral = True)
            return
        
        try:
            embed = Utils.Embeds.embed_builder(title = f"`{nationsLookup['strings']['nation']}'s Residents`", footer = commandString, author = inter.author)

            residentsString = Utils.CommandTools.list_to_string(list = nationsLookup["residents"])

            embed.add_field(name = "Residents", value = residentsString[:1024], inline = True)

            await inter.send(embed = embed, ephemeral = False)

        except:
            embed = Utils.Embeds.error_embed(value = "If it is not evident that the error was your fault, please report it", footer = commandString)

            await inter.send(embed = embed, ephemeral = True)

    @nation.sub_command(description = "View all the ranked residents of a specified nation")
    async def ranklist(
        self,
        inter: disnake.ApplicationCommandInteraction,
        nation: str = commands.Param(description = "Nation's name"),
        server: str = commands.Param(description = "Server name, defaults to Aurora", default = "aurora", choices = ["aurora", "nova"])
    ):
        commandString = f"/nation ranklist nation: {nation} server: {server}"
        try:
            nationsLookup = Utils.Lookup.lookup(server, endpoint = "nations", name = nation)
        except:
            embed = Utils.Embeds.error_embed(value = "Check if you wrote a parameter incorrectly or if the server is currently offline", type = "userError", footer = commandString)

            await inter.send(embed = embed, ephemeral = True)
            return
        
        try:
            embed = Utils.Embeds.embed_builder(title = f"`{nationsLookup['strings']['nation']}'s Ranked Residents`", footer = commandString, author = inter.author)

            for rank in nationsLookup["ranks"]:
                if len(nationsLookup["ranks"][rank]) != 0:
                    rankString = Utils.CommandTools.list_to_string(list = nationsLookup["ranks"][rank])

                    embed.add_field(name = rank.capitalize(), value = rankString[:1024], inline = True)

                else:
                    embed.add_field(name = rank.capitalize(), value = "N/A", inline = True)

            await inter.send(embed = embed, ephemeral = False)

        except:
            embed = Utils.Embeds.error_embed(value = "If it is not evident that the error was your fault, please report it", footer = commandString)

            await inter.send(embed = embed, ephemeral = True)

    @nation.sub_command(description = "View all the allies of a specified nation")
    async def allylist(
        self,
        inter: disnake.ApplicationCommandInteraction,
        nation: str = commands.Param(description = "Nation's name"),
        server: str = commands.Param(description = "Server name, defaults to Aurora", default = "aurora", choices = ["aurora", "nova"])
    ):
        commandString = f"/nation allylist nation: {nation} server: {server}"
        try:
            nationsLookup = Utils.Lookup.lookup(server, endpoint = "nations", name = nation)
        except:
            embed = Utils.Embeds.error_embed(value = "Check if you wrote a parameter incorrectly or if the server is currently offline", type = "userError", footer = commandString)

            await inter.send(embed = embed, ephemeral = True)
            return
        
        try:
            embed = Utils.Embeds.embed_builder(title = f"`{nationsLookup['strings']['nation']}'s Allies`", footer = commandString, author = inter.author)

            if len(nationsLookup["allies"]) != 0:
                alliesString = Utils.CommandTools.list_to_string(list = nationsLookup["allies"])

                embed.add_field(name = "Allies", value = alliesString[:1024], inline = True)

            else:
                embed.add_field(name = "Allies", value = f"{nationsLookup['strings']['nation']} has no allies :(", inline = True)

            await inter.send(embed = embed, ephemeral = False)

        except:
            embed = Utils.Embeds.error_embed(value = "If it is not evident that the error was your fault, please report it", footer = commandString)

            await inter.send(embed = embed, ephemeral = True)

    @nation.sub_command(description = "View all the enemies of a specified nation")
    async def enemylist(
        self,
        inter: disnake.ApplicationCommandInteraction,
        nation: str = commands.Param(description = "Nation's name"),
        server: str = commands.Param(description = "Server name, defaults to Aurora", default = "aurora", choices = ["aurora", "nova"])
    ):
        commandString = f"/nation enemylist nation: {nation} server: {server}"
        try:
            nationsLookup = Utils.Lookup.lookup(server, endpoint = "nations", name = nation)
        except:
            embed = Utils.Embeds.error_embed(value = "Check if you wrote a parameter incorrectly or if the server is currently offline", type = "userError", footer = commandString)

            await inter.send(embed = embed, ephemeral = True)
            return
        
        try:
            embed = Utils.Embeds.embed_builder(title = f"`{nationsLookup['strings']['nation']}'s Enemies`", footer = commandString, author = inter.author)

            if len(nationsLookup["enemies"]) != 0:
                enemiesString = Utils.CommandTools.list_to_string(list = nationsLookup["enemies"])

                embed.add_field(name = "Enemies", value = enemiesString[:1024], inline = True)

            else:
                embed.add_field(name = "Enemies", value = f"{nationsLookup['strings']['nation']} has no enemies :)", inline = True)

            await inter.send(embed = embed, ephemeral = False)

        except:
            embed = Utils.Embeds.error_embed(value = "If it is not evident that the error was your fault, please report it", footer = commandString)

            await inter.send(embed = embed, ephemeral = True)

    @nation.sub_command(description = "View all the towns of a specified nation")
    async def townlist(
        self,
        inter: disnake.ApplicationCommandInteraction,
        nation: str = commands.Param(description = "Nation's name"),
        server: str = commands.Param(description = "Server name, defaults to Aurora", default = "aurora", choices = ["aurora", "nova"])
    ):
        commandString = f"/nation townlist nation: {nation} server: {server}"
        try:
            nationsLookup = Utils.Lookup.lookup(server, endpoint = "nations", name = nation)
        except:
            embed = Utils.Embeds.error_embed(value = "Check if you wrote a parameter incorrectly or if the server is currently offline", type = "userError", footer = commandString)

            await inter.send(embed = embed, ephemeral = True)
            return
        
        try:
            embed = Utils.Embeds.embed_builder(title = f"`{nationsLookup['strings']['nation']}'s Towns`", footer = commandString, author = inter.author)

            townsString = Utils.CommandTools.list_to_string(list = nationsLookup["towns"])

            embed.add_field(name = "Towns", value = townsString[:1024], inline = True)

            await inter.send(embed = embed, ephemeral = False)

        except:
            embed = Utils.Embeds.error_embed(value = "If it is not evident that the error was your fault, please report it", footer = commandString)

            await inter.send(embed = embed, ephemeral = True)

    @nation.sub_command(description = "View all the nations that the specified nation hasn't allied yet")
    async def unallied(
        self,
        inter: disnake.ApplicationCommandInteraction,
        nation: str = commands.Param(description = "Nation's name"),
        server: str = commands.Param(description = "Server name, defaults to Aurora", default = "aurora", choices = ["aurora", "nova"])
    ):
        commandString = f"/nation unallied nation: {nation} server: {server}"
        try:
            nationsLookup = Utils.Lookup.lookup(server, endpoint = "nations", name = nation)
            allNationsLookup = Utils.Lookup.lookup(server, endpoint = "nations")
        except:
            embed = Utils.Embeds.error_embed(value = "Check if you wrote a parameter incorrectly or if the server is currently offline", type = "userError", footer = commandString)

            await inter.send(embed = embed, ephemeral = True)
            return
        
        try:
            embed = Utils.Embeds.embed_builder(title = f"`{nationsLookup['strings']['nation']}'s Unallied Nations`", footer = commandString, author = inter.author)

            allyList = nationsLookup["allies"]
            allNations = allNationsLookup["allNations"]
            allNations.remove(nationsLookup["strings"]["nation"])

            unalliedList = list(set(allNations).difference(set(allyList)))
            if len(unalliedList) != 0:
                unalliedString = Utils.CommandTools.list_to_string(list = unalliedList)

                embed.add_field(name = "Unallied", value = unalliedString[:1024], inline = True)

            else:
                embed.add_field(name = "Unallied", value = f"{nationsLookup['strings']['nation']} has allied everyone :)", inline = True)

            await inter.send(embed = embed, ephemeral = False)

        except:
            embed = Utils.Embeds.error_embed(value = "If it is not evident that the error was your fault, please report it", footer = commandString)

            await inter.send(embed = embed, ephemeral = True)

def setup(bot):
    bot.add_cog(NationCommand(bot))