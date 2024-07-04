import pandas as pd

import requests

from dash import Dash, html, dcc, Input, Output, State, dash_table, callback
import dash_bootstrap_components as dbc
import dash_mantine_components as dmc

import plotly.express as px

#####################################################################################################################################
# Creation of the dataframe
link = "https://raw.githubusercontent.com/chriszapp/datasets/main/books.csv"

r = requests.get(link)

if r.status_code == 200:
    book_df = pd.read_csv(link, 
                          sep = ",", 
                          on_bad_lines = "warn")
    book_df.rename(columns = {"  num_pages": "num_pages"}, inplace = True)   
else:
    print("Impossible to read the file")

#####################################################################################################################################
# Create the barplot

fig = px.bar(book_df.head(10),
            x = "num_pages", 
            y = "title",
            hover_data = "authors",
            title = "List of 10 books from your choice")

# Colors of the background and the text in the graph
colors = {'background': '#0f2537',
          'text': '#df6919',
          'bars': '#4e5d6c'}

fig.update_layout(
    plot_bgcolor=colors['background'],
    paper_bgcolor=colors['background'],
    font_color=colors['text'])

fig.update_yaxes(title_text = "Title")
fig.update_xaxes(title_text = "Number of pages")

#####################################################################################################################################
# App creation
app = Dash(__name__, external_stylesheets=[dbc.themes.SUPERHERO])


#####################################################################################################################################
# Layout of the app
app.layout = html.Div([
    
    ################################################# Nav Bar ################################################################
    dbc.NavbarSimple(
        children=[
            dbc.NavItem(dbc.NavLink("Page 1", href="#")),
            dbc.DropdownMenu(
                children=[
                    dbc.DropdownMenuItem("More to come", header=True),
                    dbc.DropdownMenuItem("Page 2", href="#"),
                ],
                nav=True,
                in_navbar=True,
                label="Droplist",
            ),
        ],
        brand="Book Selector",
        brand_href="#",
        color="primary",
        dark=True,
    ),
    
    # Header
    html.Br(style={"line-height": "5"}),
    html.H1("Read the book", className='header-title', style = {"textAlign": "center"}),
    html.Br(style={"line-height": "5"}),
    html.H2("The only book", className='header-title', style = {"textAlign": "center"}),
    
    
    html.Br(),
    dbc.Container(
        [dbc.Row(                                                                                                   
            dbc.Col(html.H4("This app will recommand you the best book to read based on your filters"))),
    
            # Button for the modal
        dbc.Row(
            dbc.Col(html.P("You can get more detail here"))),
        dbc.Row(
            dbc.Col(dbc.Button("Help", id = "open_modal", n_clicks = 0))),
        dbc.Row(
            dbc.Col(dbc.Tooltip(
                "Bouuuuuuh you really need an explanation?!",
                target="open_modal")))]),
    
    # Modal
    dbc.Modal([
        dbc.ModalHeader("Filters"),
        dbc.ModalBody("You can filter the selection by author entering the name of the author you want."),
        dbc.ModalBody("You can also modify the selection based on the max pages number of the book."),
        dbc.ModalFooter(
            dbc.Button("Close", id="close_modal", className="ml-auto")
        ),
        ], id="modal", is_open=False),

    html.Br(),
    html.Br(),
    dbc.Container([
        dbc.Row(
            dbc.Col(html.H5("Filters"))),
        dbc.Row([
            dbc.Col(
                [html.P("Enter the author's name"),
                     dcc.Input(id = 'author_name',
                               type = "text")],
                width=3, id = "col1"),
            dbc.Col([
                html.P("Enter the maximum pages in the book"),
                     dcc.Input(id = 'max_page',
                               type = 'number')],
                width=3, id = "col2")
        ]),
        dbc.Row([html.Br(),
                 dcc.Graph(figure = fig,
                           id = 'barplot',
                           style={'width': '100%'})
                 ])
        ])
    ])

    # html.Br(),
    # dcc.Graph(figure = fig, 
    # id = 'barplot')
    #             ])

#####################################################################################################################################
# Callback for the modal
@callback(
     Output("modal", "is_open"),
    Input("open_modal", "n_clicks"), Input("close_modal", "n_clicks"),
    [State("modal", "is_open")]
)

# Create a function to open and close the modal
def open_and_close_modal(n1, n2, is_open):
    if n1 or n2:
        return not is_open
    return is_open
 
# Manage the callback to catch user's choice
@callback(
    Output(component_id = 'barplot', component_property = 'figure'),
    [Input(component_id = 'author_name', component_property = 'value'),
    Input(component_id = 'max_page', component_property = 'value')]
)
 
# Create a function to update the graph   
def display_book(author, max_page):
    if author is None and max_page is None:
        search = book_df
    elif author is not None and max_page is None:
        M1 = book_df["authors"].str.contains(author, case = False)
        search = book_df[M1]
    elif author is None and max_page is not None:
        M2 = book_df["num_pages"] <= max_page
        search = book_df[M2]
    else:
        M1 = book_df["authors"].str.contains(author)
        M2 = book_df["num_pages"] <= max_page
        search = book_df[M1 & M2]
    
    fig = px.bar(search.head(10),
            x = "num_pages", 
            y = "title",
            hover_data = "authors",
            title = "List of 10 books from your choice",
            color_discrete_sequence = [colors['bars']]*10,
            height = 600
            # width = 1000
            )
    fig.update_layout(
        plot_bgcolor = colors['background'],
        paper_bgcolor = colors['background'],
        font_color = colors['text'],
        modebar_color = colors['text'],
        hoverlabel_bgcolor = colors['bars'])

    fig.update_yaxes(title_text = "Title")
    fig.update_xaxes(title_text = "Number of pages")

    return fig

#####################################################################################################################################
# App launch
if __name__ == '__main__':
    app.run_server(debug=True)