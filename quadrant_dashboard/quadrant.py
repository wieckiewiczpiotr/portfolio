import dash
import dash_html_components as html
import dash_core_components as dcc
import plotly.graph_objects as go
from dash.dependencies import Input, Output
from plotly.colors import n_colors
import pandas as pd
import numpy as np

df = pd.read_csv('https://raw.githubusercontent.com/wieckiewiczpiotr/sample/master/final2015.csv')

app_color = {"graph_bg": "#252e3f"}
colors = n_colors('rgb(53, 92, 63)', 'rgb(238, 77, 90)', 1001, colortype='rgb')
options = []
for i in range(1, 101):
    dic = {}
    dic['label'] = i
    dic['value'] = i
    options.append(dic)
    
description = '''The datases contains information on revenues, costs and the increase in the 
value of 1,000 mockup startups.  \nBy using the control panel on the left, you can manipulate the minimum and 
maximum value of revenues and expenses in such a way that only companies that meet the 
relevant criteria are marked on the chart in green color. The third slider allows additional 
selection of the given number of best performing startups in terms of value growth - the above 
information is also included in the table on the right.'''

app = dash.Dash(__name__)
server = app.server
app.layout = html.Div(
    className='app__container',
    children=[
        html.Div(
            className='app__header',
            children=[
                html.Div(
                    className='app__header__desc',
                    children=[
                        html.H4("THE STARTUP QUADRANT", 
                                className="app__header__title"),
                        html.Div(className="app__header__title--grey",
                                 children=dcc.Markdown(description),
                                 style={'textAlign': 'justify',
                                        'marginRight':'50px'})])]),
        html.Div(
            className='app__content',
            children=[
                html.Div(
                    className='two columns module__container',
                    children=[
                        html.Div(
                            [html.H6(['Revenues', html.Br(), 'cut-off point'], className="graph__title")]),
                        html.Div(
                            className='slider',
                            children=[
                                dcc.Slider(
                                    id='revenue_slider',
                                    min=100000,
                                    max=17000000,
                                    step=100000,
                                    value=9000000,
                                    updatemode='drag')]),
                        html.Div(
                            children=[
                                html.P(id='revenue_output')]),
                        html.Div(
                            children=[
                                html.H6(['Expenses', html.Br(), 'cut-off point'], className="graph__title")]),
                        html.Div(
                            className='slider',
                            children=[
                                dcc.Slider(
                                    id='expense_slider',
                                    min=120000,
                                    max=10000000,
                                    step=100000,
                                    value=6000000,
                                    updatemode='drag')]),
                        html.Div(
                            children=[
                                html.P(id='expense_output')]),
                        html.Div(
                            [html.H6(['Growth', html.Br(), 'top companies'], className="graph__title")]),
                        html.Div(
                            className='slider',
                            children=[
                                dcc.Slider(
                                    id='growth_slider',
                                    min=0,
                                    max=250,
                                    step=1,
                                    value=50,
                                    updatemode='drag')]),
                        html.Div(
                            children=[
                                html.P(id='growth_output')])]),
                html.Div(
                    className='seven columns module__container',
                    children=[
                        html.Div(
                            [html.H6("THE QUADRANT", className="graph__title")]),
                        html.Div(
                            className='graph__container',
                            children=[
                                dcc.Graph(id='graph'),
                                html.H5('')])]),
                html.Div(
                    className='three columns module__container',
                    children=[
                        html.Div(
                            className='graph__container',
                            children=[
                                html.Div([html.H6("THE STARTUPS", className="graph__title")]),
                                dcc.Graph(id='table',
                                          figure={
                                              'data': [go.Table(
                                                  header={
                                                      'values': ['<b>Rank</b>', '<b>Name</b>', '<b>Growth</b>'],
                                                      'align': ['center', 'center', 'center'],
                                                      'font': {'color': 'white', 'size': 14},
                                                      'fill_color': '#1f2630',
                                                      'line_color': '#1f2630'},
                                                  cells={
                                                      'values': [df.index+1, df.Name, (df['2015_growth']*100).map("{:.0f}%".format)],
                                                      'fill_color': [np.array(colors)[df.index]],
                                                      'line_color': '#1f2630',
                                                      'font': {'color': 'white', 'size': 12},
                                                      'align': ['center','left', 'center']},
                                                  columnwidth=[15,45,20])],
                                              'layout': go.Layout(
                                                  height=510,
                                                  plot_bgcolor=app_color["graph_bg"],
                                                  paper_bgcolor=app_color["graph_bg"],
                                                  margin=dict(t=10, b=10, l=20, r=20))}),
                                html.H5('')
                            ]
                        )
                    ]
                )
            ]
        )
    ]
)
    
@app.callback(Output('graph', 'figure'),
              [Input('revenue_slider', 'value'),
               Input('expense_slider', 'value'),
               Input('growth_slider', 'value')])
def update_graph(rev_cutoff, exp_cutoff, grw_cutoff):
    traces = []
    traces.append(go.Scatter(
        x=df.iloc[grw_cutoff:]['2015_revenue'], 
        y=df.iloc[grw_cutoff:]['2015_expenses'],
        mode='markers',
        name='',
        text=df.iloc[grw_cutoff:]['Name'].map(str)+ 
            '<br><b>Growth</b>: '+ 
            (df.iloc[grw_cutoff:]['2015_growth']*100).astype('int32').map(str)+
            '%',
        hovertemplate=
            '<b>Name</b>: %{text}<br>'+
            '<b>Revenues</b>: %{x:$,.0f}<br>'+
            '<b>Expenses</b>: %{y:$,.0f}<br>',
        marker=dict(
            size=10,
            color=(
                np.where(np.logical_and(exp_cutoff > df.iloc[grw_cutoff:]['2015_expenses'], 
                                        rev_cutoff < df.iloc[grw_cutoff:]['2015_revenue']),
                         'darkgreen', 
                         'gray')),
            opacity=0.5,
            line=dict(
                color='#242625',
                width=0.5))))
    traces.append(go.Scatter(
        x=df.iloc[:grw_cutoff]['2015_revenue'], 
        y=df.iloc[:grw_cutoff]['2015_expenses'],
        mode='markers',
        name='',
        text=df.iloc[:grw_cutoff]['Name'].map(str)+ 
            '<br><b>Growth</b>: '+ 
            (df.iloc[:grw_cutoff]['2015_growth']*100).astype('int32').map(str)+
            '%',
        hovertemplate=
            '<b>Name</b>: %{text}<br>'+
            '<b>Revenues</b>: %{x:$,.0f}<br>'+
            '<b>Expenses</b>: %{y:$,.0f}<br>',
        marker=dict(
            size=10,
            color=(
                np.where(np.logical_and(exp_cutoff > df.iloc[:grw_cutoff]['2015_expenses'], 
                                        rev_cutoff < df.iloc[:grw_cutoff]['2015_revenue']),
                         'gold', 
                         'gray')),
            opacity=(
                np.where(np.logical_and(exp_cutoff > df.iloc[:grw_cutoff]['2015_expenses'], 
                                        rev_cutoff < df.iloc[:grw_cutoff]['2015_revenue']),
                         0.8, 
                         0.5)),
            symbol=(
                np.where(np.logical_and(exp_cutoff > df.iloc[:grw_cutoff]['2015_expenses'], 
                                        rev_cutoff < df.iloc[:grw_cutoff]['2015_revenue']),
                         'star-diamond', 
                         'circle')),
            line=dict(
                color='darkgoldenrod',
                width=(
                    np.where(np.logical_and(exp_cutoff > df.iloc[:grw_cutoff]['2015_expenses'], 
                                            rev_cutoff < df.iloc[:grw_cutoff]['2015_revenue']),
                         1, 
                         0))))))
    figure={
        'data': traces,
        'layout': go.Layout(
            shapes=[{
                'type': 'line',
                'x0': 1000000,
                'x1': 17500000,
                'y0': exp_cutoff,
                'y1': exp_cutoff,
                'opacity': 0.8,
                'line': {
                        'dash': 'dash',
                        'width': 2,
                        'color': '#c7c7c7'}},
                {'type': 'line',
                'x0': rev_cutoff,
                'x1': rev_cutoff,
                'y0': 0,
                'y1': 11500000,
                'opacity': 0.8,
                'line': {
                    'dash': 'dash',
                    'width': 2,
                    'color': '#c7c7c7'}}],
            height= 510,
            showlegend=False,
            hovermode="closest",
            plot_bgcolor=app_color["graph_bg"],
            paper_bgcolor=app_color["graph_bg"],
            xaxis_title='Revenues',
            yaxis_title='Expenses',
            xaxis={'gridcolor': '#35353b'},
            yaxis={'gridcolor': '#35353b', 
                   'autorange': 'reversed', 
                   'zerolinecolor': app_color["graph_bg"]},
            font={'color': '#d8d8d8'},
            margin=dict(t=5, b=60, l=50, r=5))}
    return figure

@app.callback(
    Output('revenue_output', 'children'),
    [Input('revenue_slider', 'value')])
def update_output_rev(value):
    return ['Minimal revenues:', html.Br(), '${:,.0f}'.format(value)]

@app.callback(
    Output('expense_output', 'children'),
    [Input('expense_slider', 'value')])
def update_output_exp(value):
    return ['Maximal expenses:', html.Br(), '${:,.0f}'.format(value)]

@app.callback(
    Output('growth_output', 'children'),
    [Input('growth_slider', 'value')])
def update_output_grw(value):
    return 'Number of best startups: {}'.format(value)

if __name__ == '__main__':
    app.run_server()