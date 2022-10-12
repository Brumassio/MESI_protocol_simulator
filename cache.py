class cache:
    def __init__(self, dados):
        self.dados = dados
        self.tamBloco = 4
        self.linhaCache = 32
        self.ocupado
        self.tag[32][4]
        # TAG pode ser:  modify – exclusive – shared – invalid

    def writeBack(self, RAM, indice):
        for i in range(4):
            if self.tag[indice][i] == 'modify':
                RAM.dado[indice] = self.dados[i]

    def verificaCache(self):
        for i in self.linhaCache:
            if self.dados[i].ocupado == 0:
                return i     
        return 1
