import numpy as np
import pandas as pd
import plotly.express as px
from charts import scatter, line, radar, bar, box_plot


def select_data(df, tc, basins, methods):
    df_select = []
    
    for basin in basins:
        for method in methods:
            df_select.append([basin, method, tc[method][tc.index == basin].values[0]])

    return pd.DataFrame(df_select, columns=['Bacias', 'Método',
                                            'Tc (h)']).dropna()


def plot_data(df, x_axis, methods, opt1, basins):
    df_plot = pd.DataFrame(())
    for l in range(len(x_axis)):
        for method in methods:
            line = pd.Series([x_axis.values[l], method, df[method][l],
                              basins[l]])
            line = pd.DataFrame([line])
            df_plot = pd.concat([line, df_plot], ignore_index=True)
    
    df_plot.columns = [opt1, 'método', 'tc (h)', 'BACIAS']
    
    return df_plot


def bar_plot(df, tc, basins, methods, st):
    try:
        df_select = select_data(df, tc, basins, methods)

        bar(df_select, methods, st)

    except ValueError:
        st.text("Não foi encontrado dados para a seleção feita. Tente novamente.")


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
        
        df_plot = plot_data(df_select, x_axis, methods, opt1, basins)
        scatter(df_plot, opt1, methods, st)

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
        
        df_plot = plot_data(df_select, x_axis, methods, opt1, basins)
        df_plot = df_plot.sort_values(by=[opt1]).dropna()
        
        line(df_plot, opt1, methods, st)

    except ValueError:
        st.text("Não foram encontrados dados para esta seleção. Tente novamente.")


def boxplot_plot(df, tc, basins, methods, st):
    x_axis = st.radio('Eixo x', ['Método', 'Bacias'])
    try:
        df_select = select_data(df, tc, basins, methods)
        box_plot(df_select, basins, methods, x_axis, st)

    except ValueError:
    
        st.text("Não foi encontrado dados para a seleção feita. Tente novamente.")


def radar_plot(df, tc, basins, methods, opt1, st):

    try:
        df_select = tc[methods][tc.index.isin(basins)]
        x_axis = df[df.BACIAS.isin(basins)]
        
        correl = pd.DataFrame((), columns=x_axis.columns[1:-1])
        
        for x in correl.columns:
            corr_method = []
            for method in methods:
                v1 = pd.DataFrame(np.array([df_select[method],x_axis[x]]).T)
                v1 = v1.dropna()
                corr_method.append(v1.corr()[0][1])
            correl[x] = corr_method
        
        correl.insert(0, 'Método', methods)
                
        radar(correl, opt1, st)

    except ValueError:
        st.text("Não foram encontrados dados para esta seleção. Tente novamente.")


def heatmap_plot(df, tc, basins, methods, st, opt1=None, type=1):

    try:
        if type == 1:
            tc = tc.loc[tc.index.isin(basins)][methods]
            st.text("Matriz correlação")
            st.dataframe(tc.corr())
            st.subheader("Mapa de correlação")
            fig = px.imshow(tc.corr(), color_continuous_scale='spectral')
            st.plotly_chart(fig)
        else:
            df_select = tc[methods][tc.index.isin(basins)]
            x_axis = df[df.BACIAS.isin(basins)]
            correl = pd.DataFrame((), columns=x_axis.columns[1:-1])

            for x in correl.columns:
                corr_method = []
                for method in methods:
                    v1 = pd.DataFrame(np.array([df_select[method],x_axis[x]]).T)
                    v1 = v1.dropna()
                    corr_method.append(v1.corr()[0][1])
                correl[x] = corr_method
            
            correl.insert(0, 'Método', methods)
            correl = correl.set_index('Método')
            
            st.text("Matriz correlação")
            st.dataframe(correl)
            st.subheader("Mapa de correlação")
            
            fig = px.imshow(correl,
                            color_continuous_scale='spectral',
                            width=1000, height=800)
            st.plotly_chart(fig)
            

    except ValueError:
    
        st.text("Não foi encontrado dados para a seleção feita. Tente novamente.")