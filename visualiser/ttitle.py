import random
import asyncio
from typing import override

from textual.widgets import Static
from textual.app import RenderResult
from textual.reactive import reactive


# ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░
# ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░▀█▀░▀█▀░▀█▀░▀█▀░█░░░█▀▀
# ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░█░░░█░░░█░░░█░░█░░░█▀▀
# ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░▀░░░▀░░▀▀▀░░▀░░▀▀▀░▀▀▀
class TTitle(Static):
    _current = reactive(0)

    def __init__(self) -> None:
        super().__init__()
        self._titles = ["Abcde", "aBcde", "abCde", "abcDe", "abcdE"]

    def render(self) -> RenderResult:
        return f"{self._titles[self._current]}"

    # ########################################################################
    # ######################################################## ANIMATION #####
    def launch_animation(self) -> None:
        asyncio.create_task(self._run_animation())

    async def _run_animation(self) -> None:
        pass


# ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░
# ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░▀█▀░▀█▀░▀█▀░▀█▀░█░░░█▀▀░░░█▄█░█▀█░▀█▀░█▀█
# ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░█░░░█░░░█░░░█░░█░░░█▀▀░░░█░█░█▀█░░█░░█░█
# ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░▀░░░▀░░▀▀▀░░▀░░▀▀▀░▀▀▀░░░▀░▀░▀░▀░▀▀▀░▀░▀
class TTitleMain(TTitle):
    def __init__(self) -> None:
        super().__init__()
        self._titles = [
            """
▄▄▄▄▄   ▄▄      ▄▄ ▄▄             ▄▄   ▄▄  ▄▄
██▄▄    ██      ▀███▀     ▄▄▄     ██   ███▄██
██      ██▄▄▄     █               ██   ██ ▀██
            """,
            """
▄▄▄▄▄   ▄▄      ▄▄ ▄▄             ▄▄   ▄▄  ▄▄
██▄▄    ██      ▀███▀     ▀▄      ██   ███▄██
██      ██▄▄▄     █         ▀     ██   ██ ▀██
            """,
            """
▄▄▄▄▄   ▄▄      ▄▄ ▄▄             ▄▄   ▄▄  ▄▄
██▄▄    ██      ▀███▀      █      ██   ███▄██
██      ██▄▄▄     █        ▀      ██   ██ ▀██
            """,
            """
▄▄▄▄▄   ▄▄      ▄▄ ▄▄             ▄▄   ▄▄  ▄▄
██▄▄    ██      ▀███▀      ▄▀     ██   ███▄██
██      ██▄▄▄     █       ▀       ██   ██ ▀██
            """,
        ]

    @override
    async def _run_animation(self) -> None:
        while True:
            await asyncio.sleep(random.randint(2, 20))

            speed = random.randint(2, 20)
            for _ in range(random.randint(5, 20)):
                for i in range(len(self._titles)):
                    await asyncio.sleep(speed / 100)
                    self._current = i

            self._current = 0
