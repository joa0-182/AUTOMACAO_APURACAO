# Funções
from arquivos_base import carregar_arquivo_excel

# Arquivos
from arquivos_base import clientes_oferta, produtos_oferta, clientes_com_pendencia


dados_clientes_oferta_CLIENTE = carregar_arquivo_excel(
    clientes_oferta,
    "CNPJ Participantes Oferta",
    {
        "CNPJ": "str"
    }
)

dados_produtos_oferta_CLIENTE = carregar_arquivo_excel(
    produtos_oferta,
    "Produtos Oferta",
    None
)

dados_clientes_pendencia_juridica_CLIENTE = carregar_arquivo_excel (
    clientes_com_pendencia,
    "Pendentes Juridicamente",
    {
        "CNPJ": "str"
    }
)