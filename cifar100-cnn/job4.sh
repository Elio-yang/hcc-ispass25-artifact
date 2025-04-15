#!/bin/bash

# static fp16
python train-fp16.py -net vgg16 -gpu -b 1024 -warm 5 -mode nor -fp16 -fp16i
python train-fp16.py -net vgg16 -gpu -b 2048 -warm 5 -mode nor -fp16 -fp16i
python train-fp16.py -net resnet50 -gpu -b 1024 -warm 5 -mode nor -fp16 -fp16i
python train-fp16.py -net mobilenetv2 -gpu -b 1024 -warm 5 -mode nor -fp16 -fp16i
python train-fp16.py -net squeezenet -gpu -b 1024 -warm 5 -mode nor -fp16 -fp16i
python train-fp16.py -net squeezenet -gpu -b 2048 -warm 5 -mode nor -fp16 -fp16i
python train-fp16.py -net attention92 -gpu -b 1024 -lr 0.01 -warm 5 -mode nor -fp16 -fp16i
python train-fp16.py -net inceptionv4 -gpu -b 1024 -warm 5 -mode nor -fp16 -fp16i
echo "fp 16 with bs1024 finished" >> train.log
