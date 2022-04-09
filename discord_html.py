"""

Copyright (c) [2022] [Elon Duck]

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

"""


from itertools import cycle
from pyquery import PyQuery as pq
import sys

import asyncio
import discord
from discord.ext import commands, tasks

if len(sys.argv) != 2:
    sys.exit()

doc = pq(filename=sys.argv[1])


# Parser components

def list_presences(doc):
    presences = doc("title")
    return [x.text for x in presences]


def list_commands(doc):
    commands = doc.items("h1")
    cmds = dict()
    for cmd in commands:
        cmds[cmd.attr("id")] = cmd.text()
    return cmds


def list_token(doc):
    token = doc("meta[name='token']")
    return token.attr("content")

# The bot itself


PREFIX = "-"


client = commands.Bot(command_prefix=PREFIX)

presences = list_presences(doc)
commands = list_commands(doc)
token = list_token(doc)

presences_cycle = cycle(list_presences(doc))

@tasks.loop(seconds=30)
async def presence_loader():
    if client.is_ready():
        if len(presences) > 0:
            await client.change_presence(activity=discord.Game(next(presences_cycle)))

@client.event
async def on_message(msg):
    if msg.content.startswith(PREFIX):
        content = msg.content.replace(PREFIX, '')
        if content in commands:
            return await msg.channel.send(commands[content])


presence_loader.start()
client.run(token)
