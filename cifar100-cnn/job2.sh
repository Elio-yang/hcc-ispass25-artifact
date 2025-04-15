#!/bin/bash


# test each model
./test1.sh
echo "test1.sh finished" >> train.log

# make it stable
python train.py -net vgg16 -gpu -b 256 -warm 5 -mode nor
python train-amp.py -net vgg16 -gpu -b 256 -warm 5 -mode nor
python train.py -net vgg16 -gpu -b 512 -warm 5 -mode nor
python train-amp.py -net vgg16 -gpu -b 512 -warm 5 -mode nor
echo "stable train few finished" >> train.log

python train-fp16.py -net vgg16 -gpu -b 1024 -warm 5 -mode nor -fp16 -fp16i
python train-fp16.py -net resnet50 -gpu -b 1024 -warm 5 -mode nor -fp16 -fp16i
python train-fp16.py -net mobilenetv2 -gpu -b 1024 -warm 5 -mode nor -fp16 -fp16i
python train-fp16.py -net squeezenet -gpu -b 1024 -warm 5 -mode nor -fp16 -fp16i
python train-fp16.py -net attention92 -gpu -b 1024 -lr 0.01 -warm 5 -mode nor -fp16 -fp16i
python train-fp16.py -net inceptionv4 -gpu -b 1024 -warm 5 -mode nor -fp16 -fp16i
echo "fp 16 with bs1024 finished" >> train.log
