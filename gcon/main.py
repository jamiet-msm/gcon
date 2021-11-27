import argparse
from textual.app import App
from resources_list import ResourcesList
from textual.widgets import Placeholder
from rich.console import Console
from textual.driver import Driver
from typing import Type, Union


class FunctionsApp(App):
    def __init__(
        self,
        title: str,
        project: str,
        console: Union[Console, None] = None,
        screen: bool = True,
        driver_class: Union[Type[Driver], None] = None,
        log: str = "",
        log_verbosity: int = 1,
    ):
        self.project = project
        super().__init__(
            console=console,
            screen=screen,
            driver_class=driver_class,
            log=log,
            log_verbosity=log_verbosity,
            title=title,
        )

    async def on_load(self, event):
        await self.bind("q", "quit")

    async def on_mount(self) -> None:
        await self.view.dock(ResourcesList(project=self.project), edge="left", size=60)
        await self.view.dock(Placeholder(), edge="top")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="gcon")
    parser.add_argument("-project", type=str, help="GCP project")
    args = parser.parse_args()
    FunctionsApp.run(title=parser.description, project=args.project)
