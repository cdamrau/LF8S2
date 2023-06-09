import psutil
import time

def monitor_system():
    disk_paths = ['C:\\', 'E:\\']  # Example disk paths to monitor on Windows

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
        for path in disk_paths:
            try:
                disk_usage = psutil.disk_usage(path)
                disk_percent = disk_usage.percent
                disk_used = disk_usage.used / 1024 / 1024 / 1024  # in GB
                disk_total = disk_usage.total / 1024 / 1024 / 1024  # in GB
                print(f"Disk ({path}) Usage: {disk_used:.2f}GB / {disk_total:.2f}GB ({disk_percent}%)")
            except FileNotFoundError as e:
                print(f"Disk path '{path}' not found.")

        # Delay for 5 seconds
        time.sleep(5)
        print('\n')  # Add a new line for separation

monitor_system()