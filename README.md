Install & requirements
======================

The gist of it:

	# ArkhamHorrorGenerator
	git clone https://github.com/centime/ArkhamHorrorGenerator
	cd ArkhamHorrorGenerator

	# Torch
	# http://torch.ch/docs/getting-started.html#
	curl -sk https://raw.githubusercontent.com/torch/ezinstall/master/install-deps | bash
	git clone https://github.com/torch/distro.git ~/torch --recursive
	cd ~/torch; ./install.sh
	source ~/.bashrc # Or .zshrc, or whatever you use

	# char-nn
	# http://karpathy.github.io/2015/05/21/rnn-effectiveness/
	# https://github.com/karpathy/char-rnn
	git clone https://github.com/karpathy/char-rnn
	luarocks install nngraph 
	luarocks install optim

	# [Optional : openCL GPU]
	# For the drivers, see here: https://wiki.archlinux.org/index.php/GPGPU
	luarocks install cltorch
	luarocks install clnn

	# [Optional : Building the datasets] 
	go get github.com/ericchiang/pup

	# Spell checking
	# You'll need the en-US dict as well. For Arch : yaourt aspell-en
	pip3 install language-check


[Optional] Building the datasets
================================

	cd script 

	# The basic set
	# ../dataset/full/input.txt
	python3 scrapper.py

	# Alternative set with 'situations' (encounter = situation + challenge)
	# ../dataset/situations/input.txt
	python3 extract_situations.py

	# Create a json of featured encounters, for classification
	# ../dataset/situations/situations.json
	python3 feature_situations.py

	# HP Lovecraft's bibliography, to later add to the training sets
	# ../datasets/hplovecraft-texts/full/input.txt
	python3 HBL_scrapper.py

	# Alternative set with transformations for frequent encounter structures
	# ../datasets/transform/input.txt
	python3 transforms.py


Training
========

	th train.lua -eval_val_every 60 -batch_size 30 -seq_length 120 -data_dir ../datasets/full -checkpoint_dir ../trained/situations/bs30-sl120

See http://karpathy.github.io/2015/05/21/rnn-effectiveness/ and https://github.com/karpathy/char-rnn


Sampling
========
	
	# situ_sampler.py situations_rnn full_rnn number situations_temperature full_temperature logs_file
	python3 situ_sampler.py ../trained/situations/bs30-sl120/lm_lstm_epoch7.27_1.2093.t7 ../trained/bs30-sl200/lm_lstm_epoch29.03_1.0138.t7 5 0.6 0.6 logs

	# log_manager.py logs_file [reverse]
	python3 log_manager.py logs

Older scripts

	# python3 sampler.py path_to_file approx_number_of_samples temperature [expand]	
	# Example:
	python3 sampler.py ../trained/situations/30-120/lm_lstm_epoch28.33_1.3988.t7 6 0.7

	# Get samples and reverse the transforms
	python3 sampler.py ../trained/transformed/bs30-sl200/lm_lstm_epoch41.38_1.1378.t7 6 0.7 expand



Roadmap
=======

Randomly ordered :
	
	- Shuffle dataset prior to training (cuz of a lacking chr-rnn feature regarding init_from)
	- Situations classification (Which test/challenge is the most suited ?)
	- size_rnn, layers, ...
	- Parallela
	- Use the HPL dataset
	- Code cleaning / refactors
	- Transforms ?

Results
=======

See the Trained.txt file for validation losses with multiple setups.


Situation generation + random check + primed generation


	┌─[centime@centime-arch]-[~/projets/arkham/scripts]
	└───╼ python3 situ_sampler.py ../trained/situations/bs30-sl120/lm_lstm_epoch7.27_1.2093.t7 ../trained/bs30-sl200/lm_lstm_epoch29.03_1.0138.t7 5 0.6 0.6 logs

	[0] Spying as offiring stone. Make a Lore (+2) check. If you fail, you are delayed

	[1] You find a man painting the walls to you. Make a Speed (+2) check or lose 2 Stamina

	[2] A beasing seems to have salence. Make a Luck (+1) check. If you pass, you lose all of your more suspering and comes up to you. Take his Ally card if it's available. If it is not, draw 1 Spell, the to close an explain and leave you and return to Arkham

	[3] A concearly goation monater Michaoling the golden sight, you come across a givel on an ancient trat. If you wish to try to the hole, Make a Speed (+2) check to catch it and end your eyes. If you fail, lose 3 Stamina. Draw 1 Spell. If you fail, you realize that you are blood the darkness. On a successes you into the shack, points. You may discard 1 Spell

	[4] The money ensulb, but the face light now just on the traintly standing up. Make a Fight (+1) check. If you fail, you may draw a monster from the top of the chospures. If you fail, lose 2 Sanity

	[5] The minstwole investigating the oceatator, the locals has thought. Make a Fight (+2) check. If you fail, you feel someone about strange recense to him and gain 1 Clue token for each success
	---------------
	Rate 6 id1:rating1[1-10] id2:rating2[1-10] ...
	0:10 1:10 2:8 3:0 4:7 5:5

	┌─[centime@centime-arch]-[~/projets/arkham/scripts]
	└───╼ python3 log_manager.py logs

	[...]

	[47] 9 : During the night, and he takes a lith of your boods. Make a Lore (+1) check and gain 1 Clue token for each success.

	[48] 9 : An unruly gang have dropting that you have to take a sacrifice. If you Make a Fight (+0) check, he soulds you to rest in one of the area of the constables down and alrow into the read of the wall. Pass a Will (1) check or lose 2 Stamina

	[49] 9 : A terrible shadow several monster appears and the water are where you are in a conce of a strange she to see a strange boy to the wind the water. If you do so, Make a Speed (+1) check to gain 1 Sanity and 1 Stamina.

	[50] 9 : One of the wooden down the constrates are seems to be a bad idently. Make a Speed (+0) check or lose 1 Stamina

	[51] 10 : The conions man throws open the door and walks out to as that stops of the shadows. Make a Sneak (+0) check. If you pass, gain 1 Unique Item.

	[52] 10 : A monster appear! Make a Lore (+2) check. If you pass, you gain 1 Clue token.

	[53] 10 : Although it is strange the water surface. You may Make a Sneak (+1) check to find a small concessing a creature. If you pass, gain 1 Unique Item.

	[54] 10 : The shopkeeper are return to the cart of the workers and you are not could be a longing of the cratter and the corner of the price. If you accept, Make a Sneak (+2) check to receive them off the professor all equating and gain 2 Clue tokens. If you fail, you are delayed.

	[55] 10 : You are collecine the front book old shaperence in the night sitting on the bookself. Make a Lore (+1) check. If you pass, you may then draw a Spell and you are delayed

	[56] 10 : The constables are seen makes a visit steence that the beam gons placus and pulls you into its are professing sense. Make a Sneak (+2) check and gain 1 Clue token. If you fail, you are reduced to 1 Sanity and 1 Stamina

	[57] 10 : A terrible monster appears! Make a Speed (+2) check to reach the book is covered in the church

	[58] 10 : A young store in the wall in the Dreamlands. Make a Luck (+2) check and gain a Retainer card

	[59] 10 : A weathered man inside the trile of patch is scaries this to come. Make a Fight (+0) check or you are delayed

	[60] 10 : retrieve it, you see a tusses of those of a strange decidet. If you ignore it, Make a Luck (+0) check to try to return to Arkham. If you fail, roll a die and gain 1 Clue tokens

	[61] 10 : Spying as offiring stone. Make a Lore (+2) check. If you fail, you are delayed

	[62] 10 : You find a man painting the walls to you. Make a Speed (+2) check or lose 2 Stamina

	------------------------
	Edit rating with the following syntax: id1:rating1 id2:rating2 ...
	60:8 59:8 57:7 56:9 55:9 54:8 53:8 51:9

