#!/bin/bash

# Generate both positive and negative samples
# make sure using python 3
echo "Creating the feature vectors... "
python ./tools/feature_generator/splitTaggedText.py ./data/train_data ./tools/feature_generator/train_positive.dat pos
python ./tools/feature_generator/splitTaggedText.py ./data/train_data ./tools/feature_generator/train_negative.dat neg
python ./tools/feature_generator/splitTaggedText.py ./data/test_data ./tools/feature_generator/test_positive.dat pos
python ./tools/feature_generator/splitTaggedText.py ./data/test_data ./tools/feature_generator/test_negative.dat neg

echo "Moving the samples to ./ML/analysis "
cp ./tools/feature_generator/train_positive.dat ./ML/analysis/train_positive.dat
cp ./tools/feature_generator/train_negative.dat ./ML/analysis/train_negative.dat
cp ./tools/feature_generator/test_positive.dat ./ML/analysis/test_positive.dat
cp ./tools/feature_generator/test_negative.dat ./ML/analysis/test_negative.dat

# Prune the negative samples
echo "prune negative samples... "
python ./ML/analysis/prune_train_negative.py ./ML/analysis/train_negative.dat ./ML/analysis/train_negative_pruned.dat ./ML/analysis/blacklist.dat
python ./ML/analysis/prune_test_negative.py ./ML/analysis/test_negative.dat ./ML/analysis/test_negative_pruned.dat ./ML/analysis/blacklist.dat


# Run cross-validation on five ML classifiers, choose the best classifier and print results.
python ./ML/analysis/train.py ./ML/analysis/train_positive.dat ./ML/analysis/train_negative_pruned.dat ./ML/analysis/test_positive.dat ./ML/analysis/test_negative_pruned.dat
