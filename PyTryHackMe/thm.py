from turtle import position
import requests
#https://www.postman.com/gnarlito/workspace/tryhackme-doc/folder/18269560-afd06280-fe4d-4126-8289-33d86243739d?ctx=documentation

#Ajouter des fonctions pour si le mec a rien fait, ça crash pas yéy
def getUser(name):
	try:
		r = requests.get(f"https://tryhackme.com/api/all-completed-rooms?username={name}")
		r2 = requests.get(f"https://tryhackme.com/api/user/rank/{name}")
		if r.status_code!=200 or r2.status_code!=200:
			return False
		position=r2.json()["userRank"]
		rooms = [x["code"] for x in r.json()]
		nb_rooms = len(rooms)
		return name, position, rooms, nb_rooms
	except:
		return False


def getChall(code):
	try:
		r = requests.get(f"https://tryhackme.com/api/room/details?codes={code}").json()[code]
		#title
		#description
		#difficulty
		title = r['title']
		desc = r['description']
		diff = r['difficulty']
		return title,desc,diff
	except:
		print("[!] : ERROR - a request is bad : ")
		print(f"----> https://tryhackme.com/api/room/details?codes={code}")
		return False

#print(getChall(getUser("Aloxos")[2][4]))
