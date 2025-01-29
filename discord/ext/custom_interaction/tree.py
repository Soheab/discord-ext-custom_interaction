from __future__ import annotations

from typing import (
    TYPE_CHECKING,
    Any,
    Generic,
)

import discord

from ._types import InteractionT

if TYPE_CHECKING:
    from typing_extensions import Self


__all__ = ("InteractionTree",)


class InteractionTree(
    discord.app_commands.CommandTree,
    Generic[InteractionT],
):

    if TYPE_CHECKING:
        from collections.abc import Callable, Sequence  # noqa: PLC0415

        from ._types import (  # noqa: PLC0415
            CommandCallback,
            ContextMenuCallback,
            Coro,
            P,
            T,
        )

        def command(
            self: Self,
            *,
            name: str | discord.app_commands.locale_str = discord.utils.MISSING,
            description: str | discord.app_commands.locale_str = discord.utils.MISSING,
            nsfw: bool = False,
            guild: discord.abc.Snowflake | None = discord.utils.MISSING,
            guilds: Sequence[discord.abc.Snowflake] = discord.utils.MISSING,
            auto_locale_strings: bool = True,
            extras: dict[Any, Any] = discord.utils.MISSING,
        ) -> Callable[
            [CommandCallback[discord.app_commands.Group, InteractionT, P, T]],
            discord.app_commands.Command[discord.app_commands.Group, P, T],
        ]: ...

        def context_menu(
            self: Self,
            *,
            name: str | discord.app_commands.locale_str = discord.utils.MISSING,
            nsfw: bool = False,
            guild: discord.abc.Snowflake | None = discord.utils.MISSING,
            guilds: Sequence[discord.abc.Snowflake] = discord.utils.MISSING,
            auto_locale_strings: bool = True,
            extras: dict[Any, Any] = discord.utils.MISSING,
        ) -> Callable[[ContextMenuCallback], discord.app_commands.ContextMenu]: ...

        async def interaction_check(  # pyright: ignore[reportIncompatibleMethodOverride]
            self,
            interaction: InteractionT,
            /,
        ) -> bool: ...

        def error(  # pyright: ignore[reportIncompatibleMethodOverride]
            self,
            coro: Callable[
                [InteractionT, discord.app_commands.AppCommandError],
                Coro[Any],
            ],
        ) -> Callable[
            [InteractionT, discord.app_commands.AppCommandError],
            Coro[Any],
        ]: ...

        async def on_error(  # pyright: ignore[reportIncompatibleMethodOverride]
            self,
            interaction: InteractionT,
            error: discord.app_commands.AppCommandError,
            /,
        ) -> None: ...
