from cache import cache
from random import randint
from ram import ram

dados = [[0] for _ in range(1024)]

for i in range (1024):
    dados[i] = randint(0,1000) 
# randint em ação

memRam = ram(dados)
print(memRam.dado)
cacheProcess1 = cache()
cacheProcess2 = cache() 
cacheProcess3 = cache() 



acesso = [[0,0,0] for _ in range(30)]
# acesso[0][0] = 1 numero da cache
# acesso[0][1] = 1 operção
# acesso[0][2] = 1 pos da ram

for i in range(30):
    acesso[i][0] = randint(0,2)
    acesso[i][1] = randint(0,1)
    acesso[i][2] = randint(0,1024)
for j in range(0,30):
    cacheProcess1.fifo(memRam,cacheProcess2,cacheProcess3,acesso,j)

print("CACHE 1")
cacheProcess1.mostrarCache()
print("CACHE 2")
cacheProcess2.mostrarCache()
print("CACHE 3")
cacheProcess3.mostrarCache()
