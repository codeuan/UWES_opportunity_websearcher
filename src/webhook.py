import os
import requests

def sendToChannel(embeds, heading):
    payload = {}

    if heading:
        payload["content"] = f"**{heading}**"

    if embeds:
        payload["embeds"] = embeds
    else:
        message = "No additional postings yet."
        payload["content"] = f"**{heading}**\n{message}" if heading else message
        
    response = requests.post(
        os.environ["DISCORD_WEBHOOK_URL"],
        json=payload,
        timeout=15,
    ) #send to Discord channel.
    response.raise_for_status()
