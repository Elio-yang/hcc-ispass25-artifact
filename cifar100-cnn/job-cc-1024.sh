#!/bin/bash

echo "cc started" >> train.log
# -----------------------------------------------------------------------------------------
#!/bin/bash
python train.py -net vgg16 -gpu -b 1024 -warm 5 -mode cc
python train-amp.py -net vgg16 -gpu -b 1024 -warm 5 -mode cc
echo "cc fp32 vgg16 finished" >> train.log
python train-fp16.py -net vgg16 -gpu -b 1024 -warm 5 -mode cc -fp16 -fp16i
python train-fp16.py -net vgg16 -gpu -b 2048 -warm 5 -mode cc -fp16 -fp16i
echo "cc fp16  vgg16 done" >> train.log




python train.py -net resnet50 -gpu -b 1024 -warm 5 -mode cc
python train-amp.py -net resnet50 -gpu -b 1024 -warm 5 -mode cc
echo "cc fp32 resnet50 finished" >> train.log
python train-fp16.py -net resnet50 -gpu -b 1024 -warm 5 -mode cc -fp16 -fp16i
echo "cc fp16 resnet50 done" >> train.log




python train.py -net mobilenetv2 -gpu -b 1024 -warm 5 -mode cc
python train-amp.py -net mobilenetv2 -gpu -b 1024 -warm 5 -mode cc
echo "cc fp32 mobilenetv2 finished" >> train.log
python train-fp16.py -net mobilenetv2 -gpu -b 1024 -warm 5 -mode cc -fp16 -fp16i
echo "cc fp16  mobilenetv2 done" >> train.log




python train.py -net squeezenet -gpu -b 1024 -warm 5 -mode cc
python train-amp.py -net squeezenet -gpu -b 1024 -warm 5 -mode cc
echo "cc fp32 squeezenet finished" >> train.log
python train-fp16.py -net squeezenet -gpu -b 1024 -warm 5 -mode cc -fp16 -fp16i
python train-fp16.py -net squeezenet -gpu -b 2048 -warm 5 -mode cc -fp16 -fp16i
echo "cc fp16  squeezenet done" >> train.log




python train.py -net attention92 -gpu -b 1024 -lr 0.01 -warm 5 -mode cc
python train-amp.py -net attention92 -gpu -b 1024 -lr 0.01 -warm 5 -mode cc
echo "cc fp32 attention92 finished" >> train.log
python train-fp16.py -net attention92 -gpu -b 1024 -lr 0.01 -warm 5 -mode cc -fp16 -fp16i
echo "cc fp16  attention92 done" >> train.log




python train.py -net inceptionv4 -gpu -b 1024 -warm 5 -mode cc
python train-amp.py -net inceptionv4 -gpu -b 1024 -warm 5 -mode cc
echo "cc fp32 inceptionv4 finished" >> train.log
python train-fp16.py -net inceptionv4 -gpu -b 1024 -warm 5 -mode cc -fp16 -fp16i
echo "cc fp16  inceptionv4 done" >> train.log