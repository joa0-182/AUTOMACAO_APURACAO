import pandas as pd

from arquivos_base import arquivo_validacao_excel
from arquivos_base import data


# Arquivos das validações
from ValidacoesPY.Verificacao_1_CNPJ import validar_clientes, qtde_divergente_01
from ValidacoesPY.Verificacao_2_Somente_ProdutosOferta import validar_produtos, qtde_divergente_02
from ValidacoesPY.Verificacao_3_Pendencia_Juridica import validar_clientes_pendencia, qtde_divergente_03


status_item = {
    "Verificar CNPJ": qtde_divergente_01,
    "Verificar se os Produtos estão cadastrados dentro da Oferta.": qtde_divergente_02,
    "Pendência Júridica": qtde_divergente_03,
}

status_text = [
    "Correto",
    "Divergente"
]

validacao = []
status = []
qtde_divergente = []


for item, pendencia in status_item.items():
    if pendencia > 0:
        validacao.append(item)
        status.append(status_text[1])
        qtde_divergente.append(pendencia)
    else:
        validacao.append(item)
        status.append(status_text[0])
        qtde_divergente.append(pendencia)

resumo_validacao = pd.DataFrame({

    "Apuração": validacao,
    "Status": status,
    "Qtde. Divergente": qtde_divergente
    
    })


try:
    with pd.ExcelWriter(f"{arquivo_validacao_excel}") as writer:
        #0
        resumo_validacao.to_excel(
            writer,
            sheet_name="Resumo Apuração",
            index = False
        )
        #1
        validar_clientes.to_excel(
            writer,
            sheet_name="Verificar CNPJ",
            index = False
        )
        #2
        validar_produtos.to_excel(
            writer,
            sheet_name="Validar Produtos",
            index= False
        )
        #3
        validar_clientes_pendencia.to_excel(
            writer,
            sheet_name="Pendência Júridica",
            index = False
        )


except PermissionError:
    print("Permissão ao gerar o arquivo Excel negada, talvez o arquivo esteja aberto, feche e rode a Apuração Novamente.")

except Exception as erro:
    print(f"Erro: {erro}")
