import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
from datetime import datetime

class AppCompleto:
    def __init__(self, root):
        self.root = root
        self.root.title("App Completo Tkinter")
        self.root.geometry("800x600")
        
        # Criar notebook (abas)
        self.notebook = ttk.Notebook(root)
        self.notebook.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Criar abas
        self.criar_aba_cadastro()
        self.criar_aba_lista()
        self.criar_aba_config()
        
    def criar_aba_cadastro(self):
        # Aba de cadastro
        self.aba_cadastro = ttk.Frame(self.notebook)
        self.notebook.add(self.aba_cadastro, text='Cadastro')
        
        # Formulário
        frame_form = ttk.LabelFrame(self.aba_cadastro, text="Dados Pessoais", padding="15")
        frame_form.pack(fill='x', padx=10, pady=10)
        
        # Campos do formulário
        ttk.Label(frame_form, text="Nome completo:").grid(row=0, column=0, sticky='w', pady=5)
        self.entry_nome = ttk.Entry(frame_form, width=40)
        self.entry_nome.grid(row=0, column=1, pady=5, padx=5)
        
        ttk.Label(frame_form, text="Email:").grid(row=1, column=0, sticky='w', pady=5)
        self.entry_email = ttk.Entry(frame_form, width=40)
        self.entry_email.grid(row=1, column=1, pady=5, padx=5)
        
        ttk.Label(frame_form, text="Idade:").grid(row=2, column=0, sticky='w', pady=5)
        self.entry_idade = ttk.Spinbox(frame_form, from_=0, to=120, width=10)
        self.entry_idade.grid(row=2, column=1, sticky='w', pady=5, padx=5)
        
        ttk.Label(frame_form, text="Cidade:").grid(row=3, column=0, sticky='w', pady=5)
        self.combo_cidade = ttk.Combobox(frame_form, values=["São Paulo", "Rio de Janeiro", "Belo Horizonte", "Porto Alegre"])
        self.combo_cidade.grid(row=3, column=1, sticky='w', pady=5, padx=5)
        
        # Botões
        frame_botoes = ttk.Frame(self.aba_cadastro)
        frame_botoes.pack(pady=10)
        
        ttk.Button(frame_botoes, text="Salvar", command=self.salvar_dados).pack(side='left', padx=5)
        ttk.Button(frame_botoes, text="Limpar", command=self.limpar_formulario).pack(side='left', padx=5)
        
    def criar_aba_lista(self):
        # Aba de lista
        self.aba_lista = ttk.Frame(self.notebook)
        self.notebook.add(self.aba_lista, text='Lista')
        
        # Treeview (tabela)
        columns = ('nome', 'email', 'idade', 'cidade', 'data')
        self.tree = ttk.Treeview(self.aba_lista, columns=columns, show='headings')
        
        # Definir cabeçalhos
        self.tree.heading('nome', text='Nome')
        self.tree.heading('email', text='Email')
        self.tree.heading('idade', text='Idade')
        self.tree.heading('cidade', text='Cidade')
        self.tree.heading('data', text='Data')
        
        # Definir largura das colunas
        self.tree.column('nome', width=150)
        self.tree.column('email', width=150)
        self.tree.column('idade', width=50)
        self.tree.column('cidade', width=100)
        self.tree.column('data', width=120)
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(self.aba_lista, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscroll=scrollbar.set)
        
        self.tree.pack(side='left', fill='both', expand=True, padx=10, pady=10)
        scrollbar.pack(side='right', fill='y')
        
    def criar_aba_config(self):
        # Aba de configurações
        self.aba_config = ttk.Frame(self.notebook)
        self.notebook.add(self.aba_config, text='Configurações')
        
        # Configurações
        frame_config = ttk.LabelFrame(self.aba_config, text="Preferências", padding="15")
        frame_config.pack(fill='x', padx=10, pady=10)
        
        # Checkbuttons
        self.var_notificacoes = tk.BooleanVar(value=True)
        ttk.Checkbutton(frame_config, text="Receber notificações", 
                       variable=self.var_notificacoes).pack(anchor='w', pady=5)
        
        self.var_theme = tk.BooleanVar(value=False)
        ttk.Checkbutton(frame_config, text="Modo escuro", 
                       variable=self.var_theme).pack(anchor='w', pady=5)
        
        # Radio buttons
        frame_radio = ttk.Frame(frame_config)
        frame_radio.pack(fill='x', pady=10)
        
        ttk.Label(frame_radio, text="Tamanho de fonte:").pack(anchor='w')
        
        self.var_font_size = tk.StringVar(value="normal")
        ttk.Radiobutton(frame_radio, text="Pequeno", value="small", 
                       variable=self.var_font_size).pack(anchor='w')
        ttk.Radiobutton(frame_radio, text="Normal", value="normal", 
                       variable=self.var_font_size).pack(anchor='w')
        ttk.Radiobutton(frame_radio, text="Grande", value="large", 
                       variable=self.var_font_size).pack(anchor='w')
        
    def salvar_dados(self):
        nome = self.entry_nome.get()
        email = self.entry_email.get()
        idade = self.entry_idade.get()
        cidade = self.combo_cidade.get()
        
        if not all([nome, email, idade, cidade]):
            messagebox.showerror("Erro", "Preencha todos os campos!")
            return
        
        data = datetime.now().strftime("%d/%m/%Y %H:%M")
        
        # Adicionar à treeview
        self.tree.insert('', 'end', values=(nome, email, idade, cidade, data))
        
        messagebox.showinfo("Sucesso", "Dados salvos com sucesso!")
        self.limpar_formulario()
        
    def limpar_formulario(self):
        self.entry_nome.delete(0, tk.END)
        self.entry_email.delete(0, tk.END)
        self.entry_idade.delete(0, tk.END)
        self.combo_cidade.set('')

if __name__ == "__main__":
    root = tk.Tk()
    app = AppCompleto(root)
    root.mainloop()