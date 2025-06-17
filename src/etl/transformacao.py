import pandas as pd  

def substituir_na(df, columns, value): # Função para substituir valores em branco de uma coluna
    df[columns] = df[columns].fillna(value)
    return df
    
def substituir_info(df, columns, old_value, new_value): # Função para substituir um valor específico por outro
    df[columns] = df[columns].replace(old_value, new_value)
    return df

def convert_to_str(df,columns):
    df[columns] = df[columns].astype(str)
    return df

def convert_to_date(df, columns, format='%d-%m-%Y', errors='coerce'):
    for column in columns:
        df[column] = pd.to_datetime(df[column], errors=errors)  # Converte a coluna para datetime
    return df  # Mantém as colunas como datetime

def convert_to_int(df, columns):
    df[columns] = df[columns].astype('Int64')
    return df

def convert_to_float(df, columns):
    df[columns] = df[columns].astype('float')
    return df

import pandas as pd

def extrair (df, coluna_origem, nova_coluna, separador="-", indice=1):
    """
    Extrai uma parte de texto de uma coluna com base em um separador e cria uma nova coluna.

    Parâmetros:
    - df: DataFrame original
    - coluna_origem: nome da coluna de onde o texto será extraído
    - nova_coluna: nome da nova coluna a ser criada
    - separador: caractere ou string usada para dividir o texto (padrão: "-")
    - indice: posição da parte a ser extraída (0 para primeira, 1 para segunda, etc.)

    Retorna:
    - DataFrame com a nova coluna adicionada
    """
    df[nova_coluna] = df[coluna_origem].str.split(separador).str[indice].str.strip()
    return df


