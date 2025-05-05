import streamlit as st
from fpdf import FPDF
import uuid
from io import BytesIO

st.set_page_config(page_title="PitchGPT - Gerador de Apresentações de Vendas", layout="wide")

# Estilos de página
st.markdown("""
    <style>
        .main {
            background-color: #f9f9fb;
        }
        .stButton>button {
            background-color: #4CAF50;
            color: white;
            border-radius: 8px;
        }
        .stSlider>div>div {
            color: #4CAF50;
        }
        .premium {
            color: #e53935;
            font-weight: bold;
        }
    </style>
""", unsafe_allow_html=True)

# Título
st.markdown("""
    <div style='padding: 1rem; background-color: #e0f2f1; border-left: 5px solid #00796b; border-radius: 8px;'>
        <h2>🚀 PitchGPT - Crie sua Apresentação de Vendas em Minutos!</h2>
        <p>Responda algumas perguntas e receba um pitch incrível para seu produto ou serviço.</p>
    </div>
""", unsafe_allow_html=True)

# Função para sugerir público-alvo com base no produto
def sugerir_publico(produto):
    sugestoes = {
        "tecnologia": ["Desenvolvedores de software", "Empresas de TI", "Startups tecnológicas", "Entusiastas de tecnologia"],
        "saúde": ["Profissionais de saúde", "Consultórios médicos", "Pacientes interessados em tratamentos", "Clínicas de estética"],
        "moda": ["Fashionistas", "Lojas de roupas", "Influenciadores de moda", "Público jovem e antenado"],
        "educação": ["Professores", "Alunos de diferentes idades", "Instituições de ensino", "EAD e cursos online"],
        "beleza": ["Salões de beleza", "Influenciadores de beleza", "Marcas de cosméticos", "Consumidores de produtos de cuidado pessoal"]
    }
    
    for chave in sugestoes:
        if chave in produto.lower():
            return sugestoes[chave]
    
    return ["Público geral", "Entusiastas", "Clientes potenciais"]

# Formulário de entrada de dados
st.markdown("### 💡 Diga-nos mais sobre seu produto ou ideia:")

with st.form("pitch_form"):
    produto = st.text_input("Nome do Produto ou Serviço:")
    publico_alvo = st.text_input("Quem é o público-alvo? (Opcional):")
    problema = st.text_area("Qual problema seu produto/serviço resolve?")
    solucao = st.text_area("Qual é a solução que seu produto/serviço oferece?")
    diferenciais = st.text_area("Quais são os diferenciais do seu produto/serviço?")
    preco = st.text_input("Qual é o preço do produto (opcional):")

    # Sugestão de público-alvo se o usuário não inserir
    if not publico_alvo:
        publico_sugerido = sugerir_publico(produto)
        st.markdown(f"🔍 **Sugestões de Público-alvo para o produto '{produto}':**")
        st.write(", ".join(publico_sugerido))
    
    submit = st.form_submit_button("Gerar Pitch")

# Função para criar o pitch
def gerar_pitch(produto, publico_alvo, problema, solucao, diferenciais, preco):
    pitch = f"""
    **Produto:** {produto}

    **Público-alvo:** {publico_alvo}

    **Problema:** {problema}

    **Solução:** {solucao}

    **Diferenciais:** {diferenciais}

    **Preço:** {preco if preco else 'Não informado'}
    """
    
    # A estrutura do Pitch - AIDA (Atenção, Interesse, Desejo, Ação)
    pitch_completo = f"""
    ## 🚀 Pitch de Vendas

    ### Atraia Atenção:
    **{produto}** vai transformar a vida de **{publico_alvo}**!

    ### Gere Interesse:
    O problema de **{publico_alvo}** é **{problema}**, e a solução ideal é **{produto}**, que oferece **{solucao}**.

    ### Desperte o Desejo:
    Com **{produto}**, você vai poder [resolver o problema] e se beneficiar de **{diferenciais}**.

    ### Chame para Ação:
    Não perca a chance de melhorar sua vida com **{produto}** por apenas **{preco if preco else 'Preço a consultar'}**.
    """

    return pitch_completo

# Gerar pitch
if submit and produto:
    pitch_gerado = gerar_pitch(produto, publico_alvo, problema, solucao, diferenciais, preco)
    st.markdown("### ✨ Seu Pitch de Vendas:")
    st.markdown(pitch_gerado)

    # Exportar para PDF
    class PDF(FPDF):
        def header(self):
            self.set_font("Arial", "B", 14)
            self.cell(0, 10, "Pitch de Vendas Gerado", ln=True, align="C")

        def add_pitch(self, pitch):
            self.set_font("Arial", size=12)
            self.multi_cell(0, 10, pitch)

    pdf = PDF()
    pdf.add_page()
    pdf.add_pitch(pitch_gerado)

    # Gerar PDF em memória
    buffer = BytesIO()
    pdf.output(buffer)
    buffer.seek(0)

    st.download_button("📄 Baixar Pitch em PDF", buffer, file_name="pitch_de_vendas.pdf")

    st.success("🚀 Seu Pitch foi gerado com sucesso!")
 
