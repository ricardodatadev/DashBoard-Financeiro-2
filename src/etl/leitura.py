import pandas as pd
import logging


logging.basicConfig(level=logging.INFO, format='%(message)s')

def inspecionar_arquivo(df: pd.DataFrame) -> pd.DataFrame:
    logging.info("Carregando DataFrame...")
    
    logging.info("Visualização Geral do DataFrame:")
    logging.info(f"\n{df}")
    
    logging.info("Carregando somente as colunas...")
    
    logging.info("Colunas Presentes:")
    logging.info(f"{df.columns.tolist()}")
    
    logging.info("Analisando informações em branco...")
    
    logging.info("Quantidade de informações em branco em cada coluna:")
    logging.info(f"\n{df.isna().sum()}")
    
    logging.info("Analisando os tipos de dados de cada coluna...")
    
    logging.info("Tipos de Dados de cada coluna:")
    logging.info(f"\n{df.dtypes}")
    
    logging.info("Quantidade de linhas e colunas:")
    logging.info(f"{df.shape}")
    
    logging.info("Resumo:")
    df.info()
    logging.info("Resumo exibido acima, seguindo adiante...")
    
    logging.info("Removendo linhas em branco...")
    df = df.dropna(how="all")
    
    logging.info("Quantidade de linhas e colunas após remoção:")
    logging.info(f"{df.shape}")
    
    logging.info("Analisando informações em branco novamente...")
    
    logging.info("Quantidade de informações em branco em cada coluna:")
    logging.info(f"\n{df.isna().sum()}")
    
    logging.info("Finalizando função, próximo ao return...")
    
    return df







def open_file_excel(arquivo): 
    return pd.read_excel(arquivo)