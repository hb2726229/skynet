import config
import discord
import random

from discord import Member
from discord.ext import commands
from datetime import date


TOKEN = config.discord_token

client = commands.Bot(command_prefix="!")

# removes default help command
client.remove_command('help')

today = date.today()


@client.event
async def on_ready():
    await client.change_presence(game=discord.Game(name="Type !help for info"))
    print("Skynet is ready")


# Kick users
@client.command(pass_context=True)
@commands.has_permissions(kick_members=True)
async def kick(ctx, user: Member):
    embed = discord.Embed(
        title="Kick",
        description="{user} has been kicked!".format(user=user.display_name),
        colour=random.randint(0, 0xFFFFFF))

    await client.kick(user)
    await client.say(embed=embed)


# Ban users
@client.command(pass_context=True)
@commands.has_permissions(ban_members=True)
async def ban(ctx, user: Member):
    embed = discord.Embed(
        title="ban",
        description="{user} has been banned!".format(user=user.display_name),
        colour=random.randint(0, 0xFFFFFF))

    await client.ban(user)
    await client.say(embed=embed)


# Unban user
@client.command(pass_context=True)
@commands.has_permissions(ban_members=True)
async def unban(ctx, user: Member):
    embed = discord.Embed(
        title="unban",
        description="""{user} has been unbanned... you
            brought this on yourself""".format(
            user=user.display_name),
        colour=random.randint(0, 0xFFFFFF))

    await client.unban(ctx.message.server, user)
    await client.say(embed=embed)


# Mass unban
@client.command(pass_context=True)
async def mass_unban(ctx):
    server = ctx.message.server
    banned_users = await client.get_bans(server)

    for user in banned_users:
        await client.unban(server, user)

    await client.say("Mass Unban complete")


# Clear chat
@client.command(pass_context=True)
async def clear(ctx, user: Member = None, lim: int = 10):
    channel = ctx.message.channel
    msgs = []
    bot_msg = ""

    if user is None:
        async for message in client.logs_from(channel, int(lim)):
            if abs(today-message.timestamp.date()).days <= 14:
                msgs.append(message)
        bot_msg = "{total} messages deleted".format(total=len(msgs))
    else:
        async for message in client.logs_from(channel):
            if abs(today-message.timestamp.date()).days <= 14:
                if (len(msgs) < lim and message.author.id == user.id):
                    msgs.append(message)
        bot_msg = "Cleared {total} of {target} messages".format(
            total=len(msgs), target=user)

    await client.delete_messages(msgs)
    await client.say(bot_msg)


@client.command()
async def ping():
    await client.say('pong')


client.run(TOKEN)
