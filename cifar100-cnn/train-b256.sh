#!/bin/bash
python train.py -net resnet50 -gpu -b 256 -warm 5 -mode cc
python train-amp.py -net resnet50 -gpu -b 256 -warm 5 -mode cc

python train.py -net vgg16 -gpu -b 256 -warm 5 -mode cc
python train-amp.py -net vgg16 -gpu -b 256 -warm 5 -mode cc

python train.py -net mobilenetv2 -gpu -b 256 -warm 5 -mode cc
python train-amp.py -net mobilenetv2 -gpu -b 256 -warm 5 -mode cc

python train.py -net squeezenet -gpu -b 256 -warm 5 -mode cc
python train-amp.py -net squeezenet -gpu -b 256 -warm 5 -mode cc

python train.py -net inceptionv4 -gpu -b 256 -warm 5 -mode cc
python train-amp.py -net inceptionv4 -gpu -b 256 -warm 5 -mode cc

python train.py -net attention92 -gpu -b 256 -lr 0.01 -warm 5 -mode cc
python train-amp.py -net attention92 -gpu -b 256 -lr 0.01 -warm 5 -mode cc