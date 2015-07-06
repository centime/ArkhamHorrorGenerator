import re
from sys import argv
from os import makedirs, path

datasets_folder = argv[1]+'/' if len(argv)>1 else '../datasets/'
debug = len(argv)>2

stream = open(datasets_folder+'/full/input.txt','r').read()

stream = '\n'+stream.replace('\n','\n\n ')

keywords = [
	'[mM]ak(e|ing) a ([^ ]+) \(([\+-]\d)\)* check',
	'[mM]ak(e|ing) a ([^ ]+) \(([\+-]\d)\)* check',
	'[pP]ass(ing)* a ([^ ]+)* \(([\+-]\d)\)* check',
	'[aA]ttempt a ([^ ]+) \(([\+-]\d)\) check',
	'[sS]ucceed at a ([^ ]+) \(([\+-]\d)\) check',
	'[wW]ith a ([^ ]+) \(([\+-]\d)\) check',
	'[iI]f you succeed in a ([^ ]+) \(([\+-]\d)\) check',
	'Make a Speed check',
	'Make a \(\+0\) check',
	'Make a Fight \(\+0\) or Will \(\+0\) check.',
	'You automatically fail',
	'If you pass',
	'[lL]ose',
	'[gG]ain',
	'[lL]ose',
	'[gG]ain',
	'[pP]ay (\$\d|up to|him|her|\d Clue)',
	'give her \$5 to pay',
	'[dD]iscard',
	'[sS]pend',
	'[dD]raw a',
	'[yY]ou are delayed',
	'Cursed',
	'Blessed',
	'((If )?[yY]our|(([yY]ou )?[rR]egain) \d|([yY]ou are (reduced|restored) to|[iI]f) (your (maximum|current)|\d)) (Stamina|Sanity)',
	'currently at less',
	'Since there is only one',
	'Starting with the first player',
	'If another player agrees',
	'You may choose any one player',
	'Regain your choice of',
	' If you reach 0',
	'Take this card',
	'[tT]ake (a Retainer|(his|her|Ryan Dean\'s) Ally) card',
	'take both the Tainted card',
	'If the Act I card',
	'You may choose one Ally card',
	'Return (one|1) Ally',
	'Choose one of your Ally cards',
	'(You may s|S)earch the ',
	'[appears(\\. You| and you)] (suffer|receive)',
	'[yY]ou (suffer|receive)',
	'[rR]oll (\d|one|a|four) dic?e',
	'[tT]ake \d Clue tokens',
	'[iI]f you have \d or (more|less) Clue tokens,',
	'If you (currently )?have',
	'yields \d Clue tokens?',
	'[yY]ou may (buy|take|either) ',
	'[lL]ook at the top (\d|two)? ?card',
	'Turn over the top three Unique Item cards',
	'Turn the top card of a location',
	'Take the (first )?([^ ]+ )?(card|Tome|Mission)',
	'[dD]raw',
	'Your number of Clue tokens',
	'Take a( number of)? Clue tokens?',
	'Buy as many Clues',
	'[mM]ove to ',
	'[yY]ou are devoured',
	'Choose another investigator',
	'Give any other investigator',
	'For each (Clue token|Spell|point|[^ ]+ Item|\$\d)',
	'You may move any ',
	'For each Clue token you have',
	'you may trade',
	'(All|Any) players',
	'\d of your Spells?',
	'Your Luck slider',
	'If there are four or more elder',
	'[kK]eep this card',
	'[pP]lace an? (Patrol|explored) marker',
	'([aA]dd|[rR]emove|You may choose)? ?(\d|one|two) (uprising|monster|doom|Rift progress|gate|Dunwich Horror) token',
	'do not take an explored token',
	'If there (is|are)',
	'[sS]tay here next turn',
	'if you passed a Horror Check',
	'You encounter all monsters currently in the Outskirts',
	'choose (1 Unique Item|another investigator|\d monster|1 Corruption card)',
	'([hH]ave )?([nN]o|an|one) encounter',
	'search the ((Unique|Common) Item|Skill) deck',
	'[sS]earch either the Common',
	'Correctly guess the cost',
	'If the Rare Book Collection card',
	'If the Darke\'s Blessing card',
	'If your Will',
	'do not already have a Retainer card'


]

for kw in keywords :
	rgxp = re.compile('\n(.*) '+kw+'.*\n')
	stream = rgxp.sub('\n\\1\n', stream)
	stream = rgxp.sub('\n\\1\n', stream)

stream = re.sub('\n+', '\n', stream)
stream = re.sub('\n ', '\n', stream)
stream = re.sub('^\n', '', stream)

output_path = datasets_folder+'/situations/'
if not path.exists(output_path): makedirs(output_path)

if not debug :
	open(output_path+'input.txt','w').write(stream)
else :
	print(stream)

""" todo ?

You peek into the back room and see Miriam Beecher, the shopkeeper, unwrapping a mummy stolen from the visiting museum exhibit! If you turn her in, the Sheriff rewards you with a license to investigate as you see fit; take the Private Investigator card. However, Miriam's neighbors think you betrayed her, and you are Barred from Uptown.
 Deputy Dingby forgot to bring his lunch today, and if you help him out, he'll become very friendly and chatty. You may give the Deputy either the Food Common Item card or $1 to

 A gate opens suddenly and pulls you into a strange landscape. Move immediately to Y'ha-nthlei and have an encounter there.

 A ghostly ship captain offers you passage home, for a price. Return to Arkham, but you are

  A group of women are collecting charitable donations on behalf of orphans and widows. If you contribute $3,

 It's not safe this close to the edge of town. You encounter all monsters currently in the Outskirts, in the order of your choice. If you successfully evade any monster, you may choose to

 In this place, it's a stroke of good fortune when nothing terrible happens to you. No encounter.

Mail order! Each investigator may give you money to purchase a single Common Item of his or her choice at list price. Place the items facedown in front of you. If you enter the same location as the investigator who requested the item, give it to him and receive $1 from the bank as a delivery fee.

 Deputy Dingby forgot to bring his lunch today, and if you help him out, he'll become very friendly and chatty. You may give the Deputy either the Food Common Item card or $1 to


"""

