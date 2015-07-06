import json
from sys import argv

datasets_folder = argv[1]+'/' if len(argv)>1 else '../datasets/'
debug = len(argv)>2

situations = sorted(set(open(datasets_folder+'situations/input.txt','r').readlines()))
texts = sorted(set(open(datasets_folder+'full/input.txt','r').readlines()))


attributes = ['Will', 'Fight', 'Luck', 'Lore', 'Speed', 'Sneak']
payments = [' pay ', 'Pay', 'Discard']

cards = []
for situation in situations :
	situation = situation[:-1]
	card = {
		'situation' : situation
	}
	for text in texts :
		if situation in text :
			rest = text[len(situation):-1]
			card['rest'] = rest
			card['checks'] = [ attr for attr in attributes if ' a '+attr in rest]
			card['price'] = [ pay for pay in payments if pay in rest]
			cards.append(card)
			break

if not debug :
	open(datasets_folder+'situations/situations.json','w').write(json.dumps(cards,indent=4))
else :
	print(json.dumps([c for c in cards if c['price'] ], indent=4))

print('checks : '+str(sum([ card['checks'] != [] for card in cards ])/len(cards)))
print('price : '+str(sum([ card['price'] != [] for card in cards ])/len(cards)))