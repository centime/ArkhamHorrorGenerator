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
	
	See the Trained.txt file.

