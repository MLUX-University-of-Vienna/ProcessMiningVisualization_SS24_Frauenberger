from graphs.visualization.base_graph import BaseGraph


class InductiveGraph(BaseGraph):
    def __init__(
        self,
        process_tree,
        frequency: dict[str, int] = None,
        node_sizes: dict[str, tuple(float, float)] = None,
    ) -> None:
        super().__init__(rankdir="LR")
        self.exclusive_gates_count = 0
        self.parallel_gates_count = 0
        self.silent_activities_count = 0
        self.event_frequency = frequency
        self.node_sizes = node_sizes

        self.build_graph(process_tree)

    def build_graph(self, process_tree) -> None:
        self.add_start_node()
        self.add_end_node()

        start_node, end_node = self.add_section(process_tree)

        self.add_starting_edges([start_node])
        self.add_ending_edges([end_node])

    def add_event(
        self,
        title: str,
        **event_data,
    ) -> None:

        width, height = self.node_sizes.get(title, (1.5, 0.5))
        frequency = self.event_frequency.get(title, 0)
        label = f"{title} \\n {frequency}"
        super().add_node(
            id=title,
            label=label,
            data=event_data,
            width=str(width),
            height=str(height),
            shape="box",
            style="rounded, filled",
            fillcolor="#FFFFFF",
        )

    def add_section(self, process_tree) -> tuple:
        start_node, end_node = None, None

        if process_tree[0] == "seq":
            start_node, end_node = self.add_sequence(process_tree[1:])

        elif process_tree[0] == "xor":
            start_node, end_node = self.add_exclusive(process_tree[1:])

        elif process_tree[0] == "par":
            start_node, end_node = self.add_parallel(process_tree[1:])

        elif process_tree[0] == "loop":
            start_node, end_node = self.add_loop(process_tree[1:])

        return start_node, end_node

    # TODO: add sequence, exclusive, parallel, loop methods

    def add_sequence(self, process_tree) -> tuple:
        start_node, end_node = None, None
        for section in process_tree:
            if isinstance(section, tuple):
                start, end = self.add_section(section)
            elif isinstance(section, str) or isinstance(section, int):
                start, end = section, section

            if start_node is None:
                start_node = start

            if end_node is not None:
                self.add_edge(end_node, start)

            end_node = end

        return start_node, end_node

    def add_gate(self, type: str):
        node_attributes = {
            "shape": "diamond",
            "style": "filled",
            "fillcolor": "#FFFFFF",
        }

        if type.lower() == "xor":
            return self.add_exclusive_gate(**node_attributes)

        elif type.lower() == "par":
            return self.add_parallel_gate(**node_attributes)
        else:
            raise ValueError(f"Gate type {type} is not supported")

    def add_exclusive_gate(self, **node_attributes):
        start_id = f"exclusive_gate_start_{self.exclusive_gates_count}"
        end_id = f"exclusive_gate_end_{self.exclusive_gates_count}"

        self.add_node(id=start_id, label="X", **node_attributes)
        self.add_node(id=end_id, label="X", **node_attributes)
        self.exclusive_gates_count += 1

        return start_id, end_id

    def add_parallel_gate(self, **node_attributes):
        start_id = f"parallel_gate_start_{self.parallel_gates_count}"
        end_id = f"parallel_gate_end_{self.parallel_gates_count}"

        self.add_node(id=start_id, label="+", **node_attributes)
        self.add_node(id=end_id, label="+", **node_attributes)
        self.parallel_gates_count += 1

        return start_id, end_id