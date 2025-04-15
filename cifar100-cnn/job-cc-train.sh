#!/bin/bash

echo "cc started" >> train.log
# -----------------------------------------------------------------------------------------
# /shared/cifar100-cnn/train-b1024.sh
# echo "cc fp32 train1024.sh finished" >> train.log

# python train-fp16.py -net resnet50 -gpu -b 1024 -warm 5 -mode cc -fp16 -fp16i
# echo "cc fp16 resnet50 done" >> train.log

# python train-fp16.py -net vgg16 -gpu -b 1024 -warm 5 -mode cc -fp16 -fp16i
# python train-fp16.py -net vgg16 -gpu -b 2048 -warm 5 -mode cc -fp16 -fp16i
# echo "cc fp16  vgg16 done" >> train.log

# python train-fp16.py -net mobilenetv2 -gpu -b 1024 -warm 5 -mode cc -fp16 -fp16i
# echo "cc fp16  mobilenetv2 done" >> train.log

# python train-fp16.py -net squeezenet -gpu -b 1024 -warm 5 -mode cc -fp16 -fp16i
# python train-fp16.py -net squeezenet -gpu -b 2048 -warm 5 -mode cc -fp16 -fp16i
# echo "cc fp16  squeezenet done" >> train.log

# python train-fp16.py -net attention92 -gpu -b 1024 -lr 0.01 -warm 5 -mode cc -fp16 -fp16i
# echo "cc fp16  attention92 done" >> train.log

# python train-fp16.py -net inceptionv4 -gpu -b 1024 -warm 5 -mode cc -fp16 -fp16i
# echo "cc fp16  inceptionv4 done" >> train.log

# echo "cc train1024.sh finished" >> train.log
# # -----------------------------------------------------------------------------------------
/shared/cifar100-cnn/train-b512.sh
echo "cc train512.sh finished" >> train.log

/shared/cifar100-cnn/train-b256.sh
echo "cc train256.sh finished" >> train.log

/shared/cifar100-cnn/train-b128.sh
echo "cc train128.sh finished" >> train.log

/shared/cifar100-cnn/train-b64.sh
echo "cc train64.sh finished" >> train.log
# -----------------------------------------------------------------------------------------