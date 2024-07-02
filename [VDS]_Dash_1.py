import pandas as pd

import requests

from dash import Dash, html, dcc, Input, Output, dash_table, callback
import dash_bootstrap_components as dbc
import dash_mantine_components as dmc

import plotly.express as px

# App creation
app = Dash(__name__)

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
    

colors = {
    'background': '#111111',
    'text': '#6666a0'
}

fig = px.bar(book_df.head(10),
            x = "title", 
            y = "num_pages",
            hover_data = "authors")

fig.update_layout(
    plot_bgcolor=colors['background'],
    paper_bgcolor=colors['background'],
    font_color=colors['text'])

fig.update_yaxes(title_text = "Number of pages")
fig.update_xaxes(title_text = "Title")

# Layout of the app
app.layout = html.Div([html.H1("Read the book", className='header-title'),
                       html.H2("The only book", className='header-title'),
                       html.P("Please enter an author",
                              style={'color': '#6666a0'}),
                       dcc.Input(id = 'author_name',
                                 type = "text"),
                       html.P("Please enter a max page number",
                              style={'color': '#6666a0'}),
                       dcc.Input(id = 'max_page',
                                 type = 'number'),
                       html.P(""),
              dcc.Graph(figure = fig, 
                        id = 'barplot')
              ])

# Manage the callback to catch user's choice
# @callback(
#     Output(component_id = 'barplot', component_property = 'figure'),
#     Input(component_id = 'author_name', component_property = 'value'),
#     Input(component_id = 'max_page', component_property = 'value')
# )

# # Create a function to update the graph
# def display_book(author, max_page):
#     try:
#         M1 = book_df["authors"].str.contains(author)
#         M2 = book_df["num_pages"] < max_page
#         search = book_df[M1 & M2]
    
#     except:
#         search = book_df
    
#     fig = px.bar(search.head(10),
#                 x = "title", 
#                 y = "num_pages",
#                 hover_data = "authors"),
    # fig.update_yaxes(title_text = "Number of pages"),
    # fig.update_xaxes(title_text = "Title")
    
    # return fig

# App launch
if __name__ == '__main__':
    app.run_server(debug=True)