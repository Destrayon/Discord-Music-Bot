import discord
import youtube_dl
from discord.ext import commands
import os
import re
import time
import asyncio

import random

client = commands.Bot(command_prefix='.')

list = []

queued_list = []

path = "C:/Users/Diviel/Desktop/DiscordMusic"

songs = os.listdir(path)

current_song = ""

max_size = 0

default_size = 3

token = os.environ.get("DIS_TOKEN")


def queue_song():
    i = Random()
    return songs[i]


def select_song():
    num = queued_list[0]
    queued_list.pop(0)
    return num


def find_song_num(string: str):
    for song in range(0, len(songs) - 1):
        if string.lower() in songs[song].lower():
            queued_list.append(song)
            return song
    return -1


def Enqueue(value):
    list.insert(max_size, value)


def Dequeue():
    list.pop(0)


def Queue(num):
    if len(list) < max_size:
        list.append(num)
    else:
        Enqueue(num)
        Dequeue()


def Random():
    if len(queued_list) > 0:
        return select_song()
    random.seed()
    number = random.randint(0, len(songs) - 1)

    while number in list:
        number = random.randint(0, len(songs) - 1)

    Queue(number)

    return number


@client.event
async def on_ready():
    print("Bot is ready.")


@client.command(aliases=['p'])
async def pause(context):
    global songs
    songs = os.listdir(path)
    voice = discord.utils.get(client.voice_clients, guild=context.guild)
    if not voice.is_paused():
        await context.send(f"**Pausing:** `{current_song}`**!** :musical_note:")
        time.sleep(.5)
        voice.pause()
    else:
        await context.send("**The bot is already paused! Please type .resume to resume or .stop to stop!**")


@client.command(aliases=['s'])
async def skip(context):
    global songs
    songs = os.listdir(path)
    voice = discord.utils.get(client.voice_clients, guild=context.guild)
    await context.send(f"**Skipping:** `{current_song}`**!** :musical_note:")
    time.sleep(.5)
    voice.stop()


@client.command(aliases=['r', 'res'])
async def resume(context):
    global songs
    songs = os.listdir(path)
    voice = discord.utils.get(client.voice_clients, guild=context.guild)
    if voice.is_paused():
        await context.send(f":musical_note:**Resuming:** `{current_song}`**!** :musical_note:")
        time.sleep(.5)
        voice.resume()
    else:
        await context.send("**The bot is not paused! Please type .pause to pause or .stop to stop!**")


@client.command(aliases=['play', 'st'])
async def start(context, num=default_size):
    global songs
    songs = os.listdir(path)
    global max_size
    channel = context.message.author.voice.channel
    voice = discord.utils.get(client.voice_clients, guild=context.guild)

    if voice and voice.is_connected():
        await voice.move_to(channel)
    else:
        voice = await channel.connect()

    async def playing():
        global current_song
        song = queue_song()
        voice.play(discord.FFmpegPCMAudio(path + "/" + song), after=lambda e: after())
        current_song = re.sub('\.mp3', '', song)
        await context.send(f"**Now playing:** `{current_song}`**!** :musical_note:")

    def after():
        time.sleep(1)
        coro = playing()
        fut = asyncio.run_coroutine_threadsafe(coro, client.loop)
        try:
            fut.result()
        except:
            pass

    if not voice.is_playing() and not voice.is_paused():
        await playing()
        if num > 1:
            max_size = num
    else:
        await context.send("**The bot is already playing! Please type .stop or .resume if the bot is not working!**")


@client.command()
async def stop(context):
    global songs
    songs = os.listdir(path)
    global queued_list
    voice = discord.utils.get(client.voice_clients, guild=context.guild)
    if voice and voice.is_connected():
        queued_list = []
        await voice.disconnect()
    else:
        await context.send("**The bot is not in a channel.**")


@client.command()
async def kick(context, member: discord.Member, *, reason=None):
    author = context.message.author
    role = discord.utils.get(author.guild.roles, name='Administrators')
    if role in author.roles:
        other_role = discord.utils.get(member.guild.roles, name='Administrators')

        if other_role in member.roles:
            await context.send("You cannot kick an admin.")
        else:
            await member.kick(reason=reason)
            await context.send(f'Kicked {member.mention}')
    else:
        await context.send("You cannot use this command.")


@client.command()
async def ban(context, member: discord.Member, *, reason=None):
    author = context.message.author
    role = discord.utils.get(author.guild.roles, name='Administrators')
    if role in author.roles:
        other_role = discord.utils.get(member.guild.roles, name='Administrators')

        if other_role in member.roles:
            await context.send("You cannot kick an admin.")
        else:
            await member.ban(reason=reason)
            await context.send(f'Kicked {member.mention}')
    else:
        await context.send("You cannot use this command.")


@client.command()
async def channel(context):
    embed = discord.Embed(
        title="Diviel's Youtube.",
        description="Youtube videos.",
        colour=discord.Colour.purple()
    )
    embed.url = "https://www.youtube.com/user/PewDiePie"
    embed.set_footer(text='Go and subscribe here!')
    embed.set_image(
        url="https://cdn.discordapp.com/attachments/270411403729436688/609517176734351360/20190109_194208.jpg")
    embed.set_thumbnail(
        url="https://cdn.discordapp.com/attachments/270411403729436688/609517176734351360/20190109_194208.jpg")
    embed.set_author(name="Diviel",
                     icon_url="https://cdn.discordapp.com/attachments/270411403729436688/609517176734351360/20190109_194208.jpg")
    embed.add_field(name="Field Name", value="Field Value", inline=False)
    embed.add_field(name="Field Name", value="Field Value", inline=True)
    embed.add_field(name="Field Name", value="Field Value", inline=True)
    embed.add_field(name="Field Name", value="Field Value", inline=True)

    await context.send(embed=embed)


@client.command()
async def mute(context, member: discord.Member, *, reason=None):
    role = discord.utils.get(member.guild.roles, name='Muted')

    await member.add_roles(role)
    await context.send(f'{member.mention} is now muted!')


@client.command()
async def update(context):
    def downloading(context):
        ydl_opts = {
            'format': 'bestaudio/best',
            'outtmpl': 'C:\\Users\\Diviel\\Desktop\\DiscordMusic\\%(title)s.%(ext)s',
            'download_archive': 'C:\\Users\\Diviel\\Desktop\\DiscordMusic\\download.txt',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
        }

        try:
            with youtube_dl.YoutubeDL(ydl_opts) as ydl:
                ydl.download(["https://www.youtube.com/playlist?list=PLSoEDOPi-alj8GZZxRx6Pdsgt4-TcqaEm"])
        except:
            print("Having some issues. Gonna try again.")
            time.sleep(5)
            downloading(context)

    await context.send("**Updating playlist...**")
    downloading(context)
    await context.send("**Playlist updated!**")

    songs = os.listdir(path)


@client.command()
async def download(context, url: str):
    global songs

    def downloading(context, url: str):
        ydl_opts = {
            'format': 'bestaudio/best',
            'outtmpl': 'C:\\Users\\Diviel\\Desktop\\DiscordMusic\\%(title)s.%(ext)s',
            'download_archive': 'C:\\Users\\Diviel\\Desktop\\DiscordMusic\\download.txt',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
        }
        try:
            with youtube_dl.YoutubeDL(ydl_opts) as ydl:
                ydl.download([url])
        except:
            print("Having some issues. Gonna try again.")
            time.sleep(5)
            downloading(context, url)

    context.send("**Downloading song or playlist...**")
    downloading(context, url)
    context.send("**Download finished!**")

    songs = os.listdir(path)


@client.command()
async def queue(context, *, string: str):
    global songs
    songs = os.listdir(path)
    num = find_song_num(string)

    if num > -1:
        song = re.sub('\.mp3', '', songs[num])
        await context.send(f"**Queueing:** `{song}`**!** :musical_note: \n**Place in queue: {len(queued_list)}**")
    else:
        await context.send("**Could not find the requested song. Please try again!**")


@client.command(aliases=["songs"])
async def song_list(context):
    global songs
    songs = os.listdir(path)
    with open("list.txt", 'w', encoding="utf-8") as f:
        content = ""
        num = 1
        for song in songs:
            song2 = re.sub('\.mp3', '', song)
            content = f"{num}. {content}{num}. {song2}\n"
            num = num + 1
        f.write(content)
        file = discord.File("list.txt", filename="list.txt")
        await context.send("", file=file)


@client.command()
async def clear(context):
    global queued_list

    queued_list = []

    await context.send("**Queue has been cleared!**")


client.run(token) #Put your bot token in here.