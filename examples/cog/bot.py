# This is the basic.py example but with extensions and cogs.

from typing import Any

import discord

# import the extension
from discord.ext.custom_interactions import InteractionBot


# define a custom interaction class
class CustomInteraction(discord.Interaction):
    async def respond(self, *args: Any, **kwargs: Any) -> Any:
        if self.response.is_done():
            return await self.followup.send(*args, **kwargs)
        return await self.response.send_message(*args, **kwargs)


class MyBot(InteractionBot[CustomInteraction]):

    async def setup_hook(self):
        # load the extension
        await self.load_extension("extension")


bot = MyBot(
    command_prefix="!",
    intents=discord.Intents.default(),
    interaction_cls=CustomInteraction,
)


# define a slash command that uses the custom interaction class
@bot.tree.command()
async def ping(interaction: CustomInteraction):
    await interaction.respond("Pong!")


bot.run("TOKEN")
