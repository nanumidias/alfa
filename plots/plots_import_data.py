from streamlit_echarts import st_echarts
import streamlit as st



def clientes_pendentes(df):
    # Aggregate the data by category
    aggregated_df = df.groupby('category').sum().reset_index()
    # Aggregate the data by category
    aggregated_df = df.groupby('category').sum().reset_index()

    options = {       
        "tooltip": {
            "trigger": 'axis',
            "axisPointer": {
                "type": 'shadow'
            }
        },
        "legend": {
            "data": aggregated_df['category'].tolist()
        },
        "grid": {
            "left": '3%',
            "right": '4%',
            "bottom": '3%',
            "containLabel": True
        },
        "xAxis": {
            "type": 'category',
            "data": aggregated_df['category'].tolist()
        },
        "yAxis": {
            "type": 'value'
        },
        "series": [
            {
                "name": 'Clientes pendentes',
                "type": 'bar',
                "data": aggregated_df['Clientes pendentes'].tolist()
            }
        ]
    }
    st.subheader("category vs Clientes pendentes")
    st_echarts(options=options, height=300, width=1200)



def horario_clientsAtendidosHoje(df):
    horario            = df['horario'].tolist()
    clientes_atendidos = df['clientes_atendidos'].tolist()
    options = {
        "tooltip": {
            "trigger": "axis",
            "axisPointer": {
                "type": "cross",
                "label": {
                    "backgroundColor": "#6a7985"
                }
            }
        },
        "xAxis": {
            "type": "category",
            "boundaryGap": False,
            "data": horario
        },
        "yAxis": {
            "type": "value"
        },
        "series": [
            {
                "name": "Clientes Atendidos",
                "type": "line",
                "stack": "Total",
                "areaStyle": {},
                "emphasis": {
                    "focus": "series"
                },
                "data": clientes_atendidos
            }
        ]
    }
    st.subheader("Horário vs Clientes atendidos hoje")
    st_echarts(options=options, height=300, width=1200)



def canais_QuantidadeDeAtendimentos(df):
    # Aggregate data by 'canais'
    aggregated_data = df.groupby('canais')['quantidade_atendimentos'].sum().reset_index()
    # Prepare data for the pie chart
    pie_data = [{"value": int(aggregated_data["quantidade_atendimentos"][i]), "name": aggregated_data["canais"][i]} for i in range(len(aggregated_data))]
    # Echarts option
    pie_option = {
        "tooltip": {"trigger": "item"},
        "legend": {"top": "5%", "left": "center"},
        "series": [{
            "name": "Quantidade de Atendimentos",
            "type": "pie",
            "radius": ["40%", "70%"],
            "avoidLabelOverlap": False,
            "itemStyle": {"borderRadius": 10, "borderColor": "#fff", "borderWidth": 2},
            "label": {"show": False, "position": "center"},
            "emphasis": {"label": {"show": True, "fontSize": "20", "fontWeight": "bold"}},
            "labelLine": {"show": False},
            "data": pie_data
        }]
    }
    st.subheader("Canais vs Quantidade De atendimentos")
    st_echarts(options=pie_option, height=300, width=600)



def contatosAtendidosHoje(df):
    # Convert the value for the gauge chart to int
    contatos_atendidos_hoje = int(df["Contatos Atendidos Hoje"][0])
    # Echarts option for gauge chart
    gauge_option = { 
        "tooltip": {"formatter": "{a} <br/>{b} : {c}%"},
        "series": [{
            "name": "Contatos Atendidos Hoje",
            "type": "gauge",
            "detail": {"formatter": "{value}"},
            "data": [{"value": contatos_atendidos_hoje, "name": "Hoje"}]
        }]
    }
    st.subheader("Contatos Atendidos Hoje")
    st_echarts(options=gauge_option, height=300, width=600)



def atendimentosFinalizados(df):
    bar_option = {
        "tooltip": {"trigger": "axis", "axisPointer": {"type": "shadow"}},
        "xAxis": {
            "type": "category",
            "data": [str(i+1) for i in range(len(df))]
        },
        "yAxis": {
            "type": "value"
        },
        "series": [{
            "name": "Atendimentos Finalizados",
            "data": [int(val) for val in df["Atendimentos finalizados"]],
            "type": "bar",
            "showBackground": True,
            "backgroundStyle": {
                "color": "rgba(180, 180, 180, 0.2)"
            },
            "itemStyle": {
                "color": "#5470C6"
            }
        }]
    }
    st.subheader("Atendimentos Finalizados")
    st_echarts(options=bar_option, height=400, width=600)


def contatosFidelizados_Mês(df):
    bar_option = {
        "tooltip": {"trigger": "axis", "axisPointer": {"type": "shadow"}},
        "xAxis": {"type": "category", "data": list(range(1, len(df) + 1))},
        "yAxis": {"type": "value"},
        "series": [{
            "data": df["Contatos fidelizados / Mês"].tolist(),
            "type": "bar",
            "showBackground": True,
            "backgroundStyle": {
                "color": "rgba(180, 180, 180, 0.2)"
            }
        }]
    }
    st.subheader("Contatos fidelizados / Mês")
    st_echarts(options=bar_option, height=400, width=600)





def contatosEmChatbot(df):
    # Echarts option for line chart
    line_option = {
        "title": {
            "subtext": 'Contatos em chatbot',
            "left": 'center'
        },  
        "tooltip": {"trigger": "axis"},
        "xAxis": {
            "type": "category",
            "data": df["category"].tolist()
        },
        "yAxis": {
            "type": "value"
        },
        "series": [{
            "name": "Contatos em chatbot",
            "type": "line",
            "data": [int(val) for val in df["Contatos em chatbot"]],
            "smooth": True,
            "lineStyle": {
                "width": 2
            },
            "itemStyle": {
                "color": "#5470C6"
            }
        }]
    }
    st.subheader("Contatos em Chatbot por Categoria")
    st_echarts(options=line_option, height=400, width=1500)








