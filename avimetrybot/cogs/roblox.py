import requests
import discord
import asyncio
from discord.ext import commands, tasks
from roblox_py import Client


class RobloxUpdate(commands.Cog, name="Roblox"):
    """
    Roblox related commands.
    """
    def __init__(self, avi):
        self.avi = avi
        self.update_check.start()

    def cog_unload(self):
        self.update_check.cancel()

    @tasks.loop(seconds=59)
    async def update_check(self):
        async with self.avi.session.get(
            "http://setup.roblox.com/version"
        ) as old_version:
            a = await old_version.text()
        await asyncio.sleep(10)
        async with self.avi.session.get(
            "http://setup.roblox.com/version"
        ) as new_version:
            b = await new_version.text()
        if b != a:
            print("update!")
            channel = discord.utils.get(
                self.avi.get_all_channels(), name="gaming-announcements"
            )
            embed = discord.Embed(
                title="<:roblox:788835896354013229> A ROBLOX update has been detected.",
                description="If you don't want ROBLOX to update, keep ROBLOX open. "
                            "Please wait while people update their cool lego hak.",
            )
            embed.add_field(name="Latest Version", value=f"{b}", inline=True)
            embed.add_field(name="Last Version", value=f"{a}", inline=True)
            embed.set_footer(
                text="If you want to get notified when ROBLOX updates, use the command 'a.updateping'."
            )
            await channel.send("<@&783946910364073985>", embed=embed)

    @update_check.before_loop
    async def before_status_task(self):
        await self.avi.wait_until_ready()

    # Roblox Version Command
    @commands.command(
        aliases=["rblxver", "rversion"], brief="Gets the current ROBLOX version.",
        hidden=True
    )
    async def robloxversion(self, ctx):
        if ctx.guild.id != 751490725555994716:
            return await ctx.send("This command is for a private server.")

        a = requests.get("http://setup.roblox.com/version")
        rverembed = discord.Embed()
        rverembed.add_field(
            name="<:roblox:788835896354013229> Current Version",
            value="``" + a.text + "``",
            inline=True,
        )
        await ctx.channel.send(embed=rverembed)

    @commands.command(
        brief="Get pinged if you want to know when a ROBLOX update arrives.",
        hidden=True
    )
    async def updateping(self, ctx):
        if ctx.guild.id != 751490725555994716:
            return await ctx.send("This command is for a private server.")
        member = ctx.author
        role = discord.utils.get(member.guild.roles, name="RobloxUpdate")
        if role in member.roles:
            await discord.Member.remove_roles(member, role)
            ra = discord.Embed()
            ra.add_field(
                name="<:roblox:788835896354013229> Roblox Update Ping",
                value="You will no longer get pinged when ROBLOX recieves an update.",
            )
            await ctx.send(embed=ra)
        else:
            await discord.Member.add_roles(member, role)
            ru = discord.Embed()
            ru.add_field(
                name="<:roblox:788835896354013229> Roblox Update Ping",
                value="You will now get pinged everytime ROBLOX recieves an update.",
            )
            await ctx.send(embed=ru)

    @commands.group(
        invoke_without_command=True
    )
    async def roblox(self, ctx):
        await ctx.send_help("roblox")

    @roblox.command()
    async def user(self, ctx, user):
        client = Client()
        user = await client.get_user_by_name(user)
        user_embed = discord.Embed(title="Roblox User",)
        user_embed.add_field(name="Username", value=user.name)
        user_embed.add_field(name="User ID", value=user.id)
        user_embed.add_field(name="Join Date", value=user.account_age)
        user_embed.add_field(name="Amount of Friends", value=await user.friends_count())
        user_embed.add_field(name="Amount of Followers", value=await user.follower_count())
        user_embed.add_field(name="Amount of user badges", value=await user.count_roblox_badges())
        user_embed.set_thumbnail(url=await user.avatar())
        await ctx.send(embed=user_embed)


def setup(avi):
    avi.add_cog(RobloxUpdate(avi))
