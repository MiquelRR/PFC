import os
import csv
import platform
import pandas as pd
p = os.path.dirname(os.path.abspath(__file__))

class HallOfFame():
    """
    mantienen un archrivo csv con una lista de diccionarios  "Nombre" y "Puntos" ordenados
    """
    def __init__(self,filename,con) -> None:
        self.fn=os.path.join(p,filename+".csv")
        self.con=con

    def readRecordsFile(self) -> list: 
        if os.path.isfile(self.fn):
            with open(self.fn,"r") as f:
                reader = csv.DictReader(f, quoting=csv.QUOTE_NONNUMERIC)
                return list(reader)
        else:
            return []
        
    def writeRecordsFile(self,hf):
        header = list(hf[0].keys())
        with open(self.fn,"w") as f:
            writer = csv.DictWriter(f, fieldnames = header, quoting=csv.QUOTE_NONNUMERIC)
            writer.writeheader()
            writer.writerows(hf)

    def addRecord(self,score):
        hf=self.readRecordsFile()
        self.con.clearScreen()
        self.con.printConsole(f"Los duendecillos del ordenador no han encontrado sitio para colocar esa palabra\n HAS FINALIZADO CON {score} puntos\n")
        name=self.con.validateInput("Dime tu nombre :","res.replace(' ','').isalnum()")
        hf.append({"Nombre":name, "Puntos":score})
        hf.sort(key=lambda x:x["Puntos"],reverse=True)
        self.showScores(hf)
        self.writeRecordsFile(hf)
        
    
    def showScores(self,hf): #ojo que printconsole no imprime hasta que hay un ValidateInput o un showScreen
        topten=hf[:10]+[{"Nombre":"", "Puntos":0}]*(10-len(hf))
        self.con.printConsole(f"{self.con.red}╔═════════════════════════╗\n║{self.con.cyan}       HALL OF FAME     {self.con.red} ║\n╚═════════════════════════╝\n")
        self.con.printConsole(f"{self.con.cyan}┌──┐┌─────PLAYER─────┐┌SCO┐\n")
        for e in topten:
            if e['Puntos'] == 0:
                pos,pun,nom='··','···',"·"*16
            else:
                pos,pun=f"{self.con.endcol}{topten.index(e)+1:02d}{self.con.cyan}", f"{self.con.endcol}{int(e['Puntos']):03d}{self.con.cyan}"
                nom=f"{self.con.endcol}{e['Nombre'][:16]}{self.con.cyan}{'·'*(16-len(e['Nombre'][:16]))}"
            self.con.printConsole(f"│{pos}││{nom}││{pun}│\n")
        self.con.printConsole(f"└──┘└────────────────┘└───┘\n")
        #self.con.showScreen()
        
    
              

def welcome(con):
    wfile=os.path.join(p,"welcome_message.txt")
    with open(wfile, "r", encoding="utf-8") as f:
        r=f.read()
        con.printConsole(r)     
        con.validateInput("","True")
        con.clearScreen()

class Console():
    """
    esta clase controla cuanto caracteres imprimimos en la terminal , para borrar con \b 
    y hacer una pseudo pantalla, volviendo a imprimir en el mismo sitio
    """
    bold = '\033[1m'
    green = '\033[92m'
    yellow = '\033[93m'
    blue = '\033[94m'
    endcol = '\033[0m'
    cyan = '\033[96m'
    red = '\033[91m'
    low='\033[2m'
    infoTitle=f"{cyan}    ╔═══════════════════════╗\n    ║ {blue} P U N T U A C I O N  {cyan}║\n    ╚═══════════════════════╝\n{endcol}"
    def __init__(self) -> None:
        self.screen=""
        self.maxChar=6000
    def printConsole(self, text):
        self.screen+=str(text)
    def showScreen(self):
        print(self.screen)
    def clearDisplay(self):
        if platform.system() == "Windows":
            os.system("cls")
        elif any('jupyter' in arg for arg in platform.sys.argv):
            print('\b'*(len(self.screen)+self.screen.count("\n")))
        elif platform.system() == "Linux" or platform.system() == "Darwin":
            os.system("clear")
    def clearScreen(self):
        self.clearDisplay()
        self.screen=""
    def validateInput(self,questText,evaluableCondition=False):
        """
        validamos una input del usuario, la condicion que pongamos se evalua en referencia a la variable res
        si no es válido "borramos" y volvemos a preguntar, la funcion devuelve una variable o una lista si hay comas
        ejemplos de paramentros para evaluableCondition=
        'res.isdigit' ,
        'res.split(",")[0].isalpha() and res.split(",")[1].isdigit() and int(res.split(",")[1]) in range(0,14)'
        'res=isalpha()
        """
        dev=[]
        while True:
            self.clearDisplay()
            self.showScreen()
            print(questText)
            res=input(">")
            try:
                if eval(evaluableCondition):
                    res=res.split(",")
                    for l in res:
                        dev.append(int(l) if l.strip().isdigit() else l.strip())
                    self.clearDisplay()
                    return dev if len(dev)>1 else dev[0] #una lista, si el string lleva comas
                else:
                    pass
            except Exception:            
                pass
        

class Pawns():
    """
    este es un paquete de letras,
    esta clase se utiliza tanto para la bolsa de letras restantes
    como para las letras que tiene en ls msno del jugador
    """
    points={'A':1,'B':3,'C':3,'D':2,'E':1,'F':4,'G':2,'H':4,'I':1,'J':8,'K':5,'L':1,'M':3,'N':1,'O':1,'P':3,'Q':10,'R':1,'S':1,'T':1,'U':1,'V':4,'W':4,'X':8,'Y':4,'Z':10}
    def __init__(self,con,pt=""):
        self.letters=[]
        if pt=="":
            pt=os.path.join(p,"bag_of_pawns.csv")        
        self.filepath=pt
        self.con=con

    def addPawn(self,c):
        self.letters.append(c)

    def addPawns(self,c,n):
        for _ in range(n):
            self.addPawn(c)
    
    def createBag(self):
        import csv
        with open(self.filepath) as csvfile:
            reader = csv.DictReader(csvfile)
            for line in reader:
                self.addPawns(line["Letter"], int(line["Count"]))

    def showPawns(self,word):
        colorword= [(Console.red,i) for i in word.word]
        self.con.printConsole(self.con.yellow+"┌─┬─┬─┬─┬─┬─┬─┐  "+self.con.endcol+"┌"+"─┬"*(word.getLengthWord()-1)+"─┐\n")
        self.con.printConsole(self.con.yellow+"│")
        for c in self.letters:
            if (Console.red, c) in colorword:
                colorword[colorword.index((Console.red, c))]=(Console.yellow,c)
                ccolor=" "
            else:
                ccolor=c
            self.con.printConsole(ccolor+"│")
        self.con.printConsole(self.con.endcol+"  │")
        for c in colorword:
            self.con.printConsole(c[0]+c[1]+Console.endcol+"│")
        self.con.printConsole(self.con.yellow+"\n└─┴─┴─┴─┴─┴─┴─┘  "+self.con.endcol+"└"+"─┴"*(word.getLengthWord()-1)+"─┘\n")
        self.con.clearDisplay()
        self.con.showScreen()

    def takeRandomPawn(self):
        """
        método de Pawns que devuelve una ficha aleatória y la quita de la bolsa 
        """
        if self.getTotalPawns()<1:
            raise ValueError("No quedan más fichas")
        from numpy import random
        choice=random.choice(self.letters)
        self.letters.remove(choice)
        return choice
    
    def getFrequency(self):
        obj=FrequencyTable()
        for c in self.letters:
            obj.update(c)
        return obj
    
    def takePawn(self,c):
        self.letters.remove(c)

    def getTotalPawns(self) -> int:
        return len(self.letters)
    
    @staticmethod
    def getPoints(c):
        return Pawns.points[c]

    @staticmethod                   
    def showPawnsPoints(con):
        conb=Console()
        conb.clearScreen()
        conb.printConsole(Console.infoTitle)
        for i,l in enumerate(Pawns.points):
            v=Pawns.points[l]
            conb.printConsole(f"  {l}-{' 'if v<10 else ''}{v}")
            if i % 5 == 4:
                conb.printConsole("\n")
        conb.validateInput("","True")
        conb.clearDisplay()
        con.showScreen()


class Word():
    def __init__(self):
        self.word=[]
    
    def __str__(self):
        return "".join(self.word)

    def areEqual(self,w):
        return w.word == self.word
    
    def isEmpty(self):
        return self.getLengthWord()==0
   
    @classmethod
    def readWord(cls,con,inp="HLP"): #modificacion sobre el ejercicio,: le puedo pasar opcionalmente la palabra
        if inp=="HLP":
            inp=con.validateInput("Palabra: ","res.strip().isalpha()")
        out_word=Word()
        out_word.word=list(inp.upper().strip())
        return out_word
    
    @staticmethod
    def readWordFromFile(f):
        """
        Lee una linea de un fichero de texto y la devuelve como objeto de la clase Word
        """
        w=Word()
        w.word=list(f.readline().strip())
        return w
    
    def getFrequency(self):
        obj=FrequencyTable()
        for c in self.word:
            obj.update(c)
        return obj
    
    def getLengthWord(self) -> int:
        return len(self.word)


class Dictionary():
    """
    Manejo del diccionario de palabras válidas
    """
    filepath=os.path.join(p,"dictionary.txt")
    
    @staticmethod
    def validateWord(testword): #al final del archivo la lectura del txt con lineread devuelve cadena vacia
        """
        compara la palabra de la clase Word facilitada con el dicionario
        devuelve True si existe
        """
        with open(Dictionary.filepath, "r") as f:
            p=Word.readWordFromFile(f)
            while not p.isEmpty() and not p.areEqual(testword):
                p=Word.readWordFromFile(f)
        return False if p.isEmpty() and not testword.areEqual(p) else True
    @staticmethod
    def showWord(pawns,con) -> list:
        """
        Comprueba que palabras del diccionario se pueden hacer con las letras de pawns
        """
        res=[]
        with open(Dictionary.filepath, "r") as f:
            p=Word.readWordFromFile(f)
            while not p.isEmpty():
                if FrequencyTable.isSubset(p.getFrequency(),pawns.getFrequency()):
                    res.append(str(p))
                p=Word.readWordFromFile(f)
        con.printConsole(str(res))
        return res
    @staticmethod
    def showWordPlus(pawns,char,con) -> list:
        """
        Comprueba que palabras del diccionario se pueden hacer con las letras de pawns + un caracter char y contienen ese caracter
        """
        pawns.addPawn(char)
        res=[]
        with open(Dictionary.filepath, "r") as f:
            p=Word.readWordFromFile(f)
            while not p.isEmpty():
                if FrequencyTable.isSubset(p.getFrequency(),pawns.getFrequency()):
                    res.append(str(p))
                p=Word.readWordFromFile(f)
        res=list(filter(lambda x: 'c' in x, res))
        con.printConsole(str(res))
        pawns.takePawn(char)
        return res
            
class FrequencyTable():
    def __init__(self):
        self.letters=list("ABCDEFGHIJKLMNOPQRSTUVWXYZ")
        self.frequencies=[0]*26
    
    def showFrequency(self): #este metodo aun no lo uso,de echo no me gusta como se ve
        tpl=list(zip(self.letters, self.frequencies)) #hago una lista de tuplas para recorrerla
        for tp in tpl:
                print(tp+" " if tp[1]>0 else "", end=0) 

    @staticmethod
    def isSubset(ft1,ft2):
        return list(map(lambda a,b: a<=b,ft1.frequencies, ft2.frequencies)).count(False)==0
    
    def update(self,c):
        i=self.letters.index(c)
        self.frequencies[i] += 1

class Board():
    """
    Clase que contiene un tablero y maneja su representacións
    """
    
    def __init__(self,con)  -> None:
        self.con=con
        self.width=15
        self.height=15        
        self.board = [[" "]*self.width for i in range(self.height)]
        self.totalWords=0
        self.totalPawns=0
        self.score=0 
        self.multipliers=self.setupMultiplier()

        
    def showBoard(self):
        """
        Imprime por terminal el tablero 
        """
        gameTitle=f"{self.con.cyan}╔═══════════════════════╗╔═══════╗\n║ {self.con.blue}A P Y L A B R A D O S {self.con.cyan}║║{self.con.green}SCO:{self.score:03d}{self.con.cyan}║\n╚═══════════════════════╝╚═══════╝\n{self.con.endcol}"
        self.con.clearScreen()
        self.con.printConsole(gameTitle)
        self.con.printConsole("   0 1 2 3 4 5 6 7 8 9 0 1 2 3 4  \n")
        self.con.printConsole(self.con.cyan+" ╔═"+"═"*self.width*2+"╗\n"+self.con.endcol)
        vlegend=0
        for lin in self.board:
            self.con.printConsole(str(str(vlegend))[-1]+self.con.cyan+"║ "+self.con.endcol)
            for ele in lin:
                self.con.printConsole("· " if  ele==" " else self.con.yellow+ele+" "+self.con.endcol)
            vlegend+=1
            self.con.printConsole(self.con.cyan+"║\n"+self.con.endcol)
        self.con.printConsole(self.con.cyan+" ╚═"+"═"*self.width*2+"╝\n"+self.con.endcol)

    def placeWord(self,pl_pawns,word,x,y,dir):
        incy,incx=(0,1) if dir.upper()=="H" else (1,0)
        wordPoints,wordMult=0,1
        for c in word:
            if x>self.width-1 or y > self.height-1:
                raise IndexError("Se sale la palabra del tablero")
            elif self.board[y][x] not in [" ",c]:
                raise ValueError(f"La casilla está ocupada {c} {type(c)} {self.board[y][x]} {type(self.board[y][x])}")
            elif self.board[y][x]==" ":
                self.board[y][x]=c
                pl_pawns.takePawn(c)
                self.totalPawns +=1
                mult= self.multipliers[x][y][0] if self.multipliers[x][y][1]=="p" else 1
                wordPoints+=Pawns.points[c]*mult
                multw=self.multipliers[x][y][0] if self.multipliers[x][y][1]=="w" else 1
                wordMult*=multw
            x,y=x+incx,y+incy
        self.totalWords+=1
        self.score+=wordPoints*wordMult
        

    def isPossible(self,w,x,y,dir):
        shape=[]
        empty=[]
        equal=[]
        incy,incx=(0,1) if dir.upper()=="H" else (1,0)
        clearCond =y-incy in range(0, self.height) or x-incx in range(0, self.width) or self.board[y-incy][x-incx]==" " #no sale de rango por el orden 
        for c in w.word:
            if x>self.width-1 or y > self.height-1:
                return (False,"La palabra se saldria del tablero") #comprobamos esto primero y evitamos IndexError
            shape.append([y,x]) #coordenada,   
            empty.append(self.board[y][x]==" ") # si vacia
            equal.append(self.board[y][x]==c) #si coincide
            x,y=x+incx,y+incy
        clearCond = clearCond and (y in range(0, self.height) or x in range(0, self.width) or self.board[y][x]==" ")
        if not clearCond:
            return (False,"La palabra se juntaría por sus extremos con fichas existentes")
        if self.totalWords==0 :
            if [(self.height-1)//2,(self.width-1)//2] in shape:
                return (True, "Colocada la primera palabra")
            else:
                return (False,"La primera palabra ha de pasar por la casilla central") 
        else:
            if not True in empty:
                return (False,"La palabra no añade fichas al tablero")        
            if not True in equal:
                return (False,"Ninguna letra de la palabra coincide con las letras del tablero")
            if sum(equal)+sum(empty)!=w.getLengthWord():
                return (False,"No se puede situar una ficha en una casilla ya ocupada por otra ficha diferente")
            return (True,"La palabra puede colocarse")
    
    def getPawns(self, w,xa,ya,dir) -> Word:
        r_w=Word()
        if self.isPossible(w,x=xa,y=ya,dir=dir)[0]:
            incy,incx=(0,1) if dir.upper()=="H" else (1,0)
            for c in w.word:
                if self.board[ya][xa]!=c:
                    r_w.word.append(c)
                xa,ya=xa+incx,ya+incy
        return r_w
    
    def showWordPlacement(self,pawns,word):
        placements=[]
        for d in ["H","V"]:
            for y in range(0,self.height if d == "H" else self.height-word.getLengthWord()+1):
                for x in range(0,self.width if d == "V" else self.width-word.getLengthWord()+1): 
                        f_p=pawns.getFrequency()
                        if self.isPossible(word,x,y,d)[0] and FrequencyTable.isSubset(self.getPawns(word,x,y,d).getFrequency(),f_p):
                            placements.append([x,y,d])
                            self.con.printConsole(f"> {x},{y},{d}  ")
        return len(placements)==0
    
    # Cambiar el método de la clase Board

    def showBoardGR(self,word=" "*7):
        import matplotlib.pyplot as plt
        

        fp= os.path.join(p,"xycolor_board.csv")

        scale= lambda x: (x + 1)/17

        square= lambda x,y: [[x-.5, y-.5], [x-.5, y+.5], [x+.5, y+.5], [x+.5, y-.5]]

        colormap=pd.read_csv(fp)

        fig = plt.figure(figsize = [10, 10])
        brd = fig.add_subplot(111)

        for n in range(self.width+1):
            brd.plot([n, n], [0, 15], 'g')

        for n in range(self.height+1):
            brd.plot([0, 15], [n, n], 'g')
        
        brd.set_xlim(-1, 16)
        brd.set_ylim(-1, 16)
        brd.set_position([0, 0, 1, 1])

        brd.set_axis_off()

        for i in range(self.width):
            brd.text(scale(i + 0.5), scale(15.5), str(i)[-1],
                    verticalalignment = "center", horizontalalignment = "center",
                    fontsize = 22, fontfamily = "sans-serif", fontweight = "bold",
                    transform = brd.transAxes)

        for i in range(self.height):
            brd.text(scale(15.5), scale(i + 0.5), str(14 - i)[-1],
                    verticalalignment = "center", horizontalalignment = "center",
                    fontsize = 20, fontfamily = "sans-serif", fontweight = "bold",
                    transform = brd.transAxes)
            for j in range(self.width):
                brd.text(scale(j + 0.5), scale(14 - i + 0.5), self.board[i][j],
                        verticalalignment = "center", horizontalalignment = "center",
                        fontsize = 15, transform = brd.transAxes)
                
        for row in colormap.itertuples():
            polygon = plt.Polygon(square(row[1], row[2]), color = row[3])
            brd.add_artist(polygon)

        brd.text(scale(0), scale(-.5), f"Score: {format(self.score)}",
          verticalalignment = "center", horizontalalignment = "left",
          fontsize = 25, fontfamily = "sans-serif", fontweight = "bold",
          transform = brd.transAxes)


        for i in range(len(word)):
            px,py=5+1.5*i,-.6
            polygon = plt.Polygon(square(px,py), color = '#f8f4b8' )        
            brd.add_artist(polygon)
            brd.text(scale(px-.15),scale(py), word[i],
                verticalalignment = "center", horizontalalignment = "left",
                fontsize = 25, fontfamily = "sans-serif", fontweight = "bold",
                transform = brd.transAxes)
        


        plt.show()

    def setupMultiplier(self) -> list:
        """
        creo una matriz con los multiplicadores por defecto en 1
        accesible con lista[x][y] 
        """
        mult=[]
        for _ in range(self.height):
            m=[(1,"")]*self.width
            mult.append(m)
        from csv import reader
        fp= os.path.join(p,"multiplier_board.csv")
        with open(fp, "r") as f:
            csvFile=reader(f)
            head = next(csvFile)
            for i in csvFile:
                mult[int(i[0])][int(i[1])]=(int(i[2]),i[3])
        return mult

            
                              
                              
                              

        