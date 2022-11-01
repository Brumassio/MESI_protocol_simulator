class cache:
    def __init__(self):
        self.dados = [[0,0,0,0] for _ in range(32)]
        self.tamBloco = 4   #tamanho do bloco
        self.linhaCache = 32  #armazena o tamanho da linha da cache
        self.ocupado = [0] * 32 #verifica se a linha da cache está ocupada
        self.tag = [0] *32  # tag da linha da cache
        self.armzIndice  = [] #atributo utlizado para o writeback


    #função que realiza o writeBack
    def writeBack(self, RAM, indice):
        for i in range(4):
            if self.tag[indice][i] == 'modify':
                RAM.dado[indice] = self.dados[i]


    def verificaCache(self):
        for i in self.linhaCache:
            if self.ocupado[i] == 0:
                return i     
        return -2

    #printa as caches
    def mostrarCache(self):
        for i in range(self.linhaCache):
            print("Linha da cache: ",i)
            for j in  range(self.tamBloco):
                print("pos do bloco %d: %d" %(j,self.dados[i][j]))   
       

    # acha os índices para as operações read e write
    def acharIndice(self,pos): 
        posBloco = pos % self.tamBloco
        linCache = pos//self.tamBloco
        return linCache, posBloco 
        



    # vai armazenar o bloco(4 linhas da ram) em uma linha da cache de acordo com as posições calculadas posteriormente 
    def blocoTotal(self,linCache, posBloco, pos, RAM):
        if posBloco == 0:
            self.dados[linCache][posBloco] = RAM.leituraRAM(pos)
            self.dados[linCache][posBloco+1] = RAM.leituraRAM(pos+1)
            self.dados[linCache][posBloco+2] = RAM.leituraRAM(pos+2)
            self.dados[linCache][posBloco+3] = RAM.leituraRAM(pos+3)
        elif posBloco == 1:
            self.dados[linCache][posBloco-1] = RAM.leituraRAM(pos-1)
            self.dados[linCache][posBloco] = RAM.leituraRAM(pos)
            self.dados[linCache][posBloco+1] = RAM.leituraRAM(pos+1)
            self.dados[linCache][posBloco+2] = RAM.leituraRAM(pos+2)
        elif posBloco == 2: 
            self.dados[linCache][posBloco-2] = RAM.leituraRAM(pos-2)
            self.dados[linCache][posBloco-1] = RAM.leituraRAM(pos-1)
            self.dados[linCache][posBloco] = RAM.leituraRAM(pos)
            self.dados[linCache][posBloco+1] = RAM.leituraRAM(pos+1)
        elif posBloco == 3:
            self.dados[linCache][posBloco-3] = RAM.leituraRAM(pos-3)
            self.dados[linCache][posBloco-2] = RAM.leituraRAM(pos-2)
            self.dados[linCache][posBloco-1] = RAM.leituraRAM(pos-1)
            self.dados[linCache][posBloco] = RAM.leituraRAM(pos)

    def read(self,pos, RAM, cache2, cache3):
        linCache = 0
        posBloco = 0
        linCache, posBloco = self.acharIndice(pos)
        if int(self.dados[linCache][posBloco]) == int(RAM.leituraRAM(pos)):
            #READ HIT
            print("READ HIT :",self.dados[linCache][posBloco])
            return self.dados[linCache][posBloco]
        #READ MISS 
        #lança o bloco todo na linha da cache
        self.blocoTotal(linCache,posBloco, pos, RAM)
        if self.dados[linCache][posBloco] == cache2.dados[linCache][posBloco]:
            cache2.tag[linCache] = "shared"
        else:
            cache2.tag[linCache] = "invalid"
        if self.dados[linCache][posBloco] == cache3.dados[linCache][posBloco]:
            cache3.tag[linCache] = "shared"
        else: 
            cache3.tag[linCache] = "invalid"        
        return -1
       

    def buscaElem(self,elem):
        for i in range(self.linhaCache):
            for j in range(self.tamBloco):
                if self.dados[i][j] == elem:
                    return 1
        return -1   


    def write(self, pos,RAM,cache2,cache3):
        linCache = 0
        posBloco = 0 
        linCache, posBloco = self.acharIndice(pos)
        
        #WRITE HIT
        if self.buscaElem(self.dados[linCache][posBloco] == 1):
            if self.tag[linCache] == "shared":
                if cache2.dados[linCache][posBloco] == self.dados[linCache][posBloco]:
                    cache2.tag[pos] = "invalid"
                if cache3.dados[linCache][posBloco] == self.dados[linCache][posBloco]:
                    cache3.tag[pos] = "invalid"
            elif self.tag[linCache] == "exclusive":
                self.tag[linCache] = "modify"
        #Write Miss
        else:  
            self.dados[linCache][posBloco] = RAM.leituraRAM(pos)
            if cache2.dados[linCache][posBloco] == self.dados[linCache][posBloco]:
                cache2.tag[pos] = "invalid"
            if cache3.dados[linCache][posBloco] == self.dados[linCache][posBloco]:
                cache3.tag[pos] = "invalid"

        
    def fifo(self,RAM,cache2,cache3,acess,i):
        if acess[i][0] == 0:  # se o processador do acesso for o segundo

            if acess[i][1] == 0:  # verifica qual operação será executada
                self.read(acess[i][2],RAM,cache2,cache3)
            elif acess[i][1] == 1:
                for j in range(self.linhaCache):
                    if self.ocupado[j] == 1:
                        self.armzIndice.append(j) 
    # se a cache está lotada ela libera a primeira linha da cache   
                if len(self.armzIndice) == 32: 
                    armz = self.armzIndice.pop(0)
                    self.writeBack(RAM,0)
                    return armz 
                self.write(acess[i][2],RAM,cache2,cache3)
        
        elif acess[i][0] == 1: # se o processador do acesso for o segundo
            

            if acess[i][1] == 0: #escrita
                cache2.read(acess[i][2],RAM,self,cache3)
            elif acess[i][1] == 1: #leitura
                for j in range(cache2.linhaCache):
                    if cache2.ocupado[j] == 1:
                        cache2.armzIndice.append(j)
            # se a cache está lotada ela libera a primeira linha da cache         
                if len(cache2.armzIndice) == 32:
                    armz = cache2.armzIndice.pop(0)
                    cache2.writeBack(RAM,0)
                    return armz                
                cache2.write(acess[i][2],RAM,self,cache3) 
                 

        elif acess[i][0] == 2: # se o processador do acesso for o terceiro

            if acess[i][1] == 0: #leitura
                cache3.read(acess[i][2], RAM, self, cache2)

            elif acess[i][1] == 1: #escrita

                for j in range(cache2.linhaCache):
                    if cache3.ocupado[j] == 1:
                        cache3.armzIndice.append(j)
            # se a cache está lotada ela libera a primeira linha da cache 
                if len(cache3.armzIndice) == 32:
                    armz = cache3.armzIndice.pop(0)
                    cache3.writeBack(RAM,0)
                    return armz                
                cache3.write(acess[i][2],RAM,self,cache2)      

             
                                                                        
        