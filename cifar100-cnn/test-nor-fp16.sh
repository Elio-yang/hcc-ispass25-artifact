#!/bin/bash

echo "started" >> test.log

# amp model with amp inference
python test-fp16.py -net vgg16 -gpu -b 1024 -mode nor -fp16i -weights /shared/cifar100-cnn/normal-dnn/bf16-checkpoint/vgg16/Monday_02_December_2024_03h_02m_01s/vgg16-200-regular.pth
echo "vgg16 finished" >> test.log

python test-fp16.py -net resnet50 -gpu -b 1024 -mode nor -fp16i -weights /shared/cifar100-cnn/normal-dnn/bf16-checkpoint/resnet50/Monday_02_December_2024_03h_33m_25s//resnet50-200-regular.pth
echo "resnet50 finished" >> test.log

python test-fp16.py -net mobilenetv2 -gpu -b 1024 -mode nor -fp16i -weights /shared/cifar100-cnn/normal-dnn/bf16-checkpoint/mobilenetv2/Monday_02_December_2024_03h_57m_27s//mobilenetv2-200-regular.pth
echo "mobilenetv2 finished" >> test.log

python test-fp16.py -net squeezenet -gpu -b 1024 -mode nor -fp16i -weights /shared/cifar100-cnn/normal-dnn/bf16-checkpoint/squeezenet/Monday_02_December_2024_04h_14m_03s//squeezenet-200-regular.pth
echo "squeezenet finished" >> test.log

python test-fp16.py -net attention92 -gpu -b 1024 -mode nor -fp16i -weights /shared/cifar100-cnn/normal-dnn/bf16-checkpoint/attention92/Monday_02_December_2024_04h_45m_41s//attention92-200-regular.pth
echo "attention92 finished" >> test.log

python test-fp16.py -net inceptionv4 -gpu -b 1024 -mode nor -fp16i -weights /shared/cifar100-cnn/normal-dnn/bf16-checkpoint/inceptionv4/Monday_02_December_2024_05h_20m_59s//inceptionv4-200-regular.pth
echo "inceptionv4 finished" >> test.log