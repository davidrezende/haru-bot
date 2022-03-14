import json
import os
import profile
import random
from contextlib import nullcontext
from datetime import datetime, timedelta
from tkinter import Y
from unicodedata import name

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

bot = commands.Bot(command_prefix='!', activity=discord.Activity(type=discord.ActivityType.listening, name="🎧"))

@commands.cooldown(rate=1, per=3, type=commands.BucketType.user)
@bot.command(name='rq', help='Responds with a random quote.')
async def nine_nine(ctx):
    quotes = [
        'I\'m the human form of the 💯 emoji.',
        'Bingpot!',
        (
            'Cool. Cool cool cool cool cool cool cool, '
            'no doubt no doubt no doubt no doubt.'
        ),
    ]
    response = random.choice(quotes)
    await ctx.send(response)

@commands.cooldown(rate=1, per=3, type=commands.BucketType.user)
@bot.command(name='rolldice', help='Simulates rolling dice. Ex: !rolldice <nrs_dice> <nrs_slides>')
async def roll(ctx, number_of_dice: int, number_of_sides: int):
    print(f"{ctx.channel}: {ctx.author}: {ctx.author.name}")
    dice = [
        str(random.choice(range(1, number_of_sides + 1)))
        for _ in range(number_of_dice)
    ]
    await ctx.reply('Rolling... ' + ', '.join(dice))

@commands.cooldown(rate=1, per=3, type=commands.BucketType.user)
@bot.command(name='add', help='Add note. Ex: !add <note> <category> <category_text>')
async def addNote(ctx, nameNote: str, category: str, categoryText: str):
    print(f"{ctx.channel}: {ctx.author}: {ctx.author.name}")
    if not validateWhenAddOrUpdateFieldsEmbed(category, categoryText):
        await ctx.reply('Invalid URL from image. Only HTTPS available.')
    else:
        await ctx.reply(saveNote(ctx, nameNote, category, categoryText))

@commands.cooldown(rate=1, per=3, type=commands.BucketType.user)
@bot.command(name='edit', help='Edit note. Ex: !edit <note> <category> <new_category_text>')
async def editNote(ctx, nameNote: str, category: str, categoryText: str):
    print(f"{ctx.channel}: {ctx.author}: {ctx.author.name}")
    if not validateWhenAddOrUpdateFieldsEmbed(category, categoryText):
        await ctx.reply('Invalid URL from image. Only HTTPS available.')
    else:
        await ctx.reply(editNote(ctx, nameNote, category, categoryText))

@commands.cooldown(rate=1, per=3, type=commands.BucketType.user)
@bot.command(name='rm', help='Remove note or category of an note. Ex: !rm <note> <optional_category>')
async def removeNote(ctx, nameNote: str, category: str = None):
    print(f"{ctx.channel}: {ctx.author}: {ctx.author.name}")
    await ctx.reply(deleteNoteOrCategory(ctx, nameNote, category))

@commands.cooldown(rate=1, per=3, type=commands.BucketType.user)
@bot.command(name='show', help='Show note. Ex: !show <note>')
async def showNote(ctx, nameNote: str):
    print(f"{ctx.channel}: {ctx.author}: {ctx.author.name}")
    await findNoteByName(ctx, nameNote)

@commands.cooldown(rate=1, per=3, type=commands.BucketType.user)
@bot.command(name='notes', help='Show yours notes. Ex: !notes')
async def listNotes(ctx):
    print(f"{ctx.channel}: {ctx.author}: {ctx.author.name}")
    await findAllNotesByUser(ctx)

def myconverter(o):
    if isinstance(o, datetime):
        return o.__str__()


async def findNoteByName(ctx, nameNote):
    query = {"id_user": ctx.author.id, "notes"+"."+nameNote: {"$exists": True}}
    note = collection.find_one(query)
    if(note):
        onlyNote = note['notes'][nameNote]
        onlyNote['dat_last_modified'] = json.dumps(
            onlyNote['dat_last_modified'], default=myconverter) if 'dat_last_modified' in onlyNote else 'none'
        onlyNote['dat_creation'] = json.dumps(
            onlyNote['dat_creation'], default=myconverter)
        onlyNote = str(onlyNote).replace("\"", "")
        return await ctx.reply(embed=embedNote(ctx, nameNote, onlyNote))
    else:
        return await ctx.reply('> **' + nameNote + '** does not exists!')

async def findAllNotesByUser(ctx):
    query = {"id_user": ctx.author.id, "notes": {"$exists": True}}
    notes = collection.find(query)
    for result in notes:
        onlyNotes = json.dumps(result["notes"], default=myconverter)
        print(onlyNotes)
        return await ctx.reply(embed=embedNotes(ctx, onlyNotes))
    else:
        return await ctx.reply('> You does not have any notes.') 

def embedNote(ctx, nameNote, response: str):
    response = response.replace("\'", "\"")
    response = json.loads(response)

    embed = discord.Embed(
        title=nameNote.capitalize(),
        description=
        # "||" +
        "\n**created in=**  " + (response.get('dat_creation') if response.get('dat_creation') != None else "") +
        ("\n**last modified in=**  " + response.get('dat_last_modified') if response.get('dat_last_modified') != None else ""),
        # "||",
        color=discord.Color.blue())
    embed.set_author(name="HaruBot", url="https://github.com/davidrezende",
                     icon_url="https://yt3.ggpht.com/ytc/AAUvwnjEgzJBHFJKcDdmdF6Y4aHnmUMCJhsmVPnCHYYEQQ=s900-c-k-c0x00ffffff-no-rj")

    if not (response.get('thumbnail') is None):
        embed.set_thumbnail(url=response['thumbnail'])
    else:
        ''
    if not (response.get('image') is None):
        embed.set_image(url=response['image'])
    else:
        ''
    for key, value in response.items():
        if (key != "dat_last_modified" and key != "thumbnail" and key != "dat_creation" and key != "image"):
            embed.add_field(name="**"+key.upper()+"**",
                            value=value, inline=False)

    # embed.add_field(name="*Italics*", value="Surround your text in asterisks (\*)", inline=False)
    # embed.add_field(name="**Bold**", value="Surround your text in double asterisks (\*\*)", inline=False)
    # embed.add_field(name="__Underline__", value="Surround your text in double underscores (\_\_)", inline=False)
    # embed.add_field(name="~~Strikethrough~~", value="Surround your text in double tildes (\~\~)", inline=False)
    # embed.add_field(name="`Code Chunks`", value="Surround your text in backticks (\`)", inline=False)
    # embed.add_field(name="Blockquotes", value="> Start your text with a greater than symbol (\>)", inline=False)
    # embed.add_field(name="Secrets", value="||Surround your text with double pipes (\|\|)||", inline=False)
    embed.set_footer(text="Made with ❤️ by https://github.com/davidrezende")
    return embed


def embedNotes(ctx, response: str):
    response = response.replace("\'", "\"")
    response = json.loads(response)
    print('json',response)
    embed = discord.Embed(
        title="List of yours notes",
        color=discord.Color.blue())
    embed.set_author(name="HaruBot", url="https://github.com/davidrezende",
                     icon_url="https://yt3.ggpht.com/ytc/AAUvwnjEgzJBHFJKcDdmdF6Y4aHnmUMCJhsmVPnCHYYEQQ=s900-c-k-c0x00ffffff-no-rj")
    for note in response:
        embed.add_field(name="**"+note+"**", value='*created in: '+response[note]['dat_creation']+'*', inline=False)
    embed.set_footer(text="Made with ❤️ by https://github.com/davidrezende")
    return embed

def validateWhenAddOrUpdateFieldsEmbed(category: str, categoryText: str):
    if category in ['image', 'thumbnail']:
        print('validating embeded fields')
        if categoryText.startswith("https://") and categoryText.__contains__(".") and (len(categoryText) - categoryText.index(".")) > 2:
            return True
        else:
            return False
    else:
        return True


def saveNote(ctx, nameNote, category, categoryText):
    queryUserExists = {"id_user": ctx.author.id}
    userExists = collection.count_documents(queryUserExists)
    if(userExists <= 0):
        post = {"id_user": ctx.author.id, "dat_creation": datetime.today().replace(microsecond=0), "notes": { nameNote: { category: categoryText, "dat_creation": datetime.today().replace(microsecond=0)}}}
        collection.insert_one(post)
        return '> **' + ctx.author.name + ' congratulations!** You have created your first note: **' + nameNote + '**.\n**Helpful commands:** \n!show <note>\n!add <note> <new_category> <category_text>'
    else:
        queryNoteExists = {"id_user": ctx.author.id,
                           "notes"+"."+nameNote: {"$exists": True}}
        noteExists = collection.count_documents(queryNoteExists)
        if (noteExists <= 0):
            filter = {"id_user": ctx.author.id}
            newvalues = {"$set": {"notes"+"."+nameNote+"."+category: categoryText, "notes"+"."+nameNote+"."+"dat_creation": datetime.today().replace(microsecond=0)}}
            collection.update_one(filter, newvalues)
            return '> ' + nameNote + ' saved.'
        else:
            queryNoteCategoryExists = {
                "id_user": ctx.author.id, "notes"+"."+nameNote+"."+category: {"$exists": True}}
            noteCategoryExists = collection.count_documents(
                queryNoteCategoryExists)
            if(noteCategoryExists <= 0):
                filter = {"id_user": ctx.author.id,
                          "notes"+"."+nameNote+"."+category: {"$exists": False}}
                newvalues = {"$set": {"notes"+"."+nameNote+"."+category: categoryText, "notes"+"."+nameNote+"."+"dat_last_modified": datetime.today().replace(microsecond=0)}}
                collection.update_one(filter, newvalues)
                return '> Note **' + nameNote + '** updated with new category **' + category + '**.'
            else:
                return '> Your note **' + nameNote + '** already exists with category **' + category + '**. \n**Suggestion:**\n!edit <note> <category> <text-from-category>'


def deleteNoteOrCategory(ctx, nameNote, category):
    queryUserExists = {"id_user": ctx.author.id}
    userExists = collection.count_documents(queryUserExists)
    if(userExists <= 0):
        return "> You don't have any notes created. Start by creating your first note.\n+**Helpful commands:** \n!show <note>\n!add <note> <new_category> <category_text>"
    else:
        queryNoteExists = {"id_user": ctx.author.id,
                           "notes"+"."+nameNote: {"$exists": True}}
        noteExists = collection.count_documents(queryNoteExists)
        if (noteExists <= 0):
            return '> **' + nameNote + '** does not exists!\n+**Helpful commands:** \n!show <note>\n!add <note> <new_category> <category_text>'
        else:
            if category is None:
                filter = {"id_user": ctx.author.id}
                newvalues = {"$unset":{"notes"+"."+nameNote:""}}
                collection.update_one(filter, newvalues)
                return 'Note **' + nameNote  + '** deleted.'
            else:
                queryNoteCategoryExists = {"id_user": ctx.author.id, "notes"+"."+nameNote+'.'+category: {"$exists": True}}
                noteCategoryExists = collection.count_documents(
                    queryNoteCategoryExists)
                if(noteCategoryExists <= 0):
                    return '> Category **' + category + '** does not exists.'
                else:
                    filter = queryNoteCategoryExists
                    newvalues = {"$unset": {"notes"+"."+nameNote+'.'+category:""}}
                    collection.update_one(filter, newvalues)
                    return '> Category **' + category + '** deleted with success from **' + nameNote + '**.'


def editNote(ctx, nameNote, category, categoryText):
    queryUserExists = {"id_user": ctx.author.id}
    userExists = collection.count_documents(queryUserExists)
    if(userExists <= 0):
        return "> You don't have any notes created. \n**Helpful commands:** \n!add <note> <new_category> <category_text> \n!show <note>"
    else:
        queryNoteExists = {"id_user": ctx.author.id,
                           "notes"+"."+nameNote: {"$exists": True}}
        noteExists = collection.count_documents(queryNoteExists)
        if (noteExists <= 0):
            return '> Note **'+nameNote+'** does not exists. \n**Helpful commands:** \n!show <note>\n!add <note> <new_category> <category_text>'
        else:
            queryNoteCategoryExists = {"id_user": ctx.author.id, "notes"+"."+nameNote+'.'+category: {"$exists": True}}
            noteCategoryExists = collection.count_documents(queryNoteCategoryExists)
            if(noteCategoryExists <= 0):
                return '> Your note **' + nameNote + '** does not have this category **' + category + '**. \n**Helpful commands:** \n!show <note>\n!add <note> <new_category> <category_text>'
            else:
                filter = {"id_user": ctx.author.id,
                          "notes"+"."+nameNote+'.'+category: {"$exists": True}}
                newvalues = {"$set": { "notes"+"."+nameNote+'.'+category: categoryText, "notes"+"."+nameNote +
                                      '.'+"dat_last_modified": datetime.today().replace(microsecond=0)}}
                collection.update_one(filter, newvalues)
                return '> Note **' + nameNote + '** updated with **success** with category **' + category + '**! \n**Suggestion:** \n!show <note>'

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
