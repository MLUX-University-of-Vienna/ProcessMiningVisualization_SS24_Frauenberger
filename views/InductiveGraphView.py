from views.AlgorithmViewInterface import AlgorithmViewInterface
from graphs.visualization.inductive_graph import InductiveGraph
from controllers.InductiveMiningController import (
    InductiveMiningController,
)

from mining_algorithms.inductive_mining import InductiveMining
import streamlit as st
from components.sliders import slider


class InductiveGraphView(AlgorithmViewInterface):

    def __init__(self):
        self.controller = InductiveMiningController()

    def is_correct_model_type(self, model) -> bool:
        return isinstance(model, InductiveMining)

    def initialize_values(self):
        if "activity_threshold" not in st.session_state:
            st.session_state.activity_threshold = (
                self.controller.get_activity_threshold()
            )

        if "traces_treshold" not in st.session_state:
            st.session_state.traces_treshold = self.controller.get_traces_threshold()

    def render_sidebar(self):

        slider(
            label="Traces Threshold",
            min_value=0.0,
            max_value=1.0,
            key="traces_treshold",
            setValue=self.controller.set_traces_threshold,
            tooltip="""The traces threshold parameter determines the minimum frequency of a trace to be included in the graph. 
            All traces with a frequency that is lower than treshold * max_trace_frequency will be removed. The higher the value, the less traces will be included in the graph.""",
        )

        slider(
            label="Activity Threshold",
            min_value=0.0,
            max_value=1.0,
            key="activity_threshold",
            setValue=self.controller.set_activity_threshold,
            tooltip="""The activity threshold parameter determines the minimum frequency of an activity to be included in the graph. 
            All activities with a frequency that is lower than treshold * max_event_frequency will be removed.
            The higher the value, the less activities will be included in the graph.""",
        )

    def get_page_title(self) -> str:
        return "Inductive Mining"