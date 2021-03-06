
from flask import Flask

server = Flask(__name__)

@server.route('/')
def Hello_world():
    print("Hello")


from mlxtend.frequent_patterns import fpgrowth
from mlxtend.frequent_patterns import association_rules
import pandas as pd
import dash
import dash_table as dt
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc


app = dash.Dash(__name__, server=server, routes_pathname_prefix='/dash/',external_stylesheets=[dbc.themes.MINTY])


# App layout

COLUMNS = ['antecedent support', 'consequent support', 'support', 'confidence', 'lift']

app.layout = html.Div([

    html.A(id='top'),
    dbc.Row((dbc.Col((
        dbc.NavbarSimple(
            children=[
                dbc.DropdownMenu(
                    children=[
                        dbc.DropdownMenuItem("IB-Cells Frequent Itemsets", href="#IB-Cells Frequent Itemsets", external_link=True),
                        dbc.DropdownMenuItem("IB-Cells Association Rules", href="#IB-Cells Association Rules", external_link=True),
                        dbc.DropdownMenuItem("Cell Patterns Frequent Itemsets", href="#Cell Patterns Frequent Itemsets", external_link=True),
                        dbc.DropdownMenuItem("Cell Patterns Association Rules", href="#Cell Patterns Association Rules", external_link=True)],
                    nav=True,
                    in_navbar=True,
                    label="Tables",
                    direction="left",
                    ),
                ],
            brand="Frequent Firing Ensembles",
            color="primary",
            dark=True,
            ),
        ))
    )),


    dbc.Row((dbc.Col((html.Br())))),
    dbc.Row((dbc.Col((html.Br())))),
    dbc.Row((dbc.Col((html.Br())))),
    dbc.Row((dbc.Col((html.Br())))),

    dbc.Row((dbc.Col((html.H4("IB-Cell Parameters", style={'margin' : 'auto', 'text-align' : 'center'})), width={'size': True, }))),

    dbc.Row((dbc.Col((html.Br())))),
    dbc.Row((dbc.Col((html.Br())))),
    dbc.Row((dbc.Col((html.Br())))),

    dbc.Row((
        dbc.Col((html.H6("Minimum Support Value"),
            dcc.Input(
                id="support_number",
                type="number",
                placeholder="minimum support value",
                value=0.6,
            )),
            width={'size': True, 'offset': 1}
        ),

        dbc.Col((html.H6("Minimum Confidence Value"),
            dcc.Input(
                id="confidence_number",
                type="number",
                placeholder="minimum confidence value",
                value=0.6,
            )),
            width={'size': True, 'offset': 1}
        ),

        dbc.Col((html.H6("Minimum Lift Value"),
            dcc.Input(
                id="lift_number",
                type="number",
                placeholder="minimum lift number",
                value=1,
            )),
            width={'size': True, 'offset': 1}
        ),
    )),


    dbc.Tooltip(
            "This measure controls the frequency of an itemset.",
            target="support_number",
            placement='right',
            style={'background-color' : '#F3969A', 'color' : 'white'},
        ),

    dbc.Tooltip(
            "This measure controls how often the 'if-then' associations are found in the set.",
            target="confidence_number",
            placement='left',
            style={'background-color' : '#F3969A', 'color' : 'white'},
        ),

    dbc.Tooltip(
            "This measure controls the importance of a rule. If lift=1, there is no correlation between the antecedent and consequent. If lift>1, there is a positive correlation between the antecedent and consequent. If lift<1, there is a negative correlation between the antecedent and consequent.",
            target="lift_number",
            placement='left',
            style={'background-color' : '#F3969A', 'color' : 'white'},
        ),


    dbc.Row((dbc.Col((html.Br())))),
    dbc.Row((dbc.Col((html.Br())))),
    dbc.Row((dbc.Col((html.Br())))),

    dbc.Row((
        dbc.Col((html.H6(id='sort_text', children="Desired Subset")), width={'size': True, 'offset': 1}),
        dbc.Col((html.H6("Sort By (Order matter)", style= {"display":"inline-block"} )), width={'size': True, 'offset': 1}),
        dbc.Col((html.H6("Desired Dataset")), width={'size': True, 'offset': 1})
        )),

    dbc.Row((
        dbc.Col((dcc.Dropdown(
                id="switch",
                options=[
                    {'label': 'cells --> IB', 'value': 1},
                    {'label': 'IB--> cells', 'value': 2},
                    {'label': 'All', 'value': 3},

                ],
                placeholder="subset",
                searchable=False,
                value=4,
                clearable=False,
                multi=False,
                style={'width': "80%" },
            )),
            width={'size': True, 'offset': 1}
        ),

        dbc.Col((dcc.Dropdown(
                id="sort",
                options=[
                    {'label': 'Support', 'value': 1},
                    {'label': 'Confidence', 'value': 2},
                    {'label': 'Lift', 'value': 3},
                    {'label': 'None', 'value': 4},
                    {'label': 'Length (frequent itemsets only)' , 'value' : 5},
                ],
                placeholder="sort by",
                searchable=False,
                value=4,
                clearable=False,
                multi=True,
                style={'width': "80%"},
            )),
            width={'size': True, 'offset': 1}
        ),

        dbc.Col((dcc.Dropdown(
                    id="dataset",
                    options=[
                        {'label': 'Set2-1022_Def5_Merged.csv', 'value': 'Set2-1022_Def5_Merged.csv'},
                        {'label': 'Set1-1022_Def5_Merged.csv', 'value': 'Set1-1022_Def5_Merged.csv'},
                        {'label': 'Set1-1034_Def5_Merged.csv', 'value': 'Set1-1034_Def5_Merged.csv'},
                        {'label': 'Set2-1035_Def8_Merged.csv', 'value': 'Set2-1035_Def8_Merged.csv'},
                        {'label': 'Set1-1042_Def8_Merged.csv', 'value': 'Set1-1042_Def8_Merged.csv'},
                        {'label': '1022_Def5_close.csv', 'value': '1022_Def5_close.csv'},
                        {'label': '1022_Def5_far.csv', 'value': '1022_Def5_far.csv'},
                        {'label': '1022_Def8_close.csv', 'value': '1022_Def8_close.csv'},
                        {'label': '1022_Def8_far.csv', 'value': '1022_Def8_far.csv'},
                        {'label': '1022_HabA_close.csv', 'value': '1022_HabA_close.csv'},
                        {'label': '1022_HabA_far.csv', 'value': '1022_HabA_far.csv'},
                        {'label': '1033_Def5A_close.csv', 'value': '1033_Def5A_close.csv'},
                        {'label': '1033_Def5A_far.csv', 'value': '1033_Def5A_far.csv'},
                        {'label': '1033_Def5B_close.csv', 'value': '1033_Def5B_close.csv'},
                        {'label': '1033_Def5B_far.csv', 'value': '1033_Def5B_far.csv'},
                        {'label': '1033_Def8_close.csv', 'value': '1033_Def8_close.csv'},
                        {'label': '1033_Def8_far.csv', 'value': '1033_Def8_far.csv'},
                        {'label': '1033_Hab_close.csv', 'value': '1033_Hab_close.csv'},
                        {'label': '1033_Hab_far.csv', 'value': '1033_Hab_far.csv'},
                        {'label': '1034_Def2_close.csv', 'value': '1034_Def2_close.csv'},
                        {'label': '1034_Def2_far.csv', 'value': '1034_Def2_far.csv'},
                        {'label': '1034_Def5_close.csv', 'value': '1034_Def5_close.csv'},
                        {'label': '1034_Def5_far.csv', 'value': '1034_Def5_far.csv'},
                        {'label': '1034_Def8A_close.csv', 'value': '1034_Def8A_close.csv'},
                        {'label': '1034_Def8A_far.csv', 'value': '1034_Def8A_far.csv'},
                        {'label': '1034_Def8B_close.csv', 'value': '1034_Def8B_close.csv'},
                        {'label': '1034_Def8B_far.csv', 'value': '1034_Def8B_far.csv'},
                        {'label': '1034_Hab_close.csv', 'value': '1034_Hab_close.csv'},
                        {'label': '1034_Hab_far.csv', 'value': '1034_Hab_far.csv'},
                        {'label': '1035_Def5A_close.csv', 'value': '1035_Def5A_close.csv'},
                        {'label': '1035_Def5A_far.csv', 'value': '1035_Def5A_far.csv'},
                        {'label': '1035_Def5B_close.csv', 'value': '1035_Def5B_close.csv'},
                        {'label': '1035_Def5B_far.csv', 'value': '1035_Def5B_far.csv'},
                        {'label': '1035_Def8_close.csv', 'value': '1035_Def8_close.csv'},
                        {'label': '1035_Def8_far.csv', 'value': '1035_Def8_far.csv'},
                        {'label': '1035_Hab_close.csv', 'value': '1035_Hab_close.csv'},
                        {'label': '1035_Hab_far.csv', 'value': '1035_Hab_far.csv'},
                        {'label': '1038_Def2_close.csv', 'value': '1038_Def2_close.csv'},
                        {'label': '1038_Def2_far.csv', 'value': '1038_Def2_far.csv'},
                        {'label': '1038_Def5_close.csv', 'value': '1038_Def5_close.csv'},
                        {'label': '1038_Def5_far.csv', 'value': '1038_Def5_far.csv'},
                        {'label': '1038_Def8_close.csv', 'value': '1038_Def8_close.csv'},
                        {'label': '1038_Def8_far.csv', 'value': '1038_Def8_far.csv'},
                        {'label': '1038_Hab_close.csv', 'value': '1038_Hab_close.csv'},
                        {'label': '1038_Hab_far.csv', 'value': '1038_Hab_far.csv'},
                        {'label': '1042_Def2A_close.csv', 'value': '1042_Def2A_close.csv'},
                        {'label': '1042_Def2A_far.csv', 'value': '1042_Def2A_far.csv'},
                        {'label': '1042_Def2B_close.csv', 'value': '1042_Def2B_close.csv'},
                        {'label': '1042_Def2B_far.csv', 'value': '1042_Def2B_far.csv'},
                        {'label': '1042_Def5A_close.csv', 'value': '1042_Def5A_close.csv'},
                        {'label': '1042_Def5A_far.csv', 'value': '1042_Def5A_far.csv'},
                        {'label': '1042_Def5B_close.csv', 'value': '1042_Def5B_close.csv'},
                        {'label': '1042_Def5B_far.csv', 'value': '1042_Def5B_far.csv'},
                        {'label': '1042_Def8_close.csv', 'value': '1042_Def8_close.csv'},
                        {'label': '1042_Def8_far.csv', 'value': '1042_Def8_far.csv'},
                        {'label': '1042_Hab_close.csv', 'value': '1042_Hab_close.csv'},
                        {'label': '1042_Hab_far.csv', 'value': '1042_Hab_far.csv'},
                        {'label': '1048_Def5A_close.csv', 'value': '1048_Def5A_close.csv'},
                        {'label': '1048_Def5A_far.csv', 'value': '1048_Def5A_far.csv'},
                        {'label': '1048_Def5B_close.csv', 'value': '1048_Def5B_close.csv'},
                        {'label': '1048_Def5B_far.csv', 'value': '1048_Def5B_far.csv'},
                        {'label': '1048_Def8B_close.csv', 'value': '1048_Def8B_close.csv'},
                        {'label': '1048_Def8B_far.csv', 'value': '1048_Def8B_far.csv'},
                        {'label': '1048_Hab_close.csv', 'value': '1048_Hab_close.csv'},
                        {'label': '1048_Hab_far.csv', 'value': '1048_Hab_far.csv'},
                        {'label': '1049_Def2_close.csv', 'value': '1049_Def2_close.csv'},
                        {'label': '1049_Def2_far.csv', 'value': '1049_Def2_far.csv'},
                        {'label': '1049_Def5_close.csv', 'value': '1049_Def5_close.csv'},
                        {'label': '1049_Def5_far.csv', 'value': '1049_Def5_far.csv'},
                        {'label': '1049_Def8_close.csv', 'value': '1049_Def8_close.csv'},
                        {'label': '1049_Def8_far.csv', 'value': '1049_Def8_far.csv'},
                        {'label': '1049_Hab_close.csv', 'value': '1049_Hab_close.csv'},
                        {'label': '1049_Hab_far.csv', 'value': '1049_Hab_far.csv'},
                        {'label': '1051_Def2_close.csv', 'value': '1051_Def2_close.csv'},
                        {'label': '1051_Def2_far.csv', 'value': '1051_Def2_far.csv'},
                        {'label': '1051_Def5A_close.csv', 'value': '1051_Def5A_close.csv'},
                        {'label': '1051_Def5A_far.csv', 'value': '1051_Def5A_far.csv'},
                        {'label': '1051_Def8_close.csv', 'value': '1051_Def8_close.csv'},
                        {'label': '1051_Def8_far.csv', 'value': '1051_Def8_far.csv'},
                        {'label': '1051_Hab_close.csv', 'value': '1051_Hab_close.csv'},
                        {'label': '1051_Hab_far.csv', 'value': '1051_Hab_far.csv'},
                        {'label': '3120_Def2_close.csv', 'value': '3120_Def2_close.csv'},
                        {'label': '3120_Def2_far.csv', 'value': '3120_Def2_far.csv'},
                        {'label': '3120_Def5_close.csv', 'value': '3120_Def5_close.csv'},
                        {'label': '3120_Def5_far.csv', 'value': '3120_Def5_far.csv'},
                        {'label': '3120_Def8_close.csv', 'value': '3120_Def8_close.csv'},
                        {'label': '3120_Def8_far.csv', 'value': '3120_Def8_far.csv'},
                        {'label': '3120_Hab_close.csv', 'value': '3120_Hab_close.csv'},
                        {'label': '3120_Hab_far.csv', 'value': '3120_Hab_far.csv'},
                        {'label': '3123_Def5A_close.csv', 'value': '3123_Def5A_close.csv'},
                        {'label': '3123_Def5A_far.csv', 'value': '3123_Def5A_far.csv'},
                        {'label': '3123_Def5B_close.csv', 'value': '3123_Def5B_close.csv'},
                        {'label': '3123_Def5B_far.csv', 'value': '3123_Def5B_far.csv'},
                        {'label': '3123_Def8A_close.csv', 'value': '3123_Def8A_close.csv'},
                        {'label': '3123_Def8A_far.csv', 'value': '3123_Def8A_far.csv'},
                        {'label': '3123_Hab_close.csv', 'value': '3123_Hab_close.csv'},
                        {'label': '3123_Hab_far.csv', 'value': '3123_Hab_far.csv'},
                        {'label': '3408_Def2A_close.csv', 'value': '3408_Def2A_close.csv'},
                        {'label': '3408_Def2A_far.csv', 'value': '3408_Def2A_far.csv'},
                        {'label': '3408_Def5_close.csv', 'value': '3408_Def5_close.csv'},
                        {'label': '3408_Def5_far.csv', 'value': '3408_Def5_far.csv'},
                        {'label': '3408_Def8_close.csv', 'value': '3408_Def8_close.csv'},
                        {'label': '3408_Def8_far.csv', 'value': '3408_Def8_far.csv'},
                        {'label': '3408_Hab_close.csv', 'value': '3408_Hab_close.csv'},
                        {'label': '3408_Hab_far.csv', 'value': '3408_Hab_far.csv'},
                        {'label': '3442_Def2A_close.csv', 'value': '3442_Def2A_close.csv'},
                        {'label': '3442_Def2A_far.csv', 'value': '3442_Def2A_far.csv'},
                        {'label': '3442_Def2B_close.csv', 'value': '3442_Def2B_close.csv'},
                        {'label': '3442_Def2B_far.csv', 'value': '3442_Def2B_far.csv'},
                        {'label': '3442_Def5_close.csv', 'value': '3442_Def5_close.csv'},
                        {'label': '3442_Def5_far.csv', 'value': '3442_Def5_far.csv'},
                        {'label': '3442_Def8_close.csv', 'value': '3442_Def8_close.csv'},
                        {'label': '3442_Def8_far.csv', 'value': '3442_Def8_far.csv'},
                        {'label': '3442_Hab_close.csv', 'value': '3442_Hab_close.csv'},
                        {'label': '3442_Hab_far.csv', 'value': '3442_Hab_far.csv'},
                        {'label': '3469_Def2B_close.csv', 'value': '3469_Def2B_close.csv'},
                        {'label': '3469_Def2B_far.csv', 'value': '3469_Def2B_far.csv'},
                        {'label': '3469_Def5_close.csv', 'value': '3469_Def5_close.csv'},
                        {'label': '3469_Def5_far.csv', 'value': '3469_Def5_far.csv'},
                        {'label': '3469_Hab_close.csv', 'value': '3469_Hab_close.csv'},
                        {'label': '3469_Hab_far.csv', 'value': '3469_Hab_far.csv'},
                        {'label': '3470_Def2A_close.csv', 'value': '3470_Def2A_close.csv'},
                        {'label': '3470_Def2A_far.csv', 'value': '3470_Def2A_far.csv'},
                        {'label': '3470_Def2B_close.csv', 'value': '3470_Def2B_close.csv'},
                        {'label': '3470_Def2B_far.csv', 'value': '3470_Def2B_far.csv'},
                        {'label': '3470_Def5_close.csv', 'value': '3470_Def5_close.csv'},
                        {'label': '3470_Def5_far.csv', 'value': '3470_Def5_far.csv'},
                        {'label': '3470_Def8_close.csv', 'value': '3470_Def8_close.csv'},
                        {'label': '3470_Def8_far.csv', 'value': '3470_Def8_far.csv'},
                        {'label': '3470_HabA_close.csv', 'value': '3470_HabA_close.csv'},
                        {'label': '3470_HabA_far.csv', 'value': '3470_HabA_far.csv'},
                        {'label': '3471_Def2_close.csv', 'value': '3471_Def2_close.csv'},
                        {'label': '3471_Def2_far.csv', 'value': '3471_Def2_far.csv'},
                        {'label': '3471_Def8A_close.csv', 'value': '3471_Def8A_close.csv'},
                        {'label': '3471_Def8A_far.csv', 'value': '3471_Def8A_far.csv'},
                        {'label': '3471_Def8B_close.csv', 'value': '3471_Def8B_close.csv'},
                        {'label': '3471_Def8B_far.csv', 'value': '3471_Def8B_far.csv'},
                        {'label': '3471_HabA_close.csv', 'value': '3471_HabA_close.csv'},
                        {'label': '3471_HabA_far.csv', 'value': '3471_HabA_far.csv'},
                        {'label': '3471_HabB_close.csv', 'value': '3471_HabB_close.csv'},
                        {'label': '3471_HabB_far.csv', 'value': '3471_HabB_far.csv'},
                        {'label': '3472_Def2_close.csv', 'value': '3472_Def2_close.csv'},
                        {'label': '3472_Def2_far.csv', 'value': '3472_Def2_far.csv'},
                        {'label': '3472_Def5_close.csv', 'value': '3472_Def5_close.csv'},
                        {'label': '3472_Def5_far.csv', 'value': '3472_Def5_far.csv'},
                        {'label': '3472_Def8_close.csv', 'value': '3472_Def8_close.csv'},
                        {'label': '3472_Def8_far.csv', 'value': '3472_Def8_far.csv'},
                        {'label': '3472_Hab_close.csv', 'value': '3472_Hab_close.csv'},
                        {'label': '3472_Hab_far.csv', 'value': '3472_Hab_far.csv'},
                        {'label': '3475_Def2_close.csv', 'value': '3475_Def2_close.csv'},
                        {'label': '3475_Def2_far.csv', 'value': '3475_Def2_far.csv'},
                        {'label': '3475_Def5A_close.csv', 'value': '3475_Def5A_close.csv'},
                        {'label': '3475_Def5A_far.csv', 'value': '3475_Def5A_far.csv'},
                        {'label': '3475_Def8B_close.csv', 'value': '3475_Def8B_close.csv'},
                        {'label': '3475_Def8B_far.csv', 'value': '3475_Def8B_far.csv'},
                        {'label': '3475_Hab_close.csv', 'value': '3475_Hab_close.csv'},
                        {'label': '3475_Hab_far.csv', 'value': '3475_Hab_far.csv'}
                        ],
                    placeholder="dataset",
                    searchable=False,
                    value='Merged_1022.csv',
                    clearable=False,
                    multi=False,
                    style={'width': "80%"},
                )),
                width={'size': True, 'offset': 1}
            )
        )),


    dbc.Row((dbc.Col((html.Br())))),
    dbc.Row((dbc.Col((html.Br())))),
    dbc.Row((dbc.Col((html.Br())))),
    dbc.Row((dbc.Col((html.Br())))),
    dbc.Row((dbc.Col((html.Hr())))),
    dbc.Row((dbc.Col((html.Br())))),
    dbc.Row((dbc.Col((html.Br(id = "IB-Cells Frequent Itemsets"))))),

    dbc.Row((dbc.Col((html.H4("IB-Cells Frequent Itemsets", style={'margin' : 'auto', 'text-align' : 'center'})), width={'size': True}))),
    dbc.Row((dbc.Col((html.Br())))),

    dbc.Row((
        dbc.Col((
        dt.DataTable(id = "frequent_itemsets",  export_format="xlsx", columns=(
            [{'id': 'itemsets', 'name': 'itemsets'}]+
            [{'id': 'support', 'name': 'support'}] +
            [{'id' : 'length', 'name' : 'length'}]),
            fixed_rows={'headers': True},
            style_table={'height': 400},
            style_header={'backgroundColor': '#78C2AD', 'color' : 'white'},
            style_cell={'textAlign': 'center'},
            style_cell_conditional=[
                {'if': {'column_id': 'indecies'},'width': '1%'},
                {'if': {'column_id': 'support'},
                 'width': '40%'},
                {'if': {'column_id': 'length'},
                 'width': '40%'},
                ],
        )),
        width={"size": 10, "offset": 1})
    )),

    #dbc.Row((dbc.Col((html.Br())))),
    #dbc.Row((dbc.Col((html.Br())))),
    #dbc.Row((dbc.Col((html.H6("Frequent itemsets are a form of frequent patterns. Any set of items that occurs at the minimum support (minimum frequency) or more, is a frequent itemset.")),width={"offset": 1}))),
    dbc.Row((dbc.Col((html.Br())))),
    dbc.Row((dbc.Col((html.Br())))),
    dbc.Row((dbc.Col((html.Br())))),
    dbc.Row((dbc.Col((html.Hr())))),
    dbc.Row((dbc.Col((html.Br())))),
    dbc.Row((dbc.Col((html.Br())))),
    dbc.Row((dbc.Col((html.Br(id = "IB-Cells Association Rules"))))),

    dbc.Row((dbc.Col((html.H4("IB-Cells Association Rules", style={'margin' : 'auto', 'text-align' : 'center'})), width={'size': True}))),
    dbc.Row((dbc.Col((html.Br())))),

    dbc.Row((dbc.Col((
        dt.DataTable(id = "association_rules",  export_format="xlsx", columns=([{ 'id' : 'antecedents', 'name' : 'antecedents'}]+[{'id' : 'consequents', 'name' : 'consequents'}] + [{"name": i, "id": i} for i in COLUMNS]),
                style_cell={'textAlign': 'center'}, style_header={'backgroundColor': '#78C2AD', 'color' : 'white'},fixed_rows={'headers': True},style_table={'height': 400}, style_cell_conditional=[
                {'if': {'column_id': 'antecedent support'},'width': '16%'},
                {'if': {'column_id': 'consequent support'},'width': '16%'},
                {'if': {'column_id': 'antecedents'},'width': '13%'},
                {'if': {'column_id': 'consequents'},'width': '13%'},
                {'if': {'column_id': 'support'},'width': '16%'},
                {'if': {'column_id': 'confidence'},'width': '16%'},
                {'if': {'column_id': 'lift'},'width': '10%'},]),
            ),
            width={"size": 10, "offset": 1})
        )),

    #dbc.Row((dbc.Col((html.Br())))),
    #dbc.Row((dbc.Col((html.Br())))),
    #dbc.Row((dbc.Col((html.H6("Association rules are created by searching data for frequent 'if-then' patterns (where Antecedent is 'if' and Consequent is 'then') and using the")),width={"offset": 1}))),
    #dbc.Row((dbc.Col((html.H6("criteria'support' and 'confidence' to identify the most important relationships.")),width={"offset": 1}))),
    #dbc.Row((dbc.Col((html.H6("Support is an indication of how frequently the items appear in the data. Confidence indicates the number of times the if-then statements are")),width={"offset": 1}))),
    #dbc.Row((dbc.Col((html.H6("found true.")),width={"offset": 1}))),
    #dbc.Row((dbc.Col((html.H6("Lift is the ratio of confidence to support. If the lift value is smaller than one, then there is a negative correlation between datapoints. If the value is ")),width={"offset": 1}))),
    #dbc.Row((dbc.Col((html.H6("bigger than one, there is a positive correlation, and if the ratio equals 1, then there is no correlation.")),width={"offset": 1}))),

    dbc.Row((dbc.Col((html.Br())))),
    dbc.Row((dbc.Col((html.Br())))),
    dbc.Row((dbc.Col((html.Hr())))),
    dbc.Row((dbc.Col((html.Br())))),
    dbc.Row((dbc.Col((html.Br())))),

    dbc.Row((dbc.Col((html.H4("Cell Pattern Parameters", style={'margin' : 'auto', 'text-align' : 'center'})), width={'size': True}))),

    dbc.Row((dbc.Col((html.Br())))),
    dbc.Row((dbc.Col((html.Br())))),
    dbc.Row((dbc.Col((html.Br())))),
    dbc.Row((dbc.Col((html.Br())))),


    dbc.Row((
        dbc.Col((html.H6("Minimum Support Value"),
            dcc.Input(
                id="cp_support_number",
                type="number",
                placeholder="minimum support value",
                value=0.6,
            )),
            width={'size': True, 'offset': 1}
        ),

        dbc.Col((html.H6("Minimum Confidence Value"),
            dcc.Input(
                id="cp_confidence_number",
                type="number",
                placeholder="minimum confidence value",
                value=0.6,
            )),
            width={'size': True, 'offset': 1}
        ),

        dbc.Col((html.H6("Minimum Lift Value"),
            dcc.Input(
                id="cp_lift_number",
                type="number",
                placeholder="minimum lift number",
                value=1,
            )),
            width={'size': True, 'offset': 1}
        ),
    )),

     dbc.Tooltip(
            "This measure controls the frequency of an itemset.",
            target="cp_support_number",
            placement='right',
            style={'background-color' : '#F3969A', 'color' : 'white'},
        ),

    dbc.Tooltip(
            "This measure controls how often the 'if-then' associations are found in the set.",
            target="cp_confidence_number",
            placement='left',
            style={'background-color' : '#F3969A', 'color' : 'white'},
        ),

    dbc.Tooltip(
            "This measure controls the importance of a rule. If lift=1, there is no correlation between the antecedent and consequent. If lift>1, there is a positive correlation between the antecedent and consequent. If lift<1, there is a negative correlation between the antecedent and consequent.",
            target="cp_lift_number",
            placement='left',
            style={'background-color' : '#F3969A', 'color' : 'white'},
        ),


    dbc.Row((dbc.Col((html.Br())))),
    dbc.Row((dbc.Col((html.Br())))),
    dbc.Row((dbc.Col((html.Br())))),


    dbc.Row((dbc.Col((html.H6("Sort By (Order matters):", style={'margin-left' : 'auto','margin-right' : 'auto','margin-bottom' : '8px', 'text-align' : 'center'})), width={'size': True}))),

    dbc.Row((
        dbc.Col((dcc.Dropdown(
                id="cp_sort",
                options=[
                    {'label': 'Support', 'value': 1},
                    {'label': 'Confidence', 'value': 2},
                    {'label': 'Lift', 'value': 3},
                    {'label': 'None', 'value': 4},
                    {'label': 'Length (frequent itemsets only)' , 'value' : 5},
                ],
                placeholder="sort by",
                searchable=False,
                value=4,
                clearable=False,
                multi=True,
                style={'width': "55%"},
            )),
            width={'size': True, 'offset' : 5, 'padding-left' : '14px'}
        ))),


    dbc.Row((dbc.Col((html.Br())))),
    dbc.Row((dbc.Col((html.Br())))),
    dbc.Row((dbc.Col((html.Br())))),
    dbc.Row((dbc.Col((html.Hr())))),
    dbc.Row((dbc.Col((html.Br())))),
    dbc.Row((dbc.Col((html.Br())))),
    dbc.Row((dbc.Col((html.Br(id = "Cell Patterns Frequent Itemsets"))))),

    dbc.Row((dbc.Col((html.H4("Cell Patterns Frequent Itemsets", style={'margin' : 'auto', 'text-align' : 'center'})), width={'size': True}))),
    dbc.Row((dbc.Col((html.Br())))),

    dbc.Row((
        dbc.Col((
        dt.DataTable(id = "cp_frequent_itemsets",  export_format="xlsx", columns=(
            [{'id': 'itemsets', 'name': 'itemsets'}]+
            [{'id': 'support', 'name': 'support'}] +
            [{'id' : 'length', 'name' : 'length'}]),
            fixed_rows={'headers': True},
            style_table={'height': 400},
            style_header={'backgroundColor': '#78C2AD', 'color' : 'white'},
            style_cell={'textAlign': 'center'},
            style_cell_conditional=[
                {'if': {'column_id': 'indecies'},'width': '1%'},
                {'if': {'column_id': 'support'},
                 'width': '40%'},
                {'if': {'column_id': 'length'},
                 'width': '40%'},
            ],
        )),
        width={"size": 10, "offset": 1})
    )),


    dbc.Row((dbc.Col((html.Br())))),
    dbc.Row((dbc.Col((html.Br())))),
    dbc.Row((dbc.Col((html.Br())))),
    dbc.Row((dbc.Col((html.Hr())))),
    dbc.Row((dbc.Col((html.Br())))),
    dbc.Row((dbc.Col((html.Br())))),
    dbc.Row((dbc.Col((html.Br(id = "Cell Patterns Association Rules"))))),

    dbc.Row((dbc.Col((html.H4("Cell Patterns Association Rules", style={'margin' : 'auto', 'text-align' : 'center'})), width={'size': True}))),
    dbc.Row((dbc.Col((html.Br())))),

    dbc.Row((dbc.Col((
        dt.DataTable(id = "cp_association_rules",  export_format="xlsx", columns=([{ 'id' : 'antecedents', 'name' : 'antecedents'}]+[{'id' : 'consequents', 'name' : 'consequents'}] + [{"name": i, "id": i} for i in COLUMNS]),
                style_cell={'textAlign': 'center'}, style_header={'backgroundColor': '#78C2AD', 'color' : 'white'},fixed_rows={'headers': True},style_table={'height': 400}, style_cell_conditional=[
                {'if': {'column_id': 'antecedent support'},'width': '16%'},
                {'if': {'column_id': 'consequent support'},'width': '16%'},
                {'if': {'column_id': 'antecedents'},'width': '13%'},
                {'if': {'column_id': 'consequents'},'width': '13%'},
                {'if': {'column_id': 'support'},'width': '16%'},
                {'if': {'column_id': 'confidence'},'width': '16%'},
                {'if': {'column_id': 'lift'},'width': '10%'},]),
            ),
            width={"size": 10, "offset": 1})
        )),

    dbc.Row((dbc.Col((html.Br())))),
    dbc.Row((dbc.Col((html.Br())))),
    dbc.Row((dbc.Col(html.Div(html.A('Back to top', href='#top' , style={'color' : 'white', 'margin-left' : '15px'})),style ={'background-color' : '#78c2ad' , 'height': '50px', 'padding-top' : '10px'}))),
    dbc.Row((dbc.Col(html.Div(html.H3('© McGill Data Mining & Security Lab 2021', style={'color' : 'white', 'margin-left' : 'auto', 'margin-right' : 'auto' , 'text-align' : 'center' , 'font-size': '0.90rem'})),style ={'background-color' : '#78c2ad' , 'padding-bottom' : '10px'}))),
    ])


#Adding Functionality

@app.callback(
    [Output(component_id="frequent_itemsets", component_property="data")],

    [Input(component_id="support_number", component_property="value"),
     Input(component_id="sort", component_property="value"),
     Input(component_id="dataset", component_property="value")]
    )

#creating the IB-CELLS frequent itemsets
def table_one(min_support, sort_by, data):

    dataset = pd.read_csv(data)
    pd.set_option('display.max_rows', None)

    frequent_itemsets = pd.DataFrame()
    frequent_itemsets = fpgrowth(dataset, min_support=float(min_support), use_colnames=True)

    frequent_itemsets['length'] = frequent_itemsets['itemsets'].apply(lambda x: len(x))
    frequent_itemsets['itemsets'] = frequent_itemsets['itemsets'].apply(lambda x: list(x))
    frequent_itemsets['support'] = frequent_itemsets['support'].apply(lambda x: round(x, 3))

    val_dict = { "1" : "support", "5" : "length", "4" : "None"}
    val_list=[]

    if sort_by is None:
        sort_by = ['4']

    if isinstance(sort_by, int):
        sort_by = [str(sort_by)]

    if (not(sort_by is None)):
        for num in sort_by:
            if num==1 or num==4 or num==5:
                val_list.append(str(val_dict.get(str(num))))

        if "None" in val_list:
            val_list = val_list.remove("None")

        if len(val_list) != 0:
            frequent_itemsets =  frequent_itemsets.sort_values(by=val_list, ascending=False)


    frequent_itemsets['itemsets'] = frequent_itemsets['itemsets'].apply(lambda x: ', '.join([str(elem) for elem in x]))
    frequent_itemsets_data=[frequent_itemsets.to_dict('records')]

    return frequent_itemsets_data



@app.callback(
    [Output(component_id="association_rules", component_property="data")],

    [Input(component_id="confidence_number", component_property="value"),
     Input(component_id="lift_number", component_property="value"),
     Input(component_id="switch", component_property="value"),
     Input(component_id="frequent_itemsets", component_property="data"),
     Input(component_id="sort", component_property="value")]
    )

#creating the IB-CELLS association rules
def table_two(min_confidence, min_lift, switch, data, sort_by):

    #importing frequent_itemsets
    frequent_itemsets = pd.DataFrame.from_records(data)
    frequent_itemsets['itemsets'] =frequent_itemsets['itemsets'].apply(lambda x: x.split(", "))
    frequent_itemsets['itemsets'] = frequent_itemsets['itemsets'].apply(lambda x: frozenset(tuple(x)))

    #association rules
    rules = pd.DataFrame()
    rules = association_rules(frequent_itemsets, metric='confidence', min_threshold=float(min_confidence))
    rules = rules.drop(['leverage', 'conviction'], axis=1)
    rules = rules[(rules['lift'] >= int(min_lift)) ]
    rules['confidence'] = rules['confidence'].apply(lambda x: round(x, 3))
    rules['lift'] = rules['lift'].apply(lambda x: round(x, 3))

   #choosing the right subset
    if rules.shape[0] != 0:
        B= frozenset(['IB'])
        rules1 = pd.DataFrame()

        #only include cells with IB
        for i in range(rules.shape[0]):
            if (((rules.iat[i,0].intersection(B) == frozenset({'IB'})) and (len(rules.iat[i,0]) == 1))
                or ((rules.iat[i,1].intersection(B) == frozenset({'IB'})) and (len(rules.iat[i,1]) == 1))):
                    rules1 = pd.concat([rules.iloc[[i]], rules1])

        #IB->cells
        if switch == 2:
            rules2 = pd.DataFrame()

            for i in range(rules1.shape[0]):
                if rules1.iat[i,0] == frozenset({'IB'}):
                    rules2 = pd.concat([rules1.iloc[[i]], rules2])

            rules1 = rules2

        #cells->IB
        elif switch == 1:
            rules3 = pd.DataFrame()

            for j in range(rules1.shape[0]):
                if rules1.iat[j,1] == frozenset({'IB'}):
                    rules3 = pd.concat([rules1.iloc[[j]], rules3])

            rules1 = rules3


    if rules1.shape[0] != 0:
        rules1['antecedents'] = rules1['antecedents'].apply(lambda x: list(x))
        rules1['consequents'] =  rules1['consequents'].apply(lambda x: list(x))


    val_dict = { "1" : "support", "2" : "confidence", "3": "lift", "4" : "None"}
    val_list=[]

    if sort_by is None:
        sort_by = ['4']
    if isinstance(sort_by, int):
        sort_by = [str(sort_by)]

    if (not(sort_by is None)):
        for num in sort_by:
            val_list.append(str(val_dict.get(str(num))))

        if "None" in val_list:
            val_list = val_list.remove("None")

        if val_list !=None:
            rules1 =  rules1.sort_values(by=val_list, ascending=False)

    rules1['antecedents'] = rules1['antecedents'].apply(lambda x: ', '.join([str(elem) for elem in x]))
    rules1['consequents'] = rules1['consequents'].apply(lambda x: ', '.join([str(elem) for elem in x]))
    rules_data=[rules1.to_dict('records')]

    return rules_data



@app.callback(
    [Output(component_id="cp_frequent_itemsets", component_property="data")],

    [Input(component_id="cp_support_number", component_property="value"),
    Input(component_id="cp_sort", component_property="value"),
    Input(component_id="dataset", component_property="value")]
    )

#creating the CELL PATTERNS frequent itemsets
def table_three(min_support, sort_by, data):

    cp_data = "IB_" + data
    cp_dataset = pd.read_csv(cp_data)
    pd.set_option('display.max_rows', None)

    cp_frequent_itemsets = pd.DataFrame()
    cp_frequent_itemsets = fpgrowth(cp_dataset, min_support=float(min_support), use_colnames=True)

    cp_frequent_itemsets['length'] = cp_frequent_itemsets['itemsets'].apply(lambda x: len(x))
    cp_frequent_itemsets['itemsets'] = cp_frequent_itemsets['itemsets'].apply(lambda x: list(x))
    cp_frequent_itemsets['support'] = cp_frequent_itemsets['support'].apply(lambda x: round(x, 3))

    val_dict = { "1" : "support", "5" : "length", "4" : "None"}
    val_list=[]

    if sort_by is None:
        sort_by = ['4']

    if isinstance(sort_by, int):
        sort_by = [str(sort_by)]

    if (not(sort_by is None)):
        for num in sort_by:
            if num==1 or num==4 or num==5:
                val_list.append(str(val_dict.get(str(num))))

        if "None" in val_list:
            val_list = val_list.remove("None")

        if len(val_list) != 0:
            cp_frequent_itemsets =  cp_frequent_itemsets.sort_values(by=val_list, ascending=False)


    cp_frequent_itemsets['itemsets'] = cp_frequent_itemsets['itemsets'].apply(lambda x: ', '.join([str(elem) for elem in x]))
    cp_frequent_itemsets_data=[cp_frequent_itemsets.to_dict('records')]

    return cp_frequent_itemsets_data




@app.callback(
    [Output(component_id="cp_association_rules", component_property="data")],

    [Input(component_id="cp_confidence_number", component_property="value"),
     Input(component_id="cp_lift_number", component_property="value"),
     Input(component_id="cp_frequent_itemsets", component_property="data"),
     Input(component_id="cp_sort", component_property="value"),]
    )

#creating the CELLS PATTERNS association rules
def table_four(min_confidence, min_lift, data, sort_by):

    #importing frequent_itemsets
    frequent_itemsets = pd.DataFrame.from_records(data)
    frequent_itemsets['itemsets'] =frequent_itemsets['itemsets'].apply(lambda x: x.split(", "))
    frequent_itemsets['itemsets'] = frequent_itemsets['itemsets'].apply(lambda x: frozenset(tuple(x)))

    #association rules
    rules = pd.DataFrame()
    rules = association_rules(frequent_itemsets, metric='confidence', min_threshold=float(min_confidence))
    rules = rules.drop(['leverage', 'conviction'], axis=1)
    rules = rules[(rules['lift'] >= int(min_lift)) ]
    rules['confidence'] = rules['confidence'].apply(lambda x: round(x, 3))
    rules['lift'] = rules['lift'].apply(lambda x: round(x, 3))


    if rules.shape[0] != 0:
        rules['antecedents'] = rules['antecedents'].apply(lambda x: list(x))
        rules['consequents'] =  rules['consequents'].apply(lambda x: list(x))

    val_dict = { "1" : "support", "2" : "confidence", "3": "lift", "4" : "None"}
    val_list=[]

    if sort_by is None:
        sort_by = ['4']
    if isinstance(sort_by, int):
        sort_by = [str(sort_by)]

    if (not(sort_by is None)):
        for num in sort_by:
            val_list.append(str(val_dict.get(str(num))))

        if "None" in val_list:
            val_list = val_list.remove("None")

        if val_list !=None:
            rules =  rules.sort_values(by=val_list, ascending=False)


    rules['antecedents'] = rules['antecedents'].apply(lambda x: ', '.join([str(elem) for elem in x]))
    rules['consequents'] = rules['consequents'].apply(lambda x: ', '.join([str(elem) for elem in x]))
    rules_data=[rules.to_dict('records')]

    return rules_data



if __name__ == '__main__':
    app.run_server(debug=False)


