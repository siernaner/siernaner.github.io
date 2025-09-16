import pandas as pd #leitura de arquivos
import plotly.express as px #biblioteca de gráficos
from dash import Dash, dcc, html, Input, Output #biblioteca para criar o dashboard web

df = pd.read_csv("data/CarsData.csv") #le o arquivo csv

app = Dash(__name__) #inicia o app


app.layout = html.Div([ #layout do app
    html.H1("Quantidade de Carros por Ano", style={'textAlign': 'center'}), #título do app e estilo
    
    html.Label("Tipo de transmissão", style={'fontSize': 20}), #rótulo do dropdown e tamanho da fonte
    dcc.Dropdown( #dropdown para selecionar o tipo de transmissão
        id='dropdown-transmissao', #id do dropdown
        options=[{'label': t, 'value': t} for t in sorted(df['transmission'].dropna().unique())], #opções do dropdown, removendo valores nulos e ordenando
        value=sorted(df['transmission'].dropna().unique())[0], #valor padrão do dropdown
        style={'width': '50%'} #largura do dropdown
    ),
    
    dcc.Graph(id='grafico-transmissao') #gráfico que será atualizado com base na seleção do dropdown
])

@app.callback( #callback para atualizar o gráfico
    Output('grafico-transmissao', 'figure'), #saída do gráfico
    Input('dropdown-transmissao', 'value') #entrada do dropdown
)
def atualizar_grafico(transmissao_selecionada):#atualiza o gráfico baseando-se no item do dropdown selecionado
    df_filtrado = df[df['transmission'] == transmissao_selecionada] #filtra os dados conforme a transmissão selecionada
    contagem_por_ano = df_filtrado['year'].value_counts().sort_index() #conta a quantidade de carros por ano e ordena pelo ano
    fig = px.bar( #cria o gráfico de barras na página
        x=contagem_por_ano.index, #eixo x com os anos
        y=contagem_por_ano.values, #eixo y com a contagem de carros
        labels={'x': 'Ano', 'y': 'Quantidade de Carros'}, #textos dos eixos
        title=f"Transmissão: {transmissao_selecionada}" #título do gráfico com a transmissão selecionada
    )
    fig.update_traces(text=contagem_por_ano.values, textposition='outside') #adiciona os valores das barras acima delas
    fig.update_layout(xaxis_tickangle=-45) #rotaciona os rótulos do eixo x para melhor visualização
    return fig #retorna o gráfico atualizado

if __name__ == '__main__': #verifica se o app está em execução
    app.run(debug=True) #caso estiver, ele roda o app em modo debug