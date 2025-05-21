import os
import subprocess

def delete_file(file_path):
    try:
        os.remove(file_path)
        return f"Deleted file: {file_path}"
    except FileNotFoundError:
        return f"File not found: {file_path}"
    except PermissionError:
        return f"Permission denied: {file_path}"
    except Exception as e:
        return f"Error deleting file {file_path}: {e}"

def run_shell_command(command):
    try:
        command = command.strip()
        if not command:
            return f"Current directory: {os.getcwd()}"

        if command.startswith("cd "):
            path = command[3:].strip()
            if not os.path.isdir(path):
                return f"No such directory: {path}"
            os.chdir(path)
            return f"Changed directory to: {os.getcwd()}"

        elif command.startswith("del ") or command.startswith("rm "):
            file_path = command.replace("del ", "").replace("rm ", "").strip()
            return delete_file(file_path)

        else:
            result = subprocess.run(command, shell=True, capture_output=True, text=True)
            return result.stdout if result.returncode == 0 else result.stderr

    except Exception as e:
        return f"Error: {e}"
