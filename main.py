from cache import cache
from ram import ram

def funHash(num): #função que preenche os valores da lista dos dados da cache
    num = num + 53352
    return num

dados = {}

for i in range (1024):
    print(i)
    dados[i] = funHash(i)
# print(dados)

memRam = ram(dados)

cacheProcess1 = cache()
cacheProcess2 = cache() 
cacheProcess3 = cache() 

print(memRam.dado)
