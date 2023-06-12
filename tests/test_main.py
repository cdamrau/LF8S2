import os
import sys
from datetime import datetime
import pytest
from unittest.mock import patch
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from main import monitor_system
#test
@pytest.fixture
def log_file(tmp_path):
    file_name = tmp_path / 'system_log.txt'

    yield file_name

    # Clean up - remove the log file after the test
    if file_name.exists():
        file_name.unlink()

def test_system_monitor(log_file):
    # Run the system monitor for a duration of 15 seconds
    duration = 7

    # Set the limits for testing
    cpu_limit = 80
    ram_limit = 70
    disk_limit = 90

    # Start the system monitor
    monitor_system(duration, cpu_limit=cpu_limit, ram_limit=ram_limit, disk_limit=disk_limit)

    # Check if the log file is created
    assert log_file.exists()

    # Read the contents of the log file
    with open(log_file, 'r') as file:
        log_contents = file.read()

    # Check if the log file contains the expected data
    # Here, you can write assertions to verify the contents of the log file
    # based on your specific requirements

    # Example assertions:
    current_date = datetime.now().strftime("%Y-%m-%d")
    expected_start = f"Date: {current_date}"
    assert expected_start in log_contents

    expected_timestamp = "Timestamp:"
    assert expected_timestamp in log_contents

    expected_cpu_usage = "CPU Usage:"
    assert expected_cpu_usage in log_contents

    expected_ram_usage = "RAM Usage:"
    assert expected_ram_usage in log_contents

    expected_disk_usage = "Disk Usage"
    assert expected_disk_usage in log_contents

    # Additional assertions based on your specific log format and requirements

    # Check if the limit exceeded messages are present in the log file
    cpu_limit_message = f"CPU usage exceeded the limit of {cpu_limit}%"
    assert cpu_limit_message in log_contents

    ram_limit_message = f"RAM usage exceeded the limit of {ram_limit}%"
    assert ram_limit_message in log_contents

    disk_limit_message = f"Disk usage exceeded the limit of {disk_limit}%"
    assert disk_limit_message in log_contents