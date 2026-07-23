# pxsl :3
# dashcrikeydash

# i just want to say, we are sorry for writing some of the code in a terrible way.
# We are literally not cleaning ts up - pxsl

# anyway, now that the bot is open sourced, you can see how we are stealing all ur data and selling it to the highest bidder mwahahaha - pxsl

import discord
from discord.ext import commands, tasks
import asyncio
import os
import json
import time
import random
import topgg

with open("data.json", "r") as f:
    data = json.load(f)

TOKEN = data.get("token")
if not TOKEN:
    raise ValueError("Token not found in data.json!")

TOPGG_TOKEN = data.get("topgg_token")
if not TOPGG_TOKEN:
    raise ValueError("TOPGG_TOKEN not found in data.json!")

TESTING = False
TEST_GUILD_ID = 1482405732329459754

cooldowns = {}

intents = discord.Intents.default()
intents.guilds = True

class Clanker(commands.Bot):
    def __init__(self):
        super().__init__(
            command_prefix="lol this bot uses slash commands idot", # this literally does nothing im being serious lol - pxsl
            intents=intents
        )
        self.dbl = None
        self.active_users = {}
        self.peak_ccu = 0

    async def setup_hook(self):
        print("[BOOT] Loading cogs...")
        for file in os.listdir("./cogs"):
            if file.endswith(".py"):
                await self.load_extension(f"cogs.{file[:-3]}")
                print(f"[BOOT] Loaded cog: {file}")

        self.dbl = topgg.DBLClient(self, data.get("topgg_token"))

        print("[BOOT] Syncing commands...")

        if TESTING:
            for i in range(5):
                print("[BOOT] Running in TESTING mode, syncing to TEST guild only.")

            guild = discord.Object(id=TEST_GUILD_ID)
            self.tree.copy_global_to(guild=guild)
            synced = await self.tree.sync(guild=guild)

            print(f"[SYNC] Synced {len(synced)} commands to TEST guild")

            commands_data = []

            for cmd in self.tree.walk_commands():
                commands_data.append(cmd.to_dict(self.tree))

            with open("commands.json", "w") as f:
                json.dump(commands_data, f, indent=4)

            print(f"Exported {len(commands_data)} slash commands!")

            print("[TOP.GG] Stats update loop not starting, as we are in testing mode...")
        else:
            try:
                synced = await self.tree.sync()

                print("[SYNC] Cleared leftover commands from test guild")
            except Exception:
                pass

            synced = await self.tree.sync()
            print(f"[SYNC] Synced {len(synced)} global commands")
                        
            commands_data = []

            for cmd in self.tree.walk_commands():
                commands_data.append(cmd.to_dict(self.tree))

            with open("commands.json", "w") as f:
                json.dump(commands_data, f, indent=4)

            print(f"Exported {len(commands_data)} slash commands!")

            self.update_stats.start()

            print("[TOP.GG] Stats update loop starting...")

        print("[BOOT] Status loop starting...")
        self.statusloop.start()
        
    @tasks.loop(seconds=15)
    async def statusloop(self):
        # toggle state (create it if it doesn't exist yet)
        if not hasattr(self, "status_toggle"):
            self.status_toggle = False

        self.status_toggle = not self.status_toggle

        guild_count = len(self.guilds)
        total_members = sum(g.member_count or 0 for g in self.guilds)

        if self.status_toggle:
            activity = discord.CustomActivity(
                name=f"clanking in {guild_count:,} servers!"
            )
        else:
            activity = discord.CustomActivity(
                name=f"clanking with {total_members:,} users!"
            )

        await self.change_presence(activity=activity)

        print(
            f"[STATUS UPDATE] Guilds: {guild_count} | Members: {total_members}"
        )

    @statusloop.before_loop
    async def before_statusloop(self):
        await self.wait_until_ready()
    
    @tasks.loop(minutes=30)
    async def update_stats(self):
        try:
            await self.dbl.post_guild_count()
            print(f"[TOPGG] Posted guild count: {len(self.guilds)}")
        except Exception as e:
            print("[TOPGG] Failed to post:", e)
    
    @update_stats.before_loop
    async def before_update_stats(self):
        await self.wait_until_ready()

bot = Clanker()
bot.data = data

@bot.event
async def on_ready():
    print(f"[READY] Logged in as {bot.user}")
    print("Clanker is alive 😎") # who the fuck put this stupid fucking shit ass fucking awful disgusting fucking shit emoji here

@bot.event
async def on_interaction(interaction: discord.Interaction):
    if interaction.type == discord.InteractionType.application_command:
        now = time.time()

        bot.active_users[interaction.user.id] = now

        expired = [
            uid
            for uid, last_seen in bot.active_users.items()
            if now - last_seen > 300
        ]

        for uid in expired:
            del bot.active_users[uid]

        bot.peak_ccu = max(bot.peak_ccu, len(bot.active_users))

        cmd = interaction.data.get("name")
        options = interaction.data.get("options", [])

        args = " ".join(str(opt["value"]) for opt in options) if options else ""

        print(f"[COMMAND LOG] @{interaction.user}: {cmd} {args}")

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

@bot.event
async def on_guild_join(guild: discord.Guild):
    embed = discord.Embed(
        title="👋 Thanks for adding Clanker!",
        description=(
            "Thanks for inviting **Clanker** to your server! ❤️\n\n"
            "## 💬 Join our Discord\n"
            "Need help, have a suggestion, report a bug, or just want to chat?\n"
            "Join our community server using the button below.\n\n"
            "## ⭐ Support Clanker\n"
            "Clanker is **100% free** and **always will be**.\n"
            "If you'd like to support the project, the best thing you can do is "
            "**leave a review and vote for us on Top.gg**. It only takes a few seconds "
            "and helps more people discover Clanker.\n\n"
            "**Thanks for being part of the Clanker community! 🔧**"
        ),
        colour=discord.Colour.blurple()
    )

    embed.set_footer(text="Made with ❤️ by the Clanker team")

    view = WelcomeView()
    sent = False

    owner = guild.owner
    if owner:
        try:
            await owner.send(embed=embed, view=view)
            sent = True
        except Exception:
            pass

    if not sent and guild.system_channel:
        perms = guild.system_channel.permissions_for(guild.me)
        if perms.send_messages:
            try:
                await guild.system_channel.send(embed=embed, view=view)
                sent = True
            except Exception:
                pass

    if not sent:
        for channel in guild.text_channels:
            perms = channel.permissions_for(guild.me)
            if perms.send_messages:
                try:
                    await channel.send(embed=embed, view=view)
                    break
                except Exception:
                    continue

async def main():
    async with bot:
        await bot.start(TOKEN)

asyncio.run(main())
