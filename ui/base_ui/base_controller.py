import streamlit as st
from abc import ABC, abstractmethod


class BaseController(ABC):

    def __init__(self, views=None):

        if views is None:
            # TODO: change to a more specific exception, add logging
            raise ValueError("At least one view must be provided to the controller")

        if isinstance(views, list) or isinstance(views, tuple):
            self.views = list(views)
        else:
            self.views = [views]

        self.error_message = None
        self.info_message = None
        self.success_message = None
        self.warning_message = None

    def select_view(self):
        return self.views[0], 0

    def read_values_from_session_state(self):
        if "error" in st.session_state:
            self.error_message = st.session_state.error
            del st.session_state.error

        if "info" in st.session_state:
            self.info_message = st.session_state.info
            del st.session_state.info

        if "success" in st.session_state:
            self.success_message = st.session_state.success
            del st.session_state.success

        if "warning" in st.session_state:
            self.warning_message = st.session_state.warning
            del st.session_state.warning

    def display_messages(self):
        if self.error_message is not None:
            self.view.display_error_message(self.error_message)

        if self.info_message is not None:
            self.view.display_info_message(self.info_message)

        if self.success_message is not None:
            self.view.display_success_message(self.success_message)

        if self.warning_message is not None:
            self.view.display_warning_message(self.warning_message)

    def start(self):
        self.read_values_from_session_state()
        slected_view, pos = self.select_view()
        slected_view.set_controller(self)
        slected_view.create_layout()
        self.display_messages()

    @abstractmethod
    def run(self, slected_view, index):
        raise NotImplementedError("Method run must be implemented in the child class")
