#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jun  8 21:41:09 2021

@author: duarte
"""
import plotly.graph_objects as go
import plotly.express as px
import numpy as np


color_palette = {'Ventura': "#32964d", 'CHPW': "#83d996", 'Temez':  "#016876",
                 'Kirpich': "#aedbf0", 'Ven te Chow': "#3444bc",
                 'Pasini': "#f09bf1", 'Picking': "#9525ba",
                 'Pickering': "#528efb", 'Bransby Willians': "#514e72",
                 'Giandotti': "#1ceaf9", 'Epsey': "#0b5313",
                 'Corps Engineers': "#0b4343"}


def scatter(df_plot, opt1, methods, st):
    clrs = [color_palette[x] for x in methods]
    fig = px.scatter(df_plot, x=opt1, y='tc (h)', color="método",
                     color_discrete_sequence=clrs,
                     hover_name='BACIAS',
                     labels=methods)
    st.plotly_chart(fig)


def line(df_plot, opt1, methods, st):
    clrs = [color_palette[x] for x in methods]
    fig = px.line(df_plot, x=opt1, y='tc (h)', color="método",
                  color_discrete_sequence=clrs,
                  hover_name='BACIAS',
                  labels=methods)
    st.plotly_chart(fig)


def radar(correl, opt1, st):
    fig = go.Figure()

    if 'todos' in opt1:
        opt1 = correl.columns[1:]

    for property in list(opt1):
        fig.add_trace(go.Scatterpolar(r=correl[property],
                                      theta=correl['Método'],
                                      name=property,
                                      ))
    fig.update_layout(
      polar=dict(
        radialaxis=dict(
          visible=True,
          range=[0, 1]
        )),
      showlegend=True,
      title='Correlação'
    )

    st.plotly_chart(fig)


def bar(df_plot, methods, st):
    clrs = [color_palette[x] for x in methods]
    fig = px.bar(df_plot, x='Bacias', y='Tc (h)', color='Método',
                 color_discrete_sequence=clrs, width=1000, height=800,
                 barmode='group')
    st.plotly_chart(fig)


def box_plot(df_plot, basins, methods, x_axis, st):
    if x_axis == 'Método':
        hover = 'Bacias'
        width = 700
        height = 400
        clrs = [color_palette[x] for x in methods]
    else:
        N = len(basins)
        hover = 'Método'
        width = 1500
        height = 800
        clrs = ['hsl('+str(h)+',50%'+',50%)' for h in np.linspace(0, 360, N)]

    fig = px.box(df_plot, x=x_axis, y='Tc (h)', color=x_axis,
                 color_discrete_sequence=clrs,
                 hover_name=hover, width=width, height=height,
                 )

    st.plotly_chart(fig)
