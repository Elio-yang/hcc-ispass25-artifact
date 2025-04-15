#!/bin/bash
python train-fp16.py -net resnet50 -gpu -b 256 -warm 5 -mode cc -fp16 -fp16i
python train-fp16.py -net vgg16 -gpu -b 256 -warm 5 -mode cc -fp16 -fp16i
python train-fp16.py -net mobilenetv2 -gpu -b 256 -warm 5 -mode cc -fp16 -fp16i
python train-fp16.py -net squeezenet -gpu -b 256 -warm 5 -mode cc -fp16 -fp16i
python train-fp16.py -net attention92 -gpu -b 256 -lr 0.01 -warm 5 -mode cc -fp16 -fp16i
python train-fp16.py -net inceptionv4 -gpu -b 256 -warm 5 -mode cc -fp16 -fp16i
echo "cc train-b256.sh finished" >> train.log