from sys import argv 
from os import makedirs, path
import re


transformations = [
	{ # Overlap between gain/losses with $ and others. Those with $ need to be run first...
		'name' : 'pay', 
		'compress' : {
			'in':'([pP]ay) \$(\d)',
			'out' : '<$\\2'	
		},
		'expand' : {
			'in':'<\$(\d)',
			'out' : 'Pay $\\1'	
		}
	},
	{
		'name' : 'checks',
		'compress' : {
			'in':'[mMpP](ake|ass) a ([^ ]+) \(([\+-]\d)\) check',
			'out' : '<\\2\\3'	
		},
		'expand' : {
			'in':'<([^\+\-]+)(.\d)',
			'out' : 'Make a \\1 (\\2) check'	
		}
	},
	{
		'name' : 'pass/fails',
		'compress' : {
			'in':'f you (pass|fail)',
			'out' : '>\\1'	
		},
		'expand' : {
			'in':'>(pass|fail)',
			'out' : 'f you \\1'	
		}
	},
	{
		'name' : 'whether pass/fails',
		'compress' : {
			'in':'hether you pass[ed]?( or not| or failed)',
			'out' : '>w'	
		},
		'expand' : {
			'in':'>w',
			'out' : 'hether you pass or not'	
		}
	},
	{
		'name' : 'gain $',
		'compress' : {
			'in' : '([gG]ain) \$(\d)',
			'out' : '=\\2$'	
		},
		'expand' : {
			'in':'=(\d)\$',
			'out' : 'Gain $\\1'	
		}
	},
	{
		'name' : 'gain x',
		'compress' : {
			'in' : '([gG]ain|[dD]raw|[tT]ake) (\d|an?) ?(Clue|Unique|Common|Spell|Sanity|Stamina|Skill|Retainer)',
			'out' : '=\\2\\3'	
		},
		'expand' : {
			'in':'=(\d|a)([^ ]+)',
			'out' : 'Gain \\1 \\2'	
		}
	},
		{
		'name' : 'lose $',
		'compress' : {
			'in' : '([lL]ose) \$(\d)',
			'out' : '_\\2$'	
		},
		'expand' : {
			'in':'_(\d)\$',
			'out' : 'Lose $\\1'	
		}
	},
	{
		'name' : 'lose x',
		'compress' : {
			'in' : '([lL]ose) (\d) (Sanity|Stamina|[iI]tem)',
			'out' : '_\\2\\3'	
		},
		'expand' : {
			'in':'_(\d)([^ ]+)',
			'out' : 'Lose \\1 \\2'	
		}
	},
]

def run(action, stream) :
	for transform in transformations :
		
		operations = transform[action]

		if 'pre' in operations :
			for p in operations['pre'] :
				stream = stream.replace(p[1],p[2])
		stream = re.sub( 
			operations['in'], 
			operations['out'], 
			stream 
		)
		if 'post' in operations :
			for p in operations['post'] :
				stream = stream.replace(p[1],p[2])
		# print(stream[:1000])
		# print('-----------------------------------------------')

	return stream

def clean(stream) :
	ops = [
		['Mkae', 'Make'],
		['\[\d\] ', ''],
		['\[\[Clue', 'Clue'],
		['\[\[William Bain', 'William Bain'],
		['\[\[Madness\]', 'Madness'],
		['\[\[Stamina', 'Stamina'],
		['\[\[Spell\]', 'Spell'],
		['\[\[toughness\]', 'toughness'],
		['[dD]raw a Madness Card', 'Lose 2 Sanity'],
		['Rail Pass card', 'Common Item'],
		['gain 1 Corruption card', 'Lose 2 Sanity']
	]

	for op in ops :
		stream = re.sub(op[0], op[1], stream)

	return stream

if __name__ == '__main__' :

	action = argv[1] if len(argv)>1 else 'compress'
	if not action in ['compress', 'expand', 'test']:
		exit("dico.py [compress, expand] (file)")

	filename = argv[2] if len(argv)>2 else '../datasets/full/input.txt'
	stream = open(filename, 'r').read()

	stream = clean(stream)

	if action == 'test' :
		stream = run('compress', stream)
		stream = run('expand', stream)
		print(stream)

	else :
		stream = run(action, stream)
		out_path = '../datasets/transform/'
		if not path.exists(out_path) : makedirs(out_path)
		open(out_path+'input.txt', 'w').write(stream)



	


