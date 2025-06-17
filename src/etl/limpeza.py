import pandas as pd  

def remove_columns(df, columns): # Função para remover colunas
    return df.drop(columns=columns, axis=1)
    
def rename_columns(df, columns): # Função para renomear colunas
    return df.rename(columns=columns)  

def remove_na(df, columns): # Função para remover NA de colunas específicas
    return df.dropna(subset=columns)

def remove_info(df, columns, value): # Função para remover uma informação da coluna
    return df[df[columns] != value]

def remove_infos(df, columns, values): # Função para remover mais de uma informação ao mesmo tempo de uma coluna
    return df[~df[columns].isin(values)]


def remove_duplicate(df, subset=None): # Função para remover informações duplicadas de uma coluna 
    return df.drop_duplicates(subset=subset)

def remover_linhas_superiores(df, num_linhas):
    df_modificado = df.iloc[num_linhas:]
    df_modificado = df_modificado.reset_index(drop=True)
    return df_modificado

def strip_spaces(df):
    for col in df.select_dtypes(include='object').columns:
        df[col] = df[col].str.strip()
    return df