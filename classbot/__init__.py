from classbot.utils import Config, get_cogs
from discord.ext import commands

bot_config = Config()
client = commands.Bot(command_prefix=bot_config.PREFIX)

client.remove_command("help")

@client.event
async def on_ready():
    print(f"'{client.user.name}' is online with the ID '{client.user.id}'!")

    print("Loading cogs..")
    for cog in get_cogs():
        client.load_extension(f"{__name__}.{cog}")
    print("Loaded cogs!")
