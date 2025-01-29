from __future__ import annotations

from typing import TYPE_CHECKING, Any, Generic, TypeVar

import discord
from discord.ext import commands
import discord.state as ds

from ._types import (
    ClientT_co,
    InteractionT,
)
from ._wait_for_overloads import WaitForOverloads

__all__ = ("InteractionClient",)

if TYPE_CHECKING:
    from typing_extensions import Self, TypeVar  # noqa: TC004

    InteractionT = TypeVar(
        "InteractionT",
        bound=discord.Interaction,
        default=discord.Interaction,
    )

    from discord.types.gateway import (
        InteractionCreateEvent as InteractionCreateEventPayload,
    )
else:
    InteractionT = TypeVar("InteractionT", bound=discord.Interaction)


if TYPE_CHECKING:
    from collections.abc import Callable

    from discord.ext.commands.bot import (  # pyright: ignore[reportMissingTypeStubs]
        PrefixType,
    )

    from ._types import (
        AutocompleteCallback,
        Check,
        ChoiceT,
        CommandCallback,
        ContextMenuCallback,
        GroupT,
        P,
        T,
    )

# fmt: off
__all__ = (  # noqa: RUF022
    "InteractionClient",
    "InteractionAutoShardedClient",
    "InteractionBot",
    "InteractionAutoShardedBot",
    "command",
    "context_menu",
    "check",
    "autocomplete",
)
# fmt: on


class _CustomInteractionState(
    ds.ConnectionState[ClientT_co],
    Generic[ClientT_co, InteractionT],
):
    def __init__(
        self,
        *args: Any,
        interaction_cls: type[InteractionT],
        **kwargs: Any,
    ) -> None:
        super().__init__(*args, **kwargs)

        self.__interaction_cls: type[InteractionT] = interaction_cls

    def parse_interaction_create(self, data: InteractionCreateEventPayload) -> None:
        interaction = self.__interaction_cls(data=data, state=self)

        if (
            data["type"] in (2, 4) and self._command_tree
        ):  # application command and auto complete
            self._command_tree._from_interaction(interaction)
        elif data["type"] == 3:  # interaction component
            # These keys are always there for this interaction type
            inner_data = data["data"]
            custom_id = inner_data["custom_id"]
            component_type = inner_data["component_type"]
            self._view_store.dispatch_view(component_type, custom_id, interaction)
        elif data["type"] == 5:  # modal submit
            # These keys are always there for this interaction type
            inner_data = data["data"]
            custom_id = inner_data["custom_id"]
            components = inner_data["components"]
            self._view_store.dispatch_modal(custom_id, interaction, components)

        self.dispatch("interaction", interaction)


class InteractionClient(
    WaitForOverloads[InteractionT],
    discord.Client,
):
    def __init__(
        self,
        *args: Any,
        intents: discord.Intents,
        interaction_cls: type[InteractionT],
        **kwargs: Any,
    ) -> None:
        # passed to _CustomInteractionState via _get_state
        kwargs["interaction_cls"] = interaction_cls
        super().__init__(*args, intents=intents, **kwargs)

        error_msg = f"interaction_cls must be a subclass of discord.Interaction not {interaction_cls!r}"
        try:
            if not issubclass(interaction_cls, discord.Interaction):
                raise TypeError(error_msg)
        except TypeError as exc:
            # inspect.isclass? no thanks.
            if "must be a class" in str(exc):
                raise TypeError(error_msg) from None

            raise

    if not TYPE_CHECKING:

        def _get_state(self, **options: Any) -> _CustomInteractionState[Self]:
            return _CustomInteractionState(
                dispatch=self.dispatch,
                handlers=self._handlers,
                hooks=self._hooks,
                http=self.http,
                **options,
            )

    if TYPE_CHECKING:

        async def on_interaction(self, interaction: InteractionT) -> Any:
            pass


class InteractionAutoShardedClient(
    InteractionClient[InteractionT],
    discord.AutoShardedClient,
):
    pass


class InteractionBot(
    commands.bot.BotBase,
    InteractionClient[InteractionT],
):
    if TYPE_CHECKING:
        from .tree import InteractionTree  # noqa: PLC0415

        tree: InteractionTree[  # pyright: ignore[reportIncompatibleMethodOverride]
            InteractionT
        ]

        def __init__(
            self,
            command_prefix: PrefixType[commands.Bot],
            *args: Any,
            intents: discord.Intents,
            interaction_cls: type[InteractionT],
            **kwargs: Any,
        ) -> None: ...


class InteractionAutoShardedBot(
    InteractionBot[InteractionT],
    InteractionAutoShardedClient[InteractionT],
):
    pass


def command(  # pyright: ignore[reportGeneralTypeIssues]
    *,
    name: str | discord.app_commands.locale_str = discord.utils.MISSING,
    description: str | discord.app_commands.locale_str = discord.utils.MISSING,
    nsfw: bool = False,
    auto_locale_strings: bool = True,
    extras: dict[Any, Any] = discord.utils.MISSING,
) -> Callable[
    [CommandCallback[GroupT, InteractionT, P, T]],
    discord.app_commands.Command[GroupT, P, T],
]:
    return discord.app_commands.command(  # pyright: ignore[reportReturnType]
        name=name,
        description=description,
        nsfw=nsfw,
        auto_locale_strings=auto_locale_strings,
        extras=extras,
    )


def context_menu(  # pyright: ignore[reportGeneralTypeIssues]
    *,
    name: str | discord.app_commands.locale_str = discord.utils.MISSING,
    nsfw: bool = False,
    auto_locale_strings: bool = True,
    extras: dict[Any, Any] = discord.utils.MISSING,
) -> Callable[[ContextMenuCallback], discord.app_commands.ContextMenu]:
    return discord.app_commands.context_menu(
        name=name,
        nsfw=nsfw,
        auto_locale_strings=auto_locale_strings,
        extras=extras,
    )


def check(predicate: Check) -> Callable[[T], T]:
    return discord.app_commands.check(predicate)


def autocomplete(  # pyright: ignore[reportGeneralTypeIssues]
    **parameters: AutocompleteCallback[InteractionT, GroupT, ChoiceT],
) -> Callable[[T], T]:
    return discord.app_commands.autocomplete(
        **parameters,  # pyright: ignore[reportArgumentType]
    )
