def is_authorized(self, ctx: commands.Context) -> bool:
    return ctx.author.is_mod or ctx.author.name.lower() == CHANNEL.lower()
