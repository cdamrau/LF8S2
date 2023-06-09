import psutil
import time

def monitor_system():
    while True:
        # CPU usage
        cpu_percent = psutil.cpu_percent(interval=1)
        print(f"CPU Usage: {cpu_percent}%")

        # RAM usage
        mem = psutil.virtual_memory()
        mem_percent = mem.percent
        mem_used = mem.used / 1024 / 1024  # in MB
        mem_total = mem.total / 1024 / 1024  # in MB
        print(f"RAM Usage: {mem_used:.2f}MB / {mem_total:.2f}MB ({mem_percent}%)")

        # Disk usage
        disk_usage = psutil.disk_usage('/')
        disk_percent = disk_usage.percent
        disk_used = disk_usage.used / 1024 / 1024 / 1024  # in GB
        disk_total = disk_usage.total / 1024 / 1024 / 1024  # in GB
        print(f"Disk Usage: {disk_used:.2f}GB / {disk_total:.2f}GB ({disk_percent}%)")

        # Delay for 5 seconds
        time.sleep(5)
        print('\n')  # Add a new line for separation

monitor_system()