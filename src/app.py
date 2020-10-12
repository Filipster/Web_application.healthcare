import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from utils import FileReference, hash_file_reference

def main():
     # -------------------------------- Sidebar -------------------------------
    st.sidebar.title('Carregar o conjunto de dados')

    select_type = st.sidebar.selectbox('Escolha a extensão do arquivo', options=[
        'Selecione uma opção', 'csv', 'xlsx', 'txt'
    ])
    
    sep_text_input = st.sidebar.text_input('Informe o separador do arquivo selecionado', value=',')
    encoding_text_input = st.sidebar.text_input('Infome o encoding do arquivo selecionado', value='utf-8')

 
    file = st.sidebar.file_uploader('Uploader do arquivo', type=select_type)
    
    
    # -------------------------- Conteúdo da página principal ----------------
    # Carregando os dados de arquivo
    @st.cache(allow_output_mutation={FileReference: hash_file_reference})
    def read_file_data(file):
        try:
            if file is not None:
                if (select_type == 'csv') | (select_type == 'txt'):
                    df = pd.read_csv(file, sep=sep_text_input, encoding=encoding_text_input)
                    return df
                elif select_type == 'xlsx':
                    df = pd.read_excel(file)
                    return df
        except Exception as e:
            st.markdown(e)

    df = read_file_data(file)
    
    if df is not None:
        st.dataframe(df.columns)
    else:
        st.markdown('Dataflow')

