#!/bin/bash

echo "started" >> train.log

/shared/cifar100-cnn/train-b1024.sh
echo "train1024.sh finished" >> train.log

/shared/cifar100-cnn/train-b512.sh

echo "train512.sh finished" >> train.log

/shared/cifar100-cnn/train-b256.sh
echo "train256.sh finished" >> train.log

/shared/cifar100-cnn/train-b128.sh
echo "train128.sh finished" >> train.log

/shared/cifar100-cnn/train-b64.sh
echo "train64.sh finished" >> train.log
