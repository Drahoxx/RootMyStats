import sqlite3
from os import path
import PyRootMe.rootme as rm
import PyCryptoHack.cryptohack as ch
import PyTryHackMe.thm as thm
import random

"""
Charge les BDD, si jamais elles n'existent pas encore, cela créer la bdd et créer les tables
Args : None
"""
def loadBdds():
    global con
    global cur
    if not path.exists("RootMyStats.sqlite"):
        con = sqlite3.connect('RootMyStats.sqlite')
        cur = con.cursor()
        create_tables()
    else:
        con = sqlite3.connect('RootMyStats.sqlite')
        cur = con.cursor()
"""
Creation des tables
Détails :
- users -> Stockage des users (discordId,rmId,htbId,thmId,chId)
- challs -> Stockage des challenges des différentes personnes, permet de diminuer le nb de requêtes aux API (challId,plateforme,title,descr,score,difficulty,cat)
- servers -> Stockages des servers (et channels) sur lesquels est le bot (serverId, channelId)
- linker -> Associe les challenges et les users, les challenges validés par le user (discordId,challId)
- linker_server -> Associe les users avec les différents servers (TODO : faire en sorte que ça soit pas channel) 
"""
def create_tables():                                                                                             #A FAIRE SERVER IDl
    cur.execute('''CREATE TABLE users_596a96cc7bf9108cd896f33c44aedc8a (discordId text NOT NULL PRIMARY KEY, rmId text DEFAULT NULL, htbId text DEFAULT NULL, thmId text DEFAULT NULL, chId text DEFAULT NULL)''')
    cur.execute('''CREATE TABLE challs_f74a10e1d6b2f32a47b8bcb53dac5345 (challId NOT NULL PRIMARY KEY, plateforme int, title text, descr text, score int, difficulty text, cat text)''')
    cur.execute('''CREATE TABLE linker_d04eed22158c5db35fb77472ce67e4b2 (discordId, challId, PRIMARY KEY (discordId, challId), FOREIGN KEY (discordId) REFERENCES users_596a96cc7bf9108cd896f33c44aedc8a (discordId), FOREIGN KEY (challId) REFERENCES users_596a96cc7bf9108cd896f33c44aedc8a (challId))''')
    cur.execute('''CREATE TABLE servers_d6a6bc0db10694a2d90e3a69648f3a03 (serverId,channelId, PRIMARY KEY (serverId, channelId))''')
    cur.execute('''CREATE TABLE linker_server_2610c6feebaf885c3185ebaec440f96c (discordId, serverId, FOREIGN KEY (discordId) REFERENCES users_596a96cc7bf9108cd896f33c44aedc8a (discordId),FOREIGN KEY (serverId) REFERENCES servers_d6a6bc0db10694a2d90e3a69648f3a03 (serverId)''')
    con.commit()

"""
Ajoute un server à la bdd
Args : serverId, channelId
"""
def addServer(serverId,channelId):
    cur.execute("INSERT INTO servers_d6a6bc0db10694a2d90e3a69648f3a03 (serverId,channelId) VALUES (?,?)",(serverId,channelId))
    con.commit()
"""
Associe un user avec un serveur
Args : discordId,serverId
TODO: Associer avec un channel sur un serveur
"""
def addUserInServer(discordId,serverId):
    cur.execute("INSERT INTO linker_server_2610c6feebaf885c3185ebaec440f96c (discordId,serverId) VALUES (?,?)",(discordId,serverId))
    con.commit()
"""
Ajoute un user à la bdd
Args : discordId
TODO : Check si le user est pas déjà dans la bdd
"""
def addUser(discordId):
    cur.execute("INSERT INTO users_596a96cc7bf9108cd896f33c44aedc8a (discordId) VALUES (?)", (discordId))
    con.commit()
"""
Associe un ou plusieurs compte des différentes plateformes à un user
Args : discordId, (htb),(thm),(rm),(ch)
"""
def addCompte(discordId, htb=None,thm=None,rm=None,ch=None):
    comptes = {"htbId":htb,"thmId":thm,"rmId":rm,"chId":ch}
    for key in comptes:
        compte = comptes[key]
        if compte != None:
            cur.execute(f"UPDATE users_596a96cc7bf9108cd896f33c44aedc8a SET {key} = ? WHERE discordId=?",(compte,discordId))
    con.commit()
"""
Fait qu'un user valide un challenge, concrêtement associe un user et un challId dans la table linker
args : discordId, challId
"""
def validate_Challenge(discordId,challId):
    cur.execute("INSERT INTO linker_d04eed22158c5db35fb77472ce67e4b2 VALUES (?,?)",(discordId,challId))
    con.commit()

"""
Permet d'ajouter un challenge à la bdd. Si le challenge est déjà dans la bdd, la fonction est ignorée.
args :
- challId (str)
- plateforme (int) -> {0 : Rootme, 1 : Thm, 2 : CryptoHack}
- user (str) -> utile dans le cas de cryptohack, par défaut le pseudo du premier au ranking de cryptohack
"""
def addChallIfItDoesntExistYet(challId, plateforme, user="hellman"):
    if not isChallIntheBDD(challId):
        infos = retrieveChallInfos(challId,plateforme,user)
        query = "INSERT INTO challs_f74a10e1d6b2f32a47b8bcb53dac5345 ("
        nb_paramaters = 0
        for key in infos:
            if infos[key] != None:
                nb_paramaters +=1
                query+=str(key+",")
        query=query[:-1]+") VALUES ("+(str("?,"*nb_paramaters)[:-1])+")"

        cur.execute(query,tuple(infos.values()))
        con.commit()
        
    return False
"""
Télécharge les infos relatives à un challenge. Et cela sur les différentes plateformes
 ! - requêtes API aux services des plateformes
 args : challId, plateforme, user
 => plateforme cf "addChallIfItDoesntExistYet()"
"""
def retrieveChallInfos(challId,plateforme,user) -> (str,int,str,str,int,str):
    if plateforme == 0:
        infos = rm.getChall(challId)
        return {"challId":challId,"plateforme":0,"title":infos[0],"descr":infos[1],"score":infos[2],"cat":infos[3],"difficulty":infos[4]}
    elif plateforme == 1:
        infos = thm.getChall(challId)
        return {"challId":challId,"plateforme":1,"title":infos[0],"descr":infos[1],"score":None,"cat":None,"difficulty":infos[2]}
    elif plateforme == 2:
        challs = ch.getUser(user)[3]
        for c in challs:
            if c["name"].replace(' ','_') == challId:
                 return {"challId":challId,"plateforme":2,"title":c['name'],"descr":None,"score":c['points'],"cat":c["category"],"difficulty":None}
    return False
"""
Regarde si un challenge est dans la bdd
args : challId
return : bool
"""
def isChallIntheBDD(challId) -> bool:
    cur.execute("SELECT count(*) FROM challs_f74a10e1d6b2f32a47b8bcb53dac5345 WHERE challId=?",(challId,))
    isInTheTable = bool(cur.fetchone()[0])
    return isInTheTable



"""
TESTS
"""
loadBdds()
x= random.randint(1, 5000)
addUser(str(x),1)
addCompte(str(x),rm="Yolo")
y=5
addChallIfItDoesntExistYet(str(y),0)
validate_Challenge(x,y)