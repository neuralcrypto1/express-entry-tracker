import requests
from bs4 import BeautifulSoup
import os

URL = "https://www.canada.ca/en/immigration-refugees-citizenship/corporate/mandate/policies-operational-instructions-agreements/ministerial-instructions/express-entry-rounds.html"
DATA_FILE = "latest_draw.txt"
BOT_TOKEN = os.getenv("8386485222:AAHEASKbRq1jPg8f4szGcE-WNrqesil4lYM")
CHAT_ID = os.getenv("1349892913")

def get_latest_draw():
    response = requests.get(URL)
    soup = BeautifulSoup(response.text, "html.parser")
    table = soup.find("table")
    first_row = table.find("tbody").find("tr")
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
