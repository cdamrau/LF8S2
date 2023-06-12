import psutil
import time
from datetime import datetime

def monitor_system(duration):
    log_file = 'system_log.txt'  # Name of the log file
    first_run = True
    start_time = time.time()

    while time.time() - start_time < duration:
        timestamp = datetime.now().strftime("%H:%M:%S.%f")
        if first_run:
            first_run = False
            datestamp = datetime.now().strftime("%Y-%m-%d")
            with open(log_file, 'a') as file:
                file.write(f"Date: {datestamp}\n")

        with open(log_file, 'a') as file:
            file.write(f"Timestamp: {timestamp}\n")

            # CPU usage
            cpu_percent = psutil.cpu_percent(interval=1)
            cpu_log = f"CPU Usage: {cpu_percent}%"
            file.write(cpu_log + '\n')
            print(f"{timestamp} - {cpu_log}")

            # RAM usage
            mem = psutil.virtual_memory()
            mem_percent = mem.percent
            mem_used = mem.used / 1024 / 1024  # in MB
            mem_total = mem.total / 1024 / 1024  # in MB
            mem_log = f"RAM Usage: {mem_used:.2f}MB / {mem_total:.2f}MB ({mem_percent}%)"
            file.write(mem_log + '\n')
            print(f"{timestamp} - {mem_log}")

            # Disk usage
            partitions = psutil.disk_partitions()
            for partition in partitions:
                disk_usage = psutil.disk_usage(partition.mountpoint)
                disk_percent = disk_usage.percent
                disk_used = disk_usage.used / 1024 / 1024 / 1024  # in GB
                disk_total = disk_usage.total / 1024 / 1024 / 1024  # in GB
                disk_log = f"Disk Usage ({partition.mountpoint}): {disk_used:.2f}GB / {disk_total:.2f}GB ({disk_percent}%)"
                file.write(disk_log + '\n')
                print(f"{timestamp} - {disk_log}")

        time.sleep(5)

# Call the monitor_system() function with the specified duration
monitor_system(60)