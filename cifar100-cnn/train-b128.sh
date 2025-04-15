#!/bin/bash
python train.py -net resnet50 -gpu -b 128 -warm 5 -mode cc
python train-amp.py -net resnet50 -gpu -b 128 -warm 5 -mode cc
echo "Resnet50 Done"

python train.py -net vgg16 -gpu -b 128 -warm 5 -mode cc
python train-amp.py -net vgg16 -gpu -b 128 -warm 5 -mode cc
echo "Vgg16 Done"


python train.py -net mobilenetv2 -gpu -b 128 -warm 5 -mode cc
python train-amp.py -net mobilenetv2 -gpu -b 128 -warm 5 -mode cc
echo "mobilenetv2 Done"


python train.py -net squeezenet -gpu -b 128 -warm 5 -mode cc
python train-amp.py -net squeezenet -gpu -b 128 -warm 5 -mode cc
echo "squeezenet Done"

python train.py -net attention92 -gpu -b 128 -lr 0.01 -warm 5 -mode cc
python train-amp.py -net attention92 -gpu -b 128 -lr 0.01 -warm 5 -mode cc
echo "attention92 Done"


python train.py -net inceptionv4 -gpu -b 128 -warm 5 -mode cc
python train-amp.py -net inceptionv4 -gpu -b 128 -warm 5 -mode cc
echo "inceptionv4 Done"