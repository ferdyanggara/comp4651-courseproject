import discord
import os
import requests
import json
from dotenv import load_dotenv
import ssl
import certifi
load_dotenv()
ssl_context = ssl.create_default_context(cafile=certifi.where())
intents = discord.Intents.default()

intents.messages = True
intents.message_content = True
intents.guild_messages = True

client = discord.Client(intents=intents,ssl_context=ssl_context)

@client.event
async def on_message(message):

    # this is for NSFW (image moderation task)
    if message.attachments:
        attachment = message.attachments[0]
        print(f"Attachment URL: {attachment.url}")

        url = "http://localhost:8080/function/openfaas-opennsfw"
        headers = {'Content-Type': 'text/plain'}

        response = requests.post(url, headers=headers, data=attachment.url)
        content = response.content.decode('utf-8')
        result = json.loads(content)

        sfw_score = result['sfw_score']
        nsfw_score = result['nsfw_score']

        print('sfw: score: ' , sfw_score, 'nsfw score: ', nsfw_score)

        msg_to_delete = await message.channel.fetch_message(message.id)

        if nsfw_score > 0.5:
            await msg_to_delete.delete()
            await message.channel.send(f'{attachment.url.split("/")[-1]} removed due to displaying explicit or suggestive adult content as it has high NSFW score {nsfw_score}.')
        else:
            await message.channel.send(f'{attachment.url.split("/")[-1]} is not removed as it has low NFSW score {nsfw_score}.')
    elif message.author != client.user:
        url = "http://localhost:8080/function/toxic-comment"
        headers = {'Content-Type': 'text/plain'}
        response = requests.post(url, headers=headers, data=message.content)
        content = response.content.decode('utf-8')
        result = json.loads(content)
        label = result[0]['label']
        score = result[0]['score']
        msg_to_delete = await message.channel.fetch_message(message.id)
        if label=='toxic' and score>0.7:
            await msg_to_delete.delete()
            await message.channel.send(f'message by {message.author} removed due as it is toxic comment')
            
            
client.run(os.environ["DISCORD_BOT_TOKEN"])