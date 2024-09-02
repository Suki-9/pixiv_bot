import discord
from discord import app_commands

client = discord.Client(intents=discord.Intents.all()) 
tree = app_commands.CommandTree(client)

import bot.command
import bot.event
