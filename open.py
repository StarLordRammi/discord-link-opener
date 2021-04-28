import webbrowser
import asyncio
import discord
from discord.ext.commands import Bot
from discord.ext import commands
import re

client = Bot('adawd@@#^^')
client.remove_command('help')


keywords = ['xxxxxxxxx']
channels = ['xxxxxxxxx','xxxxxxxxx']
token = 'xxxxxxxxxx'

global start_count
start_count = 0

async def check_urls(urls):
           for url in urls:
               for keyword in keywords:
                   if keyword in url.lower():
                       webbrowser.get().open(url)
                       #print(f'Opened {keyword}')

@client.event
async def on_message(message):
    global start_count
    if start_count == 0:
        print('\n{} is waiting for drops.\n'.format(str(client.user)))
        if len(keywords) >= 1 and keywords[0] != '':
            print('Watching for keywords {}.\n'.format(', '.join(keywords)))
        else:
            print('No keywords have been provided.\n')
        start_count += 1
    else:
        if message.channel.id in channels:
            if message.embeds:
                for embed in message.embeds:
                    toembed = embed.to_dict()
                    if str(toembed['type']).lower() != 'link':
                        urls = re.findall("(?:(?:https?|ftp):\/\/|\b(?:[a-z\d]+\.))(?:(?:[^\s()<>]+|\((?:[^\s()<>]+|(?:\([^\s()<>]+\)))?\))+(?:\((?:[^\s()<>]+|(?:\(?:[^\s()<>]+\)))?\)|[^\s`!()\[\]{};:'.,<>?«»“”‘’]))?",toembed['title'])
                        if urls:
                            await check_urls(urls)
                        try:
                            urls2 = re.findall("(?:(?:https?|ftp):\/\/|\b(?:[a-z\d]+\.))(?:(?:[^\s()<>]+|\((?:[^\s()<>]+|(?:\([^\s()<>]+\)))?\))+(?:\((?:[^\s()<>]+|(?:\(?:[^\s()<>]+\)))?\)|[^\s`!()\[\]{};:'.,<>?«»“”‘’]))?",toembed['description'])
                            if urls2:
                                await check_urls(urls2)
                        except:
                            pass
                        try:
                            for field in toembed['fields']:
                                urls3 = re.findall("(?:(?:https?|ftp):\/\/|\b(?:[a-z\d]+\.))(?:(?:[^\s()<>]+|\((?:[^\s()<>]+|(?:\([^\s()<>]+\)))?\))+(?:\((?:[^\s()<>]+|(?:\(?:[^\s()<>]+\)))?\)|[^\s`!()\[\]{};:'.,<>?«»“”‘’]))?",str(field))
                                if urls3:
                                    await check_urls(urls3)
                        except:
                            pass
            if message.content != '':
                print(message.content)
                urls4 = re.findall("(?:(?:https?|ftp):\/\/|\b(?:[a-z\d]+\.))(?:(?:[^\s()<>]+|\((?:[^\s()<>]+|(?:\([^\s()<>]+\)))?\))+(?:\((?:[^\s()<>]+|(?:\(?:[^\s()<>]+\)))?\)|[^\s`!()\[\]{};:'.,<>?«»“”‘’]))?",message.content)
                if urls4:
                    await check_urls(urls4)

client.run(token,bot=False)
