from datetime import datetime, timedelta
import sys
import pandas as pd
import requests

# Força o terminal do VS Code a utilizar UTF-8
if sys.stdout.encoding != "utf-8":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass

# Cabeçalhos HTTP para simular requisição de um navegador comum (evita erro 406/bloqueio)
HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/120.0.0.0 Safari/537.36"
    ),
    "Accept": "application/json",
}

# Dicionário de séries do Banco Central do Brasil (SGS)
SERIES_BACEN = {
    432: "Taxa Selic (% a.a.)",
    433: "IPCA (Var. % mensal)",
    10813: "Dolar PTAX (Venda R$)",
    24363: "IBC-Br (Atividade Economica)",
}


def buscar_dados_bacen(
    codigo_serie, nome_indicador, data_inicial="01/01/2020"
):
    """Busca dados de uma serie temporal na API do Banco Central do Brasil (SGS)."""
    # URL filtrando a data inicial para acelerar o download e evitar timeout
    url = (
        f"https://api.bcb.gov.br/dados/serie/bcdata.sgs.{codigo_serie}/dados"
        f"?formato=json&dataInicial={data_inicial}"
    )

    print(f"[ETL] Coletando dados: {nome_indicador} (Serie {codigo_serie})...")

    try:
        response = requests.get(url, headers=HEADERS, timeout=30)
        response.raise_for_status()

        dados_json = response.json()
        if not dados_json:
            print(f"[AVISO] Nenhum dado retornado para a serie {codigo_serie}.")
            return pd.DataFrame()

        df = pd.DataFrame(dados_json)

        # Padronização e conversão de tipos
        df["data"] = pd.to_datetime(df["data"], format="%d/%m/%Y")
        df["valor"] = df["valor"].astype(float)
        df["codigo_serie"] = codigo_serie
        df["indicador"] = nome_indicador

        return df

    except Exception as e:
        print(f"[ERRO] Falha ao coletar serie {codigo_serie}: {e}")
        return pd.DataFrame()


# 1. Executar a extração para todas as séries selecionadas
lista_dfs = []
for codigo, nome in SERIES_BACEN.items():
    df_temp = buscar_dados_bacen(codigo, nome)
    if not df_temp.empty:
        lista_dfs.append(df_temp)

# 2. Consolidar os datasets
if lista_dfs:
    df_final = pd.concat(lista_dfs, ignore_index=True)

    # 3. Diagnóstico dos dados
    print("\n[OK] Extracao concluida com sucesso!")
    print(f"Dimensoes totais: {df_final.shape}")
    print(f"Valores nulos:\n{df_final.isnull().sum()}")
    print("\n--- Primeiras Linhas ---")
    print(df_final.head())

    # 4. Salvar CSV tratado temporário
    df_final.to_csv(
        "indicadores_economicos_raw.csv", index=False, encoding="utf-8"
    )
    print(
        "\n[SALVO] Arquivo 'indicadores_economicos_raw.csv' gerado com sucesso!"
    )
else:
    print("\n[ERRO CRITICO] Nao foi possivel extrair nenhuma serie da API.")

    from datetime import datetime
import sys
import pandas as pd
import requests

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/120.0.0.0 Safari/537.36"
    ),
    "Accept": "application/json",
}

SERIES_BACEN = {
    432: ("Taxa Selic (% a.a.)", "01/01/2022"),
    433: ("IPCA (Var. % mensal)", "01/01/2022"),
    10813: ("Dolar PTAX (Venda R$)", "01/01/2022"),
    24363: ("IBC-Br (Atividade Economica)", "01/01/2022"),
}


def buscar_dados_bacen(codigo_serie, nome_indicador, data_inicial):
    url = (
        f"https://api.bcb.gov.br/dados/serie/bcdata.sgs.{codigo_serie}/dados"
        f"?formato=json&dataInicial={data_inicial}"
    )
    try:
        response = requests.get(url, headers=HEADERS, timeout=30)
        response.raise_for_status()
        df = pd.DataFrame(response.json())
        df["data"] = pd.to_datetime(df["data"], format="%d/%m/%Y")
        df["valor"] = df["valor"].astype(float)
        df["codigo_serie"] = codigo_serie
        df["indicador"] = nome_indicador
        return df
    except Exception:
        return pd.DataFrame()


lista_dfs = [
    buscar_dados_bacen(cod, nome, dt)
    for cod, (nome, dt) in SERIES_BACEN.items()
]
df_final = pd.concat([d for d in lista_dfs if not d.empty], ignore_index=True)

# Garante que os números salvos no CSV estarão no formato correto
df_final.to_csv("indicadores_economicos_raw.csv", index=False, encoding="utf-8")
print(
    "✅ CSV Atualizado com Sucesso! Agora clique em 'Atualizar' no Power BI."
)