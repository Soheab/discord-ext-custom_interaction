from __future__ import annotations

from typing import TYPE_CHECKING, Any, Concatenate, ParamSpec, TypeVar
from collections.abc import Callable, Coroutine

import discord
from discord.ext.commands import Cog  # pyright: ignore[reportMissingTypeStubs]

if TYPE_CHECKING:
    from typing_extensions import TypeVar  # noqa: TC004

    from discord import Client, Interaction

    ClientT_co = TypeVar("ClientT_co", bound=Client, covariant=True, default=Client)
    InteractionT = TypeVar(
        "InteractionT",
        bound=Interaction,
        default=Interaction,
    )
else:
    ClientT_co = TypeVar("ClientT_co", bound="Client", covariant=True)
    InteractionT = TypeVar("InteractionT", bound="Interaction")


CoroT = TypeVar("CoroT")
Coro = Coroutine[Any, Any, CoroT]


P = ParamSpec("P")
T = TypeVar("T")
F = TypeVar("F", bound=Callable[..., Any])

Binding = discord.app_commands.Group | Cog
GroupT = TypeVar("GroupT", bound=Binding)
UnboundError = Callable[
    [InteractionT, discord.app_commands.AppCommandError],
    Coro[Any],
]
Error = (
    Callable[[GroupT, InteractionT, discord.app_commands.AppCommandError], Coro[Any]]
    | UnboundError
)
Check = Callable[[InteractionT], bool | Coro[bool]]

CommandCallback = (  # pyright: ignore[reportGeneralTypeIssues]
    Callable[Concatenate[GroupT, InteractionT, P], Coro[T]]
    | Callable[Concatenate[InteractionT, P], Coro[T]]
)

ContextMenuCallback = (
    Callable[[InteractionT, discord.Member], Coro[Any]]
    | Callable[[InteractionT, discord.User], Coro[Any]]
    | Callable[[InteractionT, discord.Message], Coro[Any]]
    | Callable[[InteractionT, discord.Member | discord.User], Coro[Any]]
)
ChoiceT = TypeVar("ChoiceT", str, int, float, str | int | float)

AutocompleteCallback = (  # pyright: ignore[reportGeneralTypeIssues]
    Callable[
        [InteractionT, GroupT, str],
        Coro[list[discord.app_commands.Choice[ChoiceT]]],
    ]
    | Callable[[InteractionT, str], Coro[list[discord.app_commands.Choice[ChoiceT]]]]
)
