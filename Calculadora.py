#WinCalc -chat.deepseek.com//Senai25@

import tkinter as tk
def fnAdicao():
    x=float(entryNumero1.get())
    y=float(entryNumero2.get())
    resultado =x+y
    lblResultado.config(text=f'A sua soma é {resultado}')

def fnSubtracao():
    x=float(entryNumero1.get())
    y=float(entryNumero2.get())
    resultado =x-y
    lblResultado.config(text=f'A sua subtração é {resultado}')


def fnMultiplicacao():
    x=float(entryNumero1.get())
    y=float(entryNumero2.get())
    resultado =x*y
    lblResultado.config(text=f'A sua multiplicação é {resultado}')

def fndivisao():
    x=float(entryNumero1.get())
    y=float(entryNumero2.get())
    resultado =x/y
    lblResultado.config(text=f'A sua divisão é {resultado}')


#Tk com T maiúsculo desenha uma janela. O tk minúsculo é o apelido da biblioteca para facilitar na programação.
janela     = tk.Tk()
janela.title("WinCalc - A Super Calculadora")
janela.geometry('850x600') #tamanho da janela.

lblTitulo  = tk.Label(janela,
                    
                      text   ="WinCalc",
                      font   =('verdana',35, 'bold', 'italic'),
                      fg     ='white',
                      bg     ='#2f116e',
                      width  =800,
                      justify='left')
lblTitulo.pack(padx=5,pady=5)

lblNumero1 = tk.Label(janela,
                      text   ='Digite um número:',
                      font   =('calibri',20))
lblNumero1.pack(padx=5,pady  =5)

entryNumero1 = tk.Entry(janela,
                        width=50,
                        font =('calibri',17))
entryNumero1.pack(padx=5,pady=5)

lblNumero2 = tk.Label(janela,
                      text   ='Digite outro número:',
                      font   =('calibri',20))
lblNumero2.pack(padx=5,pady  =5)

entryNumero2 = tk.Entry(janela,
                        width=50,
                        font =('calibri',17))
entryNumero2.pack(padx=5,pady=5)

btnAdicao = tk.Button(janela,
                      text    = 'Adição',
                      width   = 10,
                      bg='white',
                      command = fnAdicao) #o comando vai executar um função e toda função tem que ser criada no começo. Fu~ção é criada através do comendo def.
btnAdicao.pack(padx=5,pady=5)


btnSubtracao = tk.Button(janela,
                      text='Subtração',
                      width=10,
                      bg='white',
                      command= fnSubtracao)
btnSubtracao.pack(padx=5,pady=5)


btnMultiplicacao = tk.Button(janela,
                      text='Multiplicação',
                      width=10,
                      bg='white',
                      command= fnMultiplicacao)
btnMultiplicacao.pack(padx=5,pady=5)


btnDivisao = tk.Button(janela,
                      text='Divisão',
                      width=10,
                      bg='white',
                      command= fndivisao)
btnDivisao.pack(padx=5,pady=5)


lblResultado = tk.Label(janela,
                      text   ='0.00',
                      font   =('calibri',28, 'bold', "underline"),
                      fg="white",
                      bg='#2f116e')
lblResultado.pack(padx=5,pady  =5)











janela.mainloop()#mantém o programa rodando.