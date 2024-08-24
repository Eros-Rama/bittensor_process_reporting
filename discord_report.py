# discord_report.py
import requests
import config

def send_report_to_discord(chunks):
    for chunk in chunks:
        data = {
            "content": chunk
        }
        response = requests.post(config.DISCORD_WEBHOOK_URL, json=data)
        if response.status_code == 204:
            print("Chunk sent successfully")
        else:
            print("Failed to send chunk", response.status_code, response.text)