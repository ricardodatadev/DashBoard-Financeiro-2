import pandas as pd
import time

import pandas as pd


def contar_agrupando(df: pd.DataFrame, contar_coluna: str, agrupado_por: str) -> pd.DataFrame:
    """
    Conta quantas vezes cada valor de 'contar_coluna' aparece dentro de cada grupo de 'agrupado_por'.

    Parâmetros:
    - df: DataFrame de entrada.
    - contar_coluna: Coluna cujos valores serão contados.
    - agrupado_por: Coluna usada para fazer o agrupamento.

    Retorno:
    - DataFrame com as contagens por grupo.
    """
    return (
        df.groupby(agrupado_por)[contar_coluna]
        .count()
        .reset_index(name=f'contagem_{contar_coluna}')
    )





def contar_total(df: pd.DataFrame, coluna: str) -> int:
    """
    Retorna o total de registros não nulos na coluna.
    """
    return df[coluna].count()




def somar_total(df: pd.DataFrame, coluna: str) -> int:
    """
    Retorna o total de registros não nulos na coluna.
    """
    return df[coluna].sum()




def somar_agrupando(df: pd.DataFrame, coluna: str, agrupado_por: str = None) -> pd.DataFrame:
    """
    Soma valores de uma coluna, com ou sem agrupamento.
    """
    if agrupado_por:
        return df.groupby(agrupado_por)[coluna].sum().reset_index(name=f'soma_{coluna}')
    else:
        total = df[coluna].sum()
        return pd.DataFrame({f'soma_{coluna}': [total]})


def media(df: pd.DataFrame, coluna: str, agrupado_por: str = None) -> pd.DataFrame:
    """
    Calcula a média de uma coluna, com ou sem agrupamento.
    """
    if agrupado_por:
        return df.groupby(agrupado_por)[coluna].mean().reset_index(name=f'media_{coluna}')
    else:
        media_valor = df[coluna].mean()
        return pd.DataFrame({f'media_{coluna}': [media_valor]})



# CALCULOS COM CONDIÇÕES:



def somar_total(df: pd.DataFrame, coluna: str) -> int:
    """
    Retorna o total de registros não nulos na coluna.
    """
    return df[coluna].sum()




# MOSTRAR OS DADOS DA COLUNA X, SOMENTE ONDE NA COLUNA Y ESTIVER EM BRANCO :

def isnull(df: pd.DataFrame, coluna_principal: str, coluna_condicional: str) -> int:
    df_filtrado = df[df[coluna_condicional].isna()]
    if not df_filtrado.empty:
        return df_filtrado[[coluna_principal]]
    else:
        return pd.DataFrame({coluna_principal: []})  # retorna DataFrame vazio com a mesma coluna
    



# MOSTRAR OS DADOS DA COLUNA X, SOMENTE ONDE NA COLUNA Y NÃO ESTIVER EM BRANCO :

def notnull(df: pd.DataFrame, coluna_principal: str, coluna_condicional: str) -> int:
    df_filtrado = df[df[coluna_condicional].notna()]
    if not df_filtrado.empty:
        return df_filtrado[[coluna_principal]]
    else:
        return pd.DataFrame({coluna_principal: []})  # retorna DataFrame vazio com a mesma coluna



# APLICANDO MAIS DE UMA CONDIÇÃO: 

def contar_com_condicoes(
    df: pd.DataFrame,
    coluna_principal: str,
    condicoes: dict,
    modo: str = "and"
) -> pd.DataFrame:
    """
    Conta os valores da coluna especificada, aplicando múltiplas condições de nullidade em outras colunas,
    e retorna o resultado dentro de um DataFrame.

    Parâmetros:
    - df: DataFrame de origem.
    - coluna_principal: Nome da coluna que será contada (ex: "OS").
    - condicoes: Dicionário no formato {coluna: 'isnull' ou 'notnull'}.
    - modo: 'and' ou 'or' para combinar as condições.

    Retorno:
    - DataFrame com uma linha e uma coluna 'Contagem' contendo a contagem.
    """
    conds = []

    for coluna, valor in condicoes.items():
        if valor == "isnull":
            conds.append(df[coluna].isna())
        elif valor == "notnull":
            conds.append(df[coluna].notna())
        else:
            raise ValueError("Condição inválida! Use apenas 'isnull' ou 'notnull'.")

    if not conds:
        df_filtrado = df
    elif modo == "and":
        filtro = conds[0]
        for cond in conds[1:]:
            filtro &= cond
        df_filtrado = df[filtro]
    elif modo == "or":
        filtro = conds[0]
        for cond in conds[1:]:
            filtro |= cond
        df_filtrado = df[filtro]
    else:
        raise ValueError("Modo deve ser 'and' ou 'or'")

    contagem = df_filtrado[coluna_principal].count()
    return pd.DataFrame({"Contagem": [contagem]})




# FUNÇÃO PARA GERAR UMA NOVA COLUNA CALCULADA COM BASE NOS VALORES ENTRE DUAS COLUNAS:

def coluna_calculada(df, nova_coluna, coluna1, coluna2, operacao):
    """
    Cria uma nova coluna em um DataFrame com base em uma operação entre duas colunas.

    Parâmetros:
    - df: DataFrame do Pandas.
    - nova_coluna: nome da nova coluna a ser criada (string).
    - col1: nome da primeira coluna (string).
    - col2: nome da segunda coluna (string).
    - operacao: operação desejada ('soma', 'subtracao', 'multiplicacao', 'divisao').

    Retorno:
    - O DataFrame com a nova coluna adicionada.
    """
    if operacao == '+':
        df[nova_coluna] = df[coluna1] + df[coluna2]
    elif operacao == '-':
        df[nova_coluna] = df[coluna1] - df[coluna2]
    elif operacao == '*':
        df[nova_coluna] = df[coluna1] * df[coluna2]
    elif operacao == '/':
        # Evita divisão por zero
        df[nova_coluna] = df[coluna1] / df[coluna2].replace(0, float('nan'))
    else:
        raise ValueError("Operação inválida. Use: 'soma', 'subtracao', 'multiplicacao' ou 'divisao'")
    
    return df




# FUNÇÃO PARA CALCULAR PORCENTAGEM:

def calcular_porcentagem(df, nova_coluna, numerador, denominador, multiplicar_por_100=True):
    """
    Cria uma nova coluna com o resultado da divisão entre duas colunas, com opção de porcentagem.

    Parâmetros:
    - df: DataFrame do Pandas.
    - nova_coluna: Nome da nova coluna a ser criada.
    - numerador: Nome da coluna numerador.
    - denominador: Nome da coluna denominador.
    - multiplicar_por_100: Se True, o resultado será multiplicado por 100 (valor em %).

    Retorno:
    - O DataFrame com a nova coluna calculada.
    """
    resultado = df[numerador] / df[denominador].replace(0, pd.NA)  # Evita divisão por zero
    if multiplicar_por_100:
        resultado *= 100
    df[nova_coluna] = resultado.astype(float).round(2)
    return df

