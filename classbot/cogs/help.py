import discord
from discord.ext import commands
from classbot.utils import load_message


class Help(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(aliases=["h", "about", "invite", "inv"])
    async def help(self, ctx):
        """Help command"""

        embed = discord.Embed(title="Help", color=0x000000)

        embed.add_field(
            name="`,startraid [name]` or `,sr [name]`",
            value="Make a new raid with a given name (administator only)",
            inline=False,
        )
        embed.add_field(
            name="`,deleteraid [id]` or `,dr [id]`",
            value="Deletes a raid given the reference id found at the bottom (administator only)",
            inline=False,
        )
        embed.add_field(
            name="`,help` or `,h`", value="Shows this command", inline=False
        )

        await ctx.send(embed=embed)


def setup(client):
    client.add_cog(Help(client))
    load_message("Help")
