import os
import sys
from datetime import datetime
import pytest
from unittest.mock import Mock
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
import main
from main import monitor_system


@pytest.fixture
def log_file():
    file_name = 'system_log.txt'

    # Remove the log file if it already exists
    if os.path.exists(file_name):
        os.remove(file_name)

    yield file_name

    # Clean up - remove the log file after the test
    if os.path.exists(file_name):
        os.remove(file_name)


def test_system_monitor(log_file, mocker):
    # Mock the send_email function
    mocker.patch('main.email_notifications.send_email')

    # Run the system monitor for a duration of 15 seconds
    duration = 15

    # Start the system monitor
    monitor_system(duration, cpu_limit=80, ram_limit=70, disk_limit=90)

    # Check if the log file is created
    assert os.path.exists(log_file)

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

    # Check if the send_email function was called
    main.email_notifications.send_email.assert_called()

    # Additional assertions based on your specific log format and requirements