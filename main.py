from cache import cache
from ram import ram

def funHash(num): #função que preenche os valores da lista dos dados da cache
    num = num + 53352
    return num

dados = {}

for i in range (1024):
    dados[i] = funHash(i)
# hash em ação

memRam = ram(dados)
cacheProcess1 = cache()
print(cacheProcess1.dados)
cacheProcess2 = cache() 
cacheProcess3 = cache() 

resposta = 0
 
resposta = int(input("Escolha qual processador será usado: "))
operacao = input("Escolha qual operação deseja realizar: ")
posicao = int(input("Digite a posição: "))
print(resposta)
if resposta == 1:
    if operacao == "read":
        cacheProcess1.read(posicao,memRam,cacheProcess2,cacheProcess3)
    elif operacao == "write":
        cacheProcess1.write(posicao,memRam,cacheProcess2,cacheProcess3)
elif resposta == 2:
    if operacao == "read":
        cacheProcess2.read(posicao,memRam,cacheProcess1,cacheProcess3)
    elif operacao == "write":
        cacheProcess2.write(posicao,memRam, cacheProcess1,cacheProcess3)
elif resposta == 3:
    if operacao == "read":
        cacheProcess3.read(posicao,memRam, cacheProcess1,cacheProcess2)           
    elif operacao == "write":
        cacheProcess3.write(posicao,memRam, cacheProcess1,cacheProcess2)



#print(memRam.dado)
