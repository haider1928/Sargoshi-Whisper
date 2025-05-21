import os
import subprocess

def run_shell_command(command):
    try:
        if command.startswith("cd "):
            path = command.replace("cd ", "").strip()
            os.chdir(path)
            return f"Changed directory to: {os.getcwd()}"
        else:
            result = subprocess.run(command, shell=True, capture_output=True, text=True)
            return result.stdout if result.returncode == 0 else result.stderr
    except Exception as e:
        return f"Error: {e}"
