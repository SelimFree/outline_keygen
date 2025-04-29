import csv
import requests
import yagmail
import urllib3
from config import OUTLINE_API_URL, OUTLINE_API_SECRET, GMAIL_USER, GMAIL_APP_PASSWORD, CSV_PATH
import logging

# Create a logger
logger = logging.getLogger("outline_keygen")
logger.setLevel(logging.DEBUG)  # capture all levels, handlers will filter

# Console handler for INFO and above
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)
console_format = logging.Formatter("[%(levelname)s] %(message)s")
console_handler.setFormatter(console_format)

# File handler for ERROR and above
file_handler = logging.FileHandler("errors.log")
file_handler.setLevel(logging.ERROR)
file_format = logging.Formatter("%(asctime)s [%(levelname)s] %(message)s")
file_handler.setFormatter(file_format)

# Add both handlers to the logger
logger.addHandler(console_handler)
logger.addHandler(file_handler)

# Disable SSL warnings for self-signed Outline servers
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


def create_access_key():
    try:
        response = requests.post(f"{OUTLINE_API_URL}/{OUTLINE_API_SECRET}/access-keys", verify=False)
        response.raise_for_status()
        return response.json()["accessUrl"], response.json()["id"]
    except requests.exceptions.RequestException as e:
        logger.error(f"❌ Failed to create access key: {e}")
        return None, None
    
def rename_access_key(id, name):
    try:        
        response = requests.put(f"{OUTLINE_API_URL}/{OUTLINE_API_SECRET}/access-keys/{id}/name", data={"name": name}, verify=False)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        logger.error(f"❌ Failed to rename access key: {e}")
        return None


def send_email(recipient, name, access_url):
    subject = "Your Outline VPN Access Key"
    body = f"""
Hi {name},

Here is your access key for the VPN:

{access_url}

Just paste it into the Outline client to get started.
"""
    try:
        yag = yagmail.SMTP(GMAIL_USER, GMAIL_APP_PASSWORD)
        yag.send(to=recipient, subject=subject, contents=body)
        logger.info(f"✅ Email sent to {recipient}")
    except Exception as e:
        logger.error(f"❌ Failed to send email to {recipient}: {e}")
        

def main():
    with open(CSV_PATH, newline='') as csvfile:
        reader = csv.DictReader(csvfile, delimiter=";")
        for row in reader:
            name = row["name"]
            email = row.get("email", "").strip()
            logger.info(f"--- Processing {name} ---")

            logger.info(f"Generating access key for {name}...")
            access_url, id = create_access_key()
            
            if not access_url:
                logger.warning(f"⚠️ Skipping {name} due to access key generation failure.")
                continue
            
            logger.info(f"Renaming generated access key to {name}...")
            rename_access_key(id, name)
            
            logger.info(f"Sending access key to {name}...")
            if email:
                send_email(email, name, access_url)
            else:
                logger.warning(f"ℹ️ No email provided for {name}, key not sent.")

if __name__ == "__main__":
    main()
