import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
import plotly.express as px
import plotly.graph_objects as go



color_palette = {'Ventura': "#32964d", 'CHPW':"#83d996", 'Temez':  "#016876",
                 'Kirpich': "#aedbf0", 'Ven te Chow': "#3444bc",
                 'Pasini': "#f09bf1", 'Picking': "#9525ba",
                 'Pickering': "#528efb", 'Bransby Willians': "#514e72",
                 'Giandotti': "#1ceaf9", 'Epsey': "#0b5313"}


def select_data(df, tc, basins, methods):
    df_select = []
    
    for basin in basins:
        for method in methods:
            df_select.append([basin, method, tc[method][tc.index == basin].values[0]])

    return pd.DataFrame(df_select, columns=['Bacias', 'Método',
                                            'Tc (h)']).dropna()


def scatter_plot(df, tc, basins, methods, opt1, st):
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
            plt.scatter(x_axis.values[:], df_select[method].values[:], label=method,
                        color=color_palette[method])
        
        plt.xlabel(opt1)
        plt.ylabel('Tc (h)')
        plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left')

        st.pyplot(fig)

    except ValueError:
        st.text("Não foram encontrados dados para esta seleção. Tente novamente.")


def line_plot(df, tc, basins, methods, opt1, st):
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
            plot_data = pd.DataFrame([x_axis.values[:],
                                      df_select[method].values[:]]).T
            plot_data = plot_data.dropna()
            plot_data = plot_data.sort_values(by=[0])
            plt.plot(plot_data[0].values[:], plot_data[1].values[:],
                     color=color_palette[method], label=method)

        plt.xlabel(opt1)
        plt.ylabel('Tc (h)')
        plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
        st.pyplot(fig)
        del plot_data

    except ValueError:
        st.text("Não foram encontrados dados para esta seleção. Tente novamente.")


def boxplot_plot(df, tc, basins, methods, st):
    x_axis = st.radio('Eixo x', ['Método', 'Bacias'])

    try:
        df_select = select_data(df, tc, basins, methods)
        clrs = sns.color_palette("Paired", len(basins))
        
        if x_axis == 'Método':
            clrs = [color_palette[x] for x in methods]
        
        fig, ax = plt.subplots()
        
        f = sns.boxplot(x=x_axis, y='Tc (h)', data=df_select,
                           palette=clrs)

        f.set_xticklabels(f.get_xticklabels(),rotation=90)
        st.pyplot(fig)
    
    except ValueError:
    
        st.text("Não foi encontrado dados para a seleção feita. Tente novamente.")


def radar_plot(df, tc, basins, methods, opt1, st):

    try:
        df_select = tc[methods][tc.index.isin(basins)]
        x_axis = df[df.BACIAS.isin(basins)]
        
        try:
            n = x_axis.astype(str)
            x_axis = x_axis.str.replace(',', '.')
            x_axis[x_axis == '\xa0'] = np.nan
            x_axis = pd.to_numeric(x_axis)
        except:
            pass
        
        correl = pd.DataFrame((), columns=x_axis.columns[1:-1])
        
        for x in correl.columns:
            corr_method = []
            for method in methods:
                v1 = pd.DataFrame(np.array([df_select[method],
                                            x_axis[x].replace(',','.')]).T)
                v1 = v1.dropna()
                corr_method.append(v1.corr()[0][1])
            correl[x] = corr_method
        
        correl.insert(0, 'Método', methods)
                
        fig = go.Figure()
        
        if 'todos' in opt1:
            opt1 = correl.columns[1:]
        
        for property in list(opt1):
            fig.add_trace(go.Scatterpolar(r=correl[property],
                                          theta=correl['Método'],
                                          name=property))
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

    except ValueError:
        st.text("Não foram encontrados dados para esta seleção. Tente novamente.")
    