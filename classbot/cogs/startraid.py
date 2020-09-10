import json
import random
import discord
import datetime
from classbot import bot_config
from discord.ext import commands
from classbot.utils import CUR_RAIDS_PATH, load_message, cur_raids, get_react_message

EMPTY_RAID_CLASS = "Nobody is currently playing this class!"


class StartRaid(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(aliases=["sr"])
    async def startraid(self, ctx, *, name: str):
        """Starts a new raid with a given name"""

        # NOTE: delete this statement and it's contents if this should be allowed for everyone
        if not ctx.message.author.guild_permissions.administrator:
            noauth_embed = discord.Embed(
                title="Unauthorised!",
                description="Only administrators can start raids!",
                color=0xFF0000,
            )

            await ctx.send(embed=noauth_embed)
            return
        # NOTE: don't delete below!

        embed = discord.Embed(
            title=name, description=f"Requested by <@{ctx.author.id}>", color=0x000000,
        )

        start_date = datetime.datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")
        embed.set_footer(text=f"Started at {start_date}. Reference ID: generating..")

        for class_name, class_emote in bot_config.CLASSES.items():
            embed.add_field(name=f"{class_emote} {class_name}", value=EMPTY_RAID_CLASS)

        sent_msg = await ctx.send(embed=embed)
        raid_id = self._add_cur_raid(sent_msg.id)

        embed.set_footer(text=f"Started at {start_date}. Reference ID: {raid_id}")
        await sent_msg.edit(embed=embed)  # edit with new raid id

        await ctx.message.delete()  # delete authors message if all goes well

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, reaction_payload):
        found_guild = self.client.get_guild(reaction_payload.guild_id)
        found_user = await found_guild.fetch_member(reaction_payload.user_id)

        if reaction_payload.message_id in cur_raids:
            print("Woop")

    def _add_cur_raid(self, message_id: int) -> str:
        """Adds a new raid and returns random id given"""

        def rand_dict() -> str:
            return random.choice(bot_config.ENGLISH_DICTIONARY)

        raid_id = ""

        for i in range(2500):
            tmp_id = f"{rand_dict()}-{rand_dict()}"

            if tmp_id not in cur_raids:
                raid_id = tmp_id
                break

        if len(raid_id) == 0:
            raise Exception("Could not find suitable random raid id, tried 2500 times!")

        cur_raids[raid_id] = message_id

        self._save_cur_raids()

        return raid_id

    def _save_cur_raids(self):
        """Hacky method to save [cur_raids] to a json file"""

        json.dump(cur_raids, open(CUR_RAIDS_PATH, "w"))


def setup(client):
    client.add_cog(StartRaid(client))
    load_message("StartRaid")
