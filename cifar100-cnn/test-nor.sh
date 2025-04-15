#!/bin/bash

batchsize_list=(1)
#batchsize_list=(1024 512 256 128 64 32 16 8 4 2 1)

for batchsize in ${batchsize_list[@]}; do
    echo "nor batchsize: $batchsize" >> test.log
    #python test.py -net vgg16 -gpu -b $batchsize -mode nor -weights /shared/cifar100-cnn/normal-dnn/checkpoint/vgg16/Thursday_28_November_2024_08h_52m_11s/vgg16-200-regular.pth
    #python test-amp.py -net vgg16 -gpu -b $batchsize -mode nor -weights /shared/cifar100-cnn/normal-dnn/checkpoint/vgg16/Thursday_28_November_2024_09h_09m_34s/vgg16-200-best.pth
    #python test-fp16.py -net vgg16 -gpu -b $batchsize -mode nor -fp16i -weights /shared/cifar100-cnn/normal-dnn/bf16-checkpoint/vgg16/Monday_02_December_2024_03h_02m_01s/vgg16-200-regular.pth


    #python test.py -net resnet50 -gpu -b $batchsize -mode nor -weights /shared/cifar100-cnn/normal-dnn/checkpoint/resnet50/Thursday_28_November_2024_07h_48m_20s/resnet50-200-regular.pth
    #python test-amp.py -net resnet50 -gpu -b $batchsize -mode nor -weights /shared/cifar100-cnn/normal-dnn/checkpoint/resnet50/Thursday_28_November_2024_08h_25m_14s/resnet50-200-regular.pth
    #python test-fp16.py -net resnet50 -gpu -b $batchsize -mode nor -fp16i -weights /shared/cifar100-cnn/normal-dnn/bf16-checkpoint/resnet50/Monday_02_December_2024_03h_33m_25s//resnet50-200-regular.pth


    #python test.py -net mobilenetv2 -gpu -b $batchsize -mode nor -weights /shared/cifar100-cnn/normal-dnn/checkpoint/mobilenetv2/Thursday_28_November_2024_09h_27m_12s/mobilenetv2-200-regular.pth
    #python test-amp.py -net mobilenetv2 -gpu -b $batchsize -mode nor -weights /shared/cifar100-cnn/normal-dnn/checkpoint/mobilenetv2/Thursday_28_November_2024_09h_46m_09s/mobilenetv2-200-regular.pth
    #python test-fp16.py -net mobilenetv2 -gpu -b $batchsize -mode nor -fp16i -weights /shared/cifar100-cnn/normal-dnn/bf16-checkpoint/mobilenetv2/Monday_02_December_2024_03h_57m_27s//mobilenetv2-200-regular.pth


    #python test.py -net squeezenet -gpu -b $batchsize -mode nor -weights /shared/cifar100-cnn/normal-dnn/checkpoint/squeezenet/Thursday_28_November_2024_10h_03m_49s/squeezenet-200-regular.pth
    #python test-amp.py -net squeezenet -gpu -b $batchsize -mode nor -weights /shared/cifar100-cnn/normal-dnn/checkpoint/squeezenet/Thursday_28_November_2024_10h_19m_36s/squeezenet-200-regular.pth
    #python test-fp16.py -net squeezenet -gpu -b $batchsize -mode nor -fp16i -weights /shared/cifar100-cnn/normal-dnn/bf16-checkpoint/squeezenet/Monday_02_December_2024_04h_14m_03s//squeezenet-200-regular.pth



    python test.py -net attention92 -gpu -b $batchsize -mode nor -weights /shared/cifar100-cnn/normal-dnn/checkpoint/attention92/Thursday_28_November_2024_10h_35m_37s/attention92-200-regular.pth -times 6
    python test-amp.py -net attention92 -gpu -b $batchsize -mode nor -weights /shared/cifar100-cnn/normal-dnn/checkpoint/attention92/Thursday_28_November_2024_11h_34m_44s/attention92-200-regular.pth -times 6
    python test-fp16.py -net attention92 -gpu -b $batchsize -mode nor -fp16i -weights /shared/cifar100-cnn/normal-dnn/bf16-checkpoint/attention92/Monday_02_December_2024_04h_45m_41s//attention92-200-regular.pth -times 6


    python test.py -net inceptionv4 -gpu -b $batchsize -mode nor -weights /shared/cifar100-cnn/normal-dnn/checkpoint/inceptionv4/Thursday_28_November_2024_12h_24m_42s/inceptionv4-200-regular.pth -times 6
    python test-amp.py -net inceptionv4 -gpu -b $batchsize -mode nor -weights /shared/cifar100-cnn/normal-dnn/checkpoint/inceptionv4/Thursday_28_November_2024_15h_08m_36s/inceptionv4-200-regular.pth -times 6
    python test-fp16.py -net inceptionv4 -gpu -b $batchsize -mode nor -fp16i -weights /shared/cifar100-cnn/normal-dnn/bf16-checkpoint/inceptionv4/Monday_02_December_2024_05h_20m_59s//inceptionv4-200-regular.pth -times 6
done   
