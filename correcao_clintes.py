import streamlit as st #cria ambiente web para rodar no navegador
import datetime #retorna datetime
import re
import json #recuperar e gravar dados na json
import os # funcao do S.O
from datetime import datetime

# Nome do arquivo JSON
ARQUIVO_DADOS = "clientes.json"

#funcoes para manipulacao do arquivo JSON

def carregar_dados():
    if os.path.exists(ARQUIVO_DADOS):#verifica se o arquivo JSON existe
        with open(ARQUIVO_DADOS, "r", encoding="utf-8") as f:#utf-8 tabela de caracteres que o Brasil usa
            return json.load(f)
    return {}

def salvar_dados(dados):#pega os dados da memoria e grava no arquivo json permanente
    with open(ARQUIVO_DADOS, "w", encoding="utf-8") as f:
        json.dump(dados, f, ensure_ascii=False, indent=4)

def criar_cliente(nome, RG, CPF, Nascimento, telefone, email):#só monta e estrutura de dicionario
    return {
        "Nome": nome,
        "RG": RG,
        "CPF": CPF,
        "Nascimento": str(Nascimento),
        "telefone": telefone,
        "email": email,
        "data_cadastro": str(datetime.date.today()),
        "historico_clientes": []
    }

def validar_rg(rg):
    """Função para validar o formato do RG"""
    padrao = r'^[0-9]{2}\.?[0-9]{3}\.?[0-9]{3}-?[0-9A-Za-z]{1}$'
    return re.match(padrao, rg) is not None

def formatar_rg(rg):
    """Formata o RG para o padrão XX.XXX.XXX-X"""
    rg_limpo = re.sub(r'[^0-9A-Za-z]', '', rg)
    
    if len(rg_limpo) < 9:
        return rg_limpo
    
    rg_formatado = f"{rg_limpo[:2]}.{rg_limpo[2:5]}.{rg_limpo[5:8]}-{rg_limpo[8:]}"
    return rg_formatado

def cadastrar_clientes():
    st.title("📝 Formulário de Cadastro ERP Clientes")

    with st.form(key='formulario_cadastro'):#cria o formulario com varias informacoes
        nome = st.text_input("Nome Completo*", max_chars=100)
        rg = st.text_input("RG (Registro Geral)*", max_chars=12,
                          help="Formato: XX.XXX.XXX-X (pontos e hífen são opcionais)")
        cpf = st.text_input("CPF*", max_chars=14,
                           help="Formato: XXX.XXX.XXX-XX")
        
        data_minima = datetime.date(1900, 1, 1)
        data_maxima = datetime.date(2100, 12, 31)
        data_nascimento = st.date_input("Data de Nascimento*", format="DD/MM/YYYY", 
                                      min_value=data_minima, max_value=data_maxima)
        
        st.write('Fale um pouco sobre você')
        bio = st.text_area('')
        
        telefone = st.text_input("Telefone")
        email = st.text_input("E-mail")
        
        enviar = st.form_submit_button("Enviar Cadastro")
        
        if enviar:
            if not nome or not rg or not cpf:
                st.error("Campos com * são obrigatórios!")
                return
                
            if not validar_rg(rg):
                st.error("RG inválido! Formato esperado: XX.XXX.XXX-X")
                return
                
            dados = carregar_dados()
            
            if cpf in dados:
                st.error("CPF já cadastrado!")
                return
                
            rg_formatado = formatar_rg(rg)
            novo_cliente = criar_cliente(nome, rg_formatado, cpf, data_nascimento, telefone, email)
            
            if bio:
                novo_cliente["historico_clientes"].append(bio)
                
            dados[cpf] = novo_cliente
            salvar_dados(dados)
            st.success("Cliente cadastrado com sucesso!")

def listar_clientes():
    st.subheader("Lista de Clientes Cadastrados")
    
    dados = carregar_dados()
    
    if not dados:
        st.info("Nenhum cliente cadastrado ainda.")
        return
    
    filtro_nome = st.text_input("Filtrar por nome:")
    
    clientes_filtrados = []
    for cpf, cliente in dados.items():
        if filtro_nome.lower() in cliente["Nome"].lower():
            clientes_filtrados.append((cpf, cliente))
    
    if not clientes_filtrados:
        st.warning("Nenhum cliente encontrado com o filtro aplicado.")
        return
    
    for cpf, cliente in clientes_filtrados:
        with st.expander(f"{cliente['Nome']} - CPF: {cpf}"):
            col1, col2 = st.columns(2)
            
            with col1:
                st.write(f"**RG:** {cliente['RG']}")
                st.write(f"**Data de Nascimento:** {cliente['Nascimento']}")
                
            with col2:
                st.write(f"**Telefone:** {cliente['telefone']}")
                st.write(f"**E-mail:** {cliente['email']}")
                st.write(f"**Cadastrado em:** {cliente['data_cadastro']}")
            
            if cliente["historico_clientes"]:
                st.write("**Histórico Cliente:**")
                for item in cliente["historico_clientes"]:
                    st.write(f"- {item}")

def editar_clientes():
    st.subheader("Editar Clientes")
    
    dados = carregar_dados()
    
    if not dados:
        st.info("Nenhum cliente cadastrado para editar.")
        return
    
    cpf_selecionado = st.selectbox(
        "Selecione o cliente pelo CPF",
        options=list(dados.keys()),
        format_func=lambda x: f"{dados[x]['Nome']} - {x}"
    )
    
    cliente = dados[cpf_selecionado]
    
    with st.form(key="form_edicao"):
        col1, col2 = st.columns(2)
        
        with col1:
            novo_cpf = st.text_input("CPF", value=cliente["CPF"], max_chars=14)
            nome = st.text_input("Nome Completo", value=cliente["Nome"])
            rg = st.text_input("RG", value=cliente["RG"])
            data_nascimento = st.text_input("Data de Nascimento", value=cliente["Nascimento"])
            
        with col2:
            telefone = st.text_input("Telefone", value=cliente["telefone"])
            email = st.text_input("E-mail", value=cliente["email"])
            
        submit_button = st.form_submit_button("Atualizar Cliente")
    
    if submit_button:
        if not novo_cpf or not nome:
            st.error("CPF e Nome são campos obrigatórios!")
            return
        
        if novo_cpf != cpf_selecionado and novo_cpf in dados:
            st.error("Já existe um cliente com este novo CPF!")
            return
        
        if novo_cpf != cpf_selecionado:
            dados.pop(cpf_selecionado)
        
        cliente_atualizado = {
            "Nome": nome,
            "RG": rg,
            "CPF": novo_cpf,
            "Nascimento": data_nascimento,
            "telefone": telefone,
            "email": email,
            "data_cadastro": cliente["data_cadastro"],
            "historico_clientes": cliente["historico_clientes"]
        }
        
        dados[novo_cpf] = cliente_atualizado
        salvar_dados(dados)
        st.success("Cliente atualizado com sucesso!")

def excluir_clientes():
    st.subheader("Excluir Clientes")
    
    dados = carregar_dados()
    
    if not dados:
        st.info("Nenhum cliente cadastrado para excluir.")
        return
    
    cpf_selecionado = st.selectbox(
        "Selecione o cliente pelo CPF para excluir",
        options=list(dados.keys()),
        format_func=lambda x: f"{dados[x]['Nome']} - {x}"
    )
    
    cliente = dados[cpf_selecionado]
    
    st.warning("Você está prestes a excluir o seguinte cliente:")
    st.json(cliente)
    
    if st.button("Confirmar Exclusão"):
        dados.pop(cpf_selecionado)
        salvar_dados(dados)
        st.success("Cliente excluído com sucesso!")

# Menu lateral
st.sidebar.title("Menu")
opcao = st.sidebar.radio("Selecione uma opção:", 
                        ("Cadastrar Clientes", "Listar Clientes", "Editar Clientes", "Excluir Clientes"))

# Navegação entre páginas
if opcao == "Cadastrar Clientes":
    cadastrar_clientes()
elif opcao == "Listar Clientes":
    listar_clientes()
elif opcao == "Editar Clientes":
    editar_clientes()
elif opcao == "Excluir Clientes":
    excluir_clientes()

# Rodapé
st.sidebar.markdown("---")  
st.sidebar.markdown("Desenvolvido por Alini Ferreira Alexandre") 
st.sidebar.markdown(f"Total de clientes: {len(carregar_dados())}")