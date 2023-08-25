from discord import app_commands
from discord.ext import tasks

import asyncio
import threading
import time
import datetime
import pytz

import discord
import os
import random
from editor import Editor

bot = discord.Client(intents=discord.Intents.all())

tree = app_commands.CommandTree(bot)

# async def confirm(message):
# 	await message.add_reaction('👍')

size = [0, 180, 210, 217, 177, 39]

rolled_level = ""
rolled_point_index = ""

channel_id = 1130498794123960450
final_channel_id = 1129059787724836894
submissions_channel_id = 1129059458824278026

KAFKA = 115703582426136580
AARYASH = 180770835018153994
TIMMY = 738469919800295584
PATH = 277657928062992395

PUBLISH_TEST_HOUR = 19
PUBLISH_TEST_MINUTE = 30

PUBLISH_FINAL_HOUR = 20
PUBLISH_FINAL_MINUTE = 0

COUNT_HOUR = 20
COUNT_MINUTE = 5

probs = [0.15, 0.40, 0.30, 0.10, 0.05]

def get_days_since_epoch():
    return (datetime.datetime.now().astimezone(pytz.timezone('Europe/Lisbon')) - datetime.datetime.strptime('17/07/23', "%d/%m/%y").astimezone(pytz.timezone('Europe/Lisbon')).replace(hour=PUBLISH_TEST_HOUR, minute=PUBLISH_TEST_MINUTE)).days-1

async def roll():
    global rolled_point_index, rolled_level
    level = 0
    
    rand = random.uniform(0, 1)
    if rand < probs[0]:
        level = 5
    elif rand < probs[0]+probs[1]:
        level = 4
    elif rand < probs[0]+probs[1]+probs[2]:
        level = 3
    elif rand < probs[0]+probs[1]+probs[2]+probs[3]:
        level = 2
    else:
        level = 1

    n = size[level]
    point_index = random.randint(1, n)
    links_file = open(f'N{level}.txt')
    link = links_file.readlines()[point_index-1]

    done_links_file = open('done.txt')
    done_links = done_links_file.readlines()

    if link in done_links:  # If link is already done, reroll
        await roll()
        return

    rolled_level = level
    rolled_point_index = point_index

async def publish_test():
    channel = await bot.fetch_channel(channel_id)
    links_file = open(f'N{rolled_level}.txt')
    link = links_file.readlines()[rolled_point_index-1]

    days_since_epoch = get_days_since_epoch()
    
    month_no = days_since_epoch//28
    week_no = (days_since_epoch-month_no*28)//7
    day_no = days_since_epoch-month_no*28-week_no*7

    await channel.send(f"|| <@&1129067149776928808> ||\nThe [Bingo Grammar Point]({link}) for today has been rolled!\nMonth {month_no+1} - Week {week_no+1} - Day {day_no+1}\n\nPost your submissions in the channel <#1129059458824278026>\n\nGood Luck!")

async def publish_final():
    channel = await bot.fetch_channel(final_channel_id)
    links_file = open(f'N{rolled_level}.txt')
    link = links_file.readlines()[rolled_point_index-1]

    f = open('done.txt', 'a')
    f.write(link)

    days_since_epoch = get_days_since_epoch()
    
    month_no = days_since_epoch//28
    week_no = (days_since_epoch-month_no*28)//7
    day_no = days_since_epoch-month_no*28-week_no*7

    await channel.send(f"|| <@&1129067149776928808> ||\nThe [Bingo Grammar Point]({link}) for today has been rolled!\nMonth {month_no+1} - Week {week_no+1} - Day {day_no+1}\n\nPost your submissions in the channel <#1129059458824278026>\n\nGood Luck!")

async def count(date_str, output_channel):
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
                        if user.id == KAFKA or user.id == AARYASH or user.id == TIMMY or user.id == PATH:
                            editor.set(str(submission.author), date_str)
                            await output_channel.send(f"Counted submission for {submission.author}")

        await output_channel.send(f"Start={start_time}, end={end_time}")
    else:
        await output_channel.send(f"Please enter a date that belongs to one of the bingo dates in the sheet")


@bot.event
async def on_message(msg):
    global rolled_point_index, rolled_level
    if msg.author.id == KAFKA or msg.author.id == AARYASH or msg.author.id == TIMMY or msg.author.id == PATH:
        if msg.content == '!roll':
            await roll()
            channel = msg.channel
            links_file = open(f'N{rolled_level}.txt')
            link = links_file.readlines()[rolled_point_index-1]

            days_since_epoch = get_days_since_epoch()
            
            month_no = days_since_epoch//28
            week_no = (days_since_epoch-month_no*28)//7
            day_no = days_since_epoch-month_no*28-week_no*7

            await channel.send(f"Month {month_no+1} - Week {week_no+1} - Day {day_no+1} \n[Bunpro Link]({link})")

        if msg.content.split(' ')[0] == '!publish-test':
            await publish_test()
        
        if msg.content.split(' ')[0] == '!publish-final':
            await publish_final()
        
        if msg.content.split(' ')[0] == '!count':
            date_str = msg.content.split(' ', 1)[1]
            try:
                await count(date_str, msg.channel)
            except ValueError:
                await msg.channel.send(f"Please enter a proper date time")
        
        if msg.content.split(' ')[0] == '!today':
            editor = Editor()

            date = datetime.datetime.now().astimezone(pytz.timezone('Europe/Lisbon'))
            eight_pm = date.replace(hour=20, minute=0)
            if eight_pm > date:  # If 8pm has still not occured, it means we're on the next day hence go back one day. If 8pm has occured, it means we're still on the same day.
                date = date - datetime.timedelta(hours=24)
            date = datetime.datetime.strftime(date, "%d/%m/%y")

            score = editor.get(str(msg.author), date)
            await msg.channel.send(f"Your Today's Bingo Score is {score}")

@tasks.loop(seconds = 60) # repeat after every 60 seconds
async def checkTimeLoop():
    now = datetime.datetime.now().astimezone(pytz.timezone('Europe/Lisbon'))
    if now.hour==PUBLISH_TEST_HOUR and now.minute==PUBLISH_TEST_MINUTE:
        await roll()
        await publish_test()
    if now.hour==PUBLISH_FINAL_HOUR and now.minute==PUBLISH_FINAL_MINUTE:
        await publish_final()
    if now.hour==COUNT_HOUR and now.minute==COUNT_MINUTE:
        date = datetime.datetime.now().astimezone(pytz.timezone('Europe/Lisbon')) - datetime.timedelta(hours=24)
        date = datetime.datetime.strftime(date, "%d/%m/%y")
        channel = await bot.fetch_channel(channel_id)
        await count(date, channel)

# EVENT LISTENER FOR WHEN THE BOT HAS SWITCHED FROM OFFLINE TO ONLINE.
@bot.event
async def on_ready():
    #await tree.sync()
    checkTimeLoop.start()
    print("Ready!")

f = open('token.txt')
bot.run(f.read())
