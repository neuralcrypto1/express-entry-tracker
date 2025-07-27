import requests
from bs4 import BeautifulSoup
import os

URL = "https://www.canada.ca/en/immigration-refugees-citizenship/corporate/mandate/policies-operational-instructions-agreements/ministerial-instructions/express-entry-rounds.html"
DATA_FILE = "latest_draw.txt"
BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

def get_latest_draw():
    response = requests.get(URL)
    if response.status_code != 200:
        print(f"❌ HTTP error {response.status_code}")
        return None

    soup = BeautifulSoup(response.text, "html.parser")
    table = soup.find("table")

    if not table:
        print("❌ Table not found. Dumping HTML preview below:")
        print(soup.prettify()[:3000])  # Print first 3,000 characters of HTML
        return None

    tbody = table.find("tbody")
    if not tbody:
        print("❌ <tbody> not found.")
        return None

    first_row = tbody.find("tr")
    if not first_row:
        print("❌ No <tr> row found.")
        return None

    return first_row.get_text(separator=" | ", strip=True)


def send_telegram_message(message):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    data = {
        "chat_id": CHAT_ID,
        "text": message
    }
    requests.post(url, data=data)

def main():
    latest = get_latest_draw()
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE) as f:
            saved = f.read().strip()
    else:
        saved = ""

    if latest != saved:
        with open(DATA_FILE, "w") as f:
            f.write(latest)
        send_telegram_message(f"🆕 New Express Entry Draw:\n\n{latest}\n\n🔗 {URL}")
    else:
        print("No new draw.")

if __name__ == "__main__":
    main()
