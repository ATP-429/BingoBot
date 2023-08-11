from discord import app_commands

import datetime
import pytz

import discord
import os
import random
from editor import Editor

bot = discord.Client(intents=discord.Intents.default())

tree = app_commands.CommandTree(bot)

# async def confirm(message):
# 	await message.add_reaction('👍')

size = [0, 0, 197, 182, 132, 84]

rolled_level = ""
rolled_point_index = ""

channel_id = 1130498794123960450
final_channel_id = 1129059787724836894
submissions_channel_id = 1129059458824278026

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
        
        if msg.content.split(' ')[0] == 'count':
            date_str = msg.content.split(' ', 1)[1]
            try:
                editor = Editor()
                dates_dict = editor.get_dates_dict()
                if date_str in dates_dict:
                    start_time = datetime.datetime.strptime(date_str, "%d/%m/%y").astimezone(pytz.timezone('Europe/Lisbon')).replace(hour=20, minute=0) + datetime.timedelta(hours=24)
                    end_time = start_time + datetime.timedelta(hours=24)
                    channel = await bot.fetch_channel(submissions_channel_id)

                    async for submission in channel.history(limit=100, before=end_time, after=start_time):
                        for reaction in submission.reactions:
                            if reaction.emoji == '⭐':
                                async for user in reaction.users():
                                    if user.id == 738469919800295584:
                                        editor.set(str(submission.author), date_str)
                                        await msg.channel.send(f"Counted submission for {submission.author}")

                    await msg.channel.send(f"Start={start_time}, end={end_time}")
                else:
                    await msg.channel.send(f"Please enter a date that belongs to one of the bingo dates")
            except ValueError:
                await msg.channel.send(f"Please enter a proper date time")



# EVENT LISTENER FOR WHEN THE BOT HAS SWITCHED FROM OFFLINE TO ONLINE.
@bot.event
async def on_ready():
    await tree.sync()
    print("Ready!")

f = open('token.txt')
bot.run(f.read())