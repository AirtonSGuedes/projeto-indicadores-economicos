# 📊 Brazilian Macroeconomic Indicators - End-to-End Analytics Pipeline

![Power BI](https://img.shields.io/badge/Power_BI-F2C811?style=for-the-badge&logo=powerbi&logoColor=black)
![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Pandas](https://img.shields.io/badge/Pandas-150458?style=for-the-badge&logo=pandas&logoColor=white)
![Git](https://img.shields.io/badge/Git-F05032?style=for-the-badge&logo=git&logoColor=white)

Pipeline automatizado de Engenharia e Análise de Dados que realiza a ingestão, tratamento e modelagem dos principais indicadores econômicos oficiais do Banco Central do Brasil (SGS API), disponibilizando um Dashboard Executivo interativo no Power BI para suporte à tomada de decisão financeira.

---

## 🏛️ Arquitetura da Solução

[ API REST do BACEN ] 
          │
          ▼  (Requests & REST API / Python 3)
[ etl_bacen.py ] ➔ Extração, Limpeza, Normalização & Tipagem Decimal (Pandas)
          │
          ▼
[ indicadores_economicos_raw.csv ] ➔ Camada de Staging / Armazenamento Relacional
          │
          ▼  (Power Query & DAX / Power BI)
[ Dashboard Executivo ] ➔ Medidas Dinâmicas (VAR/CALCULATE), Filtros Temporais e Design UI/UX

---

## 📈 Indicadores Monitorados

O pipeline consome dados atualizados diretamente das séries temporais do Sistema Gerenciador de Séries Temporais (SGS) do BACEN:

| Indicador | Série SGS | Unidade | Descrição |
| :--- | :---: | :---: | :--- |
| **Taxa Selic** | 432 | % a.a. | Taxa básica de juros definida pelo COPOM |
| **IPCA** | 433 | Var. % mensal | Índice oficial da inflação no Brasil |
| **Dólar PTAX** | 10813 | R$ | Cotação oficial diária de venda do Dólar Comercial |
| **IBC-Br** | 24363 | Índice | Índice de Atividade Econômica do Banco Central (prévia do PIB) |

---

## 🛠️ Tecnologias e Conceitos Aplicados

* **Python 3:** Ingestão de APIs REST (`requests`), manipulação e estruturação de dados (`pandas`), gestão de datas e tratamento de erros.
* **Power Query (M):** Divisão de colunas concatenadas, tratamento de tipos de dados e configuração de delimitadores.
* **Power BI & DAX:**
  * Uso avançado de variáveis (`VAR ... RETURN`) para otimização do contexto de cálculo.
  * Resolução de conflitos de contexto com `CALCULATE`, `ALL`, `REMOVEFILTERS` e `MAX`.
  * Formatação condicional e dynamic measures para prevenção de agregações incorretas (Soma vs. Média / Último valor).
* **UI/UX Design Corporativo:** Containerização visual (Card design), sombras suaves, paleta de cores executiva (Navy Blue & Slate Gray) e ergonomia visual.

---

## 💻 Estrutura do Projeto

├── etl_bacen.py                   # Script Python de extração e tratamento inicial de dados
├── indicadores_economicos_raw.csv  # Dataset gerado após o processo de ETL
├── dashboard.pbix                 # Arquivo do relatório e modelo de dados no Power BI
└── README.md                      # Documentação completa do projeto

---

## 🚀 Como Executar o Projeto

### 1. Pré-requisitos
* **Python 3.10+** instalado.
* **Power BI Desktop** instalado.

### 2. Passo a Passo

1. **Clonar o repositório:**
   git clone https://github.com/SEU_USUARIO/projeto-indicadores-economicos.git
   cd projeto-indicadores-economicos

2. **Instalar as dependências do Python:**
   pip install pandas requests

3. **Executar o pipeline de extração (ETL):**
   python etl_bacen.py

4. **Abrir e Atualizar o Dashboard:**
   * Abra o arquivo `dashboard.pbix` no **Power BI Desktop**.
   * Na guia **Página Inicial**, clique em **Atualizar** para carregar os dados mais recentes do CSV.

---

## 👤 Autor

**Airton Guedes**  
*Projeto focado em Engenharia e Análise de Dados Financeiros e Macroeconômicos.*