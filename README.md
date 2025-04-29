# Outline Access Key Generator and Email Sender

This Python script automates the creation of Outline VPN access keys for a list of users and optionally emails them their keys.

## Features

- Reads users and their email addresses from a CSV file
- Generates an Outline access key for each user via the Outline Management API
- Sends the access key to each user with an email address using Gmail

## Requirements

- Python 3.7+
- Access to your Outline server's management API URL and secret
- A Gmail account (with [App Password](https://support.google.com/accounts/answer/185833?hl=en) enabled for secure login)

## Installation

1. Clone this repo or copy the files into a folder.
2. Install the required Python packages:

```bash
pip install -r requirements.txt
```

## Configuration

Create a `.env` file in the same directory as the script with the following content:

```env
OUTLINE_API_URL=https://YOUR_SERVER_IP:PORT
OUTLINE_API_SECRET=your_outline_api_secret
GMAIL_USER=yourgmail@gmail.com
GMAIL_APP_PASSWORD=your_gmail_app_password
CSV_PATH=users.csv
```
## Run the Script

Run the script with the following command:

```bash
python generate_keys.py
```