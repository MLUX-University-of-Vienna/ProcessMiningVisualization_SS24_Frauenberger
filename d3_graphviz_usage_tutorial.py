import dash_interactive_graphviz
import dash
from dash.dependencies import Input, Output
import dash_html_components as html
from dash import dcc

app = dash.Dash(__name__)

initial_dot_source = """
digraph {
	graph [bb="0,0,670.64,690.96"];
	node [label="N"];
	a	[height=2,
		label="a
40",
		pos="257.89,520.74",
		width=4];
	e	[height=2,
		label="e
40",
		pos="208.89,165.24",
		width=4];
	a -> e	[label=5,
		lp="22.265,342.99",
		penwidth=3.0,
		pos="e,98.711,211.85 131.84,485.32 88.047,466.65 43.57,438.58 18.14,396.99 -6.9002,356.04 -4.8515,331.12 18.14,288.99 33.819,260.25 59.428,\
237.23 86.865,219.25"];
	b	[height=1.5,
		label="b
21",
		pos="141.89,342.99",
		width=3];
	a -> b	[label=11,
		lp="203.64,422.86",
		penwidth=4.5,
		pos="e,175.38,394.73 213.21,452.04 203.58,437.45 193.44,422.08 183.92,407.66"];
	c	[height=1.5,
		label="c
21",
		pos="375.89,342.99",
		width=3];
	a -> c	[label=11,
		lp="334.64,422.86",
		penwidth=4.5,
		pos="e,341.82,394.73 303.34,452.04 313.14,437.45 323.45,422.08 333.14,407.66"];
	d	[height=1,
		label="d
17",
		pos="573.89,342.99",
		width=2];
	a -> d	[label=13,
		lp="461.64,422.86",
		penwidth=6.0,
		pos="e,531.92,372.56 359.71,469.31 401.48,447.91 450.01,422.13 492.89,396.99 501.36,392.02 510.18,386.56 518.75,381.09"];
	end	[fillcolor=red,
		height=0.78106,
		pos="208.89,28.118",
		shape=doublecircle,
		style=filled,
		width=0.78106];
	e -> end	[penwidth=0.1,
		pos="e,208.89,56.652 208.89,93.116 208.89,83.895 208.89,74.763 208.89,66.41"];
	b -> e	[label=11,
		lp="180.64,263.11",
		penwidth=4.5,
		pos="e,182.22,236.19 161.81,289.73 166.46,277.53 171.54,264.22 176.57,251.01"];
	c -> e	[label=11,
		lp="314.64,263.11",
		penwidth=4.5,
		pos="e,270.13,230.68 330.26,293.96 315.05,277.95 297.71,259.71 280.99,242.12"];
	d -> e	[label=13,
		lp="461.64,263.11",
		penwidth=6.0,
		pos="e,322.26,210.01 532.68,313.07 520.17,304.83 506.21,296.15 492.89,288.99 443.17,262.23 386.39,236.75 336.74,216.01"];
	d -> d	[label=4,
		lp="667.26,342.99",
		penwidth=1.5,
		pos="e,640.22,328.54 640.22,357.44 653.99,355.92 663.89,351.1 663.89,342.99 663.89,337.41 659.21,333.39 651.81,330.93"];
	start	[fillcolor=green,
		height=0.85036,
		pos="257.89,660.35",
		shape=doublecircle,
		style=filled,
		width=0.85036];
	start -> a	[penwidth=0.1,
		pos="e,257.89,593.04 257.89,629.49 257.89,621.45 257.89,612.36 257.89,602.94"];
}
"""

app.layout = html.Div(
    [
        html.Div(
            dash_interactive_graphviz.DashInteractiveGraphviz(id="gv"),
            style=dict(flexGrow=1, position="relative"),
        ),
        html.Div(
            [
                html.H3("Selected element"),
                html.Div(id="selected"),
                html.H3("Dot Source"),
                dcc.Textarea(
                    id="input",
                    value=initial_dot_source,
                    style=dict(flexGrow=1, position="relative"),
                ),
                html.H3("Engine"),
                dcc.Dropdown(
                    id="engine",
                    value="dot",
                    options=[
                        dict(label=engine, value=engine)
                        for engine in [
                            "dot",
                            "fdp",
                            "neato",
                            "circo",
                            "osage",
                            "patchwork",
                            "twopi",
                        ]
                    ],
                ),
            ],
            style=dict(display="flex", flexDirection="column"),
        ),
    ],
    style=dict(position="absolute", height="100%", width="100%", display="flex"),
)


@app.callback(
    [Output("gv", "dot_source"), Output("gv", "engine")],
    [Input("input", "value"), Input("engine", "value")],
)
def display_output(value, engine):
    return value, engine


@app.callback(Output("selected", "children"), [Input("gv", "selected")])
def show_selected(value):
    return html.Div(value)


if __name__ == "__main__":
    app.run_server(debug=False)