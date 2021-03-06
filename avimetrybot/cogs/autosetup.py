from discord.ext import commands
import logging

logger = logging.getLogger("discord")
logger.setLevel(logging.DEBUG)
handler = logging.FileHandler(filename="discord.log", encoding="utf-8", mode="w")
handler.setFormatter(
    logging.Formatter("%(asctime)s:%(levelname)s:%(name)s: %(message)s")
)
logger.addHandler(handler)


class GuildJoin(commands.Cog, name="Auto Setup"):
    def __init__(self, avi):
        self.avi = avi

    @commands.Cog.listener()
    async def on_guild_join(self, guild):
        await self.avi.config.upsert({"_id": guild.id, "prefix": "a."})


def setup(avi):
    avi.add_cog(GuildJoin(avi))
