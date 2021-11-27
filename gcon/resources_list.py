from textual.widget import Widget
from rich.tree import Tree
from typing import Union
from gcp_resources import FunctionsResources


class ResourcesList(Widget):
    def __init__(self, project: str, name: Union[str, None] = None) -> None:
        self.project = project
        super().__init__(name=name)

    def on_mount(self):
        self.set_interval(10, self.refresh)

    def render(self) -> Tree:
        tree = Tree("Resources")
        functions_node = tree.add("Functions")
        [functions_node.add(r.display_name) for r in FunctionsResources(project=self.project).resources]
        return tree
