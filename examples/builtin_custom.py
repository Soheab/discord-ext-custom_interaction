# This example uses basic.py as a base and shows how to use the built-in CustomInteraction class
import discord

# import the extension
# and the builtin custom interaction class
from discord.ext.custom_interactions import InteractionBot, CustomInteraction


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
    # use the send method and author property from the custom interaction class
    await interaction.send(f"Pong! {interaction.author.mention}")


bot.run("TOKEN")
