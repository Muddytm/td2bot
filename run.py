import asyncio
import discord
from discord.ext import commands
import config
import icon as blahblah
import json
import os
import random
import sys

TOKEN = config.app_token

BOT_PREFIX = "!"
client = commands.Bot(command_prefix=commands.when_mentioned_or(BOT_PREFIX))

if not os.path.isfile("data/icons.json"):
    with open("data/icons.json", "w") as outfile:
        data = {"used": []}
        json.dump(data, outfile)


@client.event
async def on_ready():
    print ("Logged in as")
    print (client.user.name)
    print (client.user.id)
    print ("------")

    if len(sys.argv) > 1 and sys.argv[1] == "icon":
        # Whole bunch of stuff to make the icon and make the correct name.
        hero = blahblah.make().replace(".png", "").replace("_", " ")
        hero_name = ""
        hero_words = hero.split()
        for word in hero_words:
            hero_name += word.lower().capitalize() + " "
        hero_name = hero_name.strip()

        for channel in client.get_all_channels():
            if "discussion" in channel.name:
                # Do server icon change
                with open("images/icon.png", "rb") as f:
                    icon = f.read()
                await client.edit_server(channel.server, icon=icon)

                # Rename channel (whitespace will default to a hyphen)
                await client.edit_channel(channel, name="{}-discussion".format(hero))

                # Post announcement and question
                questions = ["What item should you *never* get on this hero?",
                             "How am I supposed to play this?",
                             "Are they OP?",
                             "Are they meta right now?",
                             "How do you play them?",
                             "What's a must-get item on this bad boy/girl/thing?"]

                await client.send_message(channel,
                                          "Today's hero is **{}**. {}".format(hero_name.replace("_", " "), random.choice(questions)))
                await client.logout()


@client.event
async def on_message(message):
    """Add userdata json file and run certain functionality when a user types
    any message, anywhere.
    """
    if message.author == client.user:
        return

    # This allows us to use other commands as well.
    await client.process_commands(message)


@client.command(pass_context=True)
@commands.has_any_role("Admin")
async def scram(ctx, stuff=""):
    """Close the bot."""

    await client.say("I'm outta here.")
    await client.logout()


client.run(TOKEN)