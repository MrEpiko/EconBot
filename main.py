import disnake
from disnake.ext import commands, tasks
import os

bot = commands.Bot(command_prefix=["."], intents=disnake.Intents.all(), owner_ids=[656617935376220160], case_insensitive = True)

@tasks.loop(hours=10)
async def load():
  for filename in os.listdir("./cogs"): 
    if filename.endswith(".py"):
        bot.load_extension(f"cogs.{filename[:-3]}")
        print(f"{filename} cog loaded")

@bot.listen()
async def on_ready():
  load.start()
  print(f"{bot.user} is ready.")

if __name__ == "__main__":
    bot.run("OTk4MzAzMTQ4ODU2ODQwMjAy.G6JUDp.LJHZr8iUfgDXXeuS9FdMrrAM-VznsRxY32NBRk") 