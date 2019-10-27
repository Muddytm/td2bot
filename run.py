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
        data = []
        json.dump(data, outfile)


if not os.path.isfile("data/requests.json"):
    with open("data/icons.json", "w") as outfile:
        data = []
        json.dump(data, outfile)


@client.event
async def on_ready():
    print ("Logged in as")
    print (client.user.name)
    print (client.user.id)
    print ("------")

    if len(sys.argv) > 1 and sys.argv[1] == "icon":
        # Whole bunch of stuff to make the icon and make the correct name.
        hero_file = blahblah.make()
        hero = hero_file.replace(".png", "").replace("_", " ")
        hero_name = ""
        hero_words = hero.split()
        for word in hero_words:
            hero_name += word.lower().capitalize() + " "
        hero_name = hero_name.strip()

        for channel in client.get_all_channels():
            if "-discussion" in channel.name and "New hero discussions" in channel.topic:
                # Do server icon change
                with open("images/icon.png", "rb") as f:
                    icon = f.read()
                await client.edit_server(channel.server, icon=icon)

                # Rename channel (whitespace will default to a hyphen)
                await client.edit_channel(channel, name="{}-discussion".format(hero))

                # Post announcement and question
                questions = ["Is this hero strong in the current meta? Why or why not?",
                             "How the !@#$ you play this hero?",
                             "Is this hero's Aghanim's upgrade any good?",
                             "What's this hero's biggest weakness?",
                             "What's this hero's biggest strength?",
                             "When's the right time to pick this hero?",
                             "What is this hero's impact at each point of the game?",
                             "What's your preferred skill build with this hero?",
                             "Are their talents any good? Which ones are the best?",
                             "What are some common mistakes with this hero?"]

                with open("images/heroes/{}".format(hero_file), "rb") as f:
                    await client.send_file(channel, f)

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
async def requesthero(ctx, *stuff):
    """Request a hero for daily discussion!"""
    if ctx.message.channel.name != "botcommands":
        await client.say("Please request a hero in #botcommands.")
        return

    if not stuff:
        await client.say("Please provide a hero name (i.e. `!requesthero puck`).")
        return

    stuff_string = "_".join(stuff).replace("\'", "").lower()

    with open("data/requests.json") as f:
        request_data = json.load(f)

    with open("data/icons.json") as f:
        used_data = json.load(f)

    if stuff_string == "io":
        stuff_string = "io.png"

    for i in range(len(request_data)):
        if request_data[i]["name"] == ctx.message.author.name:
            await client.say("You've already requested a hero! Please wait until yours is featured before requesting another.")
            return
        elif stuff_string in request_data[i]["hero"]:
            await client.say("This hero's already on the waiting list.")
            return

    hero = ""
    for filename in os.listdir("images/heroes"):
        if stuff_string in filename and "README" not in filename:
            hero = filename

    if not hero:
        await client.say("This isn't a hero...")
        return
    if hero not in used_data:
        request_data.append({"name": ctx.message.author.name, "hero": hero})
        with open("data/requests.json", "w") as f:
            json.dump(request_data, f)

        wait = len(request_data)
        if wait == 1:
            await client.say("Hero was added! It will be featured tomorrow.")
        else:
            await client.say("Hero was added! It will be featured in {} days.".format(str(wait)))
        return
    else:
        await client.say("This hero has already been featured!")
        return


@client.command(pass_context=True)
async def schedule(ctx, stuff=""):
    """List the daily discussion schedule."""
    with open("data/requests.json") as f:
        request_data = json.load(f)

    if not request_data:
        await client.say("There are no hero discussions scheduled, so future discussions will be randomly selected. Type `!requesthero hero` to schedule a hero discussion!")
        return

    response = "The daily hero discussion schedule is as follows:"

    count = 1
    for request in request_data:
        hero_name = request["hero"].replace("_", " ").replace(".png", "").split()
        name = ""
        for word in hero_name:
            name += "{} ".format(word.capitalize())

        name = name.strip().replace("Of", "of")

        if count == 1:
            response += "\n`NEXT: {}`".format(name)
        elif count < 11:
            response += "\n`In {} days: {}`".format(str(count), name)
        elif count == 11:
            response += "\n...followed by: {}".format(name)
        else:
            response += ", {}".format(name)

        count += 1

    await client.say(response)


@client.command(pass_context=True)
async def test(ctx, stuff=""):
    """Test."""
    await client.say("OwO")


@client.command(pass_context=True)
@commands.has_any_role("Admin")
async def scram(ctx, stuff=""):
    """Close the bot."""

    await client.say("I'm outta here.")
    await client.logout()


client.run(TOKEN)
