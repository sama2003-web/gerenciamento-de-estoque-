import streamlit as st
import pandas as pd

# Estilo moderno e limpo
st.markdown("""
    <style>
        body {
            font-family: 'Roboto', sans-serif;
            background-color: #f5f6fa;
            color: #1e272e;
        }
        .stButton>button {
            background-color: #273c75;
            color: white;
            font-weight: bold;
            border-radius: 6px;
            padding: 8px 18px;
            border: none;
        }
        .stButton>button:hover {
            background-color: #192a56;
            color: #f5f6fa;
        }
        .stTextInput>div>div>input, .stNumberInput>div>div>input {
            background-color: #ffffff;
            color: #000000;
        }
        h1, h2, h3 {
            font-family: 'Roboto', sans-serif;
            color: #2f3640;
        }
        table {
            border: 1px solid #dcdde1;
        }
    </style>
""", unsafe_allow_html=True)

st.title("Sistema de Gerenciamento de Estoque - Comércio Eletrônico")

# Inicializa o DataFrame se ainda não existir
if "estoque" not in st.session_state:
    st.session_state.estoque = pd.DataFrame(columns=["Nome", "Categoria", "Quantidade", "Preço (R$)", "Localização", "Disponível"])

# Seção de cadastro
st.header("Cadastro de Produto")
nome = st.text_input("Nome do produto:")
categoria = st.text_input("Categoria:")
quantidade = st.number_input("Quantidade em estoque:", min_value=0, step=1)
preco = st.number_input("Preço (R$):", min_value=0.0, step=0.01)
localizacao = st.text_input("Localização no depósito:")
disponivel = st.checkbox("Produto disponível para venda? (Verdadeiro ou Falso)")

if st.button("Salvar Produto"):
    if nome.strip() != "":
        novo_produto = pd.DataFrame({
            "Nome": [nome],
            "Categoria": [categoria],
            "Quantidade": [quantidade],
            "Preço (R$)": [preco],
            "Localização": [localizacao],
            "Disponível": [disponivel]
        })
        st.session_state.estoque = pd.concat([st.session_state.estoque, novo_produto], ignore_index=True)
        st.success("Produto cadastrado com sucesso.")
    else:
        st.warning("Por favor, insira o nome do produto.")

# Exibir tabela atual
st.header("Tabela de Estoque")
if not st.session_state.estoque.empty:
    st.dataframe(st.session_state.estoque, use_container_width=True)
else:
    st.info("Nenhum produto cadastrado ainda.")

# Atualizar quantidade
st.header("Atualizar Estoque")
if not st.session_state.estoque.empty:
    produto_sel = st.selectbox("Selecione o produto:", st.session_state.estoque["Nome"])
    nova_qtd = st.number_input("Nova quantidade:", min_value=0, step=1)
    if st.button("Atualizar Quantidade"):
        st.session_state.estoque.loc[st.session_state.estoque["Nome"] == produto_sel, "Quantidade"] = nova_qtd
        st.success(f"Quantidade do produto '{produto_sel}' atualizada para {nova_qtd}.")

# Remover produto
st.header("Remover Produto")
if not st.session_state.estoque.empty:
    produto_remover = st.selectbox("Escolha o produto para remover:", st.session_state.estoque["Nome"])
    if st.button("Remover Produto"):
        st.session_state.estoque = st.session_state.estoque[st.session_state.estoque["Nome"] != produto_remover]
        st.success(f"Produto '{produto_remover}' removido com sucesso.")

# Relatórios
st.header("Relatórios de Estoque")
if not st.session_state.estoque.empty:
    baixo_estoque = st.session_state.estoque[st.session_state.estoque["Quantidade"] <= 5]
    if not baixo_estoque.empty:
        st.subheader("Produtos com baixo estoque (≤ 5 unidades)")
        st.dataframe(baixo_estoque)
    else:
        st.write("Nenhum produto com baixo estoque.")
