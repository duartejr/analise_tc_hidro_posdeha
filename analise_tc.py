#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon May 31 23:18:56 2021

@author: duarte
"""

import streamlit as st
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from utils import color_palette, scatter_plot, line_plot, select_data
from utils import boxplot_plot, radar_plot


@st.cache
def read_data():
    df = pd.read_csv('base_dados.csv', na_values=[" ", '\xa0'])
    tc = pd.read_csv('tempo_concentracao.csv',
                     na_values=['#DIV/0!', '#NUM!', '#VALOR!'],
                     index_col='BACIAS', sep=';', skiprows=1, decimal=',',
                     encoding='latin')
    tc = tc[['Ventura', 'CHPW', 'Temez', 'Kirpich', 'Ven te Chow', 'Pasini',
             'Picking', 'Pickering', 'Bransby Willians', 'Giandotti', 'Epsey']]
    return df, tc


def sidebar(df, tc):
    methods = st.sidebar.multiselect('Métodos:',
                                     ['todos'] + list(tc.columns),
                                     default='todos')    
    if 'todos' in methods:
        methods = list(tc.columns)    
    # Oção para filtrar bacias por classificação de tamanho
    size = st.sidebar.selectbox('Tamanho da bacia',
                                ['todos', 'macro', 'grande', 'média',
                                 'pequena', 'micro'])

    if size != 'todos':
        select_basins = df[df.Tamanho == size]['BACIAS']
    else:
        select_basins = df['BACIAS']

    basins = st.sidebar.multiselect('Bacias:',
                                    ['todas'] + list(select_basins),
                                    default='todas')

    if 'todas' in basins:
        basins = list(select_basins)

    return methods, basins, size


def page1(df, tc):
    # Read data
    # Exibe opção para selecionar métods de cálculo do Tc
    methods, basins, size = sidebar(df, tc)
    st.subheader("Tipo de gráfico")
    my_chart = st.radio('', ['barras', 'boxplot'])

    if not basins or not methods:
        st.text('Escolha ao menos um método e uma bacia')
    else:
        if my_chart == 'barras':
            try:
                df_select = select_data(df, tc, basins, methods)
                clrs = [color_palette[x] for x in methods]
        
                f = sns.catplot(data=df_select, kind='bar', x='Bacias', y='Tc (h)',
                                hue='Método', aspect=21.7/8.27, palette=clrs)
                f.set_xticklabels(rotation=90)
                st.pyplot(f)
        
            except ValueError:
                st.text("Não foi encontrado dados para a seleção feita. Tente novamente.")
        else:
            boxplot_plot(df, tc, basins, methods, st)


def page2(df, tc):
    methods, basins, size = sidebar(df, tc)
    st.subheader("Tipo de gráfico")
    chart_type = st.radio('', ['dispersão', 'linha', 'radar'])

    if not basins or not methods:
        st.text('Escolha ao menos um método e uma bacia')
    else:
        if chart_type == 'dispersão':
            opt1 = st.sidebar.selectbox('Parâmetro', list(df.columns[1:]))
            scatter_plot(df, tc, basins, methods, opt1, st)
        if chart_type == 'linha':
            opt1 = st.sidebar.selectbox('Parâmetro', list(df.columns[1:]))
            line_plot(df, tc, basins, methods, opt1, st)
        if chart_type == 'radar':
            opt1 = st.sidebar.multiselect('Parâmetro:',
                                     ['todos'] + list(df.columns[1:-1]),
                                     default='todos')
            if not opt1:
                st.text('Escolha ao menos um parâmetro')
            else:
                radar_plot(df, tc, basins, methods, opt1, st)


"""
# Análise do Tempo de Concentração
Comparativo do tempo de concentração entre bacias de acordo com diferentes métodos
"""
my_page = st.sidebar.radio('Page Navigation', ['page 1', 'page 2'])
df, tc = read_data()
df = df.replace(',', '.')
st.write('<style>div.row-widget.stRadio > div{flex-direction:row;}</style>', unsafe_allow_html=True)

if my_page == 'page 1':
    page1(df, tc)
else:
    page2(df, tc)

