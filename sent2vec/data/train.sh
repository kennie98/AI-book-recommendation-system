#!/bin/bash

../fasttext sent2vec -input $1 -output model -minCount 8 -dim 400 -epoch 50 -lr 0.2 -wordNgrams 2 -loss ns -neg 10 -thread 20 -t 0.000005 -dropoutK 4 -minCountLabel 20 -bucket 2000000 -maxVocabSize 400000 -numCheckPoints 10
