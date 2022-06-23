import requests
with open("../API_ROOTME.secret","r") as f:
	API_KEY = f.readline()


def getUser(uid):
	try:
		r = requests.get("https://api.www.root-me.org/auteurs/"+str(uid),cookies={"api_key":API_KEY})
		if r.status_code!=200:
			return False
		data = r.json()
		pseudo = data['nom']
		score = data['score']
		position = data['position']
		challs = [c['id_challenge'] for c in data['validations']] #à vérifier
		nb_challs = len(challs)
		r.close()
		return pseudo, score, position, challs, nb_challs
	except:
		return False

def getChall(cid):
	try:
		r = requests.get("https://api.www.root-me.org/challenges/"+str(cid),cookies={"api_key":API_KEY})
		if r.status_code!=200:
			r.close()
			return False
		data = r.json()[0]
		titre = data['titre']
		cat = data['rubrique']
		subtitle = data['soustitre']
		score = data['score']
		diff = data['difficulte']
		r.close()
		return titre, subtitle, score,cat, diff
	except:
		return False
