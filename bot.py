import os
from dotenv import load_dotenv
from twitchio.ext import commands

load_dotenv()
TOKEN = os.getenv('TWITCH_OAUTH_TOKEN')
CHANNEL = os.getenv('TWITCH_CHANNEL')

class Bot(commands.Bot):
    def __init__(self):
        super().__init__(
            token=TOKEN,
            prefix='!',
            initial_channels=[CHANNEL]
        )

    async def event_ready(self):
        print(f'✅ Logged in as {self.nick}')

    async def event_message(self, message):
        if message.echo:
            return

        print(f'{message.author.name}: {message.content}')

bot = Bot()
bot.run()
