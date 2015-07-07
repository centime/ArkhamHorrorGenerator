from os import popen, path
from sys import argv
from random import randint, choice
import json
from pprint import pprint

primes = ["A woman","A young","An old","As you","Cruel eyes","It appears","No one","Once you","Outside the","Spying a","The door","The old","Through one","You don","You hear","You try","You were","As you browse","You find a","If only one","An ancient woman","By quietly listening","Sickly-colored","Hearing the sounds","Shivering, you","Standing outside at","A reporter from","Alone in the","Meandering down a","You are asked","At key points","The mariners are","Crossing the bridge","Entering the workroom","Something calls to","A woman poses","Mail order!","A woman stands","Sneaking into the","A strange series","An odd,","A gate and","You find the","You run into","You encounter a","You recognize one","During the night","A large mirror","Suddenly you notice","The cylindered head","You share a","Nurse Sharon asks","You are suddenly","One of the","You wake up","Sneaking into an","You find it","A bunch of","The light illuminates","Following the lake","Whoever is sitting","A bored cat","You realize that","A pungent odor","Discuss the opportunity","The seclusion on","A gleam of","Nurse Sharon slips","A powerful wind","You think a","You stumble upon","You are reunited","You earn a","Tucked in a","One of the","visions of the","retrieve it,","A crazed,","Although it is","There are two","An unruly gang","If you look","You stand before"]


def sample_situations(N, temp) :
	
	length = 100*N
	seed = randint(0,10000)
	prime = choice(primes)

	cmd = 'cd '+rnn+' && th sample.lua ../scripts/'+situations_sampler+' -length '+str(length)+' -temperature '+str(temp)+' -seed '+str(seed)+' -primetext "'+prime+'"'
	
	return popen(cmd).read().split('--------------------------\x1b[0m\t\n')[1]

def sample_full(prime, temp) :
	
	length = 200
	seed = randint(0,10000)

	cmd = 'cd '+rnn+' && th sample.lua ../scripts/'+full_sampler+' -length '+str(length)+' -temperature '+str(temp)+' -seed '+str(seed)+' -primetext "'+prime+'"'
	
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
	logs_path = argv[6] if len(argv)>6 else ''

	situations = sample_situations(number, temp1).replace('"','\\"')
	cards = []
	for situation in situations.split('\n')[:-2] :
		
		card = '.'.join(sample_full(situation+random_check(), temp2).split('\n')[0].split('.')[:-1])
		print('\n['+str(len(cards))+'] '+card)
		cards.append(card)
		

	if logs_path:
		logs_file = open(logs_path)
		logs_json = logs_file.read()
		if not logs_json : logs_json = '[]'
		logs = json.loads(logs_json)

		print('---------------\nRate '+str(len(cards))+' id1:rating1[1-10] id2:rating2[1-10] ...')
		try :
			ratings = input() # id1:rating1 id2:rating2 ...
			ratings = { int(c.split(':')[0]):int(c.split(':')[1]) for c in ratings.split(' ')}

			for i, card in enumerate(cards) :
				rating = ratings[i] if i in ratings else -1
				logs.append({'text':card, 'rating':rating})
			
		except : 
			print('Error, samples rated as -1')
			for card in cards:
				logs.append({'text':card, 'rating':-1})

		logs_file.close()
		open(logs_path,'w').write(json.dumps(logs))
