import os
from dotenv import load_dotenv
from twitchio.ext import commands
from utils.translator import translate_to_target_language

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
        self.target_language = 'en'

    async def event_ready(self):
        print(f'✅ Logged in as {self.nick}')

    async def event_message(self, message):
        if message.echo:
            return

        translated = translate_to_target_language(message.content, self.target_language)
        if translated:
            output = f'🌐 {message.author.name}: {translated}'
            await message.channel.send(output)

        await self.handle_commands(message)

    @commands.command(name='setLanguage')
    async def set_target_language(self, ctx: commands.Context):
        command_name = 'setLanguage'

        if not ctx.author.is_mod and ctx.author.name.lower() != CHANNEL.lower():
            return

        parts = ctx.message.content.strip().split()
        if len(parts) != 2:
            await ctx.send(f"❓ Usage: !{command_name} [lang_code] (e.g., !{command_name} fr)")
            return

        self.target_language = parts[1].lower()
        await ctx.send(f"✅ Non-native messages will be translated to: {self.target_language}")

bot = Bot()
bot.run()