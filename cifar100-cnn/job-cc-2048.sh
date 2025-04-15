#!/bin/bash

echo "cc started" >> train.log
# -----------------------------------------------------------------------------------------
#!/bin/bash

python train.py -net vgg16 -gpu -b 2048 -warm 5 -mode cc
python train-amp.py -net vgg16 -gpu -b 2048 -warm 5 -mode cc
python train.py -net squeezenet -gpu -b 2048 -warm 5 -mode cc
python train-amp.py -net squeezenet -gpu -b 2048 -warm 5 -mode cc

echo "cc fp32 b2048 finished" >> train.log