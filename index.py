import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.graph_objs as go
import pandas as pd


covid = pd.read_csv('covid_us_county - Copy.csv')

covid1 = covid[['state', 'lat', 'long']]

list_locations = covid1.set_index('state')[['lat', 'long']].T.to_dict('dict')


updatemenus=[dict(
                active=0,
                buttons=list([dict(label='Linear Scale',
                         method='update',
                         args=[{'visible': [True, True]},
                               {'yaxis': {
                                   'type': 'linear',
                               }
                         }]),
                              
                    dict(label='Log Scale',
                         method='update',
                         args=[{'visible': [True, True]},
                               {'yaxis': {
                                   'type': 'log',
                               }
                         }]),
                ]),
                direction='up',
                pad={'t': 5, 'b': 5, 'r': 5},
                x=0,
                xanchor='left',
                y=-0.125,
                yanchor='top'
            )]

app = dash.Dash(__name__, meta_tags=[{"name": "viewport", "content": "width=device-width"}])

app.layout = html.Div([

html.Div([
        html.Div([
            html.Div([
                html.H3('Linear and Logarithmic Scales', style = {'margin-bottom': '0px', 'color': 'black'}),
            ])
        ], className = "create_container1 four columns", id = "title"),

    ], id = "header", className = "row flex-display", style = {"margin-bottom": "5px"}),

html.Div([
        html.Div([


            html.P('Select State', className = 'fix_label', style = {'color': 'black', 'margin-top': '2px'}),
            dcc.Dropdown(id = 'select_state',
                         multi = False,
                         clearable = True,
                         disabled = False,
                         style = {'display': True},
                         value = 'Alabama',
                         placeholder = 'Select state',
                         options = [{'label': c, 'value': c}
                                    for c in (covid['state'].unique())], className = 'dcc_compon'),


            ], className = "create_container2 four columns", style = {'margin-bottom': '20px', "margin-top": "20px"}),

    ], className = "row flex-display"),

            html.Div([
                html.Div([

                    dcc.Graph(id = 'map_1',
                              config = {'displayModeBar': 'hover'}),

                ], className = "create_container3 six columns"),

        html.Div([
            dcc.Graph(id = 'line_chart_1',
                      config = {'displayModeBar': 'hover'}),

        ], className = "create_container3 six columns"),

    ], className = "row flex-display"),

], id="mainContainer", style={"display": "flex", "flex-direction": "column"})

@app.callback(Output('line_chart_1', 'figure'),
              [Input('select_state', 'value')])
def update_graph(select_state):
    covid2 = covid.groupby(['date', 'state'])[['cases', 'deaths']].sum().reset_index()
    covid3 = covid2[covid2['state'] == select_state]


    return {
        'data': [go.Scatter(
            x = covid3['date'],
            y = covid3['cases'],
            mode = 'lines',
            name = 'Confirmed Cases',
            line = dict(shape = "spline", smoothing = 1.3, width = 3, color = 'orange'),
            # marker = dict(size = 10, symbol = 'circle', color = 'white',
            #               line = dict(color = 'orange', width = 2)
            #               ),

            hoverinfo = 'text',
            hovertext =
            '<b>Date</b>: ' + covid3['date'].astype(str) + '<br>' +
            '<b>Confirmed Cases</b>: ' + [f'{x:,.0f}' for x in covid3['cases']] + '<br>'

        ),

            go.Scatter(
                x = covid3['date'],
                y = covid3['deaths'],
                mode = 'lines',
                name = 'Deaths',
                line = dict(shape = "spline", smoothing = 1.3, width = 3, color = '#FF00FF'),
                # marker = dict(size = 10, symbol = 'circle', color = 'white',
                #               line = dict(color = '#FF00FF', width = 2)
                #               ),

                hoverinfo = 'text',
                hovertext =
                '<b>Date</b>: ' + covid3['date'].astype(str) + '<br>' +
                '<b>Deaths</b>: ' + [f'{x:,.0f}' for x in covid3['deaths']] + '<br>'

            )],

        'layout': go.Layout(
            updatemenus = updatemenus,
            plot_bgcolor = '#F2F2F2',
            paper_bgcolor = '#F2F2F2',
            title = {
                'text': 'Confirmed Cases and Deaths: ' + (select_state),

                'y': 0.98,
                'x': 0.5,
                'xanchor': 'center',
                'yanchor': 'top'},
            titlefont = {
                'color': 'black',
                'size': 15},

            hovermode = 'x',

            xaxis = dict(title = '<b>Date</b>',
                         color = 'black',
                         showline = True,
                         showgrid = True,
                         linecolor = 'black',
                         linewidth = 1,

                         ),

            yaxis = dict(title = '<b>Confirmed Cases and Deaths</b>',
                         color = 'black',
                         showline = False,
                         showgrid = True,
                         linecolor = 'black',

                         ),

            legend = {
                'orientation': 'h',
                'bgcolor': '#F2F2F2',
                'x': 0.5,
                'y': 1.25,
                'xanchor': 'center',
                'yanchor': 'top'},
            font = dict(
                family = "sans-serif",
                size = 12,
                color = 'black')

        )

            }


@app.callback(Output('map_1', 'figure'),
              [Input('select_state', 'value')])
def update_graph(select_state):
    covid2 = covid.groupby(['date', 'state', 'county', 'lat', 'long'])[['cases', 'deaths']].sum().reset_index()
    covid3 = covid2[covid2['state'] == select_state]


    return {
        'data': [go.Scattermapbox(
            lon = covid3['long'],
            lat = covid3['lat'],
            mode = 'markers',
            marker=go.scattermapbox.Marker(
                size = 12,
                color = covid3['cases'],
                colorscale = 'HSV',
                showscale = False,
                sizemode = 'area'),

            hoverinfo = 'text',
            hovertext =
            '<b>State</b>: ' + covid3['state'].astype(str) + '<br>' +
            '<b>County</b>: ' + covid3['county'].astype(str) + '<br>' +
            '<b>Lat</b>: ' + [f'{x:.4f}' for x in covid3['lat']] + '<br>' +
            '<b>Long</b>: ' + [f'{x:.4f}' for x in covid3['long']] + '<br>' +
            '<b>Confirmed Cases</b>: ' + [f'{x:,.0f}' for x in covid3['cases']] + '<br>' +
            '<b>Deaths</b>: ' + [f'{x:,.0f}' for x in covid3['deaths']] + '<br>'

        )],

        'layout': go.Layout(
             margin={"r": 0, "t": 0, "l": 0, "b": 0},
             hovermode='closest',
             mapbox=dict(
                accesstoken='pk.eyJ1IjoicXM2MjcyNTI3IiwiYSI6ImNraGRuYTF1azAxZmIycWs0cDB1NmY1ZjYifQ.I1VJ3KjeM-S613FLv3mtkw',  # Create free account on Mapbox site and paste here access token
                center=dict(lat=list_locations[select_state]['lat'], lon=list_locations[select_state]['long']),
                style='open-street-map',
                # style='dark',
                zoom=5,
                bearing = 0
             ),
             autosize=True,

        )

    }


if __name__ == "__main__":
    app.run_server(debug=True)
