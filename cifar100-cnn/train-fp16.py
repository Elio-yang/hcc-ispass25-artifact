# train.py
#!/usr/bin/env	python3

""" train network using pytorch

author baiyu
"""

import os
import sys
import argparse
import time
from datetime import datetime
import pandas as pd
import numpy as np
import torch
import torch.nn as nn
import torch.optim as optim
import torchvision
import torchvision.transforms as transforms
from torch.utils.data import DataLoader

from utils import set_seed
from conf import settings
from utils import get_network, get_training_dataloader, get_test_dataloader, WarmUpLR, \
    most_recent_folder, most_recent_weights, last_epoch, best_acc_weights

throughputs = []

def train(epoch,fp16, fp16i):

    start = time.time()
    net.train()
    tot_images = len(cifar100_training_loader.dataset)
    epoch_loss = 0
    # mem_before = torch.cuda.memory_allocated()
    for batch_index, (images, labels) in enumerate(cifar100_training_loader):
       
        labels = labels.to('cuda')
        # quantize input to fp16

        if fp16 and fp16i:
            images = images.half().to('cuda')
        else:
            images = images.to('cuda')
        
        outputs = net(images)
        loss = loss_function(outputs, labels)
        loss.backward()
        optimizer.step()
        optimizer.zero_grad()
        epoch_loss = loss.item()

        if epoch <= args.warm:
            warmup_scheduler.step()
    finish = time.time()
    mem_after = torch.cuda.memory_allocated()
    # print('Memory consumed: ', mem_after - mem_before)

    print('epoch {} training time consumed: {:.2f}s'.format(epoch, finish - start))
    # calculate throughputs
    epoch_time = finish - start
    th = tot_images / epoch_time
    batchsize = cifar100_test_loader.batch_size
    throughputs.append([finish, epoch, th, epoch_loss, batchsize])
    print('Epoch {} Thput: {:.2f} img/s'.format(epoch, th))


@torch.no_grad()
def eval_training(epoch=0, tb=True):

    start = time.time()
    net.eval()

    test_loss = 0.0 # cost function error
    correct = 0.0

    for (images, labels) in cifar100_test_loader:

        if args.gpu:
            images = images.cuda()
            labels = labels.cuda()

        outputs = net(images)
        loss = loss_function(outputs, labels)

        test_loss += loss.item()
        _, preds = outputs.max(1)
        correct += preds.eq(labels).sum()

    finish = time.time()

    print('Evaluating Network.....')
    print('Test set: Epoch: {}, Average loss: {:.4f}, Accuracy: {:.4f}, Time consumed:{:.2f}s'.format(
        epoch,
        test_loss / len(cifar100_test_loader.dataset),
        correct.float() / len(cifar100_test_loader.dataset),
        finish - start
    ))
    print()


    return correct.float() / len(cifar100_test_loader.dataset)

if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument('-net', type=str, required=True, help='net type')
    parser.add_argument('-gpu', action='store_true', default=False, help='use gpu or not')
    parser.add_argument('-b', type=int, default=128, help='batch size for dataloader')
    parser.add_argument('-warm', type=int, default=1, help='warm up training phase')
    parser.add_argument('-lr', type=float, default=0.1, help='initial learning rate')
    parser.add_argument('-resume', action='store_true', default=False, help='resume training')
    parser.add_argument('-mode', type=str, default='nor', help='cc or nor')
    parser.add_argument('-fp16', action='store_true', default=False, help='use fp16 to train')
    parser.add_argument('-fp16i', action='store_true', default=False, help='use fp16 for input to train')
    args = parser.parse_args()

    set_seed(42)

    net = get_network(args).to('cuda')

    if args.fp16:
        from fp16util import network_to_half
        net = network_to_half(net)
    

    #data preprocessing:
    cifar100_training_loader = get_training_dataloader(
        settings.CIFAR100_TRAIN_MEAN,
        settings.CIFAR100_TRAIN_STD,
        num_workers=4,
        batch_size=args.b,
        shuffle=True
    )

    cifar100_test_loader = get_test_dataloader(
        settings.CIFAR100_TRAIN_MEAN,
        settings.CIFAR100_TRAIN_STD,
        num_workers=4,
        batch_size=args.b,
        shuffle=True
    )


    compute_mode = args.mode
    my_logfile_name = args.net+"-"+compute_mode+"-e"+str(settings.EPOCH)+"-b"+str(cifar100_training_loader.batch_size)+"_fp16_train_throughputs.csv"
    abspath = "/shared/cifar100-cnn/mylogs/"
    logpath = abspath + my_logfile_name
    print("Logging to: ", logpath)


    loss_function = nn.CrossEntropyLoss()
    optimizer = optim.SGD(net.parameters(), lr=args.lr, momentum=0.9, weight_decay=5e-4)
    train_scheduler = optim.lr_scheduler.MultiStepLR(optimizer, milestones=settings.MILESTONES, gamma=0.2) #learning rate decay
    iter_per_epoch = len(cifar100_training_loader)
    warmup_scheduler = WarmUpLR(optimizer, iter_per_epoch * args.warm)

    if args.resume:
        recent_folder = most_recent_folder(os.path.join(settings.CHECKPOINT_PATH, args.net), fmt=settings.DATE_FORMAT)
        if not recent_folder:
            raise Exception('no recent folder were found')

        checkpoint_path = os.path.join(settings.CHECKPOINT_PATH, args.net, recent_folder)

    else:
        checkpoint_path = os.path.join(settings.CHECKPOINT_PATH, args.net, settings.TIME_NOW)

    input_tensor = torch.Tensor(1, 3, 32, 32)
    if args.gpu:
        input_tensor = input_tensor.cuda()


    #create checkpoint folder to save model
    if not os.path.exists(checkpoint_path):
        os.makedirs(checkpoint_path)
    checkpoint_path = os.path.join(checkpoint_path, '{net}-{epoch}-{type}.pth')

    best_acc = 0.0
    if args.resume:
        best_weights = best_acc_weights(os.path.join(settings.CHECKPOINT_PATH, args.net, recent_folder))
        if best_weights:
            weights_path = os.path.join(settings.CHECKPOINT_PATH, args.net, recent_folder, best_weights)
            print('found best acc weights file:{}'.format(weights_path))
            print('load best training file to test acc...')
            net.load_state_dict(torch.load(weights_path))
            best_acc = eval_training(tb=False)
            print('best acc is {:0.2f}'.format(best_acc))

        recent_weights_file = most_recent_weights(os.path.join(settings.CHECKPOINT_PATH, args.net, recent_folder))
        if not recent_weights_file:
            raise Exception('no recent weights file were found')
        weights_path = os.path.join(settings.CHECKPOINT_PATH, args.net, recent_folder, recent_weights_file)
        print('loading weights file {} to resume training.....'.format(weights_path))
        net.load_state_dict(torch.load(weights_path))

        resume_epoch = last_epoch(os.path.join(settings.CHECKPOINT_PATH, args.net, recent_folder))


    for epoch in range(1, settings.EPOCH + 1):
        if epoch > args.warm:
            train_scheduler.step(epoch)

        if args.resume:
            if epoch <= resume_epoch:
                continue
        
        train(epoch, args.fp16, args.fp16i)
        acc = eval_training(epoch)

        #start to save best performance model after learning rate decay to 0.01
        # if epoch > settings.MILESTONES[1] and best_acc < acc:
        #     weights_path = checkpoint_path.format(net=args.net, epoch=epoch, type='best')
        #     print('saving weights file to {}'.format(weights_path))
        #     torch.save(net.state_dict(), weights_path)
        #     best_acc = acc
        #     continue

        # if not epoch % settings.SAVE_EPOCH:
        #     weights_path = checkpoint_path.format(net=args.net, epoch=epoch, type='regular')
        #     print('saving weights file to {}'.format(weights_path))
        #     torch.save(net.state_dict(), weights_path)
        # if epoch == settings.EPOCH:
        #     weights_path = checkpoint_path.format(net=args.net, epoch=epoch, type='regular')
        #     print('saving weights file to {}'.format(weights_path))
        #     torch.save(net.state_dict(), weights_path)

    
    #throughputs.append([finish, epoch, th, epoch_loss, batchsize])
    df = pd.DataFrame(throughputs, columns=['Timestamps', 'Epoch', 'Thput (img/s)','Epoch Loss', 'Bsize'])
    df.to_csv(logpath, index=False)
