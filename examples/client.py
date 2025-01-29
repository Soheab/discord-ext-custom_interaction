# Using a custom interaction class with the InteractionClient, this is a subclass of discord.Client that adds the interaction_cls kwarg.

from typing import Any

import discord

# import the extension
from discord.ext.custom_interaction import InteractionClient, InteractionTree


# define a custom interaction class
class CustomInteraction(discord.Interaction):
    async def respond(self, *args: Any, **kwargs: Any) -> Any:
        if self.response.is_done():
            return await self.followup.send(*args, **kwargs)
        return await self.response.send_message(*args, **kwargs)


# before
# client = discord.Client(
#     intents=discord.Intents.default(),
# )

# after
client = InteractionClient(
    intents=discord.Intents.default(),
    interaction_cls=CustomInteraction,
)
# since Client doesn't have a built-in CommandTree, it's not typed to use the custom interaction class.
# you can import and use the InteractionTree class from the extension to add a CommandTree to the client instead.

# InteractionTree[CustomInteraction] types the tree to use the custom interaction class.
tree = InteractionTree[CustomInteraction](client)

# BUT, since it's only for type checking, you can do something like the following to still use dpy's built-in CommandTree:

# tree = discord.app_commands.CommandTree(client)
# from typing import TYPE_CHECKING

# if TYPE_CHECKING:
#     tree = InteractionTree[CustomInteraction](client)


# define a slash command that uses the custom interaction class
@tree.command()
async def ping(interaction: CustomInteraction):
    await interaction.respond("Pong!")


client.run("TOKEN")
