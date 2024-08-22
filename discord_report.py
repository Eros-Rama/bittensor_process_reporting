# discord_report.py
import requests
import config

def send_report_to_discord(report):
    data = {
        "content": "\n".join(report)
    }
    response = requests.post(config.DISCORD_WEBHOOK_URL, json=data)
    if response.status_code == 204:
        print("Report sent successfully")
    else:
        print("Failed to send report", response.status_code, response.text)
