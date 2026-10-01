import sqlite3
import pandas as pd

DB_NAME = "indicadores_financeiros.db"
CSV_FILE = "indicadores_economicos_raw.csv"

# 1. Carregar os dados limpos do CSV
df = pd.read_csv(CSV_FILE)
df["data"] = pd.to_datetime(df["data"])

# 2. Conectar ao Banco de Dados SQLite
conn = sqlite3.connect(DB_NAME)
cursor = conn.cursor()

# 3. Criar as tabelas do Modelo Dimensional (Star Schema)

# Tabela Dimensão: dim_indicador
cursor.execute(
    """
CREATE TABLE IF NOT EXISTS dim_indicador (
    id_indicador INTEGER PRIMARY KEY,
    nome_indicador TEXT NOT NULL,
    unidade_medida TEXT
)
"""
)

# Tabela Dimensão: dim_tempo
cursor.execute(
    """
CREATE TABLE IF NOT EXISTS dim_tempo (
    sk_data INTEGER PRIMARY KEY,
    data_completa TEXT NOT NULL,
    ano INTEGER,
    mes INTEGER,
    trimestre INTEGER,
    nome_mes TEXT
)
"""
)

# Tabela Fato: fato_indicadores
cursor.execute(
    """
CREATE TABLE IF NOT EXISTS fato_indicadores (
    id_fato INTEGER PRIMARY KEY AUTOINCREMENT,
    sk_data INTEGER NOT NULL,
    id_indicador INTEGER NOT NULL,
    valor REAL NOT NULL,
    FOREIGN KEY (sk_data) REFERENCES dim_tempo (sk_data),
    FOREIGN KEY (id_indicador) REFERENCES dim_indicador (id_indicador)
)
"""
)

print("[SQL] Estrutura Star Schema verificada/criada.")

# 4. Povoar dim_indicador
dim_indicador_data = [
    (432, "Taxa Selic", "% a.a."),
    (433, "IPCA", "Var. % mensal"),
    (10813, "Dolar PTAX", "R$"),
    (24363, "IBC-Br", "Indice"),
]

cursor.executemany(
    """
INSERT OR REPLACE INTO dim_indicador (id_indicador, nome_indicador, unidade_medida)
VALUES (?, ?, ?)
""",
    dim_indicador_data,
)

# 5. Povoar dim_tempo
datas_unicas = df["data"].drop_duplicates()
dim_tempo_df = pd.DataFrame({"data_completa": datas_unicas})
dim_tempo_df["sk_data"] = (
    dim_tempo_df["data_completa"].dt.strftime("%Y%m%d").astype(int)
)
dim_tempo_df["ano"] = dim_tempo_df["data_completa"].dt.year
dim_tempo_df["mes"] = dim_tempo_df["data_completa"].dt.month
dim_tempo_df["trimestre"] = dim_tempo_df["data_completa"].dt.quarter
dim_tempo_df["nome_mes"] = dim_tempo_df["data_completa"].dt.strftime("%b")
dim_tempo_df["data_completa"] = dim_tempo_df["data_completa"].dt.strftime(
    "%Y-%m-%d"
)

dim_tempo_df.to_sql("dim_tempo", conn, if_exists="replace", index=False)

# 6. Povoar fato_indicadores
df["sk_data"] = df["data"].dt.strftime("%Y%m%d").astype(int)
df_fato = df[["sk_data", "codigo_serie", "valor"]].rename(
    columns={"codigo_serie": "id_indicador"}
)
df_fato.to_sql("fato_indicadores", conn, if_exists="replace", index=False)

# 7. Criar View Executiva
cursor.execute(
    """
CREATE VIEW IF NOT EXISTS vw_indicadores_executivo AS
SELECT 
    t.data_completa AS data,
    t.ano,
    t.mes,
    t.trimestre,
    i.nome_indicador,
    i.unidade_medida,
    f.valor
FROM fato_indicadores f
JOIN dim_tempo t ON f.sk_data = t.sk_data
JOIN dim_indicador i ON f.id_indicador = i.id_indicador
"""
)

conn.commit()
conn.close()

print(
    "[OK] Banco de Dados 'indicadores_financeiros.db' e View executiva criados com sucesso!"
)