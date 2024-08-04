import streamlit as st
import pandas as pd
from plots.plots_import_data import *
import os

st.sidebar.page_link("main.py", label="Overview", icon="🏠")
st.sidebar.page_link("pages/Google_Ads_Performance.py",       label="Google",       icon="👥", disabled=False)
st.sidebar.page_link("pages/facebook_ads.py",                 label="Facebook",     icon="👥", disabled=False)
st.sidebar.page_link("pages/instagram_data.py",               label="Instagram",    icon="👥", disabled=False)

csv_file  = 'uploaded_data.csv'
xlsx_file = 'uploaded_data.xlsx'

try:
    # Check if CSV file exists in the root directory
    if os.path.exists(csv_file):
        data = pd.read_csv(csv_file)
        print("\n\n\t\t* CSV file loaded successfully.\n\n\n")
    # Check if Excel file exists in the root directory
    elif os.path.exists(xlsx_file):
        data = pd.read_excel(xlsx_file)
        print("\n\n\t\t* Excel file loaded successfully.\n\n\n")
    else:
        print("\n\n\t\t** No file found.\n\n\n")
except:
    st.error("File Not Found.")

try:
    df = pd.DataFrame(data)
except:
    pass

try:
    clientes_pendentes(df)
except:
    pass
try:
    horario_clientsAtendidosHoje(df)
except:
    pass

try:
    st.divider()
    col1, col2 = st.columns([1,1])
    with col1:
        try:
            canais_QuantidadeDeAtendimentos(df)
        except:
            pass
    with col2:
        try:
            contatosAtendidosHoje(df)
        except:
            pass
except:
    pass

try:
    st.divider()
    col1, col2 = st.columns([1,1])
    with col1:
        try:
            contatosFidelizados_Mês(df)
        except:
            pass
    with col2:
        try:  
            atendimentosFinalizados(df)
        except:
            pass
except:
    pass

try:
    st.divider()
    contatosEmChatbot(df)
except:
    pass

    






