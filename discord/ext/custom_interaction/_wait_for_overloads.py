from __future__ import annotations

from typing import (
    TYPE_CHECKING,
    Any,
    Generic,
    Literal,
    overload,
)

from ._types import InteractionT

if TYPE_CHECKING:
    from collections.abc import Callable

    from discord import (
        AutoShardedClient,
        Client,
    )
    from discord.app_commands import Command, ContextMenu
    from discord.ext.commands import (  # pyright: ignore[reportMissingTypeStubs]
        AutoShardedBot,
        Bot,
    )

    class WaitForOverloads(Generic[InteractionT]):
        @overload
        async def wait_for(  # pyright: ignore[reportNoOverloadImplementation]
            self: Client | AutoShardedClient | Bot | AutoShardedBot | WaitForOverloads,
            event: Literal["app_command_completion"],
            /,
            *,
            check: (
                Callable[[InteractionT, Command[Any, ..., Any] | ContextMenu], bool]
                | None
            ) = ...,
            timeout: float | None = ...,
        ) -> tuple[InteractionT, Command[Any, ..., Any] | ContextMenu]: ...

        @overload
        async def wait_for(
            self: Client | AutoShardedClient | Bot | AutoShardedBot | WaitForOverloads,
            event: Literal["interaction"],
            /,
            *,
            check: Callable[[InteractionT], bool] | None = ...,
            timeout: float | None = ...,
        ) -> InteractionT: ...

else:

    class WaitForOverloads(Generic[InteractionT]):
        pass
