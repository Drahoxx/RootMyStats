import PyRootMe.rootme as rm
import PyCryptoHack.cryptohack as ch
import PyHackTheBox.htb as htb
import PyTryHackMe.thm as thm

d = rm.getUser(239771)
print(d)

for i in range(len(d[3])):
	c = rm.getChall(d[3][i])
	if c==False:
		print("ça a crash : "+str(i))
	print(c)

