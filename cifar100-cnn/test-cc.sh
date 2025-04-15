#!/bin/bash

batchsize_list=(1)
#batchsize_list=(1024 512 256 128 64 32 16 8 4 2 1)

for batchsize in ${batchsize_list[@]}; do
    echo "cc batchsize: $batchsize" >> test.log
    #python test.py -net vgg16 -gpu -b $batchsize -mode cc -weights /shared/cifar100-cnn/checkpoint/vgg16/fp32-b1024/vgg16-200-regular.pth
    #python test-amp.py -net vgg16 -gpu -b $batchsize -mode cc -weights /shared/cifar100-cnn/checkpoint/vgg16/amp-b1024/vgg16-200-regular.pth
    #python test-fp16.py -net vgg16 -gpu -b $batchsize -mode cc -fp16i -weights /shared/cifar100-cnn/checkpoint/vgg16/fp16-b1024/vgg16-200-regular.pth

    #python test.py -net resnet50 -gpu -b $batchsize -mode cc -weights /shared/cifar100-cnn/checkpoint/resnet50/fp32-b1024/resnet50-200-regular.pth
    #python test-amp.py -net resnet50 -gpu -b $batchsize -mode cc -weights /shared/cifar100-cnn/checkpoint/resnet50/amp-b1024/resnet50-200-regular.pth
    #python test-fp16.py -net resnet50 -gpu -b $batchsize -mode cc -fp16i -weights /shared/cifar100-cnn/checkpoint/resnet50/fp16-b1024/resnet50-200-regular.pth

    #python test.py -net mobilenetv2 -gpu -b $batchsize -mode cc -weights /shared/cifar100-cnn/checkpoint/mobilenetv2/fp32-b1024/mobilenetv2-200-regular.pth
    #python test-amp.py -net mobilenetv2 -gpu -b $batchsize -mode cc -weights /shared/cifar100-cnn/checkpoint/mobilenetv2/amp-b1024/mobilenetv2-200-regular.pth
    #python test-fp16.py -net mobilenetv2 -gpu -b $batchsize -mode cc -fp16i -weights /shared/cifar100-cnn/checkpoint/mobilenetv2/fp16-b1024/mobilenetv2-200-regular.pth

    #python test.py -net squeezenet -gpu -b $batchsize -mode cc -weights /shared/cifar100-cnn/checkpoint/squeezenet/fp32-b1024/squeezenet-200-regular.pth
    #python test-amp.py -net squeezenet -gpu -b $batchsize -mode cc -weights /shared/cifar100-cnn/checkpoint/squeezenet/amp-b1024/squeezenet-200-regular.pth
    #python test-fp16.py -net squeezenet -gpu -b $batchsize -mode cc -fp16i -weights /shared/cifar100-cnn/checkpoint/squeezenet/fp16-b1024/squeezenet-200-regular.pth

    python test.py -net attention92 -gpu -b $batchsize -mode cc -weights /shared/cifar100-cnn/checkpoint/attention92/fp32-b1024/attention92-200-regular.pth -times 6
    python test-amp.py -net attention92 -gpu -b $batchsize -mode cc -weights /shared/cifar100-cnn/checkpoint/attention92/amp-b1024/attention92-200-regular.pth -times 6 
    python test-fp16.py -net attention92 -gpu -b $batchsize -mode cc -fp16i -weights /shared/cifar100-cnn/checkpoint/attention92/fp16-b1024/attention92-200-regular.pth -times 6

    python test.py -net inceptionv4 -gpu -b $batchsize -mode cc -weights /shared/cifar100-cnn/checkpoint/inceptionv4/fp32-b1024/inceptionv4-200-regular.pth -times 6
    python test-amp.py -net inceptionv4 -gpu -b $batchsize -mode cc -weights /shared/cifar100-cnn/checkpoint/inceptionv4/amp-b1024/inceptionv4-200-regular.pth -times 6
    python test-fp16.py -net inceptionv4 -gpu -b $batchsize -mode cc -fp16i -weights /shared/cifar100-cnn/checkpoint/inceptionv4/fp16-b1024/inceptionv4-200-regular.pth -times 6
done
