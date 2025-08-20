import re
from datetime import datetime

class Cadastro:
    def __init__(self):
        self.usuarios = []
    
    def validar_nome(self, nome):
        """Valida se o nome tem pelo menos 2 caracteres e só contém letras"""
        if len(nome.strip()) < 2:
            return False, "Nome deve ter pelo menos 2 caracteres"
        if not nome.replace(" ", "").isalpha():
            return False, "Nome deve conter apenas letras"
        return True, ""
    
    def validar_email(self, email):
        """Valida formato de email"""
        padrao_email = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        if not re.match(padrao_email, email):
            return False, "Email inválido"
        return True, ""
    
    def validar_senha(self, senha):
        """Valida força da senha"""
        if len(senha) < 6:
            return False, "Senha deve ter pelo menos 6 caracteres"
        if not any(char.isdigit() for char in senha):
            return False, "Senha deve conter pelo menos 1 número"
        if not any(char.isupper() for char in senha):
            return False, "Senha deve conter pelo menos 1 letra maiúscula"
        return True, ""
    
    def validar_data_nascimento(self, data_str):
        """Valida data de nascimento"""
        try:
            data = datetime.strptime(data_str, '%d/%m/%Y')
            if data > datetime.now():
                return False, "Data de nascimento não pode ser futura"
            idade = datetime.now().year - data.year
            if idade < 13:
                return False, "Idade mínima é 13 anos"
            return True, ""
        except ValueError:
            return False, "Data inválida. Use o formato DD/MM/AAAA"
    
    def validar_cpf(self, cpf):
        """Valida CPF (formato básico)"""
        cpf = re.sub(r'\D', '', cpf)
        if len(cpf) != 11:
            return False, "CPF deve ter 11 dígitos"
        if cpf in [s * 11 for s in "0123456789"]:
            return False, "CPF inválido"
        return True, ""
    
    def cadastrar_usuario(self):
        """Interface para cadastro de usuário"""
        print("=== CADASTRO DE USUÁRIO ===")
        
        # Nome
        while True:
            nome = input("Nome completo: ").strip()
            valido, mensagem = self.validar_nome(nome)
            if valido:
                break
            print(f"Erro: {mensagem}")
        
        # Email
        while True:
            email = input("Email: ").strip()
            valido, mensagem = self.validar_email(email)
            if valido:
                break
            print(f"Erro: {mensagem}")
        
        # Senha
        while True:
            senha = input("Senha: ").strip()
            valido, mensagem = self.validar_senha(senha)
            if valido:
                break
            print(f"Erro: {mensagem}")
        
        # Data de nascimento
        while True:
            data_nasc = input("Data de nascimento (DD/MM/AAAA): ").strip()
            valido, mensagem = self.validar_data_nascimento(data_nasc)
            if valido:
                break
            print(f"Erro: {mensagem}")
        
        # CPF (opcional)
        while True:
            cpf = input("CPF (apenas números): ").strip()
            if cpf == "":
                cpf = None
                break
            valido, mensagem = self.validar_cpf(cpf)
            if valido:
                break
            print(f"Erro: {mensagem}")
        
        # Telefone
        telefone = input("Telefone (opcional): ").strip()
        if telefone == "":
            telefone = None
        
        # Salvar usuário
        usuario = {
            'nome': nome,
            'email': email,
            'senha': senha,
            'data_nascimento': data_nasc,
            'cpf': cpf,
            'telefone': telefone,
            'data_cadastro': datetime.now().strftime('%d/%m/%Y %H:%M:%S')
        }
        
        self.usuarios.append(usuario)
        print("\n✅ Cadastro realizado com sucesso!")
        return usuario
    
    def listar_usuarios(self):
        """Lista todos os usuários cadastrados"""
        print("\n=== USUÁRIOS CADASTRADOS ===")
        if not self.usuarios:
            print("Nenhum usuário cadastrado.")
            return
        
        for i, usuario in enumerate(self.usuarios, 1):
            print(f"\nUsuário {i}:")
            for chave, valor in usuario.items():
                if chave == 'senha':
                    valor = '*' * len(valor)  # Oculta a senha
                print(f"  {chave.replace('_', ' ').title()}: {valor}")
    
    def menu(self):
        """Menu principal"""
        while True:
            print("\n" + "="*40)
            print("SISTEMA DE CADASTRO")
            print("="*40)
            print("1. Cadastrar novo usuário")
            print("2. Listar usuários cadastrados")
            print("3. Sair")
            
            opcao = input("\nEscolha uma opção: ").strip()
            
            if opcao == '1':
                self.cadastrar_usuario()
            elif opcao == '2':
                self.listar_usuarios()
            elif opcao == '3':
                print("Saindo do sistema...")
                break
            else:
                print("Opção inválida! Tente novamente.")

# Teste rápido do sistema
if __name__ == "__main__":
    sistema = Cadastro()
    sistema.menu()