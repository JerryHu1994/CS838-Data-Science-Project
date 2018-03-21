#!/bin/bash
# written by Yaqi Zhang (zhang623@wisc.edu)
# University of Wisconsin-Madison

echo "Creating the feature vectors... "
python ./src/generate_sample.py ./data/train_data ./files/train_positive.dat pos
python ./src/generate_sample.py ./data/train_data ./files/train_negative.dat neg
python ./src/generate_sample.py ./data/test_data ./files/test_positive.dat pos
python ./src/generate_sample.py ./data/test_data ./files/test_negative.dat neg



# Prune the negative samples
python src/prune_negative.py files/train_negative.dat ./files/train_negative_prune.dat ./src/blacklist.dat train
python src/prune_negative.py files/test_negative.dat ./files/test_negative_prune.dat ./src/blacklist.dat test

# train
python src/train.py files/train_positive.dat files/train_negative_prune.dat files/test_positive.dat files/test_negative_prune.dat




