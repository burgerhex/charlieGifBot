import os
# import random
import discord
import giphypop
# import TenGiphPy

COMMAND_START = "!"
LINK_KEY = "url"

client = discord.Client()
TOKEN = os.environ.get("BOT_TOKEN")

GIPHY_KEY = os.environ.get("GIPHY_API_KEY")
giphy = giphypop.Giphy(GIPHY_KEY)
# giphy = TenGiphPy.Giphy(token=GIPHY_KEY)

# TENOR_KEY = os.environ.get("TENOR_API_KEY")
# tenor = TenGiphPy.Tenor(token=TENOR_KEY)


@client.event
async def on_ready():
    print(f"Successfully logged in as {client.user} with ID {client.user.id}")


@client.event
async def on_message(message: discord.Message):
    guild: discord.Guild = message.guild

    # don't respond to DMs
    if guild is None:
        return

    channel: discord.TextChannel = message.channel
    send = channel.send # this is a function
    author: discord.Member = message.author
    msg: str = message.content

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


    elif cmd in ["gif", "gifthat", "charlie", "char"]:
        if not args:
            messages = await channel.history(limit=2).flatten()
            if len(messages) < 2:
                return

            # ideally, the last sent message should be the one that invoked this command
            # this may not be true if lag occurs, so it's commented out
            # assert messages[0].id == message.id

            search = messages[1].content
            gif = None

            try:
                for giphy_image in giphy.search(search):
                    gif = giphy_image[LINK_KEY]
                    break
            except StopIteration:
                return

            assert gif is not None

            await send(gif)


client.run(TOKEN)
