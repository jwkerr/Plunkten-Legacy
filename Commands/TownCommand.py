import disnake
from disnake.ext import commands
import Utils.Utils as Utils

class TownCommand(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.slash_command()
    async def town(
        self,
        inter
    ):
        pass

    @town.sub_command(description = "Provides general info about a town")
    async def search(
        self,
        inter: disnake.ApplicationCommandInteraction,
        town: str = commands.Param(description = "Town's name"),
        server: str = commands.Param(description = "Server name, defaults to Aurora", default = "aurora", choices = ["aurora", "nova"])
    ):
        commandString = f"/town search town: {town} server: {server}"
        try:
            townsLookup = Utils.Lookup.lookup(server, endpoint = "towns", name = town)

            locationUrl = f"https://earthmc.net/map/{server}/?zoom=4&x={townsLookup['spawn']['x']}&z={townsLookup['spawn']['z']}"

            try:
                nation = townsLookup["affiliation"]["nation"]
                joinedNationAt = f"<t:{round(townsLookup['timestamps']['joinedNationAt'] / 1000)}:R>"
            except:
                nation = None
                joinedNationAt = "N/A"

            rnaoPermsList = Utils.CommandTools.rnao_perms(json = townsLookup)

            embed = Utils.Embeds.embed_builder(title = f"`{townsLookup['strings']['town']}`", description = townsLookup["strings"]["board"], footer = commandString, author = inter.author)

            embed.add_field(name = "Mayor", value = townsLookup["strings"]["mayor"], inline = True)
            embed.add_field(name = "Nation", value = nation, inline = True)
            embed.add_field(name = "Location", value = f"[Open Dynmap]({locationUrl})", inline = True)

            embed.add_field(name = "Residents", value = townsLookup["stats"]["numResidents"], inline = True)
            embed.add_field(name = "Town Blocks", value = f"{townsLookup['stats']['numTownBlocks']}/{townsLookup['stats']['maxTownBlocks']}", inline = True)
            embed.add_field(name = "Balance", value = townsLookup["stats"]["balance"], inline = True)

            embed.add_field(name = "Founder", value = townsLookup["strings"]["founder"], inline = True)
            embed.add_field(name = "Founded", value = f"<t:{round(townsLookup['timestamps']['registered'] / 1000)}:R>", inline = True)            
            embed.add_field(name = "Joined Nation", value = joinedNationAt, inline = True)
            
            embed.add_field(name = "Perms", value = f"• `Build` — {rnaoPermsList[0]}\n• `Destroy` — {rnaoPermsList[1]}\n• `Switch` — {rnaoPermsList[2]}\n• `ItemUse` — {rnaoPermsList[3]}", inline = True)
            embed.add_field(name = "Flags", value = f"• `PvP` — {townsLookup['perms']['flagPerms']['pvp']}\n• `Explosions` — {townsLookup['perms']['flagPerms']['explosion']}\n• `Firespread` — {townsLookup['perms']['flagPerms']['fire']}\n• `Mob Spawns` — {townsLookup['perms']['flagPerms']['mobs']}", inline = True)
            embed.add_field(name = "Status", value = f"• `Capital` — {townsLookup['status']['isCapital']}\n• `Open` — {townsLookup['status']['isOpen']}\n• `Public` — {townsLookup['status']['isPublic']}\n• `Neutral` — {townsLookup['status']['isNeutral']}\n• `Overclaimed` — {townsLookup['status']['isOverClaimed']}\n• `Ruined` — {townsLookup['status']['isRuined']}", inline = True)
            
            await inter.send(embed = embed, ephemeral = False)

        except:
            embed = Utils.Embeds.error_embed(value = "Check if you wrote the town name incorrectly or if the server is currently offline, otherwise try again later", footer = commandString)

            await inter.send(embed = embed, ephemeral = True)

    @town.sub_command(description = "View all the residents of a specified town")
    async def reslist(
        self,
        inter: disnake.ApplicationCommandInteraction,
        town: str = commands.Param(description = "Town's name"),
        server: str = commands.Param(description = "Server name, defaults to Aurora", default = "aurora", choices = ["aurora", "nova"])
    ):
        commandString = f"/town reslist town: {town} server: {server}"
        try:
            townsLookup = Utils.Lookup.lookup(server, endpoint = "towns", name = town)

            embed = Utils.Embeds.embed_builder(title = f"`{townsLookup['strings']['town']}'s Residents`", footer = commandString, author = inter.author)

            residentsString = Utils.CommandTools.list_to_string(list = townsLookup["residents"])

            embed.add_field(name = "Residents", value = residentsString, inline = True)

            await inter.send(embed = embed, ephemeral = False)

        except:
            embed = Utils.Embeds.error_embed(value = "Check if you wrote the town name incorrectly or if the server is currently offline, otherwise try again later", footer = commandString)

            await inter.send(embed = embed, ephemeral = True)

    @town.sub_command(description = "View all the ranked residents of a specified town")
    async def ranklist(
        self,
        inter: disnake.ApplicationCommandInteraction,
        town: str = commands.Param(description = "Town's name"),
        server: str = commands.Param(description = "Server name, defaults to Aurora", default = "aurora", choices = ["aurora", "nova"])
    ):
        commandString = f"/town ranklist town: {town} server: {server}"
        try:
            townsLookup = Utils.Lookup.lookup(server, endpoint = "towns", name = town)

            embed = Utils.Embeds.embed_builder(title = f"`{townsLookup['strings']['town']}'s Ranked Residents`", footer = commandString, author = inter.author)

            for rank in townsLookup["ranks"]:
                if len(townsLookup["ranks"][rank]) != 0:
                    rankString = Utils.CommandTools.list_to_string(list = townsLookup["ranks"][rank])

                    embed.add_field(name = rank.capitalize(), value = rankString, inline = True)

                else:
                    embed.add_field(name = rank.capitalize(), value = "N/A", inline = True)

            if len(townsLookup["trusted"]) != 0:
                trustedString = Utils.CommandTools.list_to_string(list = townsLookup["trusted"])

                embed.add_field(name = "Trusted", value = trustedString, inline = True)

            else:
                embed.add_field(name = "Trusted", value = "N/A", inline = True)

            await inter.send(embed = embed, ephemeral = False)

        except:
            embed = Utils.Embeds.error_embed(value = "Check if you wrote the towm name incorrectly or if the server is currently offline, otherwise try again later", footer = commandString)

            await inter.send(embed = embed, ephemeral = True)

    @town.sub_command(description = "View all the outlaws of a specified town")
    async def outlawlist(
        self,
        inter: disnake.ApplicationCommandInteraction,
        town: str = commands.Param(description = "Town's name"),
        server: str = commands.Param(description = "Server name, defaults to Aurora", default = "aurora", choices = ["aurora", "nova"])
    ):
        commandString = f"/town outlawlist town: {town} server: {server}"
        try:
            townsLookup = Utils.Lookup.lookup(server, endpoint = "towns", name = town)

            embed = Utils.Embeds.embed_builder(title = f"`{townsLookup['strings']['town']}'s Outlaws`", footer = commandString, author = inter.author)

            if len(townsLookup["outlaws"]) != 0:
                outlawsString = Utils.CommandTools.list_to_string(list = townsLookup["outlaws"])

                embed.add_field(name = "Outlaws", value = outlawsString, inline = True)

            else:
                embed.add_field(name = "Outlaws", value = f"{townsLookup['strings']['town']} has no outlaws :)", inline = True)

            await inter.send(embed = embed, ephemeral = False)

        except:
            embed = Utils.Embeds.error_embed(value = "Check if you wrote the town name incorrectly or if the server is currently offline, otherwise try again later", footer = commandString)

            await inter.send(embed = embed, ephemeral = True)

def setup(bot):
    bot.add_cog(TownCommand(bot))