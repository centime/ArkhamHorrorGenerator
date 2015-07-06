from os import popen
from sys import argv
from random import randint, choice
#from enchant import Dict
import language_check
import transforms


primes = ["A woman",
"A young",
"An old",
"An old",
"An old",
"An old",
"As you",
"As you",
"As you",
"As you",
"As you",
"As you",
"As you",
"As you",
"As you",
"Cruel eyes",
"It appears",
"No one",
"Once you",
"Outside the",
"Outside the",
"Spying a",
"The door",
"The old",
"The old",
"Through one",
"You don",
"You hear",
"You hear",
"You try",
"You were"]



def sample(approx_number=5, temp=0.6) :
	
	length = 200*approx_number
	seed = randint(0,10000)
	prime = choice(primes)

	cmd = "cd "+rnn+" && th sample.lua ../scripts/"+sampler+" -length "+str(length)+" -temperature "+str(temp)+" -seed "+str(seed)+" -primetext '"+prime+"'"
	
	return popen(cmd).read().split('--------------------------\x1b[0m\t\n')[1]

def texts(stream):

	t = []

	for sample_text in stream.split('\n')[:-1]:

		suspicious_spellings = checker.check(sample_text)
		
		sample = {
			'text' : sample_text,
			'suspiciousness' : len(suspicious_spellings),
			'correction' : language_check.correct(sample_text, suspicious_spellings)

		}
		t.append(sample)
	return t


rnn = "../char-rnn/"
#dict_en = Dict("en_US")
checker = language_check.LanguageTool('en-US')

if __name__ == "__main__" :
	
	sampler = argv[1]
	number = int(argv[2]) if len(argv)>2 else 4
	temp = float(argv[3]) if len(argv)>3 else 0.7
	expand =  argv[4] if len(argv)>4 else ''

	stream = sample(number, temp)

	if expand == 'expand':
		print(stream.replace('\n','\n\n'))
		print('---------------------------------------------')
		stream = transforms.run('expand', stream)
		print(stream.replace('\n','\n\n'))
		print('---------------------------------------------')

	txts = texts(stream)

	txts.sort(key=lambda x: x['suspiciousness'] )

	#print( '\n\n'.join([x['text']+"\n-- "+str(x['suspiciousness'])+" --\n"+x['correction'] for x in s]) )
	print( '\n\n'.join([x['correction'] for x in txts]) )
