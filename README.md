# Business Extracting using Selenium with Firefox on CentOS

This guide provides step-by-step instructions for setting up Selenium with Firefox on a CentOS system. This includes creating a virtual environment, installing necessary dependencies, and setting up Firefox and its driver.

## Prerequisites

- CentOS 7 or later
- Python 3.6 or later

## Instructions

### 1. Install Firefox

First, update your system and install Firefox.

```bash
sudo yum update -y
sudo yum install -y firefox
```

### 2. Install GeckoDriver
```bash
Download the latest version of GeckoDriver and make it executable.
```
# Download the latest version of GeckoDriver
```bash
https://github.com/mozilla/geckodriver/releases
wget https://github.com/mozilla/geckodriver/releases/latest/download/geckodriver-v0.33.0-linux64.tar.gz
```
# Extract the tar file
```bash
tar -xzf geckodriver-v0.33.0-linux64.tar.gz
```
# Move the geckodriver to /usr/local/bin

```bash
sudo mv geckodriver /usr/local/bin/
```
# Make it executable
```bash
sudo chmod +x /usr/local/bin/geckodriver
```
### 3. Set Up a Python Virtual Environment

# Install virtualenv if not already installed
sudo yum install -y python3-virtualenv

# Create a virtual environment
python3 -m venv selenium_env

# Activate the virtual environment
source selenium_env/bin/activate

### 4. Install Python Dependencies
```bash
pip install -r requirements.txt
```
### 5. Edit the "Search_settings.json" file
Define the search categories and locations.

### 6. Start https://www.yell.com/ extraction
```bash
python main1.py
```

### 7. Start https://www.yelp.co.uk/ extraction
```bash
python main2.py
```
### 8. The Output Files
The output files can be found in the "files_yell" and "files_yelp" folders created in the current directory. The script generates a file for each search category and location.
