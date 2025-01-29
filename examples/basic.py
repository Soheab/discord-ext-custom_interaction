# Using a custom interaction class with the InteractionBot, this functions like ext.commands.Bot that adds the interaction_cls kwarg.
# since Bot has a built-in CommandTree at `.tree`, it's already typed to use the custom interaction class.

from typing import Any

import discord

# import the extension
from discord.ext.custom_interaction import InteractionBot


# define a custom interaction class
class CustomInteraction(discord.Interaction):
    async def respond(self, *args: Any, **kwargs: Any) -> Any:
        if self.response.is_done():
            return await self.followup.send(*args, **kwargs)
        return await self.response.send_message(*args, **kwargs)


# before
# bot = commands.Bot(
#     command_prefix="!",
#     intents=discord.Intents.default(),
# )

# after
bot = InteractionBot(
    command_prefix="!",
    intents=discord.Intents.default(),
    interaction_cls=CustomInteraction,
)


# define a slash command that uses the custom interaction class
@bot.tree.command()
async def ping(interaction: CustomInteraction):
    await interaction.respond("Pong!")


bot.run("TOKEN")
