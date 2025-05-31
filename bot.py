import os
from dotenv import load_dotenv
from twitchio.ext import commands
from utils.translator import translate_to_target_language

load_dotenv()
TOKEN = os.getenv('TWITCH_OAUTH_TOKEN')
CHANNEL = os.getenv('TWITCH_CHANNEL')


def is_authorized(ctx: commands.Context) -> bool:
    return ctx.author.is_mod or ctx.author.name.lower() == CHANNEL.lower()


class Bot(commands.Bot):
    def __init__(self):
        super().__init__(
            token=TOKEN,
            prefix='!',
            initial_channels=[CHANNEL]
        )
        self.target_language = 'en'
        self.translation_enabled = True

    async def event_ready(self):
        print(f'✅ Logged in as {self.nick}')

    async def event_message(self, message):
        if message.echo:
            return

        await self.handle_commands(message)

        if not self.translation_enabled :
            return

        translated = translate_to_target_language(message.content, self.target_language)
        if translated:
            output = f'🌐 {message.author.name}: {translated}'
            await message.channel.send(output)

    @commands.command(name='setLanguage')
    async def set_target_language(self, ctx: commands.Context):
        command_name = 'setLanguage'
        if not self.translation_enabled or not is_authorized(ctx):
            return

        parts = ctx.message.content.strip().split()
        if len(parts) != 2:
            await ctx.send(f"❓ Usage: !{command_name} [lang_code] (e.g., !{command_name} fr)")
            return

        self.target_language = parts[1].lower()
        await ctx.send(f"✅ Non-native messages will be translated to: {self.target_language}")

    @commands.command(name='toggleTranslate')
    async def toggle_translate(self, ctx: commands.Context):
        if not is_authorized(ctx):
            return

        self.translation_enabled = not getattr(self, 'translation_enabled', True)
        status = "enabled" if self.translation_enabled else "disabled"
        await ctx.send(f"🌐 Translation is now {status}.")


bot = Bot()
bot.run()