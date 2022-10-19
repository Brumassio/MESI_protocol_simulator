class cache:
    def __init__(self):
        self.dados = [0,0,0,0]*32
        self.tamBloco = 4
        self.linhaCache = 3
        self.ocupado = 0
        self.tag = [0,0,0,0]*32
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

    def fifo(self):
        for i in range(self.linhaCache):
            if self.ocupado[i] == 1:
                self.armzIndice.append(i)
                
        if self.armzIndice[31] == 32:
            armz = self.armzIndice.pop(0)
            return armz 
       
    # def inicializaCache(self):
    #     for i in range(self.linhaCache):
    #         for j in range(self.tamBloco):
    #             self.tag[i][j] = "invalid"
    def acharIndice(self,pos): 
        posBloco = pos % self.tamBloco
        linCache = pos//self.tamBloco
        return posBloco, linCache 
        

    def readMiss(self, pos, RAM):
        linCache = 0
        posBloco = 0
        linCache, posBloco = self.acharIndice(pos)
        if self.tag[i][j] == "invalid" or  self.tag[i][j] == "modify":
            self.dados[i][j] = RAM.leituraRam(pos)
                

    def read(self,pos, RAM):
        linCache = 0
        posBloco = 0
        linCache, posBloco = self.acharIndice(pos)

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

            
        
                                                                                                                                
        