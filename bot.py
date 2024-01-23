import os
import asyncio
import aiohttp
import discord
import json

BDO_API_URL = "https://api.arsha.io/v1/eu/GetWorldMarketWaitList"
TOKEN = os.getenv('DISCORD_TOKEN')
MANOS_IDS = [
    "705512",
    "705511",
    "705510",
    "705509"
]

class MyClient(discord.Client):
    async def on_ready(self):
        print(f'Logged on as {self.user}!')
        self.bg_task = self.loop.create_task(self.my_background_task())

    async def on_message(self, message):
        if message.author == self.user:
            return

        if message.content == "!dale":
            await message.channel.send("Vigilando el market: PEN Manos")

    async def my_background_task(self):
        await self.wait_until_ready()
        channel = self.get_channel(1199464907087814696)
        if not channel:
            print("Channel not found. Make sure the channel ID is correct.")
            return
        while not self.is_closed():
            try:
                async with aiohttp.ClientSession() as session:
                    async with session.get(BDO_API_URL) as response:
                        if response.status == 200:
                            data = await response.json()
                            items_data = data.get('resultMsg', '').split('|')
                            for item in items_data:
                                item_data = item.split('-')
                                if item_data[0] in MANOS_IDS and item_data[1] == "5":
                                    await channel.send(f"PEN Manos listado @everyone: Item ID {item_data[0]}, Price: {item_data[2]}")
                        else:
                            print(f"API call failed with status: {response.status}")
            except Exception as e:
                print(f"Error: {e}")
            await asyncio.sleep(60)

intents = discord.Intents.default()
intents.messages = True

client = MyClient(intents=intents)
client.run(TOKEN)