discord-ext-custom_interaction
==============================
An extension for discord.py that allows you to subclass `discord.Interaction` to add custom functionality.

Installation
------------

.. code-block:: sh
    :linenos:

    pip install discord-ext-custom_interaction

Or from source:

.. code-block:: sh
    :linenos:

    pip install git+https://github.com/Soheab/discord-ext-custom_interaction

Examples
--------
See the [`examples`](/examples) directory for examples.

Pre-built custom interactions
-----------------------------
There are two pre-built custom interactions that you can use:

- `custom_interaction.CustomInteraction` - A custom interaction that has a `send` method and the following properties: `author`, `voice_client`.
- `custom_interaction.CustomGuildInteraction` - A custom interaction inherits from `CustomInteraction` and type hints `author` and `user` as `discord.Member` and `guild` as `discord.Guild`.