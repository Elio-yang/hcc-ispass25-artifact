#!/bin/bash


python train-fp16.py -net squeezenet -gpu -b 2048 -warm 5 -mode nor -fp16 -fp16i
python train-amp.py -net squeezenet -gpu -b 2048 -warm 5 -mode nor
python train.py -net squeezenet -gpu -b 2048 -warm 5 -mode nor
