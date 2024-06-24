import datetime
import random
import pandas as pd
import os 

lista_figure = ["sasso", "carta", "forbici"]
dataCorrente = datetime.datetime.now()
data_str = dataCorrente.strftime('%m_%d_%y    %H_%M') 
nome_file1=data_str+ ".csv"

while True:
    nick=input("Inserisci il nickname") 
    if nick.isalnum():
        break
    else:
        print("il nick non deve contenre caratteri speciali!")

def gioco():
    vittorie = 0
    pareggi = 0
    sconfitte = 0
    continua = True  
    while continua:
        while True:
            scegli_simbolo = input("Scegli una figura tra carta, sasso e forbici: ")
            if scegli_simbolo in lista_figure:
                break
            else:
                print("Inserisci la figura corretta!")
        figura_computer = random.choice(lista_figure)
        print(f"Tu hai scelto: {scegli_simbolo}")
        print(f"Il computer ha scelto: {figura_computer}")
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
        while True:
            risposta = input("Vuoi continuare? (si/no): ").lower()
            if risposta == "si":
                continua = True
                break
            elif risposta == "no":
                continua = False
                break
            else:
                print("Devi scegliere se continuare digitando 'si' o 'no'.")

    salva(nick + ".csv",data_str,vittorie, pareggi, sconfitte)
    df=leggi_csv(nick + ".csv")
    vittorie_totali=df["vittorie"].sum()
    sconfitte_totali=df["sconfitte"].sum()
    pareggi_totali=df["pareggi"].sum()
    aggiorna_classifica(path="classifica.csv",nick=nick,
                        vittorie_totali=vittorie_totali,
                        pareggi_totali=pareggi_totali,
                        sconfitte_totali=sconfitte_totali,)

def salva(path,data_str,vittorie, pareggi, sconfitte):
    if not os.path.exists('salvataggi'):
        os.mkdir('salvataggi')
    
    os.chdir('salvataggi')
    
    data={
        "data":[data_str],
        "vittorie":[vittorie],
        "sconfitte":[sconfitte],
        "pareggi":[pareggi]
    }
    df=pd.DataFrame(data=data)
    df.set_index("data",inplace=True)
    if os.path.isfile(path=path):
        df.to_csv(path, mode="a",header=False)
    else:
        df.to_csv(path)        

def leggi_csv(path):
    df=pd.read_csv(filepath_or_buffer=path,sep=",")
    return df.iloc[-1]
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


gioco()




    

