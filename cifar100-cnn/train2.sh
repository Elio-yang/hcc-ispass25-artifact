#!/bin/bash

echo " bf started" >> train.log

/shared/cifar100-cnn/train-fp-b1024.sh
echo " bf train1024.sh finished" >> train.log
