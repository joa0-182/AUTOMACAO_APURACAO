#!/usr/bin/env python
# coding: utf-8

# In[1]:


# Bibliotecas 
import pandas as pd

# Para enxerga arquivos na pasta principal
import sys 
import os
sys.path.append(os.path.abspath(".."))

#Funções
from arquivos_base import contagem_validacao
from arquivos_base import observacao_validacao
from arquivos_base import colunas_finais_validacao
from arquivos_base import conecta_banco
from arquivos_base import converte_ipynb_to_py

# Bases
from carregar_arquivos_base import dados_produtos_oferta_CLIENTE


# ### 2. Garantir que a apuração contenha somente os produtos da Oferta
# 
# Utiliza com base a tabela de produtos do arquivo enviado pelo Cliente, "Produtos oferta CLIENTE.xlsx", para verificar se os produtos dessa tabela estão cadastrados dentro do banco.
# 

# In[2]:


sql = conecta_banco("ODBC Driver 17 for SQL Server", "seu servidor", "AGRO", None, None, "SIM")
codigo_oferta = 2


# In[3]:


dados_produtos_banco = pd.read_sql(
    f"""
 SELECT OFE.CODIGOOFERTA,
	      OFE.CODIGOPRODUTO,
	      PRO.DESCRICAOPRODUTO
   FROM PRODUTO_OFERTA OFE
  INNER JOIN PRODUTO PRO
		 ON OFE.CODIGOPRODUTO = PRO.CODIGOPRODUTO
  WHERE OFE.CODIGOOFERTA = {codigo_oferta}
  ORDER BY CODIGOEMPRESA

    """, sql
)


# In[6]:


dados_produtos = pd.merge(
    dados_produtos_banco,
    dados_produtos_oferta_CLIENTE,
    how="left",
    left_on="CODIGOPRODUTO",
    right_on="SKU",
    indicator=True
)



validar_produtos = dados_produtos

validar_produtos["Validação"] = validar_produtos.apply(
    lambda case: "Divergente" if case["CODIGOPRODUTO"] != case["SKU"]
    else "Correto",
    axis = 1
)

validar_produtos.head(1)


# In[7]:


qtde_correta_02, qtde_divergente_02 = contagem_validacao(validar_produtos)
validar_produtos_campanha = observacao_validacao(validar_produtos, qtde_correta_02, qtde_divergente_02)

validar_produtos = colunas_finais_validacao (
    validar_produtos,
    ["CODIGOOFERTA", "CODIGOPRODUTO", "DESCRICAOPRODUTO", "SKU", "DescricaoProduto", "Validação", "Observação"]
)