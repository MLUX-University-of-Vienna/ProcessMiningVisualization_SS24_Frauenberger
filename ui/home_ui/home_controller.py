import streamlit as st
from ui.base_ui.base_controller import BaseController
from utils.io import read_file, pickle_load
from analysis.detection_model import DetectionModel


class HomeController(BaseController):

    def __init__(self, views=None):
        self.detection_model = DetectionModel()
        if views is None:
            from ui.home_ui.home_view import HomeView

            views = [HomeView()]
        super().__init__(views)

    def get_page_title(self) -> str:
        return ""

    def process_file(self, file):

        file_type = self.detection_model.detect_file_type(file)
        # TODO: move io logic to a model
        # TODO: catch exceptions if file is not supported
        if file_type == "csv":
            line = file.readline().decode("utf-8")
            detected_delimiter = self.detection_model.detect_delimiter(line)
            file.seek(0)
            self.selected_view.display_df_import(detected_delimiter)
        elif file_type == "pickle":
            model = pickle_load(file)
            self.selected_view.display_model_import(model)
        else:
            # add logging here for unsupported file format
            st.session_state.error = "File format not supported"
            st.rerun()

    def set_model_and_algorithm(self, model, algorithm):
        st.session_state.model = model
        st.session_state.algorithm = algorithm

    def set_df(self, file, delimiter):
        if delimiter == "":
            st.session_state.error = "Please enter a delimiter"
            # change routing to home
            st.session_state.page = "Home"
            return
        # TODO: move io logic to a model
        st.session_state.df = read_file(file, delimiter=delimiter)

    def run(self, selected_view, index):
        self.selected_view = selected_view
        selected_view.display_intro()
        selected_view.display_file_upload()
