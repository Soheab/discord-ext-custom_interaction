# This example shows how to use a custom interaction in a cog.
# The main problem is that the app_commands.command etc decorators forces the interaction type to be discord.Interaction
# for that purpose, we can import the command decorator from the custom_interactions module and use it instead.

from __future__ import annotations
from typing import TYPE_CHECKING

import discord
from discord.ext import commands

# I recommend doing it at type-checking only
# but it'll work at runtime as well, it literally calls the original decorator.
if TYPE_CHECKING:
    from discord.ext.custom_interactions import command

    # import our CustomInteraction class too, only for type-checking
    from .bot import CustomInteraction
else:
    command = discord.app_commands.command


class MyCog(commands.Cog):
    @command()
    # CustomInteraction being your custom interaction class
    async def test(self, interaction: CustomInteraction) -> None:
        await interaction.respond("Here it works too!")


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(MyCog(bot))
