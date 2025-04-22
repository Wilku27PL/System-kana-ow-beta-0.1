import discord
from discord.ext import commands

class HelpEmbed(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.color = discord.Colour.from_rgb(0, 0, 0)
        self.embed = discord.Embed(color=self.color)

    def create(self, context):
        self.embed.add_field(name="view permission", value=f"?view - {context.author.mention}", inline=True)
        self.embed.add_field(name="speak permission", value=f"?speak - {context.author.mention}", inline=True)
        self.embed.add_field(name="reset permission", value=f"?reset - {context.author.mention}", inline=True)
        self.embed.add_field(name="global connect permission", value=f"?connect - ", inline=True)
        self.embed.add_field(name="global view permission", value=f"?view - ", inline=True)
        self.embed.add_field(name="global speak permission", value=f"?speak - ", inline=True)
        self.embed.add_field(name="reset global permissions", value=f"?reset", inline=True)
        self.embed.add_field(name="user limit", value=f"?limit 2", inline=True)
        self.embed.add_field(name="current channel", value=f"?vc", inline=True)
        self.embed.set_footer(text="to allow permission use +")
        

    def add_field(self, name, value, inline):
        self.embed.add_field(name=name, value=value, inline=inline)

    def to_dict(self):
        return self.embed.to_dict()

    async def send_help_embed(self, channel):
        """Send an embed help message to the specified channel."""
        embed = discord.Embed(
            title="Pomoc dla kanału głosowego",
            description="Lista dostępnych komend do zarządzania kanałem:",
            color=discord.Color.blue()
        )
        embed.add_field(name="?speak", value="Zarządzanie uprawnieniami mówienia.", inline=False)
        embed.add_field(name="?connect", value="Zarządzanie uprawnieniami połączenia.", inline=False)
        embed.add_field(name="?view", value="Zarządzanie widocznością kanału.", inline=False)
        embed.add_field(name="?chmod", value="Zarządzanie uprawnieniami moderatora.", inline=False)
        embed.add_field(name="?text", value="Zarządzanie uprawnieniami pisania na czacie.", inline=False)
        embed.add_field(name="?limit", value="Ustawianie limitu użytkowników.", inline=False)
        embed.add_field(name="?live", value="Zarządzanie uprawnieniami streamowania.", inline=False)
        embed.set_footer(text="Użyj odpowiednich komend, aby zarządzać swoim kanałem.")

        await channel.send(embed=embed)

async def setup(bot):
    # Add the HelpEmbed class as a cog to the bot
    await bot.add_cog(HelpEmbed(bot))