import streamlit as st
import pandas as pd

st.set_page_config(page_title="Contador de Obra", layout="wide")

st.subheader("⚡ Carlos Soares")

# 1. Seleção do Cômodo
comodo = st.selectbox("Selecione o Cômodo:", ["Sala", "Cozinha", "Quarto 1", "Quarto 2", "Quarto 3","Banheiro", "Outro"])

st.divider()
st.markdown("### 📦 Placas e Módulos (Grid)")

# Dicionário dos itens e quantidades
if 'contagem' not in st.session_state:
    st.session_state.contagem = {}

# Lista dos seus materiais da obra
itens_obra = [
    {"nome": "4x2 - 1 Tecla Simples", "icone": "⏹️"},
    {"nome": "4x2 - 1 Tecla Paralelo", "icone": "🔀"},
    {"nome": "4x2 - 2 Teclas Simples", "icone": "⏹️"},
    {"nome": "4x2 - 2 Teclas (1 Simples e 1 Paral)", "icone": "⏹️"},
    {"nome": "4x2 - 1 Tomada 10A", "icone": "🔌"},
    {"nome": "4x2 - 2 Tomadas 10A", "icone": "🔌"},
    {"nome": "4x2 - 1 Tomada 20A", "icone": "🔌"},
    {"nome": "4x2 - 2 Tomadas 20A", "icone": "🔌"},
    {"nome": "4x2 - 1 Tecla + 1Tomada", "icone": "🔀"},
    {"nome": "4x2 - 1 Tecla + 1Tomada 20A", "icone": "🔀"},
    {"nome": "4x4 - 4 Teclas", "icone": "⬛"},
]

# Inicializa as variáveis na memória do app
for item in itens_obra:
    chave = f"{comodo}_{item['nome']}"
    if chave not in st.session_state.contagem:
        st.session_state.contagem[chave] = 0

# 2. Construção do Grid Visual (3 colunas por linha)
cols = st.columns(2)

for idx, item in enumerate(itens_obra):
    col = cols[idx % 2]
    chave = f"{comodo}_{item['nome']}"
    
    with col:
        with st.container(border=True):
            st.markdown(f"{item['icone']} {item['nome']}")
            st.write(f"Quantidade no(a) **{comodo}**: **{st.session_state.contagem[chave]}**")
            
            c1, c2 = st.columns(2)
            if c1.button("➖ 1", key=f"sub_{chave}"):
                if st.session_state.contagem[chave] > 0:
                    st.session_state.contagem[chave] -= 1
                    st.rerun()
                    
            if c2.button("➕ 1", key=f"add_{chave}"):
                st.session_state.contagem[chave] += 1
                st.rerun()

# 3. Sumário / Relatório da Obra
st.divider()
st.subheader("📊 Sumário Consolidado da Obra")

dados_resumo = []
for chave, qtd in st.session_state.contagem.items():
    if qtd > 0:
        local, material = chave.split("_")
        dados_resumo.append({"Cômodo": local, "Material / Placa": material, "Qtd": qtd})

if dados_resumo:
    df = pd.DataFrame(dados_resumo)
    st.dataframe(df, use_container_width=True)
    
    # Exibe totais agrupados para a lista de compras
    st.markdown("### 🛒 Totais para Compra:")
    totais = df.groupby("Material / Placa")["Qtd"].sum().reset_index()
    for _, linha in totais.iterrows():
        st.write(f"• **{linha['Material / Placa']}**: {linha['Qtd']} unidades")
else:
    st.info("Nenhum item adicionado ainda. Clique nos botões ➕ acima para contar!")
