import streamlit as st
import pandas as pd

# =============================
# ESTILO VISUAL
# =============================
st.markdown("""
    <style>
        body {
            font-family: 'Roboto', sans-serif;
            background-color: #f4f6f7;
            color: #2f3640;
        }
        .stButton>button {
            background-color: #2f3640;
            color: white;
            font-weight: 600;
            border-radius: 6px;
            padding: 8px 20px;
            border: none;
        }
        .stButton>button:hover {
            background-color: #1e272e;
            color: #dcdde1;
        }
        .metric-card {
            background-color: #ffffff;
            padding: 15px;
            border-radius: 8px;
            box-shadow: 0 1px 4px rgba(0,0,0,0.1);
            text-align: center;
        }
        h1, h2, h3 {
            font-family: 'Roboto', sans-serif;
            color: #273c75;
        }
    </style>
""", unsafe_allow_html=True)

st.title("Sistema de Gerenciamento de Estoque - Comércio Eletrônico")

# =============================
# ESTRUTURAS DE DADOS
# =============================
if "estoque" not in st.session_state:
    st.session_state.estoque = pd.DataFrame(columns=[
        "Nome", "Categoria", "Quantidade", "Preço (R$)", "Localização"
    ])

if "movimentacoes" not in st.session_state:
    st.session_state.movimentacoes = pd.DataFrame(columns=[
        "Produto", "Tipo", "Quantidade", "Responsável"
    ])

# =============================
# VARIÁVEIS BOOLEANAS INTERNAS
# =============================
P = True  # Cadastro de produtos
E = True  # Atualização de estoque
L = True  # Rastreamento de localização
R = True  # Relatórios
solucao_completa = P and E and L and R  # Expressão lógica

# =============================
# FUNÇÕES
# =============================
def cadastrar_produto(nome, categoria, quantidade, preco, localizacao):
    novo = pd.DataFrame({
        "Nome": [nome],
        "Categoria": [categoria],
        "Quantidade": [quantidade],
        "Preço (R$)": [preco],
        "Localização": [localizacao]
    })
    st.session_state.estoque = pd.concat([st.session_state.estoque, novo], ignore_index=True)

def consultar_produtos():
    if not st.session_state.estoque.empty:
        st.dataframe(st.session_state.estoque, use_container_width=True)
    else:
        st.info("Nenhum produto cadastrado ainda.")

def atualizar_estoque(nome, nova_qtd, tipo_movimentacao, responsavel):
    st.session_state.estoque.loc[
        st.session_state.estoque["Nome"] == nome, "Quantidade"
    ] = nova_qtd
    st.session_state.movimentacoes.loc[len(st.session_state.movimentacoes)] = [nome, tipo_movimentacao, nova_qtd, responsavel]

def remover_produto(nome):
    st.session_state.estoque = st.session_state.estoque[st.session_state.estoque["Nome"] != nome]

def gerar_relatorios():
    if not st.session_state.estoque.empty:
        baixo = st.session_state.estoque[st.session_state.estoque["Quantidade"] <= 5]
        if not baixo.empty:
            st.subheader("Produtos com baixo estoque (≤ 5 unidades)")
            st.dataframe(baixo)
        else:
            st.write("Nenhum produto com baixo estoque.")
    else:
        st.info("Sem dados para gerar relatórios.")

# =============================
# INTERFACE PRINCIPAL
# =============================

aba = st.sidebar.radio(
    "Menu",
    ["Dashboard", "Cadastro de Produtos", "Consulta de Produtos", "Movimentar Estoque", "Remover Produtos", "Relatórios", "Tabela Verdade"]
)

# --- DASHBOARD ---
if aba == "Dashboard":
    st.header("Visão Geral do Estoque")

    if not st.session_state.estoque.empty:
        total_produtos = st.session_state.estoque["Nome"].nunique()
        total_quantidade = st.session_state.estoque["Quantidade"].sum()
        valor_total = (st.session_state.estoque["Quantidade"] * st.session_state.estoque["Preço (R$)"]).sum()

        col1, col2, col3 = st.columns(3)
        with col1:
            st.markdown(f"<div class='metric-card'><h3>Total de Produtos</h3><h2>{total_produtos}</h2></div>", unsafe_allow_html=True)
        with col2:
            st.markdown(f"<div class='metric-card'><h3>Quantidade Total</h3><h2>{total_quantidade}</h2></div>", unsafe_allow_html=True)
        with col3:
            st.markdown(f"<div class='metric-card'><h3>Valor Total (R$)</h3><h2>{valor_total:,.2f}</h2></div>", unsafe_allow_html=True)
    else:
        st.info("Nenhum produto cadastrado ainda.")

# --- CADASTRO ---
elif aba == "Cadastro de Produtos":
    st.header("Cadastro de Produto")
    nome = st.text_input("Nome do produto:")
    categoria = st.text_input("Categoria:")
    quantidade = st.number_input("Quantidade:", min_value=0, step=1)
    preco = st.number_input("Preço (R$):", min_value=0.0, step=0.01)
    localizacao = st.text_input("Localização no depósito:")

    if st.button("Salvar Produto"):
        if nome.strip():
            cadastrar_produto(nome, categoria, quantidade, preco, localizacao)
            st.success("Produto cadastrado com sucesso.")
        else:
            st.warning("O nome do produto é obrigatório.")

# --- CONSULTA ---
elif aba == "Consulta de Produtos":
    st.header("Consulta de Produtos")
    consultar_produtos()

# --- MOVIMENTAR ESTOQUE ---
elif aba == "Movimentar Estoque":
    st.header("Movimentar Estoque (Entrada ou Saída)")
    if not st.session_state.estoque.empty:
        produto_sel = st.selectbox("Selecione o produto:", st.session_state.estoque["Nome"])
        nova_qtd = st.number_input("Nova quantidade:", min_value=0, step=1)
        tipo = st.selectbox("Tipo de movimentação:", ["Entrada", "Saída"])
        responsavel = st.text_input("Responsável:")

        if st.button("Registrar Movimentação"):
            atualizar_estoque(produto_sel, nova_qtd, tipo, responsavel)
            st.success(f"Movimentação registrada para o produto {produto_sel}.")
    else:
        st.info("Cadastre produtos antes de movimentar o estoque.")

# --- REMOVER ---
elif aba == "Remover Produtos":
    st.header("Remover Produto")
    if not st.session_state.estoque.empty:
        produto_sel = st.selectbox("Selecione o produto:", st.session_state.estoque["Nome"])
        if st.button("Remover"):
            remover_produto(produto_sel)
            st.success(f"Produto '{produto_sel}' removido com sucesso.")
    else:
        st.info("Nenhum produto cadastrado para remover.")

# --- RELATÓRIOS ---
elif aba == "Relatórios":
    st.header("Relatórios de Estoque")
    gerar_relatorios()
    st.subheader("Histórico de Movimentações")
    if not st.session_state.movimentacoes.empty:
        st.dataframe(st.session_state.movimentacoes, use_container_width=True)
    else:
        st.info("Nenhuma movimentação registrada.")

# --- TABELA VERDADE ---
elif aba == "Tabela Verdade":
    st.header("Tabela Verdade - Requisitos do Sistema")

    tabela = pd.DataFrame({
        "P (Produtos)": [True, True, True, True, False, False, False, False],
        "E (Estoque)": [True, True, False, False, True, True, False, False],
        "L (Localização)": [True, False, True, False, True, False, True, False],
        "R (Relatórios)": [True, False, False, True, True, False, False, True]
    })

    tabela["Solução Completa (P ∧ E ∧ L ∧ R)"] = (
        tabela["P (Produtos)"] & tabela["E (Estoque)"] & tabela["L (Localização)"] & tabela["R (Relatórios)"]
    )

    st.dataframe(tabela, use_container_width=True)
    st.markdown("**Expressão Lógica:** P ∧ E ∧ L ∧ R — verdadeira apenas quando todos os requisitos são atendidos.")
