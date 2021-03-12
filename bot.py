import discord
import os
import random


client = discord.Client()
TOKEN = os.environ.get("BOT_TOKEN")

COMMAND_START = "!"


@client.event
async def on_ready():
    print(f"Successfully logged in as {client.user} with ID {client.user.id}")


@client.event
async def on_message(message):
    guild = message.guild
    channel = message.channel
    send = channel.send # this is a function
    author = message.author
    msg = message.content

    # don't respond to self
    if author == client.user or not msg.startswith(COMMAND_START):
        return

    print(f"Received command attempt \"{msg}\" from {author} in {channel} in {guild}")

    no_start = msg[len(COMMAND_START):]
    bad_parts = no_start.split(" ")
    parts = [part for part in bad_parts if part != ""]
    cmd = parts[0]
    args = parts[1:]

    if cmd in ["hello", "hi", "hey"]:
        await send(f"Hello, {author.mention}! :smile:")


    elif cmd in ["where", "whereami"]:
        await send(f"We are in the server **{guild.name}** in the channel {channel.mention}! :smile:")


    elif cmd in ["die", "dice"]:
        await send(f"Rolled a {random.choice(range(1, 7))}.")


    elif cmd in ["coin", "coinflip"]:
        await send(f"Flipped {'Heads' if (random.random() < 0.5) else 'Tails'}.")


client.run(TOKEN)
