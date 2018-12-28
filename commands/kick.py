import discord
import random

from discord.ext import commands
from discord import Member


class Kick:
    def __init__(self, client):
        self.client = client

    # Kick users
    @commands.command()
    @commands.has_permissions(kick_members=True)
    async def kick(self, user: Member):
        embed = discord.Embed(
            title="Kick",
            description="{user} has been kicked!".format(
                user=user.display_name),
            colour=random.randint(0, 0xFFFFFF))

        await self.client.kick(user)
        await self.client.say(embed=embed)


def setup(client):
    client.add_cog(Kick(client))
