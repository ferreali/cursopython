#Montar um programa que peça 4 notas de um aluno
#nota1 = float (input("Informe a nota1:"))
'''if(nota1 > 10):
   nota1 = float(input("Erro.Digite a nota 1:")) aqui ele pede para ficar digitando a nota certa'''
   

while True:
    nota1 =float(input("Digite a nota1: "))
    if (nota1 <= 10) and (nota1 >= 0):
     break 
   
print("Primeira nota,",nota1) 


while True:
    nota2 =float(input("Digite a nota2: "))
    if (nota2 <= 10) and (nota2 >= 0):
     break  
print("Segunda nota,",nota2) 

while True:
    nota3 =float(input("Digite a nota3: "))
    if (nota3 <= 10) and (nota3 >= 0):
     break  
print("Terceira nota,",nota3) 

while True:
    nota4 =float(input("Digite a nota4: "))
    if (nota4 <= 10) and (nota4 >= 0):
     break  
print("Quarta nota,",nota4) 

media = (nota1 + nota2 + nota3 + nota4) /4

#saida de dados
print (f"sua média é {media:,.2f}")#f no inicio é para mostrar que vai usar uma variavel entre chaves,f string
#2f é a formatacao dos numeros com 2 casas decimais em um numero float,separado pela virgula
#estrutura de comandos ordem: if -elif -else,entretanto pode usar varios elifs

if(media >= 5):
            print("Aluno APROVADO !!!")
elif(media <= 3):
            print("Aluno em Recuperação")
else:
            print("Aluno REPROVADO")
print("fim do ano letivo")
            

                   




    
                
                
                
            
