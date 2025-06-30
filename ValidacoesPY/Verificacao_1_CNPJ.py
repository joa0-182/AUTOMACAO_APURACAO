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
from carregar_arquivos_base import dados_clientes_oferta_CLIENTE


# ### 1.  Verifica os CNPJ participantes da campanha
# 
# Verifica se os CNPJ do arquivo "CNPJ dentro Oferta CLIENTE" enviado pelo Cliente, está cadastrado dentro do banco.
# 

# In[2]:


sql = conecta_banco("ODBC Driver 17 for SQL Server", "seu servidor", "AGRO", None, None, "SIM")
codigo_oferta = 2


# In[3]:


dados_clientes_banco = pd.read_sql(
    f"""
 SELECT OFE.CODIGOOFERTA,
        OFE.CODIGOEMPRESA,
        EMP.DESCRICAOEMPRESA,
        EMP.CNPJ
   FROM PRODUTO_OFERTA OFE
  INNER JOIN EMPRESA EMP
          ON OFE.CODIGOEMPRESA = EMP.CODIGOEMPRESA
  WHERE OFE.CODIGOOFERTA = {codigo_oferta}
  ORDER BY CODIGOEMPRESA

    """, sql
)


# In[18]:


dados_clientes_banco = dados_clientes_banco.rename(columns={"CNPJ": "CNPJ_BANCO"})
dados_clientes_oferta_CLIENTE = dados_clientes_oferta_CLIENTE.rename(columns={"CNPJ": "CNPJ_CLIENTE"})

dados_clientes = pd.merge(
    dados_clientes_banco[["CODIGOOFERTA", "CODIGOEMPRESA", "DESCRICAOEMPRESA", "CNPJ_BANCO"]],
    dados_clientes_oferta_CLIENTE[["CNPJ_CLIENTE", "Empresa"]],
    how="left",
    left_on="CNPJ_BANCO",
    right_on="CNPJ_CLIENTE",
    indicator=True
)


validar_clientes = dados_clientes

validar_clientes["Validação"] = validar_clientes.apply(
    lambda case: "Divergente" if case["CNPJ_BANCO"] != case["CNPJ_CLIENTE"]
    else "Correto",
    axis = 1
)


# In[19]:


qtde_correto_01, qtde_divergente_01 = contagem_validacao(validar_clientes)
validar_clientes = observacao_validacao(validar_clientes, qtde_correto_01, qtde_divergente_01)

validar_clientes = colunas_finais_validacao(
    validar_clientes,
    ["CODIGOOFERTA", "CODIGOEMPRESA", "DESCRICAOEMPRESA", "CNPJ_BANCO", "CNPJ_CLIENTE", "Empresa",
     "Validação", "Observação"]
)