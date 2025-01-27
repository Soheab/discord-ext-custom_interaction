# discord-ext-custom_interaction
An extension for discord.py that allows you to subclass `discord.Interaction` to add custom functionality.

## Installation

.. code-block:: sh
    pip install discord-ext-custom_interaction

Or from source:

.. code-block:: sh
    pip install git+https://github.com/Soheab/discord-ext-custom_interaction

## Basic example

.. code-block:: python
    import discord
    # import the extension
    from discord.ext import custom_interaction


    # define a custom interaction class
    class CustomInteraction(discord.Interaction):
        async def respond(self, *args, **kwargs) -> Any:
            if self.response.is_done():
                return await self.followup.send(*args, **kwargs)
            return await self.response.send_message(*args, **kwargs)

    # before
    # bot = commands.Bot(
    #     command_prefix="!",
    #     intents=discord.Intents.default(),
    # )

    # after
    bot = custom_interaction.InteractionBot(
        command_prefix="!",
        intents=discord.Intents.default(),
        interaction_cls=CustomInteraction,
    )

    # define a slash command that uses the custom interaction class
    @bot.tree.command()
    async def ping(interaction: CustomInteraction):
        await interaction.respond("Pong!")


    ... # same stuff

## Pre-built custom interactions
There are two pre-built custom interactions that you can use:

- `custom_interaction.CustomInteraction` - A custom interaction that has a `send` method and the following properties: `author`, `voice_client`.
- `custom_interaction.CustomGuildInteraction` - A custom interaction inherits from `CustomInteraction` and type hints `author` and `user` as `discord.Member` and `guild` as `discord.Guild`.