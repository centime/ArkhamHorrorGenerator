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

	# python3 sampler.py path_to_file approx_number_of_samples temperature [expand]	
	# Example:
	python3 sampler.py ../trained/situations/30-120/lm_lstm_epoch28.33_1.3988.t7 6 0.7

	# Get samples and reverse the transforms
	python3 sampler.py ../trained/transformed/bs30-sl200/lm_lstm_epoch41.38_1.1378.t7 6 0.7 expand

Roadmap
=======

Randomly ordered :

	- Situations classification (Which test/challenge is the most suited ?)
	- size_rnn, layers, ...
	- Parallela
	- Interactive evaluation of outputs ("This one result was really good, better add it to the dataset")
	- Use the HPL dataset
	- Code cleaning / refactors
	- Transforms ?

Results
=======

See the Trained.txt file for validation losses with multiple setups.


Situation generation + random check + primed generation

	└───╼ python3 situ_sampler.py ../trained/situations/bs30-sl120/lm_lstm_epoch2.47_1.2227.t7 ../trained/bs30-sl200/lm_lstm_epoch29.03_1.0138.t7 5 0.4 0.5 
	-
	Although it is strange the water surface. You may Make a Sneak (+1) check to find a small concessing a creature. If you pass, gain 1 Unique Item.
	-
	The shopkeeper are return to the cart of the workers and you are not could be a longing of the cratter and the corner of the price. If you accept, Make a Sneak (+2) check to receive them off the professor all equating and gain 2 Clue tokens. If you fail, you are delayed.
	-
	The more the books of the coniate your cell wall out the other Sitting of the revierd. Make a Will (+2) check. If you pass, you may search the Unique Item deck. If you fail, lose 1 Stamina.
	-
	A monster appears! Make a Speed (+1) check to take it.
	-
	A monster appear! Make a Lore (+2) check. If you pass, you gain 1 Clue token.
	-
	A strange changer from the darkness he seen your head to the wind the gravey are to purpon to the ground. Make a Sneak (+1) check to see if there are in the strange pate. If you pass, gain 1 Clue token.

	┌─[centime@centime-arch]-[~/projets/arkham/scripts]
	└───╼ python3 situ_sampler.py ../trained/situations/bs30-sl120/lm_lstm_epoch2.47_1.2227.t7 ../trained/bs30-sl200/lm_lstm_epoch29.03_1.0138.t7 5 0.4 0.5
	-
	As you browse the door to the rock to the book and a musture of the workers who challenges you a ride and have to hear the table remains to the door and a monster appear! Make a Fight (+2) check. If you pass, you see a musty pass a -1 ob eith the mostled cooticite. If you pass, gain 1 Common Item. If you fail, you are delayed.
	-
	You are winded to the box of the ancient his begin to stay to the water. If you accept, Make a Will (+0) check to convince the walls. If you pass, lose 1 Stamina.
	-
	The ciff on the walls are entructing your eyes you a ride and then return to be offers. Make a Lore (+2) check to interpret them.
	-
	A terrible shadow several monster appears and the water are where you are in a conce of a strange she to see a strange boy to the wind the water. If you do so, Make a Speed (+1) check to gain 1 Sanity and 1 Stamina.




