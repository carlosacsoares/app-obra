import streamlit as st
import pandas as pd

st.set_page_config(page_title="Montador Elétrico", layout="wide")

# CSS para congelar o topo (Menu Fixo)
st.markdown("""
    <style>
        div[data-testid="stVerticalBlock"] > div:has(div[data-testid="stSelectbox"]) {
            position: sticky;
            top: 2.8rem;
            background-color: white;
            z-index: 999;
            padding-top: 10px;
            padding-bottom: 10px;
            border-bottom: 2px solid #e6e6e6;
        }
    </style>
""", unsafe_allow_html=True)

st.title("⚡ Levantamento Elétrico - Ponto a Ponto")

# Inicializa o histórico na memória da sessão
if "pontos_cadastrados" not in st.session_state:
    st.session_state.pontos_cadastrados = []

# --- MENU FIXO NO TOPO ---
col_loc, col_cx = st.columns(2)
with col_loc:
    local = st.selectbox("📍 Local / Cômodo:", ["Sala", "Sala Estar","Cozinha", "Cozinha Gourmet","Quarto 1", "Quarto 2", "Banheiro Suite", "Banheiro Social","Corredor", "Outro"])

with col_cx:
    tamanho_caixa = st.radio("📦 Tamanho da Caixa na Parede:", ["Caixa 4x2 (Máx. 3 Módulos)", "Caixa 4x4 (Máx. 6 Módulos)"], horizontal=True)

limite_max = 3 if "4x2" in tamanho_caixa else 6

st.divider()
st.markdown(f"**Selecione os Módulos para este ponto (Capacidade: {limite_max} Módulos)**")

# Lista de Módulos disponíveis
lista_modulos = [
    "Nenhum",
    "Tomada Simples 10A",
    "Tomada 20A",
    "Interruptor Simples",
    "Interruptor Paralelo (Three-Way)",
    "Interruptor Intermediário (Four-Way)",
    "Botão de Campainha",
    "Módulo USB",
    "Módulo RJ45 (Rede/Internet)",
    "Módulo TV (Coaxial)"
]

# Formulário para adicionar Módulos no Ponto Atual
c1, c2 = st.columns(2)

with c1:
    mod1 = st.selectbox("Módulo Tipo A:", lista_modulos, key="m1")
    qtd1 = st.selectbox("Quantidade A:", list(range(0, limite_max + 1)), key="q1")

with c2:
    mod2 = st.selectbox("Módulo Tipo B:", lista_modulos, key="m2")
    # Limita a quantidade do segundo módulo para não estourar o limite da caixa
    sobra_vagas = max(0, limite_max - qtd1)
    qtd2 = st.selectbox("Quantidade B:", list(range(0, sobra_vagas + 1)), key="q2")

total_modulos = qtd1 + qtd2

# Alerta caso ultrapasse a capacidade da placa
if total_modulos > limite_max:
    st.error(f"⚠️ Atenção: Esta caixa suporta até {limite_max} módulos! Você selecionou {total_modulos}.")
elif total_modulos == 0:
    st.warning("Selecione pelo menos 1 módulo para salvar o ponto.")

# Botão para Adicionar Ponto
if st.button("➕ Salvar Ponto Elétrico", type="primary", disabled=(total_modulos == 0 or total_modulos > limite_max)):
    # Identifica o tipo de placa necessária automaticamente pelo total de módulos
    if "4x2" in tamanho_caixa:
        tipo_placa = f"Placa 4x2 com {total_modulos} Posto(s)"
    else:
        tipo_placa = f"Placa 4x4 com {total_modulos} Posto(s)"

    # Registra o ponto
    novo_ponto = {
        "Local": local,
        "Tamanho Caixa": "4x2" if "4x2" in tamanho_caixa else "4x4",
        "Placa Recomendada": tipo_placa,
        "Mod1": mod1 if mod1 != "Nenhum" else "",
        "Qtd1": qtd1,
        "Mod2": mod2 if mod2 != "Nenhum" else "",
        "Qtd2": qtd2,
        "Total Módulos": total_modulos
    }
    
    st.session_state.pontos_cadastrados.append(novo_ponto)
    st.success(f"Ponto salvo no(a) {local}!")

# --- SEÇÃO DE RELATÓRIO E LISTA DE COMPRAS ---
st.divider()
st.subheader("📊 Histórico e Lista de Compras Consolidada")

if st.session_state.pontos_cadastrados:
    df_pontos = pd.DataFrame(st.session_state.pontos_cadastrados)
    
    # 1. Tabela de Pontos Cadastrados
    st.markdown("**Pontos Registrados na Obra:**")
    st.dataframe(df_pontos[["Local", "Placa Recomendada", "Mod1", "Qtd1", "Mod2", "Qtd2"]], use_container_width=True)
    
    st.divider()
    
    # 2. Resumo Consolidado de Materiais para Compra
    st.markdown("### 🛒 Lista Final para Fazer o Pedido")
    
    col_p, col_m = st.columns(2)
    
    with col_p:
        st.markdown("**Placas e Suportes:**")
        placas_totais = df_pontos["Placa Recomendada"].value_counts()
        for placa, qtd in placas_totais.items():
            st.write(f"• **{placa}**: {qtd} un")
            
    with col_m:
        st.markdown("**Módulos Individuais:**")
        modulos_dict = {}
        
        for _, linha in df_pontos.iterrows():
            if linha["Mod1"] and linha["Qtd1"] > 0:
                modulos_dict[linha["Mod1"]] = modulos_dict.get(linha["Mod1"], 0) + linha["Qtd1"]
            if linha["Mod2"] and linha["Qtd2"] > 0:
                modulos_dict[linha["Mod2"]] = modulos_dict.get(linha["Mod2"], 0) + linha["Qtd2"]
                
        for mod, qtd in modulos_dict.items():
            st.write(f"• **{mod}**: {qtd} un")

    # Botão para limpar a lista e começar de novo
    if st.button("🗑️ Limpar Todos os Dados da Obra"):
        st.session_state.pontos_cadastrados = []
        st.rerun()
else:
    st.info("Nenhum ponto registrado ainda. Configure os módulos acima e clique em 'Salvar Ponto Elétrico'.")
