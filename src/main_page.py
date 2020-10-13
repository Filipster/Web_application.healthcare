import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

def body(df):

    st.title('DATAFLOW - PRAS analysis')

    st.header('Cases per Doctor Speciality')
    _build_hbar_chart(df, ['PROF_ESP_ATE'])    

    st.subheader('Every chart below will be filtered by selected speciality')
    speciality = st.selectbox(label='Choose a speciality', options=df['PROF_ESP_ATE'].unique())

    st.header('1 - Doctor Speciality VS Cases per Unit')
    _build_vbar_chart(df[df['PROF_ESP_ATE'] == speciality], ['ENT_DES_TIP_EST'])

    st.header('2 - Doctor Speciality VS Cases per Operative Unit')
    _build_hbar_chart(df[df['PROF_ESP_ATE'] == speciality], ['ENT_DES_CANT'])

    st.header('3 - Pacients Ethnicities')
    _build_hbar_chart(df[df['PROF_ESP_ATE'] == speciality], ['PCTE_AUTID_ETN'])

    st.header('4 - Priority Groups Distribution')
    _build_pie_chart(df[df['PROF_ESP_ATE'] == speciality])



def _build_vbar_chart(data, fields):
    """Build chart and return its plot."""
    sns.set_palette('rocket')
    labels = list(data[fields[0]].value_counts().keys())
    lbl_values = list(data[fields[0]].value_counts().values)

    
    fig, ax = plt.subplots(figsize=(15, 7))
    
    ax.bar(labels, lbl_values)
    ax.set_xlabel(fields[0])
    ax.set_ylabel('quantity')

    for lbl in enumerate(lbl_values):
        ax.text(lbl[0], lbl[1] + 100, lbl[1])
    
    return st.pyplot(fig)

def _build_hbar_chart(data, fields):
    """Build chart and return its plot."""
    sns.set_palette('rocket')
    labels = list(data[fields[0]].value_counts().keys())
    lbl_values = list(data[fields[0]].value_counts().values)

    
    fig, ax = plt.subplots(figsize=(15, 7))
    
    ax.barh(labels, lbl_values)
    ax.set_ylabel(fields[0])
    ax.set_xlabel('quantity')

    for lbl in enumerate(lbl_values):
        ax.text(lbl[1] + 100, lbl[0], lbl[1])
    
    return st.pyplot(fig)

def _build_pie_chart(df):
    """Build pie chart from priority groups."""
    sns.set_palette('rocket')

    cols = ['PCTE_GRP_PRI_Embarazadas',
       'PCTE_GRP_PRI_Discapacidad', 'PCTE_GRP_PRI_Assedio_Sexual_Trabajo',
       'PCTE_GRP_PRI_Violencia_Psicologica', 'PCTE_GRP_PRI_Violencia_Sexual',
       'PCTE_GRP_PRI_Violencia_Fisica', 'PCTE_GRP_PRI_Maltrato_Infantil',
       'PCTE_GRP_PRI_Enfermidades_Catastroficas',
       'PCTE_GRP_PRI_Desastres_Naturales',
       'PCTE_GRP_PRI_Desastres_Antropogenicos', 'PCTE_GRP_PRI_Penitenciarios']

    labels = []
    lbl_values = []
    exploding = [0, 0.1, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    for col in cols:
        labels.append(col[13:])
        lbl_values.append(df[col].sum())
    
    fig, ax = plt.subplots(figsize=(12, 12))
    
    ax.pie(lbl_values, labels=labels, explode=exploding, startangle=45)
    plt.legend(loc='lower right')
    
    return st.pyplot(fig)
