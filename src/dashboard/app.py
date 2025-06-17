import streamlit as st
import pandas as pd
import plotly.express as px
import sys
import os 



# Configuração da página
st.set_page_config(page_title="Dashboard - Financeiro", page_icon=":bar_chart:", layout="wide")
# -------- Caminho para acessar os módulos personalizados ------------
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

def load_css(file_path: str):
    with open(file_path) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# Calcula caminho relativo para o CSS
base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
css_path = os.path.join(base_dir, "styles", "main.css")

load_css(css_path)

from src.etl.tratamento_fcustos import pipeline_tratamento
from src.etl.metricas import contar_total, contar_agrupando, isnull, notnull, contar_com_condicoes, coluna_calculada, calcular_porcentagem, somar_total, somar_agrupando
from src.visualization.plots import plot_bar_comparativo_long, plot_bar, plot_donut, plot_horizontal_bar




# Carrega os dados tratados
df = pipeline_tratamento("data/raw/fcustos.xlsx")

df['Data'] = pd.to_datetime(df['Data'])
df["Mes_Ano"] = df["Data"].dt.to_period("M").astype(str)
df['Mês'] = df['Data'].dt.strftime('%b/%Y')  # exemplo: Jan/2024

# ---- INTERFACE PRINCIPAL ----

st.markdown("""
    <h1 class="dashboard-title">
        📊 Dashboard Financeiro
    </h1>
""", unsafe_allow_html=True)




# ------- SIDEBAR --------
st.sidebar.header("Selecione o Filtro:")

product = st.sidebar.multiselect(
    "Produto:",
    options=df["Produto"].unique(),
    default=[],
    placeholder="Selecione o Produto"
)

category = st.sidebar.multiselect(
    "Categoria:",
    options=df["Categoria"].unique(),
    default=[],
    placeholder="Selecione a Categoria"
)

meses_disponiveis = sorted(df["Mês"].unique())
meses_selecionados = st.sidebar.multiselect(
    "Mês/Ano:",
    options=meses_disponiveis,
    default=[],
    placeholder="Selecione um ou mais meses"
)




# ---- APLICAÇÃO DOS FILTROS ----
df_filtrado = df.copy()

if product:
    df_filtrado = df_filtrado[df_filtrado["Produto"].isin(product)]

if category:
    df_filtrado = df_filtrado[df_filtrado["Categoria"].isin(category)]


if meses_selecionados:
    df_filtrado = df_filtrado[df_filtrado["Mês"].isin(meses_selecionados)]
    
    
st.sidebar.markdown("""
    <div class="sidebar-autor">
        Criado por <b>Ricardo Pereira</b> https://github.com/ricardodatadev
    </div>
""", unsafe_allow_html=True)


# ---- INTERFACE PRINCIPAL ----




#Cabeçalho:

col1, col2, col3, col4 = st.columns(4)


# Total de manutenções

receita = round(somar_total(df_filtrado, coluna="Valor Total Venda"), 2)
titulo_receita = "Receita"
valor_receita = f"R$ {receita:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")

with col1:
    st.markdown(f'''
    <div class="card-metric receita">
      <div class="metric-label">{titulo_receita}</div>
      <div class="metric-value">{valor_receita}</div>
    </div>
    ''', unsafe_allow_html=True)
    

produtos = int(somar_total(df_filtrado, coluna="Quantidade Vendida"))
titulo_produtos = "Qtde. Produtos Vendidos"
valor_produtos = f"{produtos:,}".replace(",", ".")

with col2:
    st.markdown(f'''
    <div class="card-metric produtos">
      <div class="metric-label">{titulo_produtos}</div>
      <div class="metric-value">{valor_produtos}</div>
    </div>
    ''', unsafe_allow_html=True)

custo = round(somar_total(df_filtrado, coluna="Valor Total Custo"), 2)
titulo_custo = "Total Custos"
valor_custo = f"R$ {custo:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")

with col3:
    st.markdown(f'''
    <div class="card-metric custo">
      <div class="metric-label">{titulo_custo}</div>
      <div class="metric-value">{valor_custo}</div>
    </div>
    ''', unsafe_allow_html=True)

despesa = round(somar_total(df_filtrado, coluna="Despesas Gerais"), 2)
titulo_despesa = "Despesas Gerais"
valor_despesa = f"R$ {despesa:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")

with col4:
    st.markdown(f'''
    <div class="card-metric despesa">
      <div class="metric-label">{titulo_despesa}</div>
      <div class="metric-value">{valor_despesa}</div>
    </div>
    ''', unsafe_allow_html=True)


col1, col2, col3, col4 = st.columns(4)


lucro_bruto = receita - custo
titulo_lucro_bruto = "Lucro Bruto"
valor_lucro_bruto = f"R$ {lucro_bruto:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")

with col1:
    st.markdown(f'''
    <div class="card-metric lucro-bruto">
      <div class="metric-label">{titulo_lucro_bruto}</div>
      <div class="metric-value">{valor_lucro_bruto}</div>
    </div>
    ''', unsafe_allow_html=True)


lucro_operacional = receita-custo-despesa
titulo_lucro_operacional = "Lucro Operacional"
valor_lucro_operacional = f"R$ {lucro_operacional:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")

with col2:
    st.markdown(f'''
    <div class="card-metric lucro-operacional">
      <div class="metric-label">{titulo_lucro_operacional}</div>
      <div class="metric-value">{valor_lucro_operacional}</div>
    </div>
    ''', unsafe_allow_html=True)



margem_bruta = lucro_bruto / receita * 100
titulo_margem_bruta = "Margem Bruta"
valor_margem_bruta = f"{margem_bruta:,.2f}%".replace(",", "X").replace(".", ",").replace("X", ".")

with col3:
    st.markdown(f'''
    <div class="card-metric margem-bruta">
      <div class="metric-label">{titulo_margem_bruta}</div>
      <div class="metric-value">{valor_margem_bruta}</div>
    </div>
    ''', unsafe_allow_html=True)


margem_operacional = lucro_operacional / receita * 100
titulo_margem_operacional = "Margem Operacional"
valor_margem_operacional = f"{margem_operacional:,.2f}%".replace(",", "X").replace(".", ",").replace("X", ".")

with col4:
    st.markdown(f'''
    <div class="card-metric margem-operacional">
      <div class="metric-label">{titulo_margem_operacional}</div>
      <div class="metric-value">{valor_margem_operacional}</div>
    </div>
    ''', unsafe_allow_html=True)





# ----------GRÁFICOS------------------

df_resumo = df_filtrado.groupby('Mes_Ano')[['Valor Total Venda', 'Valor Total Custo']].sum().reset_index(). sort_values("Mes_Ano")
df_longo = pd.melt(
    df_resumo,
    id_vars='Mes_Ano',
    value_vars=['Valor Total Venda', 'Valor Total Custo'],
    var_name='Tipo',
    value_name='Valor'
)

df_receita_categoria = somar_agrupando(df=df_filtrado, coluna="Valor Total Venda", agrupado_por="Categoria")

# Cria uma nova coluna no DataFrame com o lucro bruto por linha
df_filtrado["Lucro Bruto"] = df_filtrado["Valor Total Venda"] - df_filtrado["Valor Total Custo"]


df_lucro_categoria = df_filtrado.groupby("Categoria")["Lucro Bruto"].sum().reset_index()

df_despesa_categoria = somar_agrupando(df=df_filtrado, coluna="Despesas Gerais", agrupado_por="Categoria")



col1, col2, = st.columns(2)

with col1: plot_bar_comparativo_long(data=df_longo, x="Mes_Ano", y="Valor", color="Tipo", title="VendaxCusto por Mês", theme="plotly", color_sequence=["#021938", "#f54d37"])
with col2: plot_bar(data=df_receita_categoria, x="Categoria", y="soma_Valor Total Venda", title="Receita por Categoria", theme="plotly", color_sequence=["#021938"])


col1, col2, = st.columns(2)

with col1: plot_donut(data=df_filtrado, names="Categoria", title="Lucro Bruto por Categoria", theme="plotly", color_sequence=["#021938", "#074e47", "#203a13", "#f54d37"])
with col2: plot_horizontal_bar(data=df_despesa_categoria, y="Categoria", x="soma_Despesas Gerais", title="Despesas por Categoria", theme="plotly", color_sequence=["#021938"])








