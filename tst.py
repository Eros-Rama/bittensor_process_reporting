import requests
import config
def send_discord_message(webhook_url, username, avatar_url, content):
    data = {
        "username": username,
        "avatar_url": avatar_url,
        "content": content
    }

    response = requests.post(webhook_url, json=data)

    if response.status_code == 204:
        print("Message sent successfully!")
    else:
        print(f"Failed to send message. Status code: {response.status_code}")

# Replace these variables with your own values
webhook_url = config.DISCORD_WEBHOOK_URL
username = "Custom Bot Name"
avatar_url = "https://drive.google.com/file/d/1fUXe0G-wekDjuoM5hDXn-gfDMj_vXPXp/view?usp=drive_link"
content = "Hello, this is a message with a custom avatar!"

send_discord_message(webhook_url, username, avatar_url, content)
