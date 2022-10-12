from cache import cache
from ram import ram

def funHash(num): #função que preenche os valores da lista dos dados da cache
    num = num + 53352
    return num

# linhas = {}
dados = {}

for i in range (100):
    dados[i] = funHash(i)
print(dados)

mem = ram(dados)

dadosCache = dados
TagsCache= {}

cacheProcess1 = cache(dadosCache,TagsCache) 
print(mem.dado)
