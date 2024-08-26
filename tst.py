# Example of using an invisible character in a Discord embed

import requests
import json
import config
def post_to_discord(embed, webhook_url):
    data = {
        "embeds": embed
    }

    response = requests.post(webhook_url, json=data, headers={"Content-Type": "application/json"})
    return response.status_code, response.text

invisible_character = "‎"  # This is the invisible character

embed = {
    "title": "Example with Invisible Character",
    "description": f"This text includes an invisible character: {invisible_character}",
    "color": 3447003,
    "fields": [
        {
            "name": "Field 1",
            "value": f"Value with invisible character: {invisible_character}",
            "inline": False
        }
    ],
    "footer": {
        "text": f"Footer with invisible character: {invisible_character}"
    }
}

webhook_url = config.DISCORD_WEBHOOK_URL
post_to_discord(embed, webhook_url)
