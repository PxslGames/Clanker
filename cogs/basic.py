# im a baisc file

# im going to tickle my cat's foot... tickle tickle! - dashcrikeydash

import aiohttp
from discord import app_commands, Interaction
from discord.ext import commands
from datetime import datetime, timezone
import random
import discord
import json

class WelcomeView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

        self.add_item(
            discord.ui.Button(
                label="Join Discord",
                emoji="💬",
                url="https://discord.gg/YtQdrkxfg7"
            )
        )

        self.add_item(
            discord.ui.Button(
                label="Vote on Top.gg",
                emoji="⭐",
                url="https://top.gg/bot/1482397035909873865/vote"
            )
        )

        self.add_item(
            discord.ui.Button(
                label="Website",
                emoji="🌐",
                url="https://clanker.pxsl.dev/"
            )
        )

class Basic(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.bot_start_time = datetime.now(timezone.utc)

    @app_commands.command(name="basic", description="see what the basic category does")
    async def basic(self, interaction: Interaction):
        command_count = len(self.get_app_commands())

        embed = discord.Embed(
            title="Basic 📚",
            description=(
                "Hello, the basic category handles most basic commands on the bot, which are kinda boring.\n"
                f"There are currently **{command_count} commands** in this category."
            ),
            color=discord.Color.blurple()
        )

        await interaction.response.send_message(embed=embed)
    
    @app_commands.command(name="welcome", description="show the Clanker welcome message")
    async def welcome(self, interaction: discord.Interaction):
        embed = discord.Embed(
            title="👋 Thanks for adding Clanker!",
            description=(
                "Thanks for inviting **Clanker** to your server! ❤️\n\n"
                "## 💬 Discord Server\n"
                "Need help, have suggestions, or just want to hang out?\n"
                "Join our support server using the button below.\n\n"
                "## ⭐ Support Clanker\n"
                "Clanker is **100% free** and **always will be**.\n"
                "The best way to support us is by **leaving a review and voting on Top.gg**.\n\n"
                "**Thanks for using Clanker! 🔧**"
            ),
            colour=discord.Colour.blurple()
        )

        embed.set_footer(text="Made with ❤️ by the Clanker team")

        await interaction.response.send_message(
            embed=embed,
            view=WelcomeView()
        )
    
    @app_commands.command(name="hello", description="say hello to the bot")
    async def hello(self, interaction: Interaction):
        hello_responses = [
            f"Hello, {interaction.user.name}!",
            f"Hey there, {interaction.user.name}!",
            f"Hi, {interaction.user.name}! How are you?",
            f"Greetings, {interaction.user.name}!",
            f"What's up, {interaction.user.name}?",
            f"Howdy, {interaction.user.name}!",
            f"Yo, {interaction.user.name}!",
            f"Hiya, {interaction.user.name}!",
            f"Salutations, {interaction.user.name}!",
            f"fuck off! {interaction.user.name}! Thank You :D"
        ]
        
        embed = discord.Embed(
            title="Hello! 👋",
            description=random.choice(hello_responses),
            color=discord.Color.blurple()
        )

        await interaction.response.send_message(embed=embed)
    
    @app_commands.command(name="ping", description="get bot's latency")
    async def ping(self, interaction: Interaction):
        embed = discord.Embed(
            title="Pong! 🏓",
            description=f"Ping: {round(self.bot.latency * 1000)} ms",
            color=discord.Color.blurple()
        )

        await interaction.response.send_message(embed=embed)
    
    @app_commands.command(name="uptime", description="how long bot been online")
    async def uptime(self, interaction: Interaction):
        now = datetime.now(timezone.utc)
        uptime_seconds = (now - self.bot_start_time).total_seconds()

        days, remainder = divmod(uptime_seconds, 86400)
        hours, remainder = divmod(remainder, 3600)
        minutes, seconds = divmod(remainder, 60)

        uptime_str = f"{int(days)}d {int(hours)}h {int(minutes)}m {int(seconds)}s"

        embed = discord.Embed(
            title="Uptime ⏱️",
            description=f"The bot has been online for: {uptime_str}",
            color=discord.Color.blurple()
        )

        await interaction.response.send_message(embed=embed)
    
    @app_commands.command(name="usercount", description="how many users does Clanker serve")
    async def usercount(self, interaction: Interaction):
        servers = len(self.bot.guilds)
        users = sum(g.member_count or 0 for g in self.bot.guilds)

        embed = discord.Embed(
            title="User Count 👤",
            description=f"Clanker serves **{users:,}** users across **{servers:,}** servers!",
            color=discord.Color.blurple()
        )

        await interaction.response.send_message(embed=embed)
    
    @app_commands.command(name="cmdcount", description="how many commands Clanker has")
    async def cmdcount(self, interaction: Interaction):
        total = len(self.bot.tree.get_commands())

        category_counts = {}

        for cmd in self.bot.tree.get_commands():
            cog_name = cmd.binding.__class__.__name__ if cmd.binding else "No Category"

            if cog_name not in category_counts:
                category_counts[cog_name] = 0

            category_counts[cog_name] += 1

        desc = f"**Total Commands:** {total}\n\n"

        for category, count in category_counts.items():
            desc += f"- **{category}**: {count}\n"

        embed = discord.Embed(
            title="Command Count 🤖",
            description=desc,
            color=discord.Color.blurple()
        )

        await interaction.response.send_message(embed=embed)
    
    @app_commands.command(name="version", description="see the bot's version")
    async def version(self, interaction: discord.Interaction):
        with open("data.json", "r") as f:
            data = json.load(f)
        
        v = data.get("version")
        if not v:
            raise ValueError("Version not found in data.json!")

        embed = discord.Embed(
            title="Version 🏷️",
            description=f"Clanker is currently running v{v}!",
            color=discord.Color.blurple()
        )

        await interaction.response.send_message(embed=embed)
    
    @app_commands.command(name="info", description="view information about Clanker")
    async def info(self, interaction: discord.Interaction):
        with open("data.json", "r") as f:
            data = json.load(f)

        version = data.get("version", "Unknown")
        ping = round(self.bot.latency * 1000)
        users = sum(g.member_count or 0 for g in self.bot.guilds)
        servers = len(self.bot.guilds)
        commands = len(self.bot.tree.get_commands())

        embed = discord.Embed(
            title="Info 🤖",
            color=discord.Color.blurple()
        )

        embed.add_field(name="🏷️ Version", value=f"v{version}", inline=True)
        embed.add_field(name="📡 Ping", value=f"{ping} ms", inline=True)
        embed.add_field(name="🤖 Commands", value=str(commands), inline=True)
        embed.add_field(name="👤 Users", value=f"{users:,}", inline=True)
        embed.add_field(name="🖥️ Servers", value=f"{servers:,}", inline=True)

        await interaction.response.send_message(embed=embed)
    
    @app_commands.command(name="vote", description="vote for the bot on top.gg")
    async def vote(self, interaction: discord.Interaction):
        embed = discord.Embed(
            title="Vote for Clanker! 🗳️",
            description="Help us grow by voting for the bot on top.gg!",
            color=discord.Color.blurple()
        )
        embed.add_field(name="Vote Link", value="[Click here to vote](https://top.gg/bot/1482397035909873865/vote)", inline=False)

        await interaction.response.send_message(embed=embed)
    
    @app_commands.command(name="invite", description="get bot invite link")
    async def invite(self, interaction: Interaction):
        embed = discord.Embed(
            title="Invite Me 🤖",
            description="[Click here to invite the bot](https://top.gg/bot/1482397035909873865)",
            color=discord.Color.blurple()
        )

        await interaction.response.send_message(embed=embed)

    def get_all_commands(self):
        cmds = []
        for cmd in self.bot.tree.get_commands():
            if isinstance(cmd, app_commands.Group):
                cmds.extend(cmd.commands)
            else:
                cmds.append(cmd)
        return cmds

    @app_commands.command(name="help", description="get help with the bot")
    async def help(self, interaction: discord.Interaction):

        def is_admin(user_id):
            return (
                user_id in self.bot.data.get("admins", []) or
                user_id in self.bot.data.get("owners", [])
            )

        categories = {}
        admin_commands = []

        for cmd in self.get_all_commands():
            cog_name = cmd.binding.__class__.__name__ if getattr(cmd, "binding", None) else "Other"

            if cog_name == "Admin":
                if is_admin(interaction.user.id):
                    admin_commands.append(cmd)
                continue

            categories.setdefault(cog_name, []).append(cmd)

        if is_admin(interaction.user.id) and admin_commands:
            categories["Admin"] = admin_commands

        pages = []

        for category, cmds in categories.items():
            cmds = sorted(cmds, key=lambda c: c.name)

            chunk_size = 5
            for i in range(0, len(cmds), chunk_size):
                chunk = cmds[i:i + chunk_size]

                description = "\n".join(
                    f"{getattr(cmd, 'mention', f'/{cmd.name}')} - {cmd.description}"
                    for cmd in chunk
                )

                page_num = (i // chunk_size) + 1
                total_pages = (len(cmds) + chunk_size - 1) // chunk_size

                embed = discord.Embed(
                    title=f"Help - {category} ({page_num}/{total_pages})",
                    description=description,
                    color=discord.Color.blurple()
                )

                pages.append(embed)

        if not pages:
            pages.append(
                discord.Embed(
                    title="Help",
                    description="No commands found.",
                    color=discord.Color.red()
                )
            )

        class HelpView(discord.ui.View):
            def __init__(self):
                super().__init__(timeout=120)
                self.current = 0

            @discord.ui.button(label="◀️", style=discord.ButtonStyle.gray)
            async def previous(self, interaction: discord.Interaction, button: discord.ui.Button):
                self.current = (self.current - 1) % len(pages)
                await interaction.response.edit_message(embed=pages[self.current], view=self)

            @discord.ui.button(label="▶️", style=discord.ButtonStyle.gray)
            async def next(self, interaction: discord.Interaction, button: discord.ui.Button):
                self.current = (self.current + 1) % len(pages)
                await interaction.response.edit_message(embed=pages[self.current], view=self)

        view = HelpView()

        await interaction.response.send_message(
            embed=pages[0],
            view=view,
            ephemeral=True
        )
    
    @app_commands.command(name="credits", description="view the people who helped make Clanker")
    async def credits(self, interaction: Interaction):

        async def get_credits():
            url = "https://clanker.pxsl.dev/credits.json"

            async with aiohttp.ClientSession() as session:
                async with session.get(url) as response:
                    return await response.json()


        try:
            data = await get_credits()
    
        except Exception:
            await interaction.response.send_message(
                embed=discord.Embed(
                    title="❌ Error",
                    description="Failed to load credits right now.",
                    color=discord.Color.red()
                ),
                ephemeral=True
            )
            return


        pages = []

        for key, section in data.items():

            people = section.get("people", [])

            if people:
                description = ""

                for person in people:
                    description += (
                        f"**{person['name']}**\n"
                        f"{person['role']}\n\n"
                    )

            else:
                description = "No one listed yet."

            embed = discord.Embed(
                title=f"{section.get('title', key.title())}",
                description=description,
                color=discord.Color.blurple()
            )

            pages.append(embed)


        if not pages:
            await interaction.response.send_message(
                embed=discord.Embed(
                    title="❌ Error",
                    description="No credits found.",
                    color=discord.Color.red()
                ),
                ephemeral=True
            )
            return


        def update_footer(embed, page):
            embed.set_footer(
                text=(
                    f"Page {page + 1}/{len(pages)} • "
                    "Thank you to everyone who helped make Clanker ❤️"
                )
            )


        for index, page in enumerate(pages):
            update_footer(page, index)


        class CreditsView(discord.ui.View):

            def __init__(self):
                super().__init__(timeout=120)
                self.current = 0


            @discord.ui.button(
                label="◀️",
                style=discord.ButtonStyle.gray
            )
            async def previous(
                self,
                interaction: discord.Interaction,
                button: discord.ui.Button
            ):
                self.current = (self.current - 1) % len(pages)

                await interaction.response.edit_message(
                    embed=pages[self.current],
                    view=self
                )


            @discord.ui.button(
                label="▶️",
                style=discord.ButtonStyle.gray
            )
            async def next(
                self,
                interaction: discord.Interaction,
                button: discord.ui.Button
            ):
                self.current = (self.current + 1) % len(pages)

                await interaction.response.edit_message(
                    embed=pages[self.current],
                    view=self
                )


            async def on_timeout(self):
                for item in self.children:
                    item.disabled = True


        view = CreditsView()

        await interaction.response.send_message(
            embed=pages[0],
            view=view
        )

async def setup(bot):
    await bot.add_cog(Basic(bot))
