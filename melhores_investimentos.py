#------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
'''
Criado por: Lucas Andrade
Data de criação: 02/02/2024
Versão: '1.0'
Detalhes do projeto: Esse projeto foi idealizado para ser inserido uma lista das melhores ações (segundo o Ibovespa) e com ele, ser obtido um gráfico do seu histórico nos últimos 5 anos.
                     Nele, o gráfico completo das ações é salvo dentro de uma pasta, como também os gráficos individuais de cada ação passada.
'''
#------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime, timedelta, timezone
import os

# Configuração global do fuso horário
yf.pdr_override()
pd.options.mode.chained_assignment = None  # Evitar warnings

def buscar_empresas(empresas, data_inicio):
    dados_empresas = {}

    for empresa in empresas:
        try:
            # Obtendo dados históricos com fuso horário especificado
            dados = yf.download(empresa, start=data_inicio, end=datetime.now(), progress=False, group_by='ticker', auto_adjust=True, prepost=True, threads=True, proxy=None)
            dados_empresas[empresa] = dados
        except Exception as e:
            print(f"Erro ao obter dados para {empresa}: {e}")

    return dados_empresas

def plotar_grafico_completo(dados_empresas):
    plt.figure(figsize=(12, 8))
    for empresa, dados in dados_empresas.items():
        plt.plot(dados['Close'], label=empresa)

    plt.title('Histórico de Fechamento')
    plt.xlabel('Data')
    plt.ylabel('Preço de Fechamento')
    plt.legend(loc='center left', bbox_to_anchor=(1, 0.5))  # Define a legenda à direita do gráfico
    plt.show()

def salvar_grafico_completo(dados_empresas, pasta_destino):
    plt.figure(figsize=(12, 8))
    for empresa, dados in dados_empresas.items():
        plt.plot(dados['Close'], label=empresa)

    plt.title('Histórico de Fechamento')
    plt.xlabel('Data')
    plt.ylabel('Preço de Fechamento')
    plt.legend()

    # Cria a pasta se não existir
    if not os.path.exists(pasta_destino):
        os.makedirs(pasta_destino)

    plt.savefig(os.path.join(pasta_destino, 'grafico_completo.png'))
    plt.close()

def salvar_graficos_individualmente(dados_empresas, pasta_destino):
    for empresa, dados in dados_empresas.items():
        plt.figure(figsize=(10, 5))
        plt.plot(dados['Close'], label=empresa)
        plt.title(f'Histórico de Fechamento - {empresa}')
        plt.xlabel('Data')
        plt.ylabel('Preço de Fechamento')
        plt.legend()

        # Cria a pasta se não existir
        if not os.path.exists(pasta_destino):
            os.makedirs(pasta_destino)

        plt.savefig(os.path.join(pasta_destino, f'{empresa}_historico.png'))
        plt.close()

if __name__ == "__main__":
    # Adicione o símbolo de ticker das empresas que você deseja analisar
    #empresas = ['PETR4.SA', 'VALE3.SA', 'ITUB4.SA', 'BBDC4.SA', 'ABEV3.SA', 'MGLU3.SA', 'BBAS3.SA', 'WEGE3.SA', 'RENT3.SA', 'PETR3.SA'] # Melhores ações segundo o índice Ibovespa
    empresas = ['HGLG11.SA', 'HGBS11.SA', 'KNRI11.SA', 'XPML11.SA', 'VISC11.SA', 'VRTA11.SA', 'HGRE11.SA', 'RNGO11.SA', 'MXRF11.SA', 'RECT11.SA'] # Melhores fundos de investimentos segundo o índice Ibovespa

    # Define o diretório de trabalho como o diretório do script
    script_dir = os.path.dirname(os.path.abspath(__file__))
    os.chdir(script_dir)

    # Cria uma pasta com o formato "FII-DIA-MÊS-ANO"
    pasta_destino = datetime.now().strftime("FII-%d-%m-%Y-%H-%M-%S")

    # Data de início para obter o histórico
    data_inicio = datetime.now() - timedelta(days=365*5)  # 5 anos de histórico

    # Realiza a busca das empresas
    dados_empresas = buscar_empresas(empresas, data_inicio)

    # Plota o gráfico completo na mesma tela
    plotar_grafico_completo(dados_empresas)

    # Salva o gráfico completo em um arquivo PNG na pasta criada
    salvar_grafico_completo(dados_empresas, pasta_destino)

    # Salva os gráficos individuais na mesma pasta
    salvar_graficos_individualmente(dados_empresas, pasta_destino)

    # Imprime o diretório atual
    print(f"Arquivos salvos em: {os.path.join(script_dir, pasta_destino)}")