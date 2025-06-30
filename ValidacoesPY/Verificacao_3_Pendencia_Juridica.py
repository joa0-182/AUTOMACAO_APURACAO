#!/usr/bin/env python
# coding: utf-8

# In[7]:


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
from carregar_arquivos_base import dados_clientes_pendencia_juridica_CLIENTE


# ### 3. Verificar se há pendências Jurídicas ou financeiras no Canal
# 
# Verifica se os CNPJ do arquivo "Pendentes Juridicamente CLIENTE" onde mostra todos os clientes que tem pendências fincaceira com o CLIENTE de apuração, está participando da Oferta.
# 

# In[3]:


sql = conecta_banco("ODBC Driver 17 for SQL Server", "seu servidor", "AGRO", None, None, "SIM")
codigo_oferta = 2


# In[9]:


dados_clientes_banco = pd.read_sql(
    f"""
  SELECT DISTINCT
	       OFE.CODIGOOFERTA,
	       OFE.CODIGOEMPRESA,
		     EMP.DESCRICAOEMPRESA,
         EMP.CNPJ
    FROM PRODUTO_OFERTA OFE
   INNER JOIN EMPRESA EMP
		  ON OFE.CODIGOEMPRESA = EMP.CODIGOEMPRESA
   WHERE CODIGOOFERTA = {codigo_oferta}

    """, sql
)


# In[17]:


dados_clientes_banco = dados_clientes_banco.rename(columns={"CNPJ": "CNPJ_BANCO"})
dados_clientes_pendencia_juridica_CLIENTE = dados_clientes_pendencia_juridica_CLIENTE.rename(columns={"CNPJ": "CNPJ_CLIENTE"})

dados_clientes = pd.merge(
    dados_clientes_banco[["CODIGOOFERTA", "CODIGOEMPRESA", "DESCRICAOEMPRESA", "CNPJ_BANCO"]],
    dados_clientes_pendencia_juridica_CLIENTE[["CNPJ_CLIENTE", "DESCRICAOEMPRESA"]],
    how="left",
    left_on="CNPJ_BANCO",
    right_on="CNPJ_CLIENTE",
    indicator=True
)


validar_clientes_pendencia = dados_clientes

validar_clientes_pendencia["Validação"] = validar_clientes_pendencia.apply(
    lambda case: "Divergente" if case["CNPJ_BANCO"] == case["CNPJ_CLIENTE"]
    else "Correto",
    axis = 1
)


# In[18]:


# Contagem "Correta" e "Divergente"
qtde_correto_03, qtde_divergente_03 = contagem_validacao(validar_clientes_pendencia)
validar_clientes_pendencia = observacao_validacao(validar_clientes_pendencia, qtde_correto_03, qtde_divergente_03)

validar_clientes_pendencia = colunas_finais_validacao(
    validar_clientes_pendencia,
    ["CODIGOOFERTA", "CODIGOEMPRESA", "DESCRICAOEMPRESA_x", "CNPJ_BANCO", "CNPJ_CLIENTE", "DESCRICAOEMPRESA_y",
     "Validação", "Observação"]
)