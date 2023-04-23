import datetime
import disnake
import requests
import traceback

class CommandTools():
    def get_weather(serverLookup):
        if serverLookup["world"]["hasStorm"] == True & serverLookup["world"]["isThundering"] == True:
            weather = "Thundering"
        elif serverLookup["world"]["hasStorm"] == True:
            weather = "Raining"
        else:
            weather = "Clear"

        return weather

    def rnao_perms(json):
        rnaoPermsList = []
        permsKeyList = ["buildPerms", "destroyPerms", "switchPerms", "itemUsePerms"]

        count = 0
        for section in json["perms"]["rnaoPerms"]:
            try:
                resident = json["perms"]["rnaoPerms"][permsKeyList[count]]["resident"]
            except:
                friend = json["perms"]["rnaoPerms"][permsKeyList[count]]["friend"]
            try:
                nation = json["perms"]["rnaoPerms"][permsKeyList[count]]["nation"]
            except:
                town = json["perms"]["rnaoPerms"][permsKeyList[count]]["town"]
            ally = json["perms"]["rnaoPerms"][permsKeyList[count]]["ally"]
            outsider = json["perms"]["rnaoPerms"][permsKeyList[count]]["outsider"]

            rnaoString = "----"
            try:
                if resident:
                    rnaoString = "r" + rnaoString[1:]
            except:
                if friend:
                    rnaoString = "f" + rnaoString[1:]
            try:
                if nation:
                    rnaoString = rnaoString[:1] + "n" + rnaoString[2:]
            except:
                if town:
                    rnaoString = rnaoString[:1] + "t" + rnaoString[2:]
            if ally:
                rnaoString = rnaoString[:2] + "a" + rnaoString[3:]
            if outsider:
                rnaoString = rnaoString[:-1] + "o"
            
            rnaoPermsList.append(rnaoString)

            count = count + 1

        return rnaoPermsList
    
    def list_to_string(list):
        listString = ""
        for i in range(len(list)):
            if i == len(list) - 1:
                listString += list[i]
            else:
                listString += list[i] + ", "

        return listString
    
class Lookup():
    def lookup(server, endpoint = None, name = None):
        if endpoint == None:
            api_url = f"https://api.earthmc.net/v1/{server}/"
        elif name == None:
            api_url = f"https://api.earthmc.net/v1/{server}/{endpoint}"
        else:
            api_url = f"https://api.earthmc.net/v1/{server}/{endpoint}/{name}"

        lookup = requests.get(api_url).json()

        return lookup
    
class Embeds():
    def embed_builder(title, description = None, author = None, footer = None, thumbnail = None):
        embed = disnake.Embed(
            title = title,
            description = description,
            color = 0x003cf6,
            timestamp = datetime.datetime.now()
        )

        if author != None:
            embed.set_author(
                name = f"Queried by {author}",
                icon_url = author.avatar
            )

        if footer != None:
            embed.set_footer(
                icon_url = "https://cdn.discordapp.com/attachments/1050945545037951048/1097958906233360475/plunktencommand.png",
                text = footer
            )

        else:
            embed.set_footer(
                icon_url = "https://cdn.discordapp.com/avatars/1082118155528314892/7a83e01cbb11d4115d6cd1ae3f178eb0.webp",
                text = "Plunkten"
            )

        if thumbnail != None:
            embed.set_thumbnail(url = thumbnail)
            
        embed.set_image(url = "https://cdn.discordapp.com/attachments/1050945545037951048/1099030835220467872/linebreak.png")

        return embed
    
    def error_embed(value, type = None, footer = None):
        if type != "userError":
            traceback.print_exc()
        embed = Embeds.embed_builder(title = "`Error`", footer = footer)

        embed.add_field(name = "Something went wrong", value = value, inline = True)

        return embed