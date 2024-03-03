import os
import streamlit.components.v1 as components

# Template for the component from https://docs.streamlit.io/library/components/publish and https://github.com/streamlit/component-template/tree/master/template/my_component

_RELEASE = False
_COMPONENT_NAME = "interactive-graph"

if not _RELEASE:
    _component_func = components.declare_component(
        _COMPONENT_NAME,
        url="http://localhost:3001",
    )
else:
    parent_dir = os.path.dirname(os.path.abspath(__file__))
    build_dir = os.path.join(parent_dir, "frontend/build")
    _component_func = components.declare_component(_COMPONENT_NAME, path=build_dir)


# TODO: Add Graph as input parameter, and pass it to the component
# TODO: Add onClick function as parameter, and pass it to the component
def interactiveGraph(key: int | str = None):
    """Wrapper function for the interactiveGraph component

    Parameters
    ----------
    key : int | str, optional
        key value for the component. needed if multiple components are displayed on the same page , by default None
    """

    component_value = _component_func(key=key)