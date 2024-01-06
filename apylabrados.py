from ApylabradosModule import Pawns, Word, Dictionary,FrequencyTable,Board,Console,welcome,HallOfFame
con=Console()
hallOfFame=HallOfFame("stored_scores",con)
welcome(con)
letsPlay=True
inputText0=f"Coord, dir {con.yellow}x,y,{con.endcol}({con.yellow}H{con.endcol}/{con.yellow}V{con.endcol}):"
inputText=f"Coord, dir {con.yellow}x,y,{con.endcol}({con.yellow}H{con.endcol}/{con.yellow}V{con.endcol}) / {con.yellow}HLP {con.endcol}Sug.:"
inputText1=f"{con.yellow}PALABA {con.endcol}/ {con.yellow}INFO {con.endcol}/ {con.yellow}HLP {con.endcol}Sugerencias:"


while letsPlay:
    bag_of_pawns=Pawns(con)
    bag_of_pawns.createBag()
    b=Board(con)
    player_pawns=Pawns(con)
    new_word=Word()


    message="Tus fichas : Fichas en el saco:"+str(bag_of_pawns.getTotalPawns())+"\n"
    while True: #aun no se cuando se acaba el juego
        new_word.word=[" "]
        
        for _ in range(7-player_pawns.getTotalPawns()): #rellena las fichas que le falten al jugador
            if bag_of_pawns.getTotalPawns()>0:
                player_pawns.addPawn(bag_of_pawns.takeRandomPawn())

        b.showBoard()
        con.printConsole(message)
        player_pawns.showPawns(new_word)


        while True: # No sale del bucle hasta ue acierte una palabra que esté en el diccionario        
            opt=con.validateInput(inputText1,"res.strip().isalpha()").upper()
            if opt.strip()=="HLP":
                Dictionary.showWord(player_pawns,con)
            elif opt in ["info", "INFO"]:
                Pawns.showPawnsPoints(con)
            new_word=Word.readWord(con,opt)
            if Dictionary.validateWord(new_word) : 
                con.clearScreen()
                b.showBoard()
                con.printConsole(message)
                player_pawns.showPawns(new_word)
                break     
        if b.totalWords==0:
            opt=con.validateInput(inputText0,"int(res.split(',')[0]) in range(0,15) and int(res.split(',')[1]) in range(0,15) and res.split(',')[2].upper().strip() in ['H','V']")
        else:
            
            opt=con.validateInput(inputText,"res.upper()=='INFO' or res.upper()=='HLP' or (int(res.split(',')[0]) in range(0,15) and int(res.split(',')[1]) in range(0,15) and res.split(',')[2].upper().strip() in ['H','V'])")
            if opt in ["HLP","hlp"] :
                fail=b.showWordPlacement(player_pawns,new_word)
                if fail:
                    hallOfFame.addRecord(b.score)
                    letsPlay= con.validateInput(f"¿La revancha ({con.yellow}S{con.endcol}/{con.yellow}N{con.endcol})?","res.upper() in ['S','N']") in ["S","s"]
                    break
            elif opt in ["info", "INFO"]:
                Pawns.showPawnsPoints(con)
            opt=con.validateInput(inputText0,"int(res.split(',')[0]) in range(0,15) and int(res.split(',')[1]) in range(0,15) and res.split(',')[2].upper().strip() in ['H','V']")
            

                        
        x,y,dir=int(opt[0]),int(opt[1]),opt[2].upper().strip()
        
        f_p=player_pawns.getFrequency()
        if b.isPossible(new_word,x,y,dir)[0] and FrequencyTable.isSubset(b.getPawns(new_word,x,y,dir).getFrequency(),f_p): # se accede a IsPossible antes de getPawns por si hay indexError
            b.placeWord(player_pawns,new_word.word,x,y,dir)
            message="Tus fichas :  Fichas en el saco:"+str(bag_of_pawns.getTotalPawns())+"\n"
        else:
            message=f"{str(new_word)} : {b.isPossible(new_word,x,y,dir)[1]}, inténtalo se nuevo :\n"