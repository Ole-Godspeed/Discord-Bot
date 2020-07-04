import discord
from discord.ext import commands
from discord.utils import get
import random
import os
import asyncio
import oleg_config

client = commands.Bot(command_prefix='.')


@client.event
async def on_ready():
    print('Bot Is Ready')


@client.command(aliases=['v','voic'])   # responses
async def voice(ctx, *args):
    await ctx.channel.purge(limit=1)
    await ctx.send(f'{" ".join(args)}')   # random.choice(list)


@client.command(aliases=['pic','pictur'])
async def picture(ctx, *args):
    await ctx.channel.purge(limit=1)
    if str(" ".join(args)) != '':
        await ctx.send(file=discord.File(" ".join(args)))
    else:
        await ctx.send(file=discord.File('gif.gif'))


@client.command(aliases=['rol'])
async def roll(ctx, number):
    try:
        await ctx.send(f'{number} dice face: {random.randint(1, int(number))}')
    except:
        await ctx.send('Write the number of dice faces ".roll 6"')
 
@client.command(aliases=['clr'])
#@commands.has_permissions(administrator=True)  # general permissions
async def clear(ctx, amount=1):
    await ctx.channel.purge(limit=amount+1)


@client.command(pass_context=True, aliases=['j', 'jo', 'joi'])
async def join(ctx):
    await ctx.channel.purge(limit=1)
    if ctx.message.author.voice:
        channel = ctx.message.author.voice.channel
        await channel.connect()
    await ctx.send('.manual - open manual')


@client.command(pass_context=True, aliases=['m', 'manua'])
async def manual(ctx):
    await ctx.channel.purge(limit=1)
    await ctx.send('Manual:\n' + '.join - joins channel; .manual - open manual; .shortcuts - command shortcuts;'
                   '\n.path (address) - set active folder path; .track (name) - add track from active path; .folder - add folder;'
                   '\n.start - start playlist; .next (idx) - next track (track idx); .previous - previous track;\n.pause; .play - resume;'
                   '\n.shuffleon; .shuffleoff; - turn on/off shuffle;\n.showlist (idx) - show playlist slice around current idx (idx); .clearlist;'
                   '\n.clear (x) - clear last message (x messages);\n.voice (x) - bot saying (x);'
                   '\n.picture (x) - drop file (file name + extension);\n.roll (x) - rolling dice (faces)')


@client.command(pass_context=True, aliases=['shortcut'])
async def shortcuts(ctx):
    await ctx.channel.purge(limit=1)
    await ctx.send('Shortcuts:\n' + '.join - .j; .manual - .m;\n.track - .t; .folder - .f;\n.start - .s; .next - .n; .previous - .pr; .pause - .p; .play - .pl;'
                   '\n.showlist - .pll, .sl; .clearlist - .clrl;\n.shuffleon - .shon; .shuffleoff - .shof;'
                   '\n.clear - .clr; .voice - .v; .picture - .pic;')


path_list = list()
@client.command(aliases=['pat'])
async def path(ctx, *args):
    await ctx.channel.purge(limit=1)
    await ctx.send(f'Current path: {" ".join(args)}')
    path_list.clear()
    path_list.append(" ".join(args))
    print(path_list)


playlist = list()
@client.command(aliases=['f','folde'])
async def folder(ctx, *args):
    await ctx.channel.purge(limit=1)
    await ctx.send(f'Folder is added: {" ".join(args)}')
    for song in os.listdir(" ".join(args)):
        if song[-4:] == '.mp3':
            playlist.append([" ".join(args), song[:-4]])  # - .mp3


playlist = list()
@client.command(aliases=['t', 'tr', 'trac'])
async def track(ctx, *args):
    await ctx.channel.purge(limit=1)
    await ctx.send(f'Track is added: {" ".join(args)}')
    playlist.append([path_list[0], " ".join(args)])


@client.command(aliases=['shon','sfon'])
async def shuffleon(ctx):
    await ctx.channel.purge(limit=1)
    shuffle[0] = 1
    await ctx.send('Shuffle is on')


@client.command(aliases=['shof','shoff','sfoff'])
async def shuffleoff(ctx):
    await ctx.channel.purge(limit=1)
    shuffle[0] = 0
    await ctx.send('Shuffle is off')


index_list = [0,0]
@client.command(aliases=['s', 'star'])
async def start(ctx, *args):
    await ctx.channel.purge(limit=1)
    voice = get(client.voice_clients)
    voice.stop()
    try:
        voice.play(discord.FFmpegPCMAudio(f'{playlist[0][0]}\{playlist[0][1]}.mp3'), after=myafter)
    except:
        await ctx.send('Maybe playlist is empty?')
    voice.source = discord.PCMVolumeTransformer(voice.source)
    voice.source.volume = 0.07
    await client.change_presence(status=discord.Status.idle, activity=discord.Game(playlist[0][1]))
    print(f'playing: 0) {playlist[0][0]}\{playlist[0][1]}.mp3')


def myafter(error):
    try:
        fut = asyncio.run_coroutine_threadsafe(playafter(), client.loop)
        fut.result()
    except Exception as e:
        print(e)


shuffle = [0]
async def playafter():
    index_list[1] = index_list[0]

    if shuffle[0] == 1:
        curr = index_list[0]
        while curr == index_list[0]:
            index_list[0] = random.choice(range(len(playlist)))
    else:
        index_list[0] += 1

    voice = get(client.voice_clients)
    try:
        voice.play(discord.FFmpegPCMAudio(f'{playlist[index_list[0]][0]}\{playlist[index_list[0]][1]}.mp3'), after=myafter)
    except:
        index_list[0] = 0
        voice.play(discord.FFmpegPCMAudio(f'{playlist[index_list[0]][0]}\{playlist[index_list[0]][1]}.mp3'), after=myafter)
    voice.source = discord.PCMVolumeTransformer(voice.source)
    voice.source.volume = 0.07
    await client.change_presence(status=discord.Status.idle, activity=discord.Game(playlist[index_list[0]][1]))     #status
    print(f'playing: {index_list[0]}) {playlist[index_list[0]][0]}\{playlist[index_list[0]][1]}.mp3')


@client.command(aliases=['n', 'nex'])
async def next(ctx, *args):
    await ctx.channel.purge(limit=1)
    if str(" ".join(args)) != '':
        if shuffle[0] == 1:
            shuffle[0] = 0
            await ctx.send('Shuffle is off')
        index_list[0] = int(" ".join(args))-1
    voice = get(client.voice_clients)
    voice.stop()


@client.command(aliases=['pr', 'previou'])
async def previous(ctx):
    await ctx.channel.purge(limit=1)
    index_list[0] = index_list[1]-1
    voice = get(client.voice_clients)
    if shuffle[0] == 1:
        shuffle[0] = 0
        await ctx.send('Shuffle is off')
    voice.stop()


@client.command(aliases=['p', 'paus'])
async def pause(ctx):
    await ctx.channel.purge(limit=1)
    voice = get(client.voice_clients)
    voice.pause()
    await ctx.send('Paused')


@client.command(aliases=['pl', 'pla'])
async def play(ctx):
    await ctx.channel.purge(limit=1)
    voice = get(client.voice_clients)
    voice.resume()
    await ctx.send('Resumed')


@client.command(aliases=['clrl', 'clearlis'])
async def clearlist(ctx):
    await ctx.channel.purge(limit=1)
    playlist.clear()
    await ctx.send('Playlist is empty')


@client.command(aliases=['sl', 'pll'])
async def showlist(ctx, *args):
    await ctx.channel.purge(limit=1)
    if playlist == []:
        await ctx.send('Playlist is empty')
    else:
        if str(" ".join(args)) != '':
            showindex = int(" ".join(args))
        else:
            showindex = index_list[0]
        if showindex < 0:
            showindex += len(playlist)
        if showindex > len(playlist) or showindex < 0:
            await ctx.send('Invalid index')
        elif len(playlist) < 21:
            await ctx.send(f'Playlist slice [{showindex-5}:{showindex-5} from {len(playlist)}]:\n' + "\n".join(str(elem) for elem in list(str(idx) + ') ' + track1[1] for idx, track1 in enumerate(
                playlist, 0))))
        else:
            if showindex < 5 and showindex >= 0:
                await ctx.send(f'Playlist slice [{showindex-5}:{showindex+5} from {len(playlist)}]:\n' + "\n".join(str(elem) for elem in list(str(idx) + ') ' + track1[1] for idx, track1 in enumerate(
                        playlist[showindex - 5:] + playlist[:showindex + 6], showindex-5))))
            elif showindex > len(playlist) - 5:
                await ctx.send(f'Playlist slice [{showindex-5}:{showindex+5} from {len(playlist)}]:\n' + "\n".join(str(elem) for elem in list(str(idx) + ') ' + track1[1] for idx, track1 in enumerate(
                        playlist[showindex - 6:] + playlist[:5 - len(playlist) + showindex], showindex-len(playlist)-6))))
            else:
                await ctx.send(f'Playlist slice [{showindex-5}:{showindex+5} from {len(playlist)}]:\n' + "\n".join(str(elem) for elem in list(str(idx) + ') ' + track1[1] for idx, track1 in enumerate(
                        playlist[showindex - 5:showindex + 6], showindex-5))))


client.run(oleg_config.MyToken)