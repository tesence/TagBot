import os
import logging
import sqlite3

import discord
from discord import app_commands
from discord.ext import commands

import asqlite

logger = logging.getLogger(__name__)

DB_NAME = os.getenv('TAG_BOT_DB_FILE_PATH')


class Tag(commands.Cog):
    """Custom Tag Cog"""

    def __init__(self, bot):
        self.bot = bot

    def _format_log_output(self, query, *params):
        return f"{query} [{', '.join([str(param) for param in params])}]"

    tag_group = app_commands.Group(name="tag", description="Tag commands")

    @tag_group.command(name='get')
    @app_commands.describe(code="Tag code")
    async def tag_get(self, interaction: discord.Interaction, code: str):
        """Retrieve a tag from its code

        Args:
            interaction (discord.Interaction): Discord interaction
            code (str): Tag identifier
        """
        async with asqlite.connect(DB_NAME) as connection:
            query = "UPDATE tags SET usage = usage + 1 " \
                    "WHERE code = ? AND guild_id = ? AND deleted_at IS NULL " \
                    "RETURNING content;"
            logger.debug(self._format_log_output(query, code, interaction.guild_id))
            tag = await connection.fetchone(query, code, interaction.guild_id)
            if tag:
                await interaction.response.send_message(tag['content'])
            else:
                await interaction.response.send_message(f"The tag `{code}` does not exist", ephemeral=True)
                logger.info("The tag `%s` does not exist", code)

    @tag_group.command(name='create')
    @app_commands.describe(code="Tag code")
    @app_commands.describe(content="Tag content")
    async def tag_create(self, interaction: discord.Interaction, code: str, content: str):
        """Create a tag

        Args:
            interaction (discord.Interaction): Discord interaction
            code (str): Tag identifier
            content (str): Tag body
        """
        async with asqlite.connect(DB_NAME) as connection:
            query = "INSERT INTO tags (code, content, author_id, guild_id) VALUES (?, ?, ?, ?);"
            logger.debug(self._format_log_output(query, code, content, interaction.user.id, interaction.guild_id))
            try:
                await connection.execute(query, code, content, interaction.user.id, interaction.guild_id)
                await interaction.response.send_message(f"The tag `{code}` has successfully been created",
                                                        ephemeral=True)
                logger.info("The tag `%s` has successfully been created", code)
            except sqlite3.IntegrityError:
                await interaction.response.send_message(f"The tag `{code}` already exists", ephemeral=True)
                logger.info("The tag `%s` already exists", code)

    @tag_group.command(name='delete')
    @app_commands.describe(code="Tag code")
    async def tag_delete(self, interaction: discord.Interaction, code: str):
        """Delete a tag

        Args:
            interaction (discord.Interaction): Discord interaction
            code (str): Tag identifier
        """
        async with asqlite.connect(DB_NAME) as connection:
            query = "UPDATE tags SET deleted_at = (strftime('%Y-%m-%d %H:%M:%f', 'now', 'utc')) " \
                    "WHERE code = ? AND guild_id = ? AND deleted_at is NULL " \
                    "RETURNING *;"
            logger.debug(self._format_log_output(query, code, interaction.guild_id))
            tag = await connection.fetchone(query, code, interaction.guild_id)
            if tag:
                await interaction.response.send_message(f"The tag `{code}` has successfully been deleted",
                                                        ephemeral=True)
                logger.info("The tag `%s` has successfully been deleted", code)
            else:
                await interaction.response.send_message(f"The tag `{code}` does not exist", ephemeral=True)
                logger.info("The tag `%s` does not exist", code)

    @tag_group.command(name='list')
    async def tag_list(self, interaction: discord.Interaction):
        """List all tags available

        Args:
            interaction (discord.Interaction): Discord interaction
        """
        async with asqlite.connect(DB_NAME) as connection:
            query = "SELECT code FROM tags WHERE guild_id = ? AND deleted_at is NULL;"
            logger.debug(self._format_log_output(query, interaction.guild_id))
            tags = [tag['code'] for tag in await connection.fetchall(query, interaction.guild_id)]
            result = f"**Available tags**: {', '.join(sorted(tags))}" if tags else "No tag available"
            await interaction.response.send_message(result, ephemeral=True)

    @tag_get.autocomplete('code')
    @tag_delete.autocomplete('code')
    async def tag_autocomplete(self, interaction: discord.Interaction, current: str):
        """Tag code autocomplete

        Args:
            interaction (discord.Interaction): discord interaction
            current (str): current parameter value

        Returns:
            List[app_commands.Choice]: List of current choices
        """
        async with asqlite.connect(DB_NAME) as connection:
            query = "SELECT code FROM tags " \
                    "WHERE guild_id = ? AND deleted_at is NULL AND code LIKE ? " \
                    "LIMIT 25;"
            logger.debug(self._format_log_output(query, interaction.guild_id, f"%{current}%"))
            tags = await connection.fetchall(query, interaction.guild_id, f"%{current}%")
            return [app_commands.Choice(name=tag['code'], value=tag['code']) for tag in tags]

# pylint: disable=missing-function-docstring
async def setup(bot):
    await bot.add_cog(Tag(bot))
