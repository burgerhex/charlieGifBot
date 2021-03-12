import os
import random
import discord
import giphypop

COMMAND_START = "!"
LINK_KEY = "url"

client = discord.Client()
TOKEN = os.environ.get("BOT_TOKEN")

GIPHY_KEY = os.environ.get("GIPHY_API_KEY")
giphy = giphypop.Giphy(GIPHY_KEY)


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
        await send(random.choice([
            "shake shack?", "YOOOOO", "based based??", "alex literally shut the fuck up",
            "justin you're literally so annoying", "listening to podcast rn",
            "alkjfnlajniaundkljn", "WEIRDCHAMP", "POG", "LOL stop", "i'm on tiktok",
            "new vid up on yt", "bedwars?", "wanna speedrun", "mc?", "fall guys?",
            "OMG let's play speedrunners that actually sounds like so much fun",
            "i'll prob just order a refund but wtv", "that's HYPE", "that's so pog",
            "i hate college", "reading is for losers", "ping me when ur not playing league",
            "i don't even like films or filmmaking", "gifs are so pog", "TIMOTHEE CHALAMET",
            "laughing my ass off right now at the current moment, no cap",
            "stop roasting my gifs let me live", "seraphine gap or smtn idk league",
            "they really need to open up movie theaters bruh", "let's watch a movie",
            "can we do something i'm so bored", "rgmormlkfdmsoimoan", "i love gifs so much",
            "fuck you aviv", "gn"
        ]))


    elif cmd in ["gif", "gifthat", "charlie", "char"]:
        search = None

        if args:
            search = " ".join(args)
        else:
            messages = await channel.history(limit=2).flatten()
            if len(messages) < 2:
                return

            # ideally, the last sent message should be the one that invoked this command
            # this may not be true if lag occurs, so it's commented out
            # assert messages[0].id == message.id

            search = messages[1].content

        assert search is not None
        gif = None

        try:
            for giphy_image in giphy.search(search):
                gif = giphy_image[LINK_KEY]
                break
        except StopIteration:
            return

        if gif:
            await send(gif)


client.run(TOKEN)
