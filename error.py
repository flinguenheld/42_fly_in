from __future__ import annotations
from typing import Callable, Any, Dict


# ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░
# ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░█▀▀░█▀▄░█▀▄░█▀█░█▀▄
# ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░█▀▀░█▀▄░█▀▄░█░█░█▀▄
# ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░▀▀▀░▀░▀░▀░▀░▀▀▀░▀░▀
class ErrorFlyIn(Exception):
    def __init__(self, message: str, **context: str) -> None:
        super().__init__(message)
        self.context: Dict[str, str] = context

    # ########################################################################
    # ################################################################# + ####
    def __add__(self, other: Dict[str, str]) -> ErrorFlyIn:
        self.context.update(other)
        return self

    # ########################################################################
    # ################################################## STR WITH CONTEXT ####
    def str_with_context(self) -> str:

        text = ""
        if "title" in self.context:
            text += f"-= {self.context['title']} =-\n"
        if "file" in self.context:
            text += f"On file: '{self.context['file']}'\n"
        if "line" in self.context:
            text += f"On line: '{self.context['line']}'\n"

        text += "\n" + str(self)
        return text

    # ########################################################################
    # ################################################## SPREAD DECORATOR ####
    @staticmethod
    def spread(title: str) -> Callable:
        def decorator(func: Callable) -> Callable:
            def wrapper(*args: Any, **kwargs: Any) -> Any:

                try:
                    return func(*args, **kwargs)

                except ErrorFlyIn as e:
                    raise ErrorFlyIn(str(e), title=title) + e.context
                except Exception as e:
                    raise ErrorFlyIn(str(e), title=title)

            return wrapper

        return decorator
