import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash
from dash import Input, Output, State, html
from dash_bootstrap_components._components.Container import Container

colors_imagotipo = {'yellow': '#e5b622',
                    'brown': '#623812',
                    'grey_l': '#e4e4e4',
                    'grey_m': '#B4AA99'}

app = dash.Dash(external_stylesheets=[dbc.themes.SKETCHY])
server = app.server

logo = html.Div([html.Img(src=app.get_asset_url('ChelaSabe_logo.png'),
                                 style={'height':'75px',
                                        'width':'24%'})],
                style={'margin-left':'40%'})

navbar = html.Div([dbc.Nav([dbc.NavItem(dbc.NavLink("Todos para uno",
                                                    href="/tpu",
                                                    active="exact")),
                            dbc.NavItem(dbc.NavLink("Uno para todos",
                                                    href="/upt",
                                                    active="exact")),
                            dbc.NavItem(dbc.NavLink("Hoppy Places",
                                                    href="/hp",
                                                    active="exact"))
                            ],
                           justified=True,
                           pills=True)],
                  style={'backgroundColor':colors_imagotipo['yellow']})

app.layout = html.Div([logo,
                       navbar,
                       dcc.Location(id="url")])

@app.callback(Output("page-content", "children"),
              Input("url", "pathname"))
def render_page_content(pathname):
    if pathname == "/":
        return html.P("This is the content of the home page!")
    elif pathname == "/page-1":
        return html.P("This is the content of page 1. Yay!")
    elif pathname == "/page-2":
        return html.P("Oh cool, this is page 2!")
    # If the user tries to reach a different page, return a 404 message
    return html.Div(
        [
            html.H1("404: Not found", className="text-danger"),
            html.Hr(),
            html.P(f"The pathname {pathname} was not recognised..."),
        ],
        className="p-3 bg-light rounded-3",
    )

if __name__ == '__main__':
    app.run_server()
