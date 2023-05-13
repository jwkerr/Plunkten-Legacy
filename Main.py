import disnake
from disnake.ext import commands
import os
import dotenv
import Utils.Utils as Utils

bot = commands.InteractionBot()

@bot.event
async def on_ready():
    await bot.change_presence(activity = disnake.Game(name = "EarthMC.net"))
    print(f"Logged in as {bot.user}")
    print(f"Operating in {len(bot.guilds)} guild/s")

bot.load_extension("Commands.ServerCommand")
bot.load_extension("Commands.ResCommand")
bot.load_extension("Commands.TownCommand")
bot.load_extension("Commands.NationCommand")

dotenv.load_dotenv("secrets.env")
bot.run(os.getenv("TOKEN"))