import discord
from discord.ext import commands
from datetime import datetime, timedelta  # Import datetime and timedelta
from asyncio import sleep  # Import asyncio.sleep for proper delay handling

class VoiceChannelCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.temp_channel_mapping = {
            1358036171418239157: 1358037315968172239,  # Category and temp channel for role ⁑
            1360419193815830619: 1360419723526803526,  # Category and temp channel for role ⁑
            1360387763622379581: 1360401203007193188,  # Category and temp channel for role ID ⁑
            1360388495054471218: 1360402382101676182,  # Category and temp channel for role ID 1
            1360388540097364220: 1360402445704101908,  # Category and temp channel for role ID 2
            1360419938799452201: 1360421709395791952,  # Category and temp channel for role ID 3
            1360419940867244155: 1360421735496679524,  # Category and temp channel for role ID 4
            1360420023914729683: 1360421762935951460   # Category and temp channel for role ID 5
        }
        self.role_to_category_mapping = {
            1358053339983646790: 1358036171418239157,  # Only this role is allowed
        }
        self.allowed_role = "⁑"  # Only this role is allowed to create temporary channels
        self.roles_with_create_permissions = [1358053339983646790]  # Only this role ID
        self.allowed_roles = ["⁑"]  # Only this role name

    async def has_allowed_role(self, member):
        """Check if the member has the allowed role."""
        if not member.roles or len(member.roles) == 1:  # Ensure the user has at least one role (excluding @everyone)
            return False
        return any(role.id == 1358053339983646790 for role in member.roles)

    async def is_temp_channel(self, channel):
        """Check if the channel is a temporary user channel."""
        # Check if the channel is in the predefined list of temporary channels
        if channel.id in self.temp_channel_mapping.values():
            return True

        # Dynamically check if the channel name or category matches user-created patterns
        if channel.category and "user" in channel.category.name.lower():
            return True

        # Check if the channel name starts with a role name or user identifier
        if any(channel.name.startswith(role) for role in self.allowed_roles):
            return True

        return False

    @commands.command(name="speak", aliases=["s"])
    async def speak(self, ctx, action: str = None, user: discord.Member = None):
        """Zarządzanie uprawnieniami mówienia na kanale głosowym."""
        if not ctx.author.voice or not await self.is_temp_channel(ctx.author.voice.channel):
            await ctx.send("Ta komenda działa tylko na kanałach użytkowników.")
            return
        if not await self.has_allowed_role(ctx.author):
            await ctx.send("Nie masz odpowiedniej roli, aby użyć tej komendy.")
            return
        if not action or action not in ["+", "-"]:
            await ctx.send("Nieprawidłowe użycie komendy. Użyj ?speak + @użytkownik, ?speak - @użytkownik lub ?speak +/-.")
            return

        channel = ctx.author.voice.channel
        afk_channel = ctx.guild.get_channel(1358550526442344742)  # AFK channel
        if user:
            overwrite = channel.overwrites_for(user)
            overwrite.speak = action == "+"
            await channel.set_permissions(user, overwrite=overwrite)

            if afk_channel and action == "-":
                await user.move_to(afk_channel)
                await sleep(2)  # Wait for 2 seconds
                await user.move_to(channel)
            
            if afk_channel and action == "+" and user.voice and user.voice.channel == channel:
                await user.move_to(afk_channel)
                await sleep(2)  # Wait for 2 seconds
                await user.move_to(channel)

            await ctx.send(f"Prawo mówienia zostało {'nadane' if action == '+' else 'odebrane'} dla {user.mention}.")
        else:
            creator = ctx.author  # Assume the creator is the one managing the channel
            for member in channel.members:
                if member == creator:
                    continue  # Skip the creator of the channel
                overwrite = channel.overwrites_for(member)
                overwrite.speak = action == "+"
                await channel.set_permissions(member, overwrite=overwrite)
                if afk_channel and action == "-":
                    await member.move_to(afk_channel)
                    await sleep(2)  # Wait for 2 seconds
                    await member.move_to(channel)
                
                if afk_channel and action == "+":
                    await member.move_to(afk_channel)
                    await sleep(2) # Wait for 2 seconds
                    await member.move_to(channel)

            await ctx.send(f"Prawo mówienia zostało {'nadane' if action == '+' else 'odebrane'} wszystkim użytkownikom.")

    @commands.command(name="connect", aliases=["c"])
    async def connect(self, ctx, action: str = None, user: discord.Member = None):
        """Zarządzanie uprawnieniami połączenia na kanale głosowym."""
        if not ctx.author.voice or not await self.is_temp_channel(ctx.author.voice.channel):
            await ctx.send("Ta komenda działa tylko na kanałach użytkowników.")
            return
        if not await self.has_allowed_role(ctx.author):
            await ctx.send("Nie masz odpowiedniej roli, aby użyć tej komendy.")
            return
        if not action or action not in ["+", "-"]:
            await ctx.send("Nieprawidłowe użycie komendy. Użyj ?connect + @użytkownik, ?connect - @użytkownik lub ?connect +/-.")
            return

        channel = ctx.author.voice.channel
        afk_channel = ctx.guild.get_channel(1358550526442344742)  # AFK channel
        if user:
            overwrite = channel.overwrites_for(user)
            overwrite.connect = action == "+"
            await channel.set_permissions(user, overwrite=overwrite)

            if afk_channel and action == "-" and user.voice and user.voice.channel == channel:
                await user.move_to(afk_channel)

            await ctx.send(f"Prawo łączenia zostało {'nadane' if action == '+' else 'odebrane'} dla {user.mention}.")
        else:
            creator = ctx.author  # Assume the creator is the one managing the channel
            for member in channel.members:
                if member == creator:
                    continue  # Skip the creator of the channel
                overwrite = channel.overwrites_for(member)
                overwrite.connect = action == "+"
                await channel.set_permissions(member, overwrite=overwrite)

                if afk_channel and action == "-" and member.voice and member.voice.channel == channel:
                    await member.move_to(afk_channel)

            await ctx.send(f"Prawo łączenia zostało {'nadane' if action == '+' else 'odebrane'} wszystkim użytkownikom poza twórcą kanału.")

    @commands.command(name="live", aliases=["lv"])
    async def live(self, ctx, action: str = None, user: discord.Member = None):
        """Zarządzanie uprawnieniami streamowania na kanale głosowym."""
        if not ctx.author.voice or not await self.is_temp_channel(ctx.author.voice.channel):
            await ctx.send("Ta komenda działa tylko na kanałach użytkowników.")
            return
        if not await self.has_allowed_role(ctx.author):
            await ctx.send("Nie masz odpowiedniej roli, aby użyć tej komendy.")
            return
        if not action or action not in ["+", "-"]:
            await ctx.send("Nieprawidłowe użycie komendy. Użyj ?live + @użytkownik, ?live - @użytkownik lub ?live +/-.")
            return

        channel = ctx.author.voice.channel
        afk_channel = ctx.guild.get_channel(1358550526442344742)  # AFK channel
        if user:
            overwrite = channel.overwrites_for(user)
            overwrite.stream = action == "+"
            await channel.set_permissions(user, overwrite=overwrite)

            if afk_channel and action == "-":
                await user.move_to(afk_channel)
                await sleep(2)  # Wait for 2 seconds
                await user.move_to(channel)
            
            if afk_channel and action == "+" and user.voice and user.voice.channel == channel:
                await user.move_to(afk_channel)
                await sleep(2)  # Wait for 2 seconds
                await user.move_to(channel)

            await ctx.send(f"Prawo streamowania zostało {'nadane' if action == '+' else 'odebrane'} dla {user.mention}.")
        else:
            for member in channel.members:
                overwrite = channel.overwrites_for(member)
                overwrite.stream = action == "+"
                await channel.set_permissions(member, overwrite=overwrite)

                if afk_channel and action == "-":
                    await member.move_to(afk_channel)
                    await sleep(2)  # Wait for 2 seconds
                    await member.move_to(channel)

            await ctx.send(f"Prawo streamowania zostało {'nadane' if action == '+' else 'odebrane'} wszystkim użytkownikom.")

    @commands.command(name="view", aliases=["v"])
    async def view(self, ctx, action: str = None, target: str = None):
        """Ukryj kanał głosowy wszystkim użytkownikom poza twórcą kanału lub wybraną osobą."""
        if not ctx.author.voice or not await self.is_temp_channel(ctx.author.voice.channel):
            await ctx.send("Ta komenda działa tylko na kanałach użytkowników.")
            return
        if not await self.has_allowed_role(ctx.author):
            await ctx.send("Nie masz odpowiedniej roli, aby użyć tej komendy.")
            return
        if not action or action not in ["+", "-"]:
            await ctx.send("Nieprawidłowe użycie komendy. Użyj ?view + @użytkownik/id lub ?view - @użytkownik/id.")
            return

        channel = ctx.author.voice.channel
        afk_channel = ctx.guild.get_channel(1358550526442344742)  # AFK channel

        # Resolve user by mention or ID
        user = None
        if target:
            if target.isdigit():
                user = ctx.guild.get_member(int(target))
            else:
                user = ctx.message.mentions[0] if ctx.message.mentions else None

        if not user:
            await ctx.send("Nie znaleziono użytkownika. Użyj poprawnej wzmianki lub ID.")
            return

        overwrite = channel.overwrites_for(user)
        if action == "+":
            overwrite.view_channel = True
            overwrite.connect = True
            await ctx.send(f"{user.mention} może teraz widzieć i dołączać do kanału {channel.name}.")
        elif action == "-":
            overwrite.view_channel = False
            overwrite.connect = False
            await channel.set_permissions(user, overwrite=overwrite)

            # Move the user to the AFK channel if they are currently in the voice channel
            if user.voice and user.voice.channel == channel and afk_channel:
                await user.move_to(afk_channel)
                await ctx.send(f"{user.mention} został przeniesiony na kanał AFK i zablokowano mu dostęp do kanału {channel.name}.")
        await channel.set_permissions(user, overwrite=overwrite)
    @commands.command(name="text", aliases=["txt"])
    async def text(self, ctx, action: str = None, user: discord.Member = None):
        """Zarządzanie uprawnieniami pisania na czacie kanału głosowego."""
        if not ctx.author.voice or not await self.is_temp_channel(ctx.author.voice.channel):
            await ctx.send("Ta komenda działa tylko na kanałach użytkowników.")
            return
        if not await self.has_allowed_role(ctx.author):
            await ctx.send("Nie masz odpowiedniej roli, aby użyć tej komendy.")
            return
        if not action or action not in ["+", "-"]:
            await ctx.send("Nieprawidłowe użycie komendy. Użyj ?text + @użytkownik, ?text - @użytkownik lub ?text +/-.")
            return

        channel = ctx.author.voice.channel
        if user:
            overwrite = channel.overwrites_for(user)
            overwrite.send_messages = action == "+"
            await channel.set_permissions(user, overwrite=overwrite)
            await ctx.send(f"Prawo pisania na czacie zostało {'nadane' if action == '+' else 'odebrane'} dla {user.mention}.")
        else:
            for member in channel.members:
                overwrite = channel.overwrites_for(member)
                overwrite.send_messages = action == "+"
                await channel.set_permissions(member, overwrite=overwrite)
            await ctx.send(f"Prawo pisania na czacie zostało {'nadane' if action == '+' else 'odebrane'} wszystkim użytkownikom.")

    @commands.command(name="chmod", aliases=["ch"]) # Changed the command name to avoid conflict with built-in mod command
    async def chmod(self, ctx, action: str = None, user: discord.Member = None):
        """Zarządzanie uprawnieniami moderatora na kanale głosowym."""
        if not ctx.author.voice or not await self.is_temp_channel(ctx.author.voice.channel):
            await ctx.send("Ta komenda działa tylko na kanałach użytkowników.")
            return
        if not await self.has_allowed_role(ctx.author):
            await ctx.send("Nie masz odpowiedniej roli, aby użyć tej komendy.")
            return
        if not action or action not in ["+", "-"]:
            await ctx.send("Nieprawidłowe użycie komendy. Użyj ?chmod + @użytkownik lub ?chmod - @użytkownik.")
            return

        channel = ctx.author.voice.channel
        if user:
            overwrite = channel.overwrites_for(user)
            if action == "+":
                overwrite.manage_channels = True
                overwrite.manage_permissions = True
                await ctx.send(f"{user.mention} został dodany jako moderator kanału.")
            elif action == "-":
                overwrite.manage_channels = False
                overwrite.manage_permissions = False
                await ctx.send(f"{user.mention} został usunięty z listy moderatorów kanału.")
            await channel.set_permissions(user, overwrite=overwrite)
        else:
            await ctx.send("Musisz podać użytkownika.")

    @commands.command(name="autokick", aliases=["ak"])
    async def autokick(self, ctx, action: str = None, user: discord.Member = None):
        """Zarządzanie automatycznym wyrzucaniem użytkowników na kanale głosowym."""
        if not ctx.author.voice or not await self.is_temp_channel(ctx.author.voice.channel):
            await ctx.send("Ta komenda działa tylko na kanałach użytkowników.")
            return
        if not await self.has_allowed_role(ctx.author):
            await ctx.send("Nie masz odpowiedniej roli, aby użyć tej komendy.")
            return
        if not action or action not in ["+", "-"]:
            await ctx.send("Nieprawidłowe użycie komendy. Użyj ?autokick + @użytkownik lub ?autokick - @użytkownik.")
            return

        # Initialize or retrieve the autokick list from the bot's cache
        if not hasattr(self.bot, "autokick_list"):
            self.bot.autokick_list = {}

        channel = ctx.author.voice.channel

        if action == "+":
            if user:
                if channel.id not in self.bot.autokick_list:
                    self.bot.autokick_list[channel.id] = []

                if len(self.bot.autokick_list[channel.id]) >= 3:
                    await ctx.send("Lista autokick jest pełna (maksymalnie 3 osoby).")
                    return

                if user.id not in self.bot.autokick_list[channel.id]:
                    self.bot.autokick_list[channel.id].append(user.id)
                    await ctx.send(f"{user.mention} został dodany do listy autokick na kanale {channel.name}.")
                    
                    # Check if the user is currently in the channel and kick them
                    if user in channel.members:
                        afk_channel = ctx.guild.get_channel(1358550526442344742)  # AFK channel
                        if afk_channel:
                            await user.move_to(afk_channel)
                            await ctx.send(f"{user.mention} został automatycznie wyrzucony z kanału {channel.name}.")
                else:
                    await ctx.send(f"{user.mention} już znajduje się na liście autokick.")
            else:
                await ctx.send("Musisz podać użytkownika.")
        elif action == "-":
            if user:
                if channel.id in self.bot.autokick_list and user.id in self.bot.autokick_list[channel.id]:
                    self.bot.autokick_list[channel.id].remove(user.id)
                    await ctx.send(f"{user.mention} został usunięty z listy autokick na kanale {channel.name}.")
                else:
                    await ctx.send(f"{user.mention} nie znajduje się na liście autokick.")
            else:
                await ctx.send("Musisz podać użytkownika.")

    @commands.Cog.listener()
    async def on_voice_state_update(self, member, before, after):
        """Automatyczne wyrzucanie użytkowników z listy autokick."""
        if after.channel:
            channel_id = after.channel.id
            if hasattr(self.bot, "autokick_list") and channel_id in self.bot.autokick_list:
                if member.id in self.bot.autokick_list[channel_id]:
                    afk_channel = member.guild.get_channel(1358550526442344742)  # AFK channel
                    if afk_channel:
                        await member.move_to(afk_channel)
                        await after.channel.guild.system_channel.send(
                            f"{member.mention} został automatycznie wyrzucony z kanału {after.channel.name}."
                        )

    @commands.Cog.listener()
    async def on_voice_state_update(self, member, before, after):
        """Automatyczne tworzenie kanałów głosowych w odpowiednich kategoriach."""
        if after.channel and after.channel.id in self.temp_channel_mapping.values():
            guild = member.guild

            # Ensure the member has the allowed role
            if not await self.has_allowed_role(member):
                await member.send("Nie masz odpowiedniej roli, aby utworzyć kanał głosowy.")
                return

            # Determine the assigned category based on the temporary channel
            assigned_category = None
            for category_id, temp_channel_id in self.temp_channel_mapping.items():
                if after.channel.id == temp_channel_id:
                    assigned_category = discord.utils.get(guild.categories, id=category_id)
                    break

            if not assigned_category:
                return

            # Create a temporary voice channel
            temp_channel = await guild.create_voice_channel(
                name=f"{self.allowed_role}-{member.display_name}",
                category=assigned_category,
                user_limit=99
            )

            # Set default permissions for the channel
            overwrite = discord.PermissionOverwrite(
                connect=True,
                speak=True,
                stream=True,
                view_channel=True,
                send_messages=True
            )
            await temp_channel.set_permissions(guild.default_role, overwrite=overwrite)

            # Assign ownership to the user who created the channel
            owner_overwrite = discord.PermissionOverwrite(
                manage_channels=True,
                manage_permissions=True
            )
            await temp_channel.set_permissions(member, overwrite=owner_overwrite)

            # Move the user to the new channel
            await member.move_to(temp_channel)

            # Monitor the channel and delete it when the creator leaves
            while True:
                await sleep(10)
                temp_channel = discord.utils.get(guild.voice_channels, id=temp_channel.id)
                if not temp_channel or len(temp_channel.members) == 0 or member not in temp_channel.members:
                    if temp_channel:
                        await temp_channel.delete()
                    break

    @commands.Cog.listener()
    async def on_ready(self):
        """Ensure roles have permissions to create channels under specified categories."""
        guild = self.bot.get_guild(1357375974458654881)  # Replace with your guild ID
        if not guild:
            return

        for role_id, category_id in self.role_to_category_mapping.items():
            role = discord.utils.get(guild.roles, id=role_id)
            if role:
                category = discord.utils.get(guild.categories, id=category_id)
                if category:
                    overwrite = discord.PermissionOverwrite(manage_channels=True)
                    await category.set_permissions(role, overwrite=overwrite)

    @commands.command(name="voicechat", aliases=["vc"])
    async def voicechat(self, ctx):
        """Wysyła informacje o kanale głosowym."""
        if not ctx.author.voice or not ctx.author.voice.channel:
            await ctx.send("Musisz być na kanale głosowym, aby użyć tej komendy.")
            return

        channel = ctx.author.voice.channel
        owner = channel.guild.owner.mention if channel.guild and channel.guild.owner else "Nieznany właściciel"

        default_role = ctx.guild.default_role if ctx.guild else None
        permissions = {
            "connect": "Włączone" if default_role and channel.permissions_for(default_role).connect else "Wyłączone",
            "speak": "Włączone" if default_role and channel.permissions_for(default_role).speak else "Wyłączone",
            "stream": "Włączone" if default_role and channel.permissions_for(default_role).stream else "Wyłączone",
            "view": "Włączone" if default_role and channel.permissions_for(default_role).view_channel else "Wyłączone",
            "text": "Włączone" if default_role and channel.permissions_for(default_role).send_messages else "Wyłączone"
        }

        moderators = [
            member.mention for member in channel.members
            if any(role.permissions.manage_channels for role in member.roles)
        ]
        moderators_text = ", ".join(moderators) if moderators else "Brak"

        embed = discord.Embed(
            title="Informacje o kanale głosowym",
            description="Aktualne informacje o kanale oraz jego uprawnieniach.",
            color=discord.Color.blue()
        )
        embed.add_field(name="Właściciel", value=owner, inline=False)
        embed.add_field(name="Moderatorzy", value=moderators_text, inline=False)
        embed.add_field(
            name="Uprawnienia domyślne",
            value="\n".join([f"{perm}: {status}" for perm, status in permissions.items()]),
            inline=False
        )

        # Add information about categories and temporary channels
        categories_info = ""
        for category_id, temp_channel_id in self.temp_channel_mapping.items():
            category = discord.utils.get(ctx.guild.categories, id=category_id)
            temp_channel = discord.utils.get(ctx.guild.voice_channels, id=temp_channel_id)
            if category and temp_channel:
                categories_info += f"Kategoria: {category.name}, Kanał tymczasowy: {temp_channel.name}\n"

        embed.add_field(name="Kategorie i kanały tymczasowe", value=categories_info or "Brak danych", inline=False)
        embed.set_footer(text=f"Kanał: {channel.name}")

        await ctx.send(embed=embed)

    @commands.command(name="reset", aliases=["rt"])
    async def reset(self, ctx):
        """Reset all permissions in the voice channel."""
        if not ctx.author.voice or not await self.is_temp_channel(ctx.author.voice.channel):
            await ctx.send("Ta komenda działa tylko na kanałach użytkowników.")
            return
        if not await self.has_allowed_role(ctx.author):
            await ctx.send("Nie masz odpowiedniej roli, aby użyć tej komendy.")
            return
        channel = ctx.author.voice.channel
        members_to_reconnect = channel.members  # Store members currently in the channel
        await channel.edit(overwrites={})
        await ctx.send("Wszystkie uprawnienia zostały zresetowane.")

        # Reconnect all users in the channel
        for member in members_to_reconnect:
            if member.voice and member.voice.channel != channel:
                await member.move_to(channel)

    @commands.command(name="limit", aliases=["l"])
    async def limit(self, ctx, limit: int):
        """Ustaw limit użytkowników w kanale głosowym."""
        if not ctx.author.voice or not await self.is_temp_channel(ctx.author.voice.channel):
            await ctx.send("Ta komenda działa tylko na kanałach użytkowników.")
            return
        if not await self.has_allowed_role(ctx.author):
            await ctx.send("Nie masz odpowiedniej roli, aby użyć tej komendy.")
            return
        if 1 <= limit <= 99:
            channel = ctx.author.voice.channel
            await channel.edit(user_limit=limit)
            await ctx.send(f"Limit użytkowników został ustawiony na {limit}.")
        else:
            await ctx.send("Podaj prawidłowy limit w zakresie od 1 do 99.")

async def setup(bot):
    await bot.add_cog(VoiceChannelCommands(bot))
