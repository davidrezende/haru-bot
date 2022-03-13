import json
import os
import random
from datetime import datetime, timedelta

import certifi
import discord
import pymongo
from discord.ext import commands
from dotenv import load_dotenv
from pymongo import MongoClient

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')
CONNECTION = os.getenv('CONNECTION_URL')

ca = certifi.where()
cluster = MongoClient(CONNECTION, tlsCAFile=ca)
db = cluster["harubotdb"]
collection = db["UserData"]

bot = commands.Bot(command_prefix='!')


@bot.command(name='rolldice', help='Simulates rolling dice. Ex: !rolldice <nrs_dice> <nrs_slides>')
async def roll(ctx, number_of_dice: int, number_of_sides: int):
    print(f"{ctx.channel}: {ctx.author}: {ctx.author.name}")
    dice = [
        str(random.choice(range(1, number_of_sides + 1)))
        for _ in range(number_of_dice)
    ]
    # save(ctx)
    await ctx.reply('Rolling... ' + ', '.join(dice))


@bot.command(name='add', help='Add note. Ex: !add <note> <category> <category_text>')
async def addNote(ctx, nameNote: str, category: str, categoryText: str):
    print(f"{ctx.channel}: {ctx.author}: {ctx.author.name}")
    await ctx.reply(saveNote(ctx, nameNote, category, categoryText))


@bot.command(name='show', help='Show note. Ex: !show <note>')
async def showNote(ctx, nameNote: str):
    print(f"{ctx.channel}: {ctx.author}: {ctx.author.name}")
    await findNoteByName(ctx, nameNote)


def myconverter(o):
    if isinstance(o, datetime):
        return o.__str__()


async def findNoteByName(ctx, nameNote):
    query = {"id_user": ctx.author.id, nameNote: {"$exists": True}}
    note = collection.find_one(query)
    if(note):
        print(str(note))
        onlyNote = note[nameNote]
        if(onlyNote['dat_last_modified']):
            onlyNote['dat_last_modified'] = json.dumps(
                onlyNote['dat_last_modified'], default=myconverter)
        onlyNote['dat_creation'] = json.dumps(
            onlyNote['dat_creation'], default=myconverter)
        onlyNote = str(onlyNote).replace("\"", "")
        print(onlyNote)
        return await ctx.reply(embed=embed(ctx, nameNote, onlyNote))
    else:
        return await ctx.reply('> **' + nameNote + '** does not exists!')


def embed(ctx, nameNote, response: str):
    print(response)
    embed = discord.Embed(
        title=nameNote,
        url="https://realdrewdata.medium.com/",
        description="Details from " + nameNote + ":",
        color=discord.Color.blue())
    embed.set_author(name="Sheila", url="https://twitter.com/RealDrewData",
                     icon_url="https://cdn-images-1.medium.com/fit/c/32/32/1*QVYjh50XJuOLQBeH_RZoGw.jpeg")
    # embed.set_author(name=ctx.author.display_name, url="https://twitter.com/RealDrewData", icon_url=ctx.author.avatar_url)
    embed.set_thumbnail(url="https://i.imgur.com/axLm3p6.jpeg")
    response = response.replace("\'", "\"")
    print(response)
    response = json.loads(response)
    print(response)
    for key, value in response.items():
        if (key == "dat_creation"):
            key = "date creation"
            embed.add_field(name="**"+key.upper()+"**",
                            value=value, inline=False)
        else:
            if (key != "dat_last_modified"):
                embed.add_field(name="**"+key.upper()+"**",
                                value=value, inline=False)

    # embed.add_field(name="*Italics*", value="Surround your text in asterisks (\*)", inline=False)
    # embed.add_field(name="**Bold**", value="Surround your text in double asterisks (\*\*)", inline=False)
    # embed.add_field(name="__Underline__", value="Surround your text in double underscores (\_\_)", inline=False)
    # embed.add_field(name="~~Strikethrough~~", value="Surround your text in double tildes (\~\~)", inline=False)
    # embed.add_field(name="`Code Chunks`", value="Surround your text in backticks (\`)", inline=False)
    # embed.add_field(name="Blockquotes", value="> Start your text with a greater than symbol (\>)", inline=False)
    # embed.add_field(name="Secrets", value="||Surround your text with double pipes (\|\|)||", inline=False)
    embed.set_footer(text="About: haru-bot on Github")
    return embed


def saveNote(ctx, nameNote, category, categoryText):
    queryUserExists = {"id_user": ctx.author.id}
    userExists = collection.count_documents(queryUserExists)
    if(userExists <= 0):
        post = {"id_user": ctx.author.id, "dat_creation": datetime.today().replace(microsecond=0), nameNote: {
            category: categoryText, "dat_creation": datetime.today().replace(microsecond=0)}}
        collection.insert_one(post)
        return '> **' + ctx.author.name + ' congratulations!** You have created your first note: **' + nameNote + '**.\n+**Helpful commands:** \n!show <note>\n!add <note> <new_category> <category_text>'
    else:
        queryNoteExists = {"id_user": ctx.author.id,
                           nameNote: {"$exists": True}}
        noteExists = collection.count_documents(queryNoteExists)
        if (noteExists <= 0):
            filter = {"id_user": ctx.author.id}
            newvalues = {"$set": {nameNote+'.'+category: categoryText, nameNote +
                                  '.'+"dat_creation": datetime.today().replace(microsecond=0)}}
            collection.update_one(filter, newvalues)
            return '> ' + nameNote + ' saved.'
        else:
            queryNoteCategoryExists = {
                "id_user": ctx.author.id, nameNote+'.'+category: {"$exists": True}}
            noteCategoryExists = collection.count_documents(
                queryNoteCategoryExists)
            if(noteCategoryExists <= 0):
                filter = {"id_user": ctx.author.id,
                          nameNote+'.'+category: {"$exists": False}}
                newvalues = {"$set": {nameNote+'.'+category: categoryText, nameNote +
                                      '.'+"dat_last_modified": datetime.today().replace(microsecond=0)}}
                collection.update_one(filter, newvalues)
                return '> Note **' + nameNote + '** updated with new category **' + category + '**.'
            else:
                return '> Note **' + category + '** already exists! \n**Suggestion:**\n!edit <note> <category> <text-from-category>'


def save(ctx):
    myquery = {"_id": ctx.author.id}
    if (collection.count_documents(myquery) == 0):
        post = {"_id": ctx.author.id, "score": 1}
        collection.insert_one(post)
    else:
        query = {"_id": ctx.author.id}
        user = collection.find(query)
        for result in user:
            print(result)
            score = result["score"]
        score = score + 1
        collection.update_one({"_id": ctx.author.id}, {
                              "$set": {"score": score}})


@bot.command(name='99', help='Responds with a random quote from Brooklyn 99')
async def nine_nine(ctx):
    brooklyn_99_quotes = [
        'I\'m the human form of the 💯 emoji.',
        'Bingpot!',
        (
            'Cool. Cool cool cool cool cool cool cool, '
            'no doubt no doubt no doubt no doubt.'
        ),
    ]
    response = random.choice(brooklyn_99_quotes)
    await ctx.send(response)


@bot.command(name='create-channel')
@commands.has_role('admin')
async def create_channel(ctx, channel_name='real-python'):
    guild = ctx.guild
    existing_channel = discord.utils.get(guild.channels, name=channel_name)
    if not existing_channel:
        print(f'Creating a new channel: {channel_name}')
        await guild.create_text_channel(channel_name)


@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.errors.CheckFailure):
        await ctx.reply('You do not have the correct role for this command.')
    await ctx.reply(error)

bot.run(TOKEN)
