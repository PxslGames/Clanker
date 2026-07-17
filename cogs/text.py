# im a tehxt file!

from discord import app_commands, Interaction, User, TextChannel
from discord.ext import commands
import discord
import random

def uwuify(text: str) -> str:
    faces = ["(・`ω´・)", "uwu", "owo", ">w<", "^w^"]
    text = text.replace("r", "w").replace("l", "w")
    text = text.replace("R", "W").replace("L", "W")
    return text + " " + random.choice(faces)

def reverse_text(text: str) -> str:
    return text[::-1]

def random_case(text: str) -> str:
    return "".join(
        c.upper() if random.random() > 0.5 else c.lower()
        for c in text
    )

def no_vowels(text: str) -> str:
    return "".join(c for c in text if c.lower() not in "aeiou")

def snake_case(text: str) -> str:
    return text.replace(" ", "_").lower()

def mock(text: str) -> str:
    return "".join(
        c.upper() if i % 2 else c.lower()
        for i, c in enumerate(text)
    )

def leet(text: str) -> str:
    mapping = str.maketrans({
        "a": "4", "e": "3", "i": "1", "o": "0", "s": "5", "t": "7"
    })
    return text.translate(mapping)

def zalgo(text: str) -> str:
    zalgo_chars = ['̍','̎','̄','̅','̿','̑','̆','̐','͒','͗','͑']
    return "".join(c + "".join(random.choice(zalgo_chars) for _ in range(2)) for c in text)

class Text(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    async def resolve_text(
        self,
        interaction: Interaction,
        text: str,
        target: User,
        action_name: str
    ):
        channel = interaction.channel

        if not isinstance(channel, TextChannel):
            embed = discord.Embed(
                title="Error ❌",
                description=f"Cannot read messages here!",
                color=discord.Color.red()
            )
            await interaction.response.send_message(embed=embed)
            return None, None

        if target:
            async for msg in channel.history(limit=100):
                if msg.author.id == target.id and msg.content:
                    return (
                        msg.content,
                        f"{action_name} {target.display_name}'s last message ⌨️"
                    )

            embed = discord.Embed(
                title="Error ❌",
                description=f"Could not find a recent message from {target.mention} 😳",
                color=discord.Color.red()
            )
            await interaction.response.send_message(embed=embed)
            return None, None

        elif text:
            return text, f"{action_name} Text ⌨️"

        else:
            embed = discord.Embed(
                title="Error ❌",
                description="Please provide either text or ping a user!",
                color=discord.Color.red()
            )
            await interaction.response.send_message(embed=embed)
            return None, None
    
    async def transform_text(
        self,
        interaction: Interaction,
        text: str,
        target: User,
        action_name: str,
        transform_func
    ):
        text, title = await self.resolve_text(interaction, text, target, action_name)
        if text is None:
            return

        text = transform_func(text)

        embed = discord.Embed(
            title=title,
            description=text,
            color=discord.Color.blurple()
        )
        await interaction.response.send_message(embed=embed)

    @app_commands.command(name="text", description="see what the text category does")
    async def text(self, interaction: Interaction):
        command_count = len(self.get_app_commands())

        embed = discord.Embed(
            title="Text 📚",
            description=(
                "This category contains text manipulation commands.\n"
                f"There are currently **{command_count} commands** available."
            ),
            color=discord.Color.blurple()
        )

        await interaction.response.send_message(embed=embed)

    @app_commands.command(name="uwu", description="uwuify text")
    async def uwu(self, interaction: Interaction, text: str = None, target: User = None):
        await self.transform_text(interaction, text, target, "UwUifying", uwuify)

    @app_commands.command(name="caps", description="uppercase text")
    async def caps(self, interaction: Interaction, text: str = None, target: User = None):
        await self.transform_text(interaction, text, target, "Making", str.upper)

    @app_commands.command(name="lower", description="lowercase text")
    async def lower(self, interaction: Interaction, text: str = None, target: User = None):
        await self.transform_text(interaction, text, target, "Making", str.lower)

    @app_commands.command(name="reverse", description="reverse text")
    async def reverse(self, interaction: Interaction, text: str = None, target: User = None):
        await self.transform_text(interaction, text, target, "Reversing", reverse_text)

    @app_commands.command(name="randomcase", description="randomize letter casing")
    async def randomcase(self, interaction: Interaction, text: str = None, target: User = None):
        await self.transform_text(interaction, text, target, "Randomizing", random_case)

    @app_commands.command(name="novowels", description="remove vowels from text")
    async def novowels(self, interaction: Interaction, text: str = None, target: User = None):
        await self.transform_text(interaction, text, target, "Removing vowels from", no_vowels)

    @app_commands.command(name="snake", description="convert text to snake_case")
    async def snake(self, interaction: Interaction, text: str = None, target: User = None):
        await self.transform_text(interaction, text, target, "Snake-casing", snake_case)

    @app_commands.command(name="mock", description="mocking spongebob text")
    async def mock_cmd(self, interaction: Interaction, text: str = None, target: User = None):
        await self.transform_text(interaction, text, target, "Mocking", mock)
    
    @app_commands.command(name="leet", description="make text l33t c4s3")
    async def leet_cmd(self, interaction: Interaction, text: str = None, target: User = None):
        await self.transform_text(interaction, text, target, "Leeting", leet)

    @app_commands.command(name="zalgo", description="make text z̍͗͑a̎̄̐l̅̿͒g̑̆͗o̍̐̎")
    async def zalgo_cmd(self, interaction: Interaction, text: str = None, target: User = None):
        await self.transform_text(interaction, text, target, "Zalgoifying", zalgo)
    
async def setup(bot):
    await bot.add_cog(Text(bot))
