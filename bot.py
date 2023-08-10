from discord import app_commands
import discord
import os
import random
import editor

bot = discord.Client(intents=discord.Intents.default())

tree = app_commands.CommandTree(bot)

# async def confirm(message):
# 	await message.add_reaction('👍')

size = [0, 0, 197, 182, 132, 84]

rolled_level = ""
rolled_point_index = ""

channel_id = 1130498794123960450
final_channel_id = 1129059787724836894

@bot.event
async def on_message(msg):
    global rolled_point_index, rolled_level
    if msg.author.id == 115703582426136580 or msg.author.id == 180770835018153994:
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

        if msg.content.split(' ')[0] == 'publish-test':
            additional = msg.content.split(' ', 1)[1] if len(msg.content.split(' ', 1)) > 1 else ""
            channel = await bot.fetch_channel(channel_id)
            links_file = open(f'N{rolled_level}.txt')
            link = links_file.readlines()[rolled_point_index-1]
            img = open(f'N{rolled_level}/{rolled_point_index}.png', 'rb')
            await channel.send(f"<@&1129067149776928808>\nThe Bingo Grammar Point for today has been rolled!\n{additional}\nPost your submissions in the channel <#1129059458824278026>\nCheck out the link below for more information about the grammar point : {link}", file=discord.File(img))
        
        if msg.content.split(' ')[0] == 'publish-final':
            additional = msg.content.split(' ', 1)[1] if len(msg.content.split(' ', 1)) > 1 else ""
            channel = await bot.fetch_channel(final_channel_id)
            links_file = open(f'N{rolled_level}.txt')
            link = links_file.readlines()[rolled_point_index-1]
            img = open(f'N{rolled_level}/{rolled_point_index}.png', 'rb')
            await channel.send(f"<@&1129067149776928808>\nThe Bingo Grammar Point for today has been rolled!\n{additional}\nPost your submissions in the channel <#1129059458824278026>\nCheck out the link below for more information about the grammar point : {link}", file=discord.File(img))


# EVENT LISTENER FOR WHEN THE BOT HAS SWITCHED FROM OFFLINE TO ONLINE.
@bot.event
async def on_ready():
    await tree.sync()
    print("Ready!")

f = open('token.txt')
bot.run(f.read())