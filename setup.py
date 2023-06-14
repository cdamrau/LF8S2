import subprocess

# Check if Python is installed
try:
    subprocess.check_call(['python', '-V'])
except Exception:
    print("Python is not installed on your system. Please visit https://www.python.org/downloads/ to download and install Python.")

# Check if pip is installed
try:
    subprocess.check_call(['pip', '-V'])
except Exception:
    print("pip is not installed on your system. Please visit https://pip.pypa.io/en/stable/installing/ to download and install pip.")

# Update pip if available
subprocess.call(['pip', 'install', '--upgrade', 'pip'])

# Define the required packages
packages = [
    'psutil',
    'python-dotenv',
    'unittest',
    'sendgrid',
    'py-notifier',
    'pytest-mock'
]

# Install each package using pip
for package in packages:
    subprocess.call(['pip', 'install', package])
