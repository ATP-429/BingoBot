from discord import app_commands
import discord
import os
import random

bot = discord.Client(intents=discord.Intents.default())

tree = app_commands.CommandTree(bot)

# async def confirm(message):
# 	await message.add_reaction('👍')

size = [0, 0, 197, 182, 132, 84]

rolled_level = ""
rolled_point_index = ""

@bot.event
async def on_message(msg):
    global rolled_point_index, rolled_level
    if msg.content == 'roll':
        level = random.randint(2, 5)
        n = size[level]
        point_index = random.randint(1, n)
        links_file = open(f'N{level}.txt')
        link = links_file.readlines()[point_index-1]
        img = open(f'N{level}/{point_index}.png', 'rb')

        rolled_level = level
        rolled_point_index = point_index

        channel = msg.channel
        await channel.send(f"{link}", file=discord.File(img))

    if msg.content == 'publish':
        channel = await bot.fetch_channel('1098615520447709247')
        links_file = open(f'N{rolled_level}.txt')
        link = links_file.readlines()[rolled_point_index-1]
        img = open(f'N{rolled_level}/{rolled_point_index}.png', 'rb')
        await channel.send(f"{link}", file=discord.File(img))


# EVENT LISTENER FOR WHEN THE BOT HAS SWITCHED FROM OFFLINE TO ONLINE.
@bot.event
async def on_ready():
    await tree.sync()
    print("Ready!")

f = open('token.txt')
bot.run(f.read())