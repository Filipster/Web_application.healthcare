import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import numpy as np
import warnings
warnings.filterwarnings('ignore')


def body(df):

    st.title('DATAFLOW - PRAS analysis')

    st.header('Statistics')
    st.markdown('Total of registers in file: **{}**'.format(len(df)))
    st.markdown('% Women: **{:.1f}%**'.format(df.PCTE_SEXO.value_counts(normalize=True)['Mujer'] * 100))
    st.markdown('% Men: **{:.1f}%**'.format(df.PCTE_SEXO.value_counts(normalize=True)['Hombre'] * 100))

    # Cases per Month
    st.header('Cases per Month')
    _df = df.groupby(['ATEMED_MONTH']).agg({'ENT_DES_PARR': 'count'}).reset_index().sort_values(by='ATEMED_MONTH')
    st.markdown('Month with most register: **{}** with **{:.1f}%** of the total appointments'.format(_df.loc[np.argmax(_df.ENT_DES_PARR)][0], (_df.loc[np.argmax(_df.ENT_DES_PARR)][1] / len(df) * 100)))

    labels = list(_df['ATEMED_MONTH'])
    lbl_values = list(_df['ENT_DES_PARR'])
    _build_vbar_chart(labels, lbl_values, 0)

    # build list of months
    months = list(df['ATEMED_MONTH'].unique())
    months.insert(0, 'All Data')
    month_analyzed = st.selectbox(label='Choose a Month to filter further charts', options=months)

    # Priority Group Treatment
    st.header('{} - Priority Appointments'.format(month_analyzed))
    if month_analyzed == 'All Data':
        filter_1 = (df[(df.PCTE_GRP_PRI_QTD > 0)])
        st.markdown('% Priority Group Appointments: **{} - {:.1f}%**'.format(len(filter_1), (len(filter_1) / len(df) * 100)))
    else:
        filter_1 = (df[(df.ATEMED_MONTH == month_analyzed) & (df.PCTE_GRP_PRI_QTD > 0)])
        st.markdown('% Priority Group Appointments: **{} - {:.1f}%**'.format(len(filter_1), (len(filter_1) / len(df[(df.ATEMED_MONTH == month_analyzed)]) * 100)))

    _ = ['PCTE_GRP_PRI_Embarazadas', 'PCTE_GRP_PRI_Discapacidad', 'PCTE_GRP_PRI_Assedio_Sexual_Trabajo',
        'PCTE_GRP_PRI_Violencia_Psicologica', 'PCTE_GRP_PRI_Violencia_Sexual', 'PCTE_GRP_PRI_Violencia_Fisica',
        'PCTE_GRP_PRI_Maltrato_Infantil', 'PCTE_GRP_PRI_Enfermidades_Catastroficas', 'PCTE_GRP_PRI_Desastres_Naturales',
        'PCTE_GRP_PRI_Desastres_Antropogenicos', 'PCTE_GRP_PRI_Penitenciarios']
    tt = filter_1[_].sum().transpose()
    tmp = pd.DataFrame(tt, columns=['t1']).reset_index().sort_values(by='t1', ascending=True)

    labels = list(tmp['index'])
    lbl_values = list(tmp['t1'])

    _build_hbar_chart(labels, lbl_values, 0)
    st.markdown('> We have pacients that belongs to more than 1 priority group.')
    
    groups = _
    groups.insert(0, 'All Groups')
    focus_group = st.selectbox(label='Choose a Priority Group to filter further charts', options=groups)

    # Priority Group Diagnostic
    st.header('{} - {} - Top 10 Most Frequent CIE'.format(month_analyzed, focus_group))

    if focus_group == 'All Groups':
        filter_2 = filter_1.copy()
    else:
        filter_2 = filter_1[filter_1[focus_group] > 0]
    
    _df = filter_2.ATEMED_DES_CIE10.value_counts().head(10)

    labels = list(_df.keys())
    lbl_values = list(_df.values)

    _build_vbar_chart(labels, lbl_values, 90)

    # Map of occurencies
    st.header('Occurencies by Area')
    _df = df[['ENT_NOM', 'ENT_NOM_LAT', 'ENT_NOM_LONG', 'ENT_DES_PARR']].rename({'ENT_NOM_LAT': 'lat', 'ENT_NOM_LONG': 'lon'}, axis=1)
    _df = _df.groupby(['ENT_NOM', 'lat', 'lon']).agg({'ENT_DES_PARR': 'count'}).reset_index()
    _df.rename({'ENT_DES_PARR': 'qty'}, axis=1, inplace=True)

    fig = px.scatter_mapbox(
        _df,
        lat='lat',
        lon='lon',
        color_discrete_sequence=['purple'],
        size='qty',
        hover_data=['ENT_NOM'],
        zoom=7,
        height=400)
    fig.update_layout(mapbox_style="open-street-map")

    st.plotly_chart(fig)




def _build_vbar_chart(labels, lbl_values, angle):
    """Build chart and return its plot."""
    sns.set_palette('rocket')
   
    fig, ax = plt.subplots(figsize=(15, 7))
    
    ax.bar(labels, lbl_values)
    plt.xticks(rotation=angle)

    for lbl in enumerate(lbl_values):
        ax.text(lbl[0], lbl[1] + 10, lbl[1])
    
    return st.pyplot(fig)

def _build_hbar_chart(labels, lbl_values, angle):
    """Build chart and return its plot."""
    sns.set_palette('rocket')
    
    fig, ax = plt.subplots(figsize=(15, 7))

    ax.barh(labels, lbl_values)
    plt.xticks(rotation=angle)

    for lbl in enumerate(lbl_values):
        ax.text(lbl[1] + 10, lbl[0], lbl[1])
    
    return st.pyplot(fig)

