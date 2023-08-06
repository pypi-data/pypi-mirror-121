from time import sleep
from customselectmenu.option import Option
import os
import keyboard


class SelectMenu:
    def __init__(self, *options: Option) -> None:
        self.options = options

        self.running = False
        self.selected_index = 0

    def start(self) -> None:
        self.running = True

        while self.running:
            option_selected = self.options[self.selected_index]

            for op in self.options:
                op.active = False
            option_selected.active = True

            self.refresh()

            key = keyboard.read_key()

            if key == "w" or key == "up":
                self.selected_index -= 1
            if key == "s" or key == "down":
                self.selected_index += 1
            if key == "enter":
                if option_selected.exit:
                    self.stop()

                option_selected.function(option_selected)

            self.selected_index = min(self.selected_index, len(self.options) - 1)
            self.selected_index = max(self.selected_index, 0)

            sleep(0.1)

    def stop(self) -> None:
        self.running = False

    def refresh(self) -> None:
        if os.name == "nt":
            os.system("cls")
        else:
            os.system("clear")

        for op in self.options:
            print(op)
