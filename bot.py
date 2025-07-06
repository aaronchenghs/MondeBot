import os
import openai
from dotenv import load_dotenv
from twitchio.ext import commands
from langcodes import Language
from utils.translator import detect_language
from utils.constants import OUTPUT_MODE_LABELS, COMMANDS_PREFIX
from utils.suggestions import query_suggestions
from utils.translator import translate_to_target_language

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")
TOKEN = os.getenv('TWITCH_OAUTH_TOKEN')
CHANNEL = os.getenv('TWITCH_CHANNEL')


def is_authorized(ctx: commands.Context) -> bool:
    return  ctx.author.name.lower() == CHANNEL.lower() # or ctx.author.is_mod


class Bot(commands.Bot):
    def __init__(self):
        super().__init__(
            token=TOKEN,
            prefix=COMMANDS_PREFIX,
            initial_channels=[CHANNEL]
        )
        self.target_language = 'en'
        self.translation_enabled = True
        self.output_mode = list(OUTPUT_MODE_LABELS.keys())[0]

    async def event_ready(self):
        print(f'✅ Logged in as {self.nick}')

    async def event_message(self, message):
        if message.echo:
            return

        await self.handle_commands(message)

        if not self.translation_enabled or message.content.startswith(COMMANDS_PREFIX):
            return

        lang_code = detect_language(message.content)

        if lang_code == self.target_language and self.output_mode == "terminal":
            print(f'🌐 {message.author.name} (native): {message.content}')
            return

        translated = translate_to_target_language(message.content, self.target_language)
        if not translated:
            return

        output = f'🌐 {message.author.name}: {translated}'
        if self.output_mode == 'chat':
            await message.channel.send(output)
        else:
            print(output)

        try:
            lang_code = detect_language(message.content)
            readable_lang = Language.get(lang_code).display_name()

            suggestions = query_suggestions(
                original_text=message.content,
                language_code=readable_lang
            )

            if suggestions and self.output_mode == 'terminal':
                print(f"🤖 Suggested responses for {message.author.name} (in {readable_lang}):")
                for suggestion in suggestions:
                    print(f"💬 {suggestion}")
                print('-' * 40)

        except Exception as e:
            print(f"⚠️ Error generating suggestions: {e}")

    @commands.command(name='lang')
    async def set_target_language(self, ctx: commands.Context):
        command_name = 'lang'
        if not self.translation_enabled or not is_authorized(ctx):
            return

        parts = ctx.message.content.strip().split()
        if len(parts) != 3:
            await ctx.send(f"❓ Usage: !{command_name} [lang_code]")
            return

        self.target_language = parts[2].lower()
        await ctx.send(f"✅ Non-native messages will be translated to: {self.target_language}")

    @commands.command(name='toggle')
    async def toggle_translate(self, ctx: commands.Context):
        if not is_authorized(ctx):
            return

        self.translation_enabled = not getattr(self, 'translation_enabled', True)
        status = "enabled" if self.translation_enabled else "disabled"
        await ctx.send(f"🌐 Translation is now {status}.")

    @commands.command(name='dest')
    async def set_output_destination(self, ctx: commands.Context):
        if not is_authorized(ctx):
            return

        parts = ctx.message.content.strip().split()

        if len(parts) != 3 or parts[2].lower() not in OUTPUT_MODE_LABELS:
            modes = '|'.join(OUTPUT_MODE_LABELS.keys())
            await ctx.send(f"❓ Usage: !mb dest [{modes}]")
            return

        self.output_mode = parts[2].lower()
        destination = OUTPUT_MODE_LABELS.get(self.output_mode, "Unknown")
        await ctx.send(f"✅ Translated messages will now be sent to: {destination}")

    @commands.command(name='help')
    async def show_help(self, ctx: commands.Context):
        if not is_authorized(ctx):
            return

        help_text = (
            "🤖 MondeBot Commands: \n"
            "• `!mb lang` - Set target lang (e.g., `!mbLang fr`)\n"
            "• `!mb toggle` - Enable/disable translation\n"
            "• `!mb dest [chat|terminal]` - Set output dest\n"
        )
        await ctx.send(help_text)
