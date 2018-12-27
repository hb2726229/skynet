import discord
import config
from discord.ext import commands
from datetime import date


TOKEN = config.discord_token

client = commands.Bot(command_prefix="!")

today = date.today()


@client.event
async def on_ready():
    print("Skynet is ready")


# @client.event
# async def on_message(message: discord.Message):
#     print("{user} has sent a message".format(user=message.author))
#     await client.process_commands(message)


@client.command(pass_context=True)
async def clear(ctx, user: discord.User = None, lim: int = 10):
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
