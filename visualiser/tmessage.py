from textual.app import ComposeResult
from textual.screen import ModalScreen
from textual.widgets import Label, Button
from textual.containers import Vertical, Center, VerticalScroll

from visualiser.ttitle import TTitle, TTitleError, TTitleSuccess


# ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░
# ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░▀█▀░█▄█░█▀▀░█▀▀░█▀▀░█▀█░█▀▀░█▀▀
# ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░█░░█░█░█▀▀░▀▀█░▀▀█░█▀█░█░█░█▀▀
# ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░▀░░▀░▀░▀▀▀░▀▀▀░▀▀▀░▀░▀░▀▀▀░▀▀▀
class TMessage(ModalScreen):
    BINDINGS = [
        ("escape", "cancel", "Cancel"),
        ("enter", "cancel", "Cancel"),
        ("space", "cancel", "Cancel"),
        ("q", "cancel", "Cancel"),
    ]

    def __init__(
        self, title: TTitle, button: Button, message: str, css_class: str
    ) -> None:
        super().__init__()

        self._title = title
        self._bt_close = button

        self._layout = Vertical(
            classes=f"tmessage_layout_base tmessage_border_{css_class}",
        )

        self._message = Label(
            self._format_text(message),
            classes=f"tmessage_label tmessage_font_{css_class}",
            markup=False,
        )

    # ########################################################################
    # ###################################################### FORMAT TEXT #####
    def _format_text(self, message: str, max_len: int = 72) -> str:
        txt = ""
        for line in message.splitlines():
            if len(line) > max_len:
                if line[-1] == "'":
                    txt += f"{line[: max_len - 1]}...'\n"
                elif line[-1] == '"':
                    txt += f'{line[: max_len - 1]}..."\n'
                else:
                    txt += f"{line[:max_len]}...\n"

            else:
                txt += line + "\n"

        return txt

    # ########################################################################
    # ############################################################ MOUNT #####
    def compose(self) -> ComposeResult:
        with self._layout:
            yield self._title

            with VerticalScroll(classes="tmessage_scroll"):
                yield self._message

            with Center():
                yield self._bt_close

    # ########################################################################
    # ############################################################ CANCEL ####
    def action_cancel(self) -> None:
        self.dismiss(None)

    # ########################################################################
    # ################################################### BUTTON PRESSED #####
    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button == self._bt_close:
            self.action_cancel()


# ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░
# ░░░░░░░░░░░░░░░░░░░░░░░▀█▀░█▄█░█▀▀░█▀▀░█▀▀░█▀█░█▀▀░█▀▀░░░█▀▀░█▀▄░█▀▄░█▀█░█▀▄
# ░░░░░░░░░░░░░░░░░░░░░░░░█░░█░█░█▀▀░▀▀█░▀▀█░█▀█░█░█░█▀▀░░░█▀▀░█▀▄░█▀▄░█░█░█▀▄
# ░░░░░░░░░░░░░░░░░░░░░░░░▀░░▀░▀░▀▀▀░▀▀▀░▀▀▀░▀░▀░▀▀▀░▀▀▀░░░▀▀▀░▀░▀░▀░▀░▀▀▀░▀░▀
class TMessageError(TMessage):
    def __init__(self, message: str):
        super().__init__(
            TTitleError("tmessage_font_error"),
            Button(
                "Ok",
                variant="error",
                classes="tmessage_button",
            ),
            message,
            "error",
        )


# ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░
# ░░░░░░░░░░░░░░░▀█▀░█▄█░█▀▀░█▀▀░█▀▀░█▀█░█▀▀░█▀▀░░░█▀▀░█░█░█▀▀░█▀▀░█▀▀░█▀▀░█▀▀
# ░░░░░░░░░░░░░░░░█░░█░█░█▀▀░▀▀█░▀▀█░█▀█░█░█░█▀▀░░░▀▀█░█░█░█░░░█░░░█▀▀░▀▀█░▀▀█
# ░░░░░░░░░░░░░░░░▀░░▀░▀░▀▀▀░▀▀▀░▀▀▀░▀░▀░▀▀▀░▀▀▀░░░▀▀▀░▀▀▀░▀▀▀░▀▀▀░▀▀▀░▀▀▀░▀▀▀
class TMessageSuccess(TMessage):
    def __init__(self, message: str):
        super().__init__(
            TTitleSuccess("tmessage_font_success"),
            Button(
                "Ok",
                variant="success",
                classes="tmessage_button",
            ),
            message,
            "success",
        )
