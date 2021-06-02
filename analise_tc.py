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

@st.cache
def read_data():
    df = pd.read_csv('base_dados.csv', decimal=',', na_values=[" ", '\xa0'])
    tc = pd.read_csv('tempo_concentracao.csv',
                     na_values=['#DIV/0!', '#NUM!', '#VALOR!'],
                     index_col='BACIAS', sep=';', skiprows=1, decimal=',',
                     encoding='latin')
    tc = tc[['Ventura', 'CHPW', 'Temez', 'Kirpich', 'Ven te Show', 'Pasini',
             'Picking', 'Pickering', 'Bransby Willians', 'Giandotti', 'Epsey']]
    return df, tc

@st.cache
def select_data(df, tc, basins, methods):
    df_select = []
    
    for basin in basins:
        for method in methods:
            df_select.append([basin, method, tc[method][tc.index == basin].values[0]])

    return pd.DataFrame(df_select, columns=['Bacias', 'Método',
                                                         'Tc (h)']).dropna()


def sidebar(df, tc):
    methods = st.sidebar.multiselect('Métodos:',
                                     ['todos'] + list(tc.columns),
                                     default='todos')
    
    if 'todos' in methods:
        methods = list(tc.columns)
    
    # Oção para filtrar bacias por classificação de tamanho
    size = st.sidebar.selectbox('Tamanho da bacia',
                                ['todos', 'macro', 'grande', 'média', 'pequena',
                                 'micro'])

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
    
    if not basins or not methods:
        st.text('Escolha ao menos um método e uma bacia')
    else:
        try:
            df_select = select_data(df, tc, basins, methods)
    
            f = sns.catplot(data=df_select, kind='bar', x='Bacias', y='Tc (h)',
                            hue='Método', aspect=21.7/8.27)
            f.set_xticklabels(rotation=90)
            st.pyplot(f)
    
        except ValueError:
    
            st.text("Não foi encontrado dados para a seleção feita. Tente novamente.")


def page2(df, tc):
    opt1 = st.sidebar.selectbox('Variável', list(df.columns[1:]))
    
    methods, basins, size = sidebar(df, tc)
    
    if not basins or not methods:
        st.text('Escolha ao menos um método e uma bacia')
    else:
        try:
            df_select = tc[methods][tc.index.isin(basins)]
            x_axis = df[df.BACIAS.isin(basins)][opt1]
            try:
                n = x_axis.astype(str)
                x_axis = x_axis.str.replace(',', '.')
                x_axis[x_axis == '\xa0'] = np.nan
                x_axis = pd.to_numeric(x_axis)
            except:
                pass
            
            fig, ax = plt.subplots()
            
            for method in methods:
                plt.scatter(x_axis, df_select[method], label=method)
            
            plt.xlabel(opt1)
            plt.ylabel('Tc (h)')
            plt.legend()
    
            st.pyplot(fig)
    
        except ValueError:
    
            st.text("Não foi encontrado dados para a seleção feita. Tente novamente.")
    
    

"""
# Análise do Tempo de Concetração
Comparativo do tempo de concentração entre bacias de acordo com diferentes métodos
"""
my_page = st.sidebar.radio('Page Navigation', ['page 1', 'page 2'])
df, tc = read_data()
df = df.replace(',', '.')

if my_page == 'page 1':
    page1(df, tc)
else:
    page2(df, tc)

