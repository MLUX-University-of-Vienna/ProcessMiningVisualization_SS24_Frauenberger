from graphs.visualization.base_graph import BaseGraph


class HeuristicGraph(BaseGraph):
    def __init__(
        self,
    ) -> None:
        super().__init__(rankdir="TB")

    def add_event(
        self,
        title: str,
        frequency: int,
        size: tuple[int, int],
        **event_data,
    ) -> None:
        event_data["frequency"] = frequency
        width, height = size
        label = f"{title}\n{frequency}"
        super().add_node(
            id=title,
            label=label,
            data=event_data,
            width=str(width),
            height=str(height),
            shape="box",
            style="rounded",  # , filled",
            # fillcolor="lightblue",
        )

    # Rename
    def create_edge(
        self,
        source: str,
        destination: str,
        size: float,
        weight: int = None,
    ) -> None:
        super().add_edge(source, destination, weight, penwidth=str(size))

    def add_starting_edges(self, start_nodes: list[str]) -> None:
        super().add_starting_edges(start_nodes, penwidth="0.1")

    def add_ending_edges(self, end_nodes: list[str]) -> None:
        super().add_ending_edges(end_nodes, penwidth="0.1")