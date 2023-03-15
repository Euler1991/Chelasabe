import pandas as pd
import numpy as np
import dash
import dash_bootstrap_components as dbc
from dash import html, dcc, Input, Output, State
import plotly.graph_objects as go
import plotly.express as px
import dash_tabulator
import style_recommendations as sr

sites_df = pd.read_csv('../Datasets/Catálogo_Establecimientos.csv')
sites_df['Latitud'] = sites_df['Latitud'].str.replace(',','.').astype(np.float64)
sites_df['Longitud'] = sites_df['Longitud'].str.replace(',','.').astype(np.float64)

beers_df = pd.read_csv('../Datasets/Catálogo_Cervezas.csv')
beers_df['ABV'] = beers_df['ABV'].str.replace(',','.').astype(np.float64)

# ----------------------------------------------------------------------------------------------------------------------#
# Creación de elementos para el dashboard
craft_colors = {'Wheat Beer': '#f9e16c',
                'Pilsner': '#f9e16c',
                'Pale Lager': '#f9e16c',
                'Amber Lager': '#ad4418',
                'Bock': '#983013',
                'Dark Lager': '#a73e16',
                'Pale Ale': '#e49c1a',
                'Indian Pale Ale': '#e49c1a',
                'Brown Ale': '#983013',
                'Porter': '#4b090b',
                'Stout': '#240b0b',
                'Strong Ale': '#c05925'}

colors_imagotipo = {'yellow': '#e5b622',
                    'brown': '#623812',
                    'grey_l': '#e4e4e4',
                    'grey_m': '#B4AA99'}

beers_dict = {'Bohemia Oscura': 'Boh_Osc',
              'Corona': 'Cor',
              'Dos Equis Ambar': 'Dos_Equ_Amb',
              'Dos Equis Laguer': 'Dos_Equ_Lag',
              'Indio': 'Ind',
              'Modelo Especial': 'Mod_Esp',
              'Negra Modelo': 'Neg_Mod',
              'Sol': 'Sol',
              'Tecate Light': 'Tec_Lig',
              'Victoria': 'Vic'}

lager_dict = {'Pilsner': 'Pil',
              #'Pale Lager': 'Pal_Lag',
              'Amber Lager': 'Amb_Lag',
              'Bock': 'Boc',
              'Dark Lager': 'Dar_Lag'}

lager_colors = {'Pilsner': '#f9e16c',
                #'Pale Lager': '#f9e16c',
                'Amber Lager': '#ad4418',
                'Bock': '#983013',
                'Dark Lager': '#a73e16'}

ale_dict = {'Wheat Beer':'Whe_Bee',
            'Pale Ale': 'Pal_Ale',
            'Indian Pale Ale': 'Ind_Pal_Ale',
            'Strong Ale': 'Str_Ale',
            'Brown Ale': 'Bro_Ale',
            'Stout': 'Sto'}

ale_colors = {'Wheat Beer':'#f9e16c',
              'Pale Ale': '#e49c1a',
              'Indian Pale Ale': '#e49c1a',
              'Strong Ale': '#c05925',
              'Brown Ale': '#983013',
              'Stout': '#240b0b'}

beer_columns = [{"title": "Cerveza",
                 "field": "beer",
                 'hozAlign': "center",
                 'headerHozAlign': "center",
                 'headerSort': False},
                {'title': "Calificación",
                 'field': "rating",
                 'formatter': "star",
                 'hozAlign': "center",
                 'headerHozAlign': "center",
                 'headerSort': False,
                 'editor': True}]

lager_data = [{'id': lager_dict[key], 'style': key, 'rating': '0'} for key in lager_dict.keys()]

ale_data = [{'id': ale_dict[key], 'style': key, 'rating': '0'} for key in ale_dict.keys()]

beer_data = [{'id': beers_dict[key], 'beer': key, 'rating': '0'} for key in beers_dict.keys()]

craft_columns = [{"title": "Estilo",
                  "field": "style",
                  'hozAlign': "center",
                  'headerHozAlign': "center",
                  'headerSort': False},
                 {'title': "Calificación",
                  'field': "rating",
                  'formatter': "star",
                  'hozAlign': "center",
                  'headerHozAlign': "center",
                  'headerSort': False,
                  'editor': True}]

tap_columns=[{"title": "Cerveza",
              "field": "beer",
              'hozAlign': "center",
              'headerHozAlign': "center",
              'headerSort': False},
             {"title": "Cervecería",
              "field": "brewery",
              'hozAlign': "center",
              'headerHozAlign': "center",
              'headerSort': False},
             {"title": "Estilo",
              "field": "style",
              'hozAlign': "center",
              'headerHozAlign': "center",
              'headerSort': False},
             {"title": "ABV",
              "field": "abv",
              'hozAlign': "center",
              'headerHozAlign': "center",
              'headerSort': False}]

# ----------------------------------------------------------------------------------------------------------------------#
# Creación de componentes del dashboard

beer_form = dash_tabulator.DashTabulator(id='beer-form',
                                         columns=beer_columns,
                                         data=beer_data)

craft_form = html.Div([dash_tabulator.DashTabulator(id='craft-form',
                                                    columns=craft_columns,
                                                    data=lager_data + ale_data)])

tap_table = dash_tabulator.DashTabulator(id='tap-table',
                                         columns=tap_columns,
                                         data=[])

mode_dropdown = dbc.Row(dbc.Col(dcc.Dropdown(id='mode_dropdown',
                                             options=[{'label': 'Todos para uno',
                                                       'value':'TPU'},
                                                      {'label': 'Uno para todos',
                                                       'value':'UPT'}],
                                             value='TPU'),
                                width={"size": 10, "offset": 1},
                                style={"margin-bottom": "15px"}))

tpu_button = dbc.Button("Obtener Recomendaciones",
                        id='compute',
                        color="primary",
                        n_clicks=0)

upt_button = dbc.Button("Compartir gustos",
                        id='share',
                        color="primary",
                        n_clicks=0)

tap_dropdown = dcc.Dropdown(id='tap-dropdown',
                            options=[{'label':place, 'value':place} for place in sites_df['Nombre']],
                            value='Apóstol Tap Room')

# ----------------------------------------------------------------------------------------------------------------------#
# Creación de elementos para el modo "Todos para uno" (principiantes)

comercial = dbc.Row(dbc.Col([html.P('Usa una estrella para las que no te gustan, y cinco para las que más te gustan. Las cervezas que no conozcas déjalas sin estrellas.'),
                             beer_form],
                            width={"size": 10, "offset": 1},
                            style={"margin-bottom": "15px"}))

craft = dbc.Row(dbc.Col(html.Div(id='craft'),
                        width={"size": 10, "offset": 1},
                        style={"margin-bottom": "15px"}))

craft_graph = dcc.Graph(id='craft-graph')

tpu_card = dbc.Card(dbc.CardBody([html.H2("Todos para uno",
                                          className="card-title",
                                          style={'textAlign': 'center',
                                                 'color': colors_imagotipo['brown']}),
                                  html.P("¿No sabes qué beber?"),
                                  html.P("Responde el cuestionario de cervezas para recomendarte estilos.")]),
                    style={'height': '100%'})

upt_card = dbc.Card(dbc.CardBody([html.H2("Uno para todos",
                                          className="card-title",
                                          style={'textAlign': 'center',
                                                 'color': colors_imagotipo['brown']}),
                                  html.P("¿Ya sabes qué estilos te gustan más?"),
                                  html.P(
                                      "Responde los cuestionarios de cervezas y estilos para  ayudar a recomendar estilos a usuarios nuevos.")]),
                    style={'height': '100%'})

cards_tpu_utp = dbc.Row([dbc.Col(tpu_card,
                                 width=5),
                         dbc.Col(upt_card,
                                 width=5)],
                        justify='center',
                        className="h-25",
                        style={"margin-bottom": "15px"})

tap_networks = html.Div([html.A("Facebook",
                                id= 'tap-fb',
                                target="_blank"),
                         html.Br(),
                         html.A("Instagram",
                                id='tap-ig',
                                target="_blank")],
                        style={'textAlign': 'center'})

hoppy_places = dbc.Row(dbc.Col([html.H2("Hoppy Places",
                                        className="card-title",
                                        style={'textAlign': 'center',
                                               'color': colors_imagotipo['yellow']}),
                                tap_dropdown,
                                html.P(id='tap-estatus',
                                       style={'textAlign': 'center',
                                              'color': colors_imagotipo['brown'],
                                              "margin-top": "15px"}),
                                tap_table,
                                dcc.Graph(id='beer-map'),
                                tap_networks],
                               width={"size": 10, "offset": 1}))
#style={"margin-bottom": "15px"}
# ----------------------------------------------------------------------------------------------------------------------#
# Dashboard
app = dash.Dash(external_stylesheets=[dbc.themes.SKETCHY])
server = app.server

app.layout = html.Div([html.H1('Chelasabe:Pienso luego pisto',
                               style={'textAlign': 'center',
                                      'color': colors_imagotipo['yellow']}),
                       cards_tpu_utp,
                       mode_dropdown,
                       comercial,
                       html.Div(id='tpu-button',
                                style={'display': 'flex',
                                       'justify-content': 'center',
                                       "margin-bottom": "15px"}),
                       craft,
                       html.Div(id='upt-button',
                                style={'display': 'flex',
                                       'justify-content': 'center'}),
                       html.Div(id='status-share',
                                style={'display': 'flex',
                                       'justify-content': 'center',
                                       "margin-bottom": "15px"}),
                       html.Hr(),
                       hoppy_places])

# ----------------------------------------------------------------------------------------------------------------------#
# Funciones y Callbacks

def render_recommendations(style_scores):
    style_avg = sum(style_scores) / len(style_scores)
    fig = go.Figure()

    fig.add_trace(go.Bar(y=[['Lagers'] * 4, list(lager_dict.keys())],
                         x=style_scores[:4],
                         orientation='h',
                         marker=dict(color=list(lager_colors.values()))))

    fig.add_trace(go.Bar(y=[['Ales'] * 6, list(ale_dict.keys())],
                         x=style_scores[4:],
                         orientation='h',
                         marker=dict(color=list(ale_colors.values()))))

    fig.add_shape(type="line",
                  xref="paper",
                  yref="paper",
                  x0=style_avg / 5,
                  y0=0,
                  x1=style_avg / 5,
                  y1=1,
                  line=dict(color=colors_imagotipo['yellow'],
                            width=2,
                            dash='dot'))

    fig.update_layout(title='Recomendaciones de Estilos',
                      title_x=0.5,
                      showlegend=False,
                      xaxis=dict(title='Afinidad',
                                 titlefont_size=16,
                                 tickfont_size=14,
                                 dtick=1.0),
                      margin=dict(l=20,
                                  r=20,
                                  b=20,
                                  t=30))

    fig.update_xaxes(range=[0, 5],
                     constrain='domain')

    return fig


@app.callback([Output('tpu-button', 'children'),
               Output('upt-button', 'children'),
               Output('craft', 'children')],
              Input('mode_dropdown', 'value'))
def define_button(mode_value):
    if mode_value == 'TPU':
        return tpu_button, '', craft_graph
    else:
        return '', upt_button, craft_form


@app.callback(Output('craft-graph', 'figure'),
              Input('compute', 'n_clicks'),
              [State('beer-form', 'data')])
def com_rec(n_clicks, beer_ratings):
    if n_clicks == 0:
        return render_recommendations([0] * 10)
    else:
        form = [float(beer['rating']) for beer in beer_ratings]
        rec = sr.drink_team_rec(form)
        return render_recommendations(rec)


@app.callback(Output('status-share', 'children'),
              Input('share', 'n_clicks'),
              [State(beers_dict[beer], 'value') for beer in beers_dict.keys()] +
              [State(lager_dict[lager], 'value') for lager in lager_dict.keys()] +
              [State(ale_dict[ale], 'value') for ale in ale_dict.keys()])
def sha_sty(n_clicks, vb1, vb2, vb3, vb4, vb5, vb6, vb7, vb8, vb9, vb10, vl1, vl2, vl3, vl4, va1, va2, va3, va4, va5, va6):
    if n_clicks == 0:
        return html.P()
    else:
        SP_df = pd.read_csv('../Datasets/style_preferences.csv')
        print(n_clicks, SP_df.info())
        SP_df.loc[-1] = [vb1, vb2, vb3, vb4, vb5, vb6, vb7, vb8, vb9, vb10,
                         vl1, vl2, vl3, vl4,
                         va1, va2, va3, va4, va5, va6]
        SP_df.index += 1
        SP_df = SP_df.sort_index()
        SP_df.to_csv('../Datasets/style_preferences.csv', index=False)
        return html.P("¡Gracias por compatir tus preferencias!")

@app.callback(Output('beer-map', 'figure'),
              Input('tap-dropdown', 'value'))
def update_map(tap):
    tap_df = sites_df[sites_df.Nombre == tap]
    token = open(".mapbox_token").read()

    px.set_mapbox_access_token(open(".mapbox_token").read())

    fig = go.Figure(go.Scattermapbox(mode="markers+text",
                                     lon=tap_df['Longitud'].values,
                                     lat=tap_df['Latitud'].values,
                                     text=tap_df['Nombre'].values[0],
                                     textposition='bottom center',
                                     marker={'size': 15,
                                             'symbol': "beer",
                                             'color': 'rgb(229, 182, 34)'}))

    fig.update_layout(mapbox={'accesstoken': token,
                              'style': "streets",
                              'center': {'lat': tap_df['Latitud'].values[0],
                                         'lon': tap_df['Longitud'].values[0]},
                              'zoom': 13},
                      showlegend=False,
                      margin=dict(t=20, b=20, l=0, r=0))

    return fig

@app.callback([Output('tap-estatus','children'),
               Output('tap-table', 'data'),
               Output('tap-fb', 'href'),
               Output('tap-ig', 'href')],
              Input('tap-dropdown', 'value'))
def update_tap_info(tap):
    site_tap = beers_df[beers_df.Establecimiento == tap]
    site_info = sites_df[sites_df.Nombre == tap]
    tap_list_dict = site_tap.to_dict(orient='records')
    tap_data = [{'beer': row['Cerveza'],
                 'brewery': row['Cervecería'],
                 'style': row['Estilo Real'],
                 'abv': row['ABV']} for row in tap_list_dict]
    if len(tap_data)>0:
        estatus = 'Última actualización: {}'.format(site_info['Última Actualización'].values[0])
    else:
        estatus = 'Tap no disponibe por el momento'
    return estatus, tap_data, site_info['Facebook'].values[0], site_info['Instagram'].values[0]

# ----------------------------------------------------------------------------------------------------------------------#
# Código para iniciar el dashboard

if __name__ == '__main__':
    app.run_server()
