import requests


def getUser(uid):
    head = {"User-Agent": "RootMyStats"}
    r = requests.get("https://www.hackthebox.com/api/v4/profile/progress/challenges/479925",headers=head).json()
    r2 = requests.get("https://www.hackthebox.com/api/v4/profile/479925",headers=head).json()
    print(r)
    print(r2)
    pseudo = r2['profile']['name']
    nb_challs = r["profile"]["challenge_owns"]["solved"]
    return pseudo, nb_challs

#print(getUser(479925))