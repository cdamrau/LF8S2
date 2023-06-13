# LF8S2
Key Features:

CPU Usage Monitoring: The tool tracks and logs the CPU usage percentage at regular intervals.
RAM Usage Monitoring: The tool captures and logs the RAM usage, including used and total memory in megabytes (MB) along with the percentage.
Disk Usage Monitoring: It monitors the disk usage for each partition and provides detailed information such as used space, total space, and percentage usage.
Log File Generation: The tool creates a log file (system_log.txt) to store the monitored system data.
Timestamps: The log file and console output include timestamps for each logged entry, providing a time reference for system monitoring.
Usage Instructions:
Run the monitor_system() function in the main.py module to start the system monitoring process.
The tool will record system resource data, including CPU, RAM, and disk usage, at regular intervals.
The collected data will be stored in the system_log.txt file and displayed in the console output.
The tool supports a duration parameter to limit the monitoring process to a specific timeframe.

Please note that the System Monitoring Tool is provided as-is without any warranty. Use it responsibly and ensure compliance with system monitoring guidelines and policies.
Your feedback and suggestions for future enhancements are highly appreciated.

for sending Emails you will neeed a .env with following contents:
SENDGRID_API_KEY=
SENDER_EMAIL=<example@mail.com>
RECEIVER_EMAIL=<example@mail.com>
