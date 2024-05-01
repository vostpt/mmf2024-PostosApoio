import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import pandas as pd
import dash_bootstrap_components as dbc

# Initialize the Dash app
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

# Define the layout of the app
app.layout = dbc.Container([
    dcc.Input(
        id='search-box', 
        type='text', 
        placeholder='Pesquisar por Distrito', 
        style={'margin': '20px 0', 'width': '100%'}
    ),
    dbc.Row(id='cards-container', className='g-4')
], fluid=True)

# Callback to update the cards based on the search input
@app.callback(
    Output('cards-container', 'children'),
    Input('search-box', 'value')
)
def update_cards(search_value):
    # Load the data from a CSV file inside the callback to get the latest data
    df = pd.read_csv('https://docs.google.com/spreadsheets/d/e/2PACX-1vRrsDGcWj6pm3XH8Z0mrSftss9Hy1JSfh7Wi0zYoY1YMfCEclt3cfaibPmEwhTECpualvNfiZpVvOuy/pub?gid=307363106&single=true&output=csv')
    
    # Define service columns
    service_columns = ['ENFERMAGEM', 'FISIOTERAPIA', 'LAVA-PÉS', 'REFORÇO ALIMENTAR', 'BANHOS', 'DORMIDAS', 'ASSISTÊNCIA ESPIRITUAL']
    
    # Filter the DataFrame based on the search input
    filtered_df = df[df['DISTRITO'].str.contains(search_value, case=False, na=False)] if search_value else df
    
    # Create a card for each row in the filtered DataFrame
    cards = []
    for index, row in filtered_df.iterrows():
        # List available services
        available_services = [service for service in service_columns if row[service] == 'SIM']
        
        # Create a card for each row in the filtered DataFrame
        card = dbc.Card(
            [
                dbc.CardHeader(row['ENTIDADE'] + " - " + row['NOME DO LOCAL'], style={'background-color': '#df9037', 'color': 'white'}),
                dbc.CardBody(
                    [
                        html.P(f"Morada: {row['MORADA DO LOCAL']}", className='card-text'),
                        html.P(f"Dias de Funcionamento: {row['DIAS DE FUNCIONAMENTO']}", className='card-text'),
                        html.P(f"Horário: {row['HORÁRIO DE FUNCIONAMENTO']}", className='card-text'),
                        html.P(f"Contacto: {row['CONTACTO TELEFÓNICO 01']}", className='card-text'),
                        html.A("Google Maps Link", href=row['LINK GOOGLE MAPS'], target="_blank", className='btn',style={'background-color': '#df9037', 'color': 'white', 'border': 'none'}),
                        html.Br(),
                        html.Br(),
                        html.H3('Apoio Disponível'),
                        html.Ul([html.Li(service) for service in available_services], className='list-unstyled')
                    ],
                    style={'background-color': '#f5dbbd'}
                )
            ],
            className='mb-3'
        )
        cards.append(dbc.Col(card, width=12, md=6, lg=4))
    
    return cards


if __name__ == '__main__':
    app.run_server(debug=False)
