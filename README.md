# 🤖 Automação de Apuração

---

## 🧠 Conceito

Este projeto simula uma **automação de apuração de dados** enviada por um cliente (fictício) com base em **regras de negócio específicas**, como validação de CNPJs, composição de ofertas, pendências jurídicas, entre outras.

Foi desenvolvido para ser **modular, escalável e de fácil uso**.  
Pode ser adaptado facilmente a **novos clientes**, **novas políticas comerciais** e **regras de apuração específicas**.

✅ **Objetivo principal**: reduzir o tempo de análise manual (que normalmente leva de 1 a 2 dias) para **menos de 15 minutos**, com relatórios automatizados e visuais.

---

## 🗂️ Estrutura do Projeto

```
AUTOMACAO_APURACAO/
├── Arquivos/              <- Arquivos gerados: Excel de Resumo e Word com Laudo Final
├── Bases/                 <- Arquivos externos (enviados pelo cliente)
├── Integracao/            <- Geração dos relatórios finais (.xlsx + .docx)
│   └── Word/              <- Modelo de Word para gerar o laudo da apuração
├── ValidacoesIPYNB/       <- Jupyter Notebooks para validação com visualização dos dados
├── ValidacoesPY/          <- Scripts .py gerados a partir dos notebooks
├── arquivos_base.py       <- Funções auxiliares e definição das bases a serem utilizadas
├── carregar_arquivos_base.py <- Carregamento dos arquivos das bases
├── classificacoes.py      <- Regras de negócio específicas (por cliente, política, etc.)
├── main.ipynb             <- Painel principal de execução e visualização dos resultados
└── Banco/                 <- Scripts para criar o banco de dados e alimentar com dados de teste
```

---

## ✅ Principais Funcionalidades

- Validação automática de múltiplas regras de negócio
- Resumo visual com **checklist** do que está **OK** e do que está **divergente**
- Geração de **relatório final em Excel**
- Geração de **laudo técnico em Word com inteligencia artifical**
- Integração com bancos de dados e arquivos Excel
- Visualização clara via Jupyter Notebook
- Código escalável, pronto para novos clientes e regras

---

## 📊 Exemplo de Saída

### ✔️ Checklist de Validações

#### Painel de resumo main.ipynb apareceria todas as validações.

<p align="center">
  <img src="https://github.com/user-attachments/assets/47d915fd-556f-4a60-8353-5e80155cd96b" width="600">
</p>

#### Arquivos Gerados

<p align="center">
  <img src="https://github.com/user-attachments/assets/eaa73e80-ae5f-41f5-a39f-867aaae275ba" width="600">
</p>

#### Arquivo Excel

<p align="center">
  <img src="https://github.com/user-attachments/assets/c0e3eb40-9e74-4b74-bd13-bfae59c2b44d" width="600">
</p>

##### Exemplo

<p align="center">
  <img src="https://github.com/user-attachments/assets/c51feca2-1193-47e4-90e4-5ea87177294d" width="600">
</p>

#### Laudo

<p align="center">
  <img src="https://github.com/user-attachments/assets/09b0196b-e243-4ddf-8bea-36f61a833317" width="600">
</p>


---

## 🛠️ Tecnologias utilizadas

- Python 3.10+
- Pandas
- openpyxl / xlsxwriter (para exportar Excel)
- python-docx (para gerar documentos Word)
- Jupyter Notebook
- SQL Server (scripts de criação disponíveis na pasta `/Banco`)

---

## 💾 Como utilizar

1. Clone o repositório:
```bash
git clone https://github.com/seuusuario/automacao_apuracao.git
```

2. Adicione os arquivos do cliente na pasta `/Bases`

3. Execute o painel:
```bash
jupyter notebook main.ipynb
```

Ou, se preferir rodar por script:
```bash
python main.py
```

---

## 🧪 Banco de Teste

Na pasta `/Banco`, você encontra os scripts para:
- Criar o banco de dados
- Popular com dados fictícios
- Realizar testes locais sem necessidade de conexão com sistemas reais

---

## 🚀 Resultado Final

Ao fim da execução, você terá:

- 📊 Arquivo Excel com resumo das validações
- 📄 Documento Word com laudo técnico
- ✅ Redução drástica do tempo de análise (de **2 dias para cerca de 15 minutos** ou menos)

---

## 👥 Público-Alvo

Este projeto foi pensado tanto para:
- **Analistas de Dados**, **Desenvolvedores**, **Auditores**.
- Equipes que precisam de validações constante, diaramente, semanalmente, mensalmente, etc.

---

## 📌 Observação

Este projeto utiliza dados **fictícios** e empresas **inventadas** para fins de simulação e teste.

---

## 📫 Contato

Caso deseje adaptar esse projeto ao seu contexto real, entre em contato:
📧 `joaopedromaria182@gmail.com`

---


