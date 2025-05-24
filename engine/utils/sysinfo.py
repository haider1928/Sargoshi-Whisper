import requests
import platform
import socket
import psutil
import os
import json

class SystemInfo:
    def __init__(self):
        self.system_info = {
            "OS": platform.system(),
            "OS Version": platform.version(),
            "Architecture": platform.architecture()[0],
            "Hostname": socket.gethostname(),
            "IP Address": self.get_ip_address(),
            "CPU": self.get_cpu_info(),
            "RAM": self.get_ram_info(),
            "Disk": self.get_disk_info()
        }
        self.ip_address = self.get_ip_address()
        self.cpu_info = self.get_cpu_info()

    def get_ip_address(self):
        try:
            response = requests.get('https://httpbin.org/ip')
            response.raise_for_status()
            return response.json()['origin']
        except requests.exceptions.RequestException as e:
            return "Unavailable"

    def get_cpu_info(self):
        try:
            cpu_info = psutil.cpu_times()
            return {
                "User Time": cpu_info.user,
                "System Time": cpu_info.system,
                "Idle Time": cpu_info.idle
            }
        except Exception as e:
            return str(e)

    def get_ram_info(self):
        try:
            ram_info = psutil.virtual_memory()
            return {
                "Total": ram_info.total,
                "Available": ram_info.available,
                "Used": ram_info.used
            }
        except Exception as e:
            return str(e)

    def get_disk_info(self):
        try:
            disk_info = psutil.disk_usage('/')
            return {
                "Total": disk_info.total,
                "Used": disk_info.used,
                "Free": disk_info.free
            }
        except Exception as e:
            return str(e)

    def get_system_info(self):
        return self.system_info

