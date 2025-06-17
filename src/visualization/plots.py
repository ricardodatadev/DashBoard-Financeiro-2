import plotly.express as px 
import streamlit as st 


# --------------------- FUNÇÕES DE PLOTAGEM ---------------------
def plot_histogram(data, column, title, theme):
    try:
        fig = px.histogram(data, x=column, title=title, template=theme)
        st.plotly_chart(fig, use_container_width=True)
    except Exception as e:
        st.error(f"Erro ao gerar histograma de {column}: {e}")


def plot_box(data, column, title, theme):
    try:
        fig = px.box(data, y=column, title=title, template=theme)
        st.plotly_chart(fig, use_container_width=True)
    except Exception as e:
        st.error(f"Erro ao gerar box plot de {column}: {e}")

def plot_bar(data, x, y, title, theme, color_sequence=None):
    try:
        fig = px.bar(
            data,
            x=x,
            y=y,
            title=title,
            template=theme,
            color_discrete_sequence=color_sequence  # adiciona aqui o parâmetro de cor
        )
        st.plotly_chart(fig, use_container_width=True)
    except Exception as e:
        st.error(f"Erro ao gerar gráfico de barras: {e}")

        
        
def plot_horizontal_bar(data, y, x, title, theme, color=None, color_sequence=None):
    try:
        fig = px.bar(
            data,
            y=y,
            x=x,
            title=title,
            template=theme,
            orientation='h',
            color_discrete_sequence=color_sequence  # lista de cores para categorias
        )
        if color:
            fig.update_traces(marker_color=color)  # cor única para todas as barras
        
        st.plotly_chart(fig, use_container_width=True)
    except Exception as e:
        st.error(f"Erro ao gerar gráfico de barras horizontal: {e}")



def plot_pie(data, names, title, theme):
    try:
        fig = px.pie(data, names=names, title=title, template=theme)
        st.plotly_chart(fig, use_container_width=True)
    except Exception as e:
        st.error(f"Erro ao gerar gráfico de pizza: {e}")
        
def plot_donut(data, names, title, theme, color=None, color_sequence=None):
    try:
        fig = px.pie(
            data,
            names=names,
            title=title,
            template=theme,
            hole=0.5,
            color_discrete_sequence=color_sequence  # aceita lista de cores
        )
        if color:
            # Se quiser uma cor única para todas as fatias (não usual para donut, mas possível)
            fig.update_traces(marker=dict(colors=[color] * len(data)))

        st.plotly_chart(fig, use_container_width=True)
    except Exception as e:
        st.error(f"Erro ao gerar gráfico de rosca: {e}")



def plot_scatter(data, x, y, title, theme):
    try:
        fig = px.scatter(data, x=x, y=y, title=title, template=theme)
        st.plotly_chart(fig, use_container_width=True)
    except Exception as e:
        st.error(f"Erro ao gerar gráfico de dispersão: {e}")

def plot_corr_heatmap(data, num_cols, theme):
    try:
        corr_matrix = data[num_cols].corr()
        fig = px.imshow(corr_matrix, text_auto=True, title="Matriz de Correlação", template=theme)
        st.plotly_chart(fig, use_container_width=True)
    except Exception as e:
        st.error(f"Erro ao gerar heatmap de correlação: {e}")
        
  
  
# FUNÇÃO DE PLOTAGEM PARA COMPARAR MULTIPLOS:
      
def plot_bar_comparativo_long(data, x, y, color, title, theme, color_sequence=None):
    try:
        fig = px.bar(
            data, 
            x=x, 
            y=y, 
            color=color,
            barmode='group',
            title=title, 
            template=theme,
            color_discrete_sequence=color_sequence  # aqui passa as cores, se vier
        )
        st.plotly_chart(fig, use_container_width=True)
        return fig
    except Exception as e:
        st.error(f"Erro ao gerar gráfico de barras comparativas: {e}")
        return None

       
