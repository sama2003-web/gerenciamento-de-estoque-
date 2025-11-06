import streamlit as st

# Título da aplicação
st.title("🛒 Sistema de Gerenciamento de Estoque - Comércio Eletrônico")

# Seção de entrada de dados
st.header("Adicionar novo produto")
nome = st.text_input("Nome do produto:")
quantidade = st.number_input("Quantidade em estoque:", min_value=0, step=1)
preco = st.number_input("Preço (R$):", min_value=0.0, step=0.01)

# Seção de controle de disponibilidade (Verdadeiro ou Falso)
disponivel = st.checkbox("Produto disponível para venda?")
st.write("Disponibilidade:", "✅ Verdadeiro" if disponivel else "❌ Falso")

# Botão para salvar
if st.button("Salvar Produto"):
    if nome:
        st.success(f"Produto '{nome}' salvo com sucesso!")
        st.write("📦 Dados do produto:")
        st.write({
            "Nome": nome,
            "Quantidade": quantidade,
            "Preço": preco,
            "Disponível": disponivel
        })
    else:
        st.error("Por favor, insira o nome do produto!")
