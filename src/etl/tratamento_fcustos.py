import sys
import os
sys.path.append(os.path.abspath('../..'))


from src.etl.leitura import open_file_excel, inspecionar_arquivo
from src.etl.limpeza import remove_columns, remove_duplicate, remove_info, remove_infos, remove_na, remover_linhas_superiores, rename_columns
from src.etl.transformacao import extrair

import pandas as pd

pd.set_option('display.max_columns', None)
pd.set_option('display.width', 1000)


def pipeline_tratamento(caminho_entrada):   
    try:
        df = open_file_excel(caminho_entrada)
        df = inspecionar_arquivo(df)
        return df
    except Exception as e: 
        print(f"Erro no pipeline de tratamento: {e}")
        return None


if __name__ == "__main__":
    tratamento_fcustos = pipeline_tratamento("../../data/raw/fcustos.xlsx")
    if tratamento_fcustos is not None:
        print(tratamento_fcustos)
    else: 
        print("Erro ao gerar o arquivo")
