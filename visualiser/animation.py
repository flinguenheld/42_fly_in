import asyncio
from typing import Callable, Any, Iterator


# ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░
# ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░█▀█░█▀█░▀█▀░█▄█
# ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░█▀█░█░█░░█░░█░█
# ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░▀░▀░▀░▀░▀▀▀░▀░▀
class Anim:
    """
    Mother to manage async animations.
    Override the _anim_run() method which will be start / stop on mount.
    Use the toggle_anim decorator to stop/restart all attributes which are
    Anim children.
    """

    def __init__(self) -> None:
        self._animation: asyncio.Task[None] | None = None

    async def _anim_run(self) -> None:
        pass

    # ########################################################################
    # ##################################################### ANIM ON / OFF ####
    async def anim_on(self) -> None:
        if self._animation is None:
            self._animation = asyncio.create_task(self._anim_run())

    async def anim_off(self) -> None:
        if self._animation is not None:
            self._animation.cancel()
            try:
                await self._animation
            except asyncio.CancelledError:
                pass
            finally:
                self._animation = None

    # ########################################################################
    # ################################################### MOUNT / UNMOUNT ####
    async def on_mount(self) -> None:
        await self.anim_on()

    async def on_unmount(self) -> None:
        await self.anim_off()

    # ########################################################################
    # ############################################# TOGGLE ANIM DECORATOR ####
    @staticmethod
    def toggle_anim(func: Callable) -> Any:
        """
        Get all attributes which have the 'anim_off' 'anim_on' methods.
        Then toggle animations while the decorated function is running.
        """

        def __attributes_with(instance: Any, which_method: str) -> Iterator:
            return filter(
                lambda a: hasattr(a, which_method),
                (
                    instance.__getattribute__(attr)
                    for attr in instance.__dict__.keys()
                ),
            )

        async def wrapper(*args: Any, **kwargs: Any) -> Any:

            for a in __attributes_with(args[0], "anim_off"):
                await a.anim_off()

            val = await func(*args, **kwargs)

            for a in __attributes_with(args[0], "anim_on"):
                await a.anim_on()

            return val

        return wrapper
