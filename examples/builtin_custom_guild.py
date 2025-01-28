# This example uses builtin_custom.py as a base and shows how to use the built-in CustomGuildInteraction class
import discord

# import the extension
# and the builtin custom interaction class
from discord.ext.custom_interactions import InteractionBot, CustomGuildInteraction


# before
# bot = commands.Bot(
#     command_prefix="!",
#     intents=discord.Intents.default(),
# )

# after
bot = InteractionBot(
    command_prefix="!",
    intents=discord.Intents.default(),
    interaction_cls=CustomGuildInteraction,
)


# define a slash command that uses the custom interaction class
@bot.tree.command()
async def ping(interaction: CustomGuildInteraction):
    # interaction.guild etc won't be None/User AT TYPE CHECKING TIME
    print(
        type(interaction.guild), type(interaction.channel), type(interaction.user)
    )  # discord.Guild, discord.abc.GuildChannel, discord.Member
    await interaction.send(f"Pong! {interaction.author.mention}")


bot.run("TOKEN")
