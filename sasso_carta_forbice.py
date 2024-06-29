#importazione librerie er l'iterazione dle progetto
import datetime
import random
import pandas as pd
import os 

#dichiarazini delle variabili pubbliche
lista_figure = ["sasso", "carta", "forbici"]
dataCorrente = datetime.datetime.now()
data_str = dataCorrente.strftime('%m_%d_%y    %H_%M') 
nome_file1=data_str+ ".csv"
nick=input("Inserisci il nickname: ") 

#funzione "gioco" è dove verrà gestita tutta la perte dell'elaborazione del programma
def gioco():
    #creazione delle varibili di controllo
    vittorie = 0
    pareggi = 0
    sconfitte = 0
    continua = True  
    
    #li cliclo segunte permette continare a giocare
    while continua:
        
        #contrllo dell'imput da perte dell'utente
        while True:
            scegli_simbolo = input("Scegli una figura tra carta, sasso e forbici: ")
            
            #questa qui la potevi gestire come una funzione (la usi piu volte)
            if scegli_simbolo in lista_figure:
                break
            else:
                print("Inserisci la figura corretta!")
        
        #stabilisce la carta estratta dal sistema in modo randomico su una lista di carte stabilite
        figura_computer = random.choice(lista_figure)
        
        #rendiamo visibili la carta scelta dall'utente e dal computer 
        print(f"Tu hai scelto: {scegli_simbolo}")
        print(f"Il computer ha scelto: {figura_computer}")
        
        #contrlliamo chi ha vnto il match il caso di parteggio e vittoria
        #aggiungo il valore dei risultati in memoria
        if scegli_simbolo == figura_computer:
            print("Pareggio!")
            pareggi += 1
        elif (scegli_simbolo == "sasso" and figura_computer == "forbici") or \
             (scegli_simbolo == "carta" and figura_computer == "sasso") or \
             (scegli_simbolo == "forbici" and figura_computer == "carta"):
            print("Hai vinto!")
            vittorie += 1
        else:
            print("Hai perso!")
            sconfitte += 1
        
        #da gesture ome funzione di controllo cntina a giocare(def continue_game() return True/False)
        #chiediamo all'utente se vuole continaure a giocare facendo un controlo sull'input inserito
        while True:
            risposta = input("Vuoi continuare? (si/no): ").lower()
            if risposta == "si" or "s" or "y" or "yes":
                continua = True
                break
            elif risposta == "no"or "n":
                continua = False
                break
            else:
                print("Devi scegliere se continuare digitando 'si' o 'no'.")

    #richiamo la funzione "salva" per salvare i dati in meoria su un file
    salva(nick + ".csv",data_str,vittorie, pareggi, sconfitte)
    
    df=leggi_csv(nick + ".csv")
    
    vittorie_totali=df["vittorie"].sum()
    sconfitte_totali=df["sconfitte"].sum()
    pareggi_totali=df["pareggi"].sum()
    
    #richiamo la funzione "aggiorna_classifica" la quale va a verificare i migliori giocatori tra tutti i dati salvati 
    aggiorna_classifica(path="classifica.csv",
                        nick=nick,
                        vittorie_totali=vittorie_totali,
                        pareggi_totali=pareggi_totali,
                        sconfitte_totali=sconfitte_totali,)
 #--- fine funzione def gioco()

#la fuznione "salva" prende come parametri:
# path      => nome file dove verra salvato
# data_str  => data del giorno della partita giocata
# vittorie  => vittore effetutate durante le partite
# pareggi   => pareggi effetutate durante le partite
# sconfitte => sconfitte effetutate durante le partite
def salva(path,data_str,vittorie, pareggi, sconfitte):
    
    #creo un dizionario per gestire i dati da salvare in modo ordinato
    data={
        "data":[data_str],
        "vittorie":[vittorie],
        "sconfitte":[sconfitte],
        "pareggi":[pareggi]
    }
    
    #inserisco il dizionario all'interno di un dataframe e lo salvo sul file
    df=pd.DataFrame(data=data)
    df.set_index("data",inplace=True)
    
    #verifico se esiste un file gia con il nome definito da "path"
    if os.path.isfile(path=path):
        #se  esiste il file aggiungo il rislstato della risultato della partitae
        df.to_csv(path, mode="a",header=False)
    else:
        #se  non esiste il file creo un nuovo file con il risultato della partita
        df.to_csv(path)
               
# con la funzione "leggi" andiamo a leggere il file restituendo l'ultima riga del DataFrame del file letto
def leggi_csv(path):
    df=pd.read_csv(filepath_or_buffer=path,sep=",")
    return df.iloc[-1]

# con la funzione "aggiorna_classifica"mi crea un file con tutte 
def aggiorna_classifica(path, nick, vittorie_totali, pareggi_totali, sconfitte_totali):
    
    if os.path.isfile(path):
        df = pd.read_csv(path, index_col="nick")
    else:
        data = {
            "nick": [],
            "Vittorie Totali": [],
            "Sconfitte Totali": [],
            "Pareggi Totali": []
        }
        df = pd.DataFrame(data=data)
        df.set_index("nick", inplace=True)
        
    if nick in df.index:
        df.loc[nick, "Vittorie Totali"] += vittorie_totali
        df.loc[nick, "Sconfitte Totali"] += sconfitte_totali
        df.loc[nick, "Pareggi Totali"] += pareggi_totali
        max_win=df["Vittorie Totali"].max()
        max_lose=df["Sconfitte Totali"].max()
        max_tie=df["Pareggi Totali"].max()
        print(f"Le vittorie totali sono : {max_win}, Le sconfitte totali sono: {max_lose}, I pareggi totali sono: {max_tie}")
    else:
        df.loc[nick] = [vittorie_totali, sconfitte_totali, pareggi_totali]
        max_win=df["Vittorie Totali"].max()
        max_lose=df["Sconfitte Totali"].max()
        max_tie=df["Pareggi Totali"].max()
        print(f"Le vittorie totali sono : {max_win}, Le sconfitte totali sono: {max_lose}, I pareggi totali sono: {max_tie}")
        
    df_sorted = df.sort_values(by=["Vittorie Totali", "Pareggi Totali", "Sconfitte Totali"], ascending=[False, False, True])
    top_10 = df_sorted.head(10)
    
    for idx in range(len(top_10)):
        row = top_10.iloc[idx]
        print(f"posizione {idx + 1} {top_10.index[idx]}\n vittorie {row['Vittorie Totali']}\n sconfitte {row['Sconfitte Totali']}\n pareggi {row['Pareggi Totali']}")
    df.to_csv(path)


# BONUS 5: Scrivi un codice che crei 20 liste con list comprehension fatte in questo modo:
# [numeroVittorie, numeroPareggi, numeroSconfitte]
# con ciascun valore estratto a sorte tra 0 e 10
# Sviluppa poi un algoritmo per ordinare queste 20 liste trovando il primo, secondo e terzo posto


# # con la funzione "generatore_di_risultati" crea una lista di liste di risultati randomici
# def generatore_di_risultati():
#     # Genera 20 liste con valori casuali tra 0 e 10 per numeroVittorie, numeroPareggi e numeroSconfitte
#     liste_partite = [[random.randint(0, 10), random.randint(0, 10), random.randint(0, 10)] for _ in range(20)]
#     return liste_partite

# # con la funzione "stampa_risultati" i valori preseti in una lista di liste
# def stampa_risultati(liste_partite):
#   for lista in liste_partite:
#     print(lista)
    
# #main
# lista_risultati= generatore_di_risultati()
# stampa_risultati(lista_risultati)






# main
gioco()




    

