import discord
import asyncio
from discord.ext import commands

class Help(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='help', help='Wyświetla listę dostępnych komend lub informacje o konkretnej komendzie.')
    async def help_command(self, ctx, *command_name):
        if not command_name:
            # Display a categorized and styled list of all commands
            commands_per_page = 5
            categories = {}
            for command in self.bot.commands:
                if not command.hidden:
                    category = command.cog_name or "Inne"
                    if category not in categories:
                        categories[category] = []
                    categories[category].append(command)

            if not categories:
                await ctx.send("Brak dostępnych komend.")
                return

            pages = []
            for category, commands_list in categories.items():
                for i in range(0, len(commands_list), commands_per_page):
                    pages.append((category, commands_list[i:i + commands_per_page]))

            current_page = 0

            def create_embed(page):
                category, commands_list = pages[page]
                embed = discord.Embed(
                    title=f"Pomoc - {category}",
                    description=f"Strona {page + 1}/{len(pages)}",
                    color=discord.Color.dark_teal()
                )
                for command in commands_list:
                    embed.add_field(
                        name=f"`{ctx.prefix}{command.name}`",
                        value=command.help or "Brak opisu",
                        inline=False
                    )
                embed.set_footer(text="Styl: Dark Retro")
                return embed

            message = await ctx.send(embed=create_embed(current_page))

            if len(pages) > 1:
                reactions = ["◀️", "▶️", "❌"]
                for reaction in reactions:
                    await message.add_reaction(reaction)

                def check(reaction, user):
                    return (
                        user == ctx.author
                        and reaction.message.id == message.id
                        and str(reaction.emoji) in reactions
                    )

                while True:
                    try:
                        reaction, user = await self.bot.wait_for("reaction_add", timeout=60.0, check=check)

                        if str(reaction.emoji) == "❌":  # Exit condition
                            await message.clear_reactions()
                            break
                        elif str(reaction.emoji) == "▶️" and current_page < len(pages) - 1:
                            current_page += 1
                            await message.edit(embed=create_embed(current_page))
                        elif str(reaction.emoji) == "◀️" and current_page > 0:
                            current_page -= 1
                            await message.edit(embed=create_embed(current_page))

                        await message.remove_reaction(reaction, user)
                    except asyncio.TimeoutError:  # Properly handle timeout
                        await message.clear_reactions()
                        break
                    except Exception as e:
                        print(f"Error in help pagination: {e}")
                        await message.clear_reactions()
                        break
        else:
            # Display detailed help for a specific command
            command = self.bot.get_command(command_name[0])
            if command:
                embed = discord.Embed(title=f"Pomoc - {command.name}", color=discord.Color.dark_gold())
                embed.add_field(name="Opis", value=command.help or "Brak opisu", inline=False)
                embed.add_field(name="Użycie", value=f"`{ctx.prefix}{command.name} {command.signature}`", inline=False)
                embed.set_footer(text="Styl: Dark Retro")
                await ctx.send(embed=embed)
            else:
                await ctx.send(f"Komenda `{command_name[0]}` nie została znaleziona. Użyj `{ctx.prefix}help` aby zobaczyć listę dostępnych komend.")

async def setup(bot):
    await bot.add_cog(Help(bot))