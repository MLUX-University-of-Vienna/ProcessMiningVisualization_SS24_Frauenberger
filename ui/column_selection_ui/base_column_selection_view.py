import streamlit as st
from abc import ABC, abstractmethod
from ui.base_ui.base_view import BaseView
from components.buttons import home_button, navigation_button


class BaseColumnSelectionView(BaseView):
    """Base class for the column selection view.
    It provides the basic layout and methods for the column selection view and allows for customization by the child classes.
    """

    def create_layout(self):
        """Creates the layout for the column selection view."""
        super().create_layout()
        self.column_selections_container = st.container()
        self.df_container = st.container()
        self.back_col, _, self.algorithm_column, _, self.mine_col = st.columns(
            [2, 1, 4, 1, 2]
        )

    @abstractmethod
    def get_needed_columns(self) -> list[str]:
        """Returns the columns needed for the algorithm. This will be used to display the column selection options.
        This must be implemented in the child class.

        Returns
        -------
        list[str]
            The columns needed for the algorithm.

        Raises
        ------
        NotImplementedError
            If the method is not implemented in the child class.
        """
        raise NotImplementedError(
            "Method get_needed_columns must be implemented in the child class"
        )

    @abstractmethod
    def get_column_styles(self) -> dict[str, str]:
        """Returns the styles for the columns. This will be used to style the column selection options.
        The keys are the column names (e.g. time_column) and the values are the styles for the selected columns.

        Returns
        -------
        dict[str, str]
            The styles for the columns. The keys are the needed columns e.g 'time_column' and the values are the styles for the selected columns.

        Raises
        ------
        NotImplementedError
            If the method is not implemented in the child class.
        """
        raise NotImplementedError(
            "Method get_column_styles must be implemented in the child class"
        )

    @abstractmethod
    def render_column_selections(self, columns: list[str]):
        """Renders the column selection options. This must be implemented in the child class.
        The column selection options are rendered in the column_selections_container automatically.
        The streamlit select or multiselect widget should be used to render the column selection options.


        Parameters
        ----------
        columns : list[str]
            The names of the needed columns

        Raises
        ------
        NotImplementedError
            If the method is not implemented in the child class.
        """
        raise NotImplementedError(
            "Method render_column_selections must be implemented in the child class"
        )

    def display_column_selections(self, columns: list[str]):
        """Displays the column selection options in the column_selections_container.

        Parameters
        ----------
        columns : list[str]
            The names of the needed columns
        """
        with self.column_selections_container:
            self.render_column_selections(columns)

    def display_algorithm_selection(self, algorithm_selection_options: list[str]):
        """Displays the algorithm selection options.

        Parameters
        ----------
        algorithm_selection_options : list[str]
            The algorithm selection options.
        """
        with self.algorithm_column:
            algorithm = st.selectbox(
                "Select the algorithm",
                algorithm_selection_options,
                key="algorithm_selection",
            )

    def display_back_button(self):
        """Displays the back button in the back_col."""
        with self.back_col:
            st.write("")
            home_button(label="Back", use_container_width=True)

    def display_mine_button(self):
        """Displays the mine button in the mine_col."""
        with self.mine_col:
            st.write("")
            navigation_button(
                label="Mine",
                route="Algorithm",
                use_container_width=True,
                beforeNavigate=self.controller.on_mine_click,
            )

    def display_df(self, styled_df):
        """Displays the dataframe in the df_container.

        Parameters
        ----------
        styled_df : pd.DataFrame
            The styled dataframe to display.
        """
        with self.df_container:
            st.dataframe(
                styled_df,
                use_container_width=True,
                hide_index=True,
                height=500,
            )
