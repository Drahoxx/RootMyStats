import requests


def getUser(name):
	try:
		r = requests.get(f"https://cryptohack.org/api/user/{name}/")
		if r.status_code!=200:
			return False
		j = r.json()
		challs = j["solved_challenges"]
		score = j["score"]
		rank = j["rank"]
		level = j["level"]
		return name,score,rank,challs,len(challs)
	except:
		return False


#print(getUser("Drahoxx"))