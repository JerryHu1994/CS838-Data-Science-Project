#!/bin/bash

# Generate both positive and negative samples
# make sure using python 3
echo "Creating the feature vectors..."
python ./tools/feature_generator/splitTaggedText.py ./data/train_data ./tools/feature_generator/train_positive.dat pos
python ./tools/feature_generator/splitTaggedText.py ./data/train_data ./tools/feature_generator/train_negative.dat neg
python ./tools/feature_generator/splitTaggedText.py ./data/test_data ./tools/feature_generator/test_positive.dat pos
python ./tools/feature_generator/splitTaggedText.py ./data/test_data ./tools/feature_generator/test_negative.dat neg

echo "Moving the samples to for ML use..."
cp ./tools/feature_generator/train_positive.dat ./Ml/analysis/
cp ./tools/feature_generator/train_negative.dat ./Ml/analysis/
cp ./tools/feature_generator/test_positive.dat ./Ml/analysis/
cp ./tools/feature_generator/test_negative.dat ./Ml/analysis/

# Prune the negative samples

# Run cross-validation on five ML classifiers, choose the best classifier and print results.
# python train.py