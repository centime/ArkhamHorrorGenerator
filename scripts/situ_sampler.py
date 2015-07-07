from os import popen
from sys import argv
from random import randint, choice

primes = ["A woman","A young","An old","As you","Cruel eyes","It appears","No one","Once you","Outside the","Spying a","The door","The old","Through one","You don","You hear","You try","You were","As you browse","You find a","If only one","An ancient woman","By quietly listening","Sickly-colored","Hearing the sounds","Shivering, you","Standing outside at","A reporter from","Alone in the","Meandering down a","You are asked","At key points","The mariners are","Crossing the bridge","Entering the workroom","Something calls to","A woman poses","Mail order!","A woman stands","Sneaking into the","A strange series","An odd,","A gate and","You find the","You run into","You encounter a","You recognize one","During the night","A large mirror","Suddenly you notice","The cylindered head","You share a","Nurse Sharon asks","You are suddenly","One of the","You wake up","Sneaking into an","You find it","A bunch of","The light illuminates","Following the lake","Whoever is sitting","A bored cat","You realize that","A pungent odor","Discuss the opportunity","The seclusion on","A gleam of","Nurse Sharon slips","A powerful wind","You think a","You stumble upon","You are reunited","You earn a","Tucked in a","One of the","visions of the","retrieve it,","A crazed,","Although it is","There are two","An unruly gang","If you look","You stand before"]


def sample_situations(N, temp) :
	
	length = 100*N
	seed = randint(0,10000)
	prime = choice(primes)

	cmd = "cd "+rnn+" && th sample.lua ../scripts/"+situations_sampler+" -length "+str(length)+" -temperature "+str(temp)+" -seed "+str(seed)+" -primetext '"+prime+"'"
	
	return popen(cmd).read().split('--------------------------\x1b[0m\t\n')[1]

def sample_full(prime, temp) :
	
	length = 200
	seed = randint(0,10000)

	cmd = "cd "+rnn+" && th sample.lua ../scripts/"+full_sampler+" -length "+str(length)+" -temperature "+str(temp)+" -seed "+str(seed)+" -primetext '"+prime+"'"
	
	return popen(cmd).read().split('--------------------------\x1b[0m\t\n')[1]


rnn = "../char-rnn/"

attributes = ['Will', 'Fight', 'Lore', 'Luck', 'Speed', 'Sneak']

def random_check():
	return ' Make a '+choice(attributes)+' (+'+str(randint(0,2))+') check'

if __name__ == "__main__" :
	
	situations_sampler = argv[1]
	full_sampler = argv[2]
	number = int(argv[3]) if len(argv)>3 else 4
	temp1 = float(argv[4]) if len(argv)>4 else 0.7
	temp2 = float(argv[5]) if len(argv)>5 else 0.7

	situations = sample_situations(number, temp1)
	for situation in situations.split('\n')[:-2] :
		print('-')
		print(sample_full(situation+random_check(), temp2).split('\n')[0])