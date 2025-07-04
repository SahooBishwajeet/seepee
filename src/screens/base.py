from textual.screen import Screen
from textual.binding import Binding
from textual.widgets import Button, Input, Select
from textual.events import Key


class BaseScreen(Screen):

    BINDINGS = [
        Binding("escape", "app.pop_screen", "Back", show=True),
        Binding("up", "focus_previous", "Up", show=False),
        Binding("down", "focus_next", "Down", show=False),
        Binding("enter", "activate_focused", "Select", show=False),
    ]

    def notify_error(self, message: str) -> None:
        self.notify(message, severity="error")

    def notify_success(self, message: str) -> None:
        self.notify(message, severity="success")

    def get_focusable_widgets(self):

        widgets = []
        for widget_type in (Button, Input, Select):
            widgets.extend(self.query(widget_type))
        return widgets

    def action_focus_previous(self) -> None:

        current = self.screen.focused
        widgets = self.get_focusable_widgets()
        if not widgets:
            return
        if current not in widgets:
            widgets[0].focus()
            return
        idx = widgets.index(current)
        widgets[(idx - 1) % len(widgets)].focus()

    def action_focus_next(self) -> None:

        current = self.screen.focused
        widgets = self.get_focusable_widgets()
        if not widgets:
            return
        if current not in widgets:
            widgets[0].focus()
            return
        idx = widgets.index(current)
        widgets[(idx + 1) % len(widgets)].focus()

    def action_activate_focused(self) -> None:

        focused = self.screen.focused
        if isinstance(focused, Button):
            focused.press()

    def on_key(self, event: Key) -> None:

        if event.key == "escape" and isinstance(self, BaseScreen):
            if len(self.app.screen_stack) <= 1:
                self.app.exit()
