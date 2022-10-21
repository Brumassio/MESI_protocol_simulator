class cache:
    def __init__(self):
        self.dados = [0,0,0,0]*32
        self.tamBloco = 4
        self.linhaCache = 3
        self.ocupado = 0
        self.tag = [0]*32
        self.armzIndice  = []
        # TAG pode ser:  modify – exclusive – shared – invalid

    def writeBack(self, RAM, indice):
        for i in range(4):
            if self.tag[indice][i] == 'modify':
                RAM.dado[indice] = self.dados[i]

    def verificaCache(self):
        for i in self.linhaCache:
            if self.ocupado[i] == 0:
                return i     
        return 1

    def mostrarCache(self):
        for i in range(self.linhaCache):
            if self.ocupado[i] == 1:
                print("linha:" + i + 1)
            else: return
            for j in  range(self.tamBloco):
                print("pos do bloco %d: %d" %(j,self.dados[i][j]))   
 
       
    # def inicializaCache(self):
    #     for i in range(self.linhaCache):
    #         for j in range(self.tamBloco):
    #             self.tag[i][j] = "invalid"

    def acharIndice(self,pos): 
        posBloco = pos % self.tamBloco
        linCache = pos//self.tamBloco
        return linCache, posBloco 
        

    # def readMiss(self, pos, RAM):
    #     linCache = 0
    #     posBloco = 0
    #     linCache, posBloco = self.acharIndice(pos)
    #     if self.tag[i][j] == "invalid" or  self.tag[i][j] == "modify":
    #         self.dados[i][j] = RAM.leituraRam(pos)

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
        if self.dados[linCache][posBloco] == RAM.leituraRAM(pos):
            #READ HIT
            print("READ HIT :",self.dados[linCache][posBloco])
            return self.dados[linCache][posBloco]
        #READ MISS 
        #lança o bloco todo na linha da cache
        self.blocoTotal(linCache,posBloco, pos, RAM)
        if self.dados[linCache][posBloco] == cache2.dados[linCache][posBloco]:
            cache2.tag[pos] = "shared"
        else:
            cache2.tag[pos] = "invalid"
        if self.dados[linCache][posBloco] == cache3.dados[linCache][posBloco]:
            cache3.tag[pos] = "shared"
        else: 
            cache3.tag[pos] = "invalid"        
        return -1
       

    def write(self, pos,RAM):
        linCache = 0
        posBloco = 0 
        linCache, posBloco = self.acharIndice(pos)
        self.dados[linCache][posBloco] = RAM.leituraRAM(pos)
        if self.tag[linCache][posBloco] == "shared":
            return -2
        elif self.tag[linCache][posBloco] == "exclusive":
            self.tag[linCache][posBloco] = "modify"
            return -3

            
        
    def fifo(self):
        for i in range(self.linhaCache):
            if self.ocupado[i] == 1:
                self.armzIndice.append(i)
                
        if self.armzIndice[31] == 32:
            armz = self.armzIndice.pop(0)
            return armz 
        # testando operações, arrumar o fifo dps    
        if self.read() == -1:
            print("HEY VINI VAI TOMA NO CU")
        #testando operações de escrita da cache
                                                                                                              
        