#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon May 31 23:18:56 2021

@author: duarte
"""

import streamlit as st
import pandas as pd
import numpy as np
from scipy.stats import zscore
from utils import scatter_plot, line_plot
from utils import boxplot_plot, radar_plot, bar_plot, heatmap_plot


@st.cache
def read_data():
    df = pd.read_csv('base_dados.csv', sep=',', decimal='.',
                     na_values=['', ' ', '\xa0'])
    tc = pd.read_csv('tempo_concentracao.csv', index_col='BACIAS',
                     na_values=['', ' ', '\xa0'])
    tc = tc[['Bransby Willians', 'CHPW', 'Corps Engineers', 'Dooge',
             'Epsey', 'Kirpich', 'Pasini', 'Pickering', 'Picking',
             'Temez', 'Ven te Chow', 'Ventura']].dropna()
    z_scores = zscore(tc)
    abs_z_scores = np.abs(z_scores)
    filtered_entries = (abs_z_scores < 3).all(axis=1)
    tc = tc[filtered_entries]
    df = df[df.BACIAS.isin(tc.index.values[:])]
    return df, tc


def sidebar(df, tc):
    methods = st.sidebar.multiselect('Métodos:',
                                     ['todos'] + list(tc.columns),
                                     default='todos')
    if 'todos' in methods:
        methods = list(tc.columns)
    # Oção para filtrar bacias por classificação de tamanho
    size = st.sidebar.multiselect('Tamanho da bacia',
                                ['todos', 'macro', 'grande', 'média',
                                 'pequena', 'micro'], default='todos')

    if 'todos' in size:
        select_basins = df['BACIAS']
    else:
        select_basins = df[df.Tamanho.isin(size)]['BACIAS']

    basins = st.sidebar.multiselect('Bacias:',
                                    sorted(list(select_basins)),
                                    default=sorted(list(select_basins)))

    if 'todas' in basins:
        basins = list(select_basins)

    return methods, basins, size


def page1(df, tc):
    # Read data
    # Exibe opção para selecionar métods de cálculo do Tc
    methods, basins, size = sidebar(df, tc)
    st.subheader("Tipo de gráfico")
    my_chart = st.radio('', ['barras', 'boxplot', 'heatmap'])

    if not basins or not methods:
        st.text('Escolha ao menos um método e uma bacia')
    else:
        if my_chart == 'barras':
            bar_plot(df, tc, basins, methods, st)
        elif my_chart == 'heatmap':
            heatmap_plot(df, tc, basins, methods, st)
        else:
            boxplot_plot(df, tc, basins, methods, st)


def page2(df, tc):
    methods, basins, size = sidebar(df, tc)
    st.subheader("Tipo de gráfico")
    chart_type = st.radio('', ['dispersão', 'linha', 'radar', 'heatmap'])

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
                                          sorted(list(df.columns[1:-1])),
                                          default=sorted(list(df.columns[1:-1])))
            if not opt1:
                st.text('Escolha ao menos um parâmetro')
            else:
                radar_plot(df, tc, basins, methods, opt1, st)
        if chart_type == 'heatmap':
            opt1 = st.sidebar.multiselect('Parâmetro:',
                                          sorted(list(df.columns[1:-1])),
                                          default=sorted(list(df.columns[1:-1])))
            heatmap_plot(df, tc, basins, methods, st, opt1=opt1, type=2)


"""
# Análise do Tempo de Concentração
Comparativo do tempo de concentração entre bacias de acordo com diferentes
métodos
"""
my_page = st.sidebar.radio('Page Navigation', ['page 1', 'page 2'])
df, tc = read_data()
df = df.replace(',', '.')
st.write('<style>div.row-widget.stRadio > div{flex-direction:row;}</style>',
         unsafe_allow_html=True)

if my_page == 'page 1':
    page1(df, tc)
else:
    page2(df, tc)
