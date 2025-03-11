import discord
from discord.ext import commands
import socket
from discord.utils import get

# Create a bot instance with appropriate intents
intents = discord.Intents.default()
intents.messages = True
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)
hostname = socket.gethostname().lower()
def is_correct_channel(ctx):
    return ctx.channel.name == hostname

@bot.event
async def on_ready():
    
    if is_correct_channel:
        for guild in bot.guilds:
            channel = get(guild.text_channels, name=hostname)
        # Get the channel by name
        if channel:
            await channel.send("Hello! The bot is now online and sending a message here. 🚀")

@bot.event
async def show_message(message):
    print(message.content)
bot.run("MTIyNTM4MDkyNzYzMTUyMzk0MA.GWC_96.VITD_ajUnWf33cVPbYhTEoyYV5x-9EeIb1lzjE")