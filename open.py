import webbrowser
import asyncio
import discord
from discord.ext.commands import Bot
from discord.ext import commands
import re

'''
by cleary#6546 // @preorderd
'''

#pylint: disable=anomalous-backslash-in-string

client = Bot('adawd@@#^^')
client.remove_command('help')

#prompt user enter keywords to check for in links
keywords = list(map(str,input("Enter keywords seperated by space: ").split()))

#prompt user to enter negative keywords that will prevent a browser window from opening to have no blacklisted words, press enter right away
blacklist = list(map(str,input("Enter blacklisted keywords seperated by space: ").split()))

#enter channel id(s) where links would be picked up (monitor channel id) seperated by commas. these should be ints
channels = []

#enter token of discord account that has access to watch specified channels
token = ''

global start_count
start_count = 0

#check for keywords and blacklisted words in message urls and open browser if conditions are met
async def check_urls(urls):
    for url in urls:
        if any(x in url.lower() for x in keywords) and all(x not in url.lower() for x in blacklist):
            #enter path to chrome here, for windows 10, this should work
            webbrowser.get("C:/Program Files (x86)/Google/Chrome/Application/chrome.exe %s").open(url)
            print(f'Opened {url}')

@client.event
async def on_message(message):
    global start_count
    # temporary bypass to weird d.py cacheing issue
    # only print this info on the first time the client launches. this is due to d.py calling on_ready() after the bot regains connection
    if start_count == 0:
        print('\n{} is ready to cop some restocks.\n'.format(str(client.user)))
        if len(keywords) >= 1 and keywords[0] != '':
            print('Watching for keywords {}.\n'.format(', '.join(keywords)))
        else:
            print('No keywords have been provided.\n')
        if len(blacklist) > 0:
            print('Ignoring keywords {}.\n'.format(', '.join(blacklist)))
        else:
            print('No keywords currently blacklisted.\n')
        start_count += 1
    else:
        if message.channel.id in channels:
            if message.embeds:
                for embed in message.embeds:
                    toembed = embed.to_dict()
                    if str(toembed['type']).lower() != 'link':
                        try:
                            for field in toembed['fields']:
                                urls = re.findall("(?:(?:https?|ftp)://)?[\w/-?=%.#&+]+.[\w/-?=%.#&+]+",str(field))
                                if urls:
                                    await check_urls(urls)
                        except:
                            pass
            if message.content != '':
                urls = re.findall("(?:(?:https?|ftp)://)?[\w/-?=%.#&+]+.[\w/-?=%.#&+]+",message.content)
                if urls:
                    await check_urls(urls)

client.run(token,bot=False)
