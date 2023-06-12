import os
import psutil
import time
from datetime import datetime
import email_notifications

# Load environment variables from .env file
import dotenv
dotenv.load_dotenv()

def monitor_system(duration, cpu_limit=None, ram_limit=None, disk_limit=None):
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

        # Check limits
        if cpu_limit is not None and cpu_percent > cpu_limit:
            cpu_message = f"CPU usage exceeded the limit of {cpu_limit}%"
            print(cpu_message)
            email_notifications.send_email("CPU Usage Limit Exceeded", cpu_message)
            with open(log_file, 'a') as file:
                file.write(f"Limit Exceeded: {cpu_message}\n")
            break

        if ram_limit is not None and mem_percent > ram_limit:
            ram_message = f"RAM usage exceeded the limit of {ram_limit}%"
            print(ram_message)
            email_notifications.send_email("RAM Usage Limit Exceeded", ram_message)
            with open(log_file, 'a') as file:
                file.write(f"Limit Exceeded: {ram_message}\n")
            break

        if disk_limit is not None:
            for partition in partitions:
                disk_usage = psutil.disk_usage(partition.mountpoint)
                disk_percent = disk_usage.percent
                if disk_percent > disk_limit:
                    disk_message = f"Disk usage on {partition.mountpoint} exceeded the limit of {disk_limit}%"
                    print(disk_message)
                    email_notifications.send_email("Disk Usage Limit Exceeded", disk_message)
                    with open(log_file, 'a') as file:
                        file.write(f"Limit Exceeded: {disk_message}\n")
                    break

        time.sleep(5)

# Call the monitor_system() function with the specified duration and limits
monitor_system(duration=60, cpu_limit=80, ram_limit=70, disk_limit=90)