class ram:
    def __init__(self,dado):
        # self.linha = linha
        self.tamRam = 1024
        self.dado = dado

    def mostrarRam(self): #imprime a ram 
        for i in range (self.tamRam):
            print(i, self.dado[i])

    def leituraRAM(self,pos):
        return self.dado[pos]