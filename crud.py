#crud programa que faz cadastro,onde as ações são cadastrar,pesquisar,excluir
#ao desligar o crud tudo apaga,perde a memoria pq nao tem BD,tem um dicionario
#Sistema de cadastro de pets(add,editar,remover,limpar) frontend
#grid linhas e colunas//grade
#colchete [] =lista-exemplo? animais =['cao','gato','rato'];print (animais[posicao])
#chaves {} = dicionario -exemplo pessoa ={"nome":"Gilberto","idade":49}

import tkinter as tk #ferramentas basicas
from tkinter import ttk,messagebox

#carregar pets
def carregar_pets():
    for item in tree.get_children():
        tree.delete(item)
    for pet in pets:
        tree.insert('', 'end', values=(pet['ID'],
             pet['Tutor'],pet['Nome'], pet['Espécie'],pet['Raça'],pet['Idade']))
        
#adicionar pets
def adicionar_pet():
    global next_pet_id
    Tutor = entry_tutor.get()
    Nome = entry_Nome.get()
    Espécie =entry_Especie.get()
    Raça =entry_Raca.get()
    Idade =entry_Idade.get()
    
    if not Tutor or not Nome:
        messagebox.showerror("Erro", "Tutor e nome pet são obrigatórios!")
        return
    
    try:
        Idade_int = int(Idade) if Idade else 0
    except ValueError:
        messagebox.showerror("Erro", "Idade deve ser um numero inteiro!")
        return
    novo_pet ={'ID': next_pet_id,'Tutor': Tutor,'Nome': Nome,'Espécie': Espécie,'Raça':Raça,'Idade':Idade_int}
    
    pets.append(novo_pet)
    next_pet_id +=1
    
    messagebox.showinfo("Sucesso", "Pet cadastrado com sucesso!")
    limpar_campos()
    carregar_pets()

def selecionar_pet(event):
    selected_item = tree.selection()
    if not selected_item:
        return
    
    values = tree.item(selected_item)['values']
    limpar_campos()
    
    entry_tutor.insert(0, values[1])
    entry_Nome.insert(0,values[2])
    entry_Especie.insert(0, values[3])
    entry_Raca.insert(0,values[4])
    entry_Idade.insert(0,str(values[5]))
    
def limpar_campos():
    entry_tutor.delete(0, 'end')
    entry_Nome.delete(0,'end')
    entry_Especie.delete(0,'end')
    entry_Raca.delete(0,'end')
    entry_Idade.delete(0,'end')
    
def editar_pet():
    selected_item = tree.selection()
    if not selected_item:
        messagebox.showerror("Erro", "Selecione um pet para editar!")
        return
    pet_id = tree.item(selected_item)['values'][0]
    tutor =entry_tutor.get()
    nome =entry_Idade.get()
    especie = entry_Especie.get()
    raca= entry_Raca.get()
    idade =entry_Idade.get()
    
    if not tutor or not nome:
        messagebox.showerror("Erro", "Tutor e nome do pet são obrigatórios!")
        return
    try:
        idade_int = int(idade) if idade else 0
    except ValueError:
        messagebox.showerror("Erro", "Idade deve ser um numero inteiro!")
        return
    
    for pet in pets:
        if pet['id']== pet_id:
           pet.updade({'tutor': tutor,'nome':nome,'especie':especie,'raca':raca,'idade':idade_int})
           break
       
    messagebox.showinfo("Sucesso", "Pet atualizado com sucesso!")
       
    carregar_pets()
    
def remover_pet():  
    selected_item = tree.selection()
    if not selected_item:
        messagebox.showerror("Erro","selecione um pet para remover!")  
        return
    
    pet_id =tree.item(selected_item)['values'][0]
    
    if messagebox.askyesno("Confirmação", "Tem certeza que deseja remover este pet?"):
        global pets
        pets = [pet for pet in pets if pet['ID'] !=pet_id]
        messagebox.showinfo("Sucesso","Pet removido com sucesso!")
        
    limpar_campos()
    carregar_pets()
        
        

        

#dados em memoria
pets =[] #criando a lista vazia/estrutura da lista =[]/print (animais[posicao])
next_pet_id =1 #contador

#Configuracao da janela principal
root =tk.Tk()
root.title("Sistema de Cadastro de Pets")
root.geometry("800x500")

#frame do formulario
frame_form = ttk.LabelFrame(root, text="Formulário de Pets")
frame_form.pack(padx=10, pady=5, fill= 'x')

#Campos do formulario
#dados dos pets:nome,especie,raça 

ttk.Label(frame_form,text ="Tutor:").grid(row=0,column=0,padx=5,pady=5,sticky='e')
entry_tutor =ttk.Entry(frame_form, width=40)
entry_tutor.grid(row=0,column=1,padx=5, pady=5) 

ttk.Label(frame_form,text ="Nome:").grid(row=1,column=0,padx=5,pady=5,sticky='e')
entry_Nome =ttk.Entry(frame_form, width=40)
entry_Nome.grid(row=1,column=1,padx=5, pady=5)      

ttk.Label(frame_form,text ="Espécie:").grid(row=2,column=0,padx=5,pady=5,sticky='e')
entry_Especie =ttk.Entry(frame_form, width=40)
entry_Especie.grid(row=2,column=1,padx=5, pady=5)

ttk.Label(frame_form,text ="Raça:").grid(row=3,column=0,padx=5,pady=5,sticky='e')
entry_Raca =ttk.Entry(frame_form, width=40)
entry_Raca.grid(row=3,column=1,padx=5, pady=5)

ttk.Label(frame_form,text ="Idade:").grid(row=4,column=0,padx=5,pady=5,sticky='e')
entry_Idade =ttk.Entry(frame_form, width=40)
entry_Idade.grid(row=4,column=1,padx=5, pady=5)


#Frame de botões
frame_botoes = ttk.Frame(root)
frame_botoes.pack(pady=5)

btn_adicionar = ttk.Button(frame_botoes,text ="Adicionar",command= adicionar_pet)
btn_adicionar.grid(row=0, column=0, padx=5)

btn_editar = ttk.Button(frame_botoes,text ="Editar",command=None)
btn_editar.grid(row=0, column=1, padx=5)

btn_remover = ttk.Button(frame_botoes,text ="Remover",command=remover_pet)
btn_remover.grid(row=0, column=2, padx=5)

btn_limpar = ttk.Button(frame_botoes,text ="Limpar",command=limpar_campos)
btn_limpar.grid(row=0, column=3, padx=5)

#tabela de pets /heading é o cabeçalho
frame_tabela = ttk.Frame(root)
frame_tabela.pack(padx=10, pady=5, fill='both', expand=True)

tree =ttk.Treeview(frame_tabela,columns=('ID', 'Tutor','Nome','Espécie','Raça','Idade'), show='headings')
tree.heading('ID', text='ID')
tree.heading('Tutor', text='Tutor')
tree.heading('Nome', text='Nome')
tree.heading('Espécie', text='Espécie')
tree.heading('Raça', text='Raça')
tree.heading('Idade', text='Idade')

#criando as colunascom seus tamanhos na horizontal
tree.column('ID', width=50)
tree.column('Tutor', width=150)
tree.column('Nome', width=100)
tree.column('Espécie', width=100)
tree.column('Raça',width=100)
tree.column('Idade', width=50)

#scrollbar -barra de rolagem na vertical
scrollbar =ttk.Scrollbar(frame_tabela,
                orient ='vertical',
                command =tree.yview)
tree.configure(yscrollcommand=scrollbar.set)

tree.pack(side='left',fill='both',
                expand=True)
scrollbar.pack(side='right',fill='y')

tree.bind('<<TreeviewSelect>>', selecionar_pet)
#bind fica monitorando os eventos no treeviewSelect,ele captura e mostra oq tem que ser feito
#e fica a linha azul ao selecionar uma linha com os dados cadastrado do pet.




                
root.mainloop()
