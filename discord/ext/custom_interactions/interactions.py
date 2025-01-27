from typing import Any, overload  # noqa: I002
from collections.abc import Sequence

import discord
from discord.utils import MISSING

__all__ = ("CustomGuildInteraction", "CustomInteraction")


class CustomInteraction(discord.Interaction):
    @property
    def author(self) -> discord.Member | discord.User:
        return self.user

    @property
    def voice_client(self) -> discord.VoiceProtocol | None:
        return self.guild and self.guild.voice_client

    @overload
    async def send(
        self,
        content: str = MISSING,
        *,
        username: str = MISSING,
        ephemeral: bool = MISSING,
        file: discord.File = MISSING,
        files: Sequence[discord.File] = MISSING,
        embed: discord.Embed = MISSING,
        embeds: Sequence[discord.Embed] = MISSING,
        allowed_mentions: discord.AllowedMentions = MISSING,
        view: discord.ui.View = MISSING,
        thread: discord.abc.Snowflake = MISSING,
        thread_name: str = MISSING,
        suppress_embeds: bool = MISSING,
        silent: bool = MISSING,
        applied_tags: list[discord.ForumTag] = MISSING,
        poll: discord.Poll = MISSING,
    ) -> discord.WebhookMessage: ...

    @overload
    async def send(
        self,
        content: str = MISSING,
        *,
        username: str = MISSING,
        ephemeral: bool = MISSING,
        file: discord.File = MISSING,
        files: Sequence[discord.File] = MISSING,
        embed: discord.Embed = MISSING,
        embeds: Sequence[discord.Embed] = MISSING,
        allowed_mentions: discord.AllowedMentions = MISSING,
        view: discord.ui.View = MISSING,
        thread: discord.abc.Snowflake = MISSING,
        thread_name: str = MISSING,
        suppress_embeds: bool = MISSING,
        silent: bool = MISSING,
        applied_tags: list[discord.ForumTag] = MISSING,
        poll: discord.Poll = MISSING,
    ) -> None: ...

    async def send(
        self,
        content: str = MISSING,
        *,
        username: str = MISSING,
        ephemeral: bool = False,
        file: discord.File = MISSING,
        files: Sequence[discord.File] = MISSING,
        embed: discord.Embed = MISSING,
        embeds: Sequence[discord.Embed] = MISSING,
        allowed_mentions: discord.AllowedMentions = MISSING,
        view: discord.ui.View = MISSING,
        thread: discord.abc.Snowflake = MISSING,
        thread_name: str = MISSING,
        suppress_embeds: bool = False,
        silent: bool = False,
        applied_tags: list[discord.ForumTag] = MISSING,
        poll: discord.Poll = MISSING,
    ) -> discord.WebhookMessage | None:
        send_kwargs: dict[str, Any] = {
            "content": content,
            "username": username,
            "ephemeral": ephemeral,
            "file": file,
            "files": files,
            "embed": embed,
            "embeds": embeds,
            "allowed_mentions": allowed_mentions,
            "view": view,
            "thread": thread,
            "thread_name": thread_name,
            "suppress_embeds": suppress_embeds,
            "silent": silent,
            "applied_tags": applied_tags,
            "poll": poll,
        }

        if self.response.is_done():
            return await self.followup.send(wait=True, **send_kwargs)

        return await self.response.send_message(**send_kwargs)


class CustomGuildInteraction(CustomInteraction):
    author: discord.Member  # pyright: ignore[reportIncompatibleMethodOverride]
    user: discord.Member  # pyright: ignore[reportIncompatibleVariableOverride]
    guild: discord.Guild  # pyright: ignore[reportIncompatibleMethodOverride]
