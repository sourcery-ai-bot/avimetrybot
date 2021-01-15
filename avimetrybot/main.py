import discord
import os
import asyncio
import json
import datetime
import pymongo
from pymongo import MongoClient
from discord.ext import commands, tasks
from dotenv import load_dotenv
from utils.mongo import Document
import motor.motor_asyncio

#Get Bot Token
load_dotenv()
avitoken = os.getenv('Bot_Token')

ccluster=MongoClient(os.getenv('DB_Token'))
cdb=ccluster['avimetry']
ccollection=cdb['new']

#Command Prefix and Intents
async def prefix(client, message):
    if not message.guild:
        return [str("a.")]
    try:
        data=await avimetry.config.find(message.guild.id)
        if not data or "prefix" not in data:
            return "a."
        return data["prefix"]
    except:
        return "a."
avimetry = commands.Bot(command_prefix = prefix, case_insensitive=True, intents=discord.Intents.all())
avimetry.launch_time=datetime.datetime.utcnow()

#Database 
avimetry.cluster=MongoClient(os.getenv('DB_Token'))
avimetry.db=avimetry.cluster['avimetry']
avimetry.collection=avimetry.db['new']
avimetry.mutes=avimetry.collection.find_one({"_id":"mutes"})
avimetry.muted_users={}


#No Commands in DMs
@avimetry.check
async def globally_block_dms(ctx):
    return ctx.guild is not None

#Reload main cogs 
@tasks.loop(minutes=5)
async def load_important():
    try:
        avimetry.load_extension('jishaku')
        avimetry.load_extension("cogs.loads")
    except commands.ExtensionAlreadyLoaded:
        return
load_important.start()

@avimetry.event
async def on_ready():
    avimetry.mongo = motor.motor_asyncio.AsyncIOMotorClient(os.getenv('DB_Token'))
    avimetry.db=avimetry.mongo['avimetry']
    avimetry.config=Document(avimetry.db, 'new')
    for yes in await avimetry.config.get_all():
        print(yes)


#Load Cogs
avimetry.load_extension('jishaku')
os.environ["JISHAKU_HIDE"] = "True"
os.environ["JISHAKU_NO_UNDERSCORE"] = "True"
os.environ["JISHAKU_NO_DM_TRACEBACK"] = "True" 
for filename in os.listdir('./avimetrybot/cogs'):
    if filename.endswith('.py'):
        avimetry.load_extension(f'cogs.{filename[:-3]}')

#Log-In
avimetry.run(avitoken)