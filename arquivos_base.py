import pandas as pd
import os
import nbformat
import unicodedata

from nbconvert import PythonExporter
from IPython import get_ipython
from datetime import datetime

# Para conexão ao banco de dados
from sqlalchemy import create_engine
from sqlalchemy.exc import SQLAlchemyError


# === Caminho dos arquivos base ===
path = r"C:fakepath\AUTOMACAO_APURACAO\Bases"
path_resumo_validacao = r"C:fakepath\AUTOMACAO_APURACAO\Arquivos"

# === Nome dos arquivos CLIENTE ===
produtos_oferta = "Produtos oferta CLIENTE.xlsx"
clientes_oferta = "CNPJ dentro Oferta CLIENTE.xlsx"
clientes_com_pendencia = "Pendentes Juridicamente CLIENTE.xlsx"

# === Nome arquivo
data = datetime.now()
nome_arquivo_excel = f"Apuração Oferta 2025 {data.date()}.xlsx"
nome_arquivo_word = f"Laudo - Resumo Apuração Oferta 2025 {data.date()}.docx"


# Para geração do arquivo validado
arquivo_validacao_excel = os.path.join(path_resumo_validacao, nome_arquivo_excel)
arquivo_validacao_word = os.path.join(path_resumo_validacao, nome_arquivo_word)


def carregar_arquivo_excel(nome_arquivo, sheet, tipo_dado=None):

    """
    Carrega um arquivo Excel.

    Verifica se o arquivo existe, e carrega usando o pandas.

    Args:
        nome_arquivo (str): Nome do arquivo Excel a ser carregado.
        sheet (str ou int): Nome ou índice da aba do Excel.
        tipo_dado (dict, Opcional): Dicionário com tipos de dados para as colunas.

    Returns:
        pd.DataFrame: Um DataFrame do pandas com os dados do Excel.

    Raises:
        FileNotFoundError: Se o arquivo especificado não for encontrado.
    """
    try:
        caminho_completo = os.path.join(path, nome_arquivo)

        ##validação
        if not os.path.exists(caminho_completo):
            raise FileNotFoundError(f"Arquivo não encontrado: {caminho_completo}")
        
        return pd.read_excel(caminho_completo, sheet_name=sheet, dtype=tipo_dado)
    
    except Exception as erro:
        raise Exception(f"Algo de errado aconteceu na hora de carregar o arquivo excel: {erro}")



def contagem_validacao(validacao):

    """
    Conta a quantidade de resultados "Correto" e "Divergente" em uma validação.
    Deve conter o campo "Validação" no DataFrame.

    Args:
        validacao (pd.DataFrame): DataFrame geral de validação

    Returns:
        tuple: Uma tupla com a quantidade de itens "Correto" e "Divergente" (int, int).
    """

    try:
        contagem_validacao = validacao["Validação"].value_counts()

        qtde_correta = contagem_validacao.get("Correto", 0)
        qtde_divergente = contagem_validacao.get("Divergente", 0)

        return qtde_correta, qtde_divergente
    
    except Exception as erro:
        raise Exception(f"Algo de errado aconteceu ao contar Correto, e Divergente dentro do Dataframe: {erro}")



def observacao_validacao(validacao, qtde_correto, qtde_divergente):

    """
    Adiciona uma observação ao DataFrame de validação com as quantidades de itens "Correta" e "Divergente".

    Args:
        validacao (pd.DataFrame): DataFrame de validação dos items.
        qtde_correto (int): Quantidade de itens "Correto".
        qtde_divergente (int): Quantidade de itens "Divergente".

    Returns:
        pd.DataFrame: O DataFrame de validação com a coluna "Observação" preenchida.
    """
    
    try:
        validacao.loc[0, "Observação"] = f"Existem {qtde_correto} Correto, e {qtde_divergente} Divergentes"

        return validacao
    
    except Exception as erro:
        raise Exception(f"Ocorreu um erro na hora da adição do campo Observacao ao Dataframe: {erro}")


def colunas_finais_validacao (validacao, colunas):

    """
    Seleciona as colunas finais desejadas em um DataFrame de validação.

    Args:
        validacao (pd.DataFrame): DataFrame de validação.
        colunas (list): Lista de nomes das colunas a serem selecionadas.

    Returns:
        pd.DataFrame: O DataFrame de validação, apenas as colunas especificadas.
    """
    try:
        colunas_finais = colunas

        validacao = validacao[colunas_finais]

        return validacao
    
    except Exception as erro:
        raise Exception (f"Erro ao selecionar as colunas finais: {erro}")


def converte_ipynb_to_py(caminho_arquivo_ipynb=None, caminho_destino="ValidacoesPY"):

    """
    Converte um arquivo .ipynb para .py e salva na pasta especificada (padrão: ValidacoesPY).
    
    Parâmetros:
        caminho_arquivo_ipynb (str): Caminho para o arquivo .ipynb. Se None, tenta usar o nome do próprio notebook.
        caminho_destino (str): Pasta onde o .py será salvo (criada se não existir).
    """

    try:
        if caminho_arquivo_ipynb is None:

            ipython = get_ipython()

            if ipython:
                caminho_arquivo_ipynb = ipython.run_line_magic("notebook", "")
            else:
                raise ValueError("Caminho do arquivo não fornecido e IPython não detectado.")
            

        if not os.path.isfile(caminho_arquivo_ipynb):
            raise FileNotFoundError(f"Arquivo não encontrado: {caminho_arquivo_ipynb}")
        

        caminho_notebook = os.path.abspath(caminho_arquivo_ipynb)
        pasta_raiz_projeto = os.path.dirname(os.path.dirname(caminho_notebook))

        caminho_final = os.path.join(pasta_raiz_projeto, caminho_destino)
        

        nome_arquivo = os.path.splitext(os.path.basename(caminho_arquivo_ipynb))[0] + ".py"
        destino = os.path.join(caminho_final, nome_arquivo)


        with open(caminho_arquivo_ipynb, "r", encoding="utf-8") as arquivo:
            notebook = nbformat.read(arquivo, as_version = 4)


        exportador = PythonExporter()
        corpo_arquivo, _ = exportador.from_notebook_node(notebook)

        os.makedirs(caminho_final, exist_ok=True)

        with open(destino, "w", encoding="utf-8") as saida_py:
            saida_py.write(corpo_arquivo)

    except Exception as erro:
        raise Exception(f"Erro ao converter notebook: {erro}")
    
def formata_texto(texto):

    """
    Formata o texto, retirando caracteres especiais, ocultos, espaços das pontas, espaços internos.

    Parâmetros:
        texto (str): campo a ser formatado.

    """

    if pd.isna(texto):
        return None

    texto = str(texto)
    texto = texto.strip()
    texto = unicodedata.normalize("NFKD", texto)
    texto = texto.encode("ASCII", "ignore").decode("utf-8")
    texto = texto.replace("\xa0", "")
    texto = texto.replace(" ", "")
    texto = texto.casefold()

    return texto

def conecta_banco(driver, server, database, username=None, password=None, trusted_connection=None):
    """
    Conexão ao banco de dados SQL Server usando SQLAlchemy

    Parâmetros:
        driver (str): Nome do driver ODBC (ex: 'ODBC Driver 17 for SQL Server, ou SQL Server')
        server (str): Nome do servidor do banco de dados
        database (str): Nome do banco (database) para conectar
        username (str): Opcional, Nome do usuário
        password (str): Opcional, Senha do usuário
        trusted_connection (str): "SIM" para usar autenticação integrada do Windows e "NÂO" quando for autenticação por Usuario e Senha
    """

    try:
        # Formatar driver para URL encoding (espaços viram +)
        driver_formatado = driver.replace(" ", "+")
        
        # Conexão com autenticação Windows
        if trusted_connection and trusted_connection.upper() == 'SIM':
            connection_string = (
                f"mssql+pyodbc://@{server}/{database}"
                f"?driver={driver_formatado}&trusted_connection=yes"
            )
        
        # Conexão com usuário e senha
        else:
            if not username or not password:
                raise ValueError("Username e password são obrigatórios se 'trusted_connection' não for 'SIM'")
            connection_string = (
                f"mssql+pyodbc://{username}:{password}@{server}/{database}"
                f"?driver={driver_formatado}"
            )

        engine = create_engine(connection_string)
        # Testar conexão
        with engine.connect() as conn:
            print("Conexão bem-sucedida!")

        return engine

    except SQLAlchemyError as erro:
        print(f"Erro ao conectar com SQLAlchemy: {erro}")
        return None

    except ValueError as erro:
        print(f"Erro de configuração: {erro}")
        return None