import pandas as pd  # pip install pandas openpyxl
import plotly.graph_objects as go
import altair as alt


class charts():

    def tester():
        from vega_datasets import data

        source = data.iowa_electricity()

        fig = alt.Chart(source).mark_bar(opacity=0.7).encode(
            x='year:O',
            y=alt.Y('net_generation:Q', stack=None),
            color="source",
        )

        print(source)
        return fig


    def test(afaire, fait):
        test = []
        for elem in afaire:    
            test.append((elem[0], "A faire", elem[1]))
        for elem in fait:
            test.append((elem[0], "Fait", elem[1]))
        
        df = pd.DataFrame(test, columns=["Catégories", "Bilan", "Objectif / Réalisé"])
        base = alt.Chart(df).encode(
            theta=alt.Theta("Objectif / Réalisé:Q", stack=True),
            radius=alt.Radius("Catégories", scale=alt.Scale(type="sqrt", zero=True, rangeMin=20)),
            color="Objectif / Réalisé:N",
        )

        c1 = base.mark_arc(innerRadius=20, stroke="#fff")

        c2 = base.mark_text(radiusOffset=10).encode(text="Catégories:Q")

        c1 + c2
        base

        return base




    def _charts_pie(forma):
        # ---- CHARTS ----
        labels = ['A faire', 'Fait']
        sizes = [forma[0], forma[1]]
        
        fig = go.Figure(
            go.Pie(
                labels=labels,
                values=sizes,
                hoverinfo="label+value",

            )
        )
        return fig

    def _charts_bars(afaire, fait):
        test = []
        for elem in afaire:    
            test.append((elem[0], "A faire", elem[1]))
        for elem in fait:
            test.append((elem[0], "Fait", elem[1]))

        df = pd.DataFrame(test, columns=["Catégories", "Bilan", "Nombre"])
       
        fig = alt.Chart(df).mark_bar(opacity=0.7).encode(
            x='Catégories:O',
            y=alt.Y('Nombre:Q', stack=None),
            color = 'Bilan',
            tooltip=['Catégories','Bilan', 'Nombre']
        ).add_selection(alt.selection_interval(bind='scales')
        )
        return fig
    
    def _chart_radar(afaire, fait):
        df = pd.DataFrame(afaire, columns=["Catégories", "Nombre"]) # - Transforme la liste en table, en attribuant le noms de colonne
        
        fig = go.Figure()
        fig.add_trace(go.Scatterpolar(
            r=df["Nombre"], 
            theta=df["Catégories"],
            fill='toself',
            name='Objectif'
        ))

        df = pd.DataFrame(fait, columns=["Catégories", "Nombre"])

        fig.add_trace(go.Scatterpolar(
            r=df["Nombre"],
            theta=df["Catégories"],
            fill='none',
            name='Réalisé'
        ))


        fig.update_layout(
            polar=dict(
                radialaxis=dict(
                    visible=True
                )),
            showlegend=True
        )
        fig.update_traces(fill='toself')

        return fig
    
    
