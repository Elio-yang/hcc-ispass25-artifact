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
from torch.utils.tensorboard import SummaryWriter

from utils import set_seed

from conf import settings
from utils import get_network, get_training_dataloader, get_test_dataloader, WarmUpLR, \
    most_recent_folder, most_recent_weights, last_epoch, best_acc_weights

throughputs = []

def train(epoch, amp_scaler):

    start = time.time()
    net.train()
    tot_images = len(cifar100_training_loader.dataset)
    epoch_loss = 0
    for batch_index, (images, labels) in enumerate(cifar100_training_loader):

        if args.gpu:
            labels = labels.cuda()
            images = images.cuda()

        # amp
        with torch.autocast(device_type='cuda', dtype=torch.float16):
            outputs = net(images)
            assert outputs.dtype is torch.float16
            loss = loss_function(outputs, labels)
            assert loss.dtype is torch.float32
        # loss.backward()
        # optimizer.step()
        # amp related
        amp_scaler.scale(loss).backward()
        amp_scaler.step(optimizer)
        amp_scaler.update()
        optimizer.zero_grad()

        epoch_loss = loss.item()

        if epoch <= args.warm:
            warmup_scheduler.step()
    finish = time.time()

    for name, param in net.named_parameters():
        layer, attr = os.path.splitext(name)
        attr = attr[1:]
        writer.add_histogram("{}/{}".format(layer, attr), param, epoch)

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
    # if args.gpu:
    #     print('GPU INFO.....')
    #     print(torch.cuda.memory_summary(), end='')
    print('Evaluating Network.....')
    print('Test set: Epoch: {}, Average loss: {:.4f}, Accuracy: {:.4f}, Time consumed:{:.2f}s'.format(
        epoch,
        test_loss / len(cifar100_test_loader.dataset),
        correct.float() / len(cifar100_test_loader.dataset),
        finish - start
    ))
    print()

    #add informations to tensorboard
    if tb:
        writer.add_scalar('Test/Average loss', test_loss / len(cifar100_test_loader.dataset), epoch)
        writer.add_scalar('Test/Accuracy', correct.float() / len(cifar100_test_loader.dataset), epoch)

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
    args = parser.parse_args()

    set_seed(42)
    net = get_network(args)


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
    my_logfile_name = args.net+"-"+compute_mode+"-e"+str(settings.EPOCH)+"-b"+str(cifar100_training_loader.batch_size)+"_amp_train_throughputs.csv"
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

    #use tensorboard
    if not os.path.exists(settings.LOG_DIR):
        os.mkdir(settings.LOG_DIR)

    #since tensorboard can't overwrite old values
    #so the only way is to create a new tensorboard log
    writer = SummaryWriter(log_dir=os.path.join(
            settings.LOG_DIR, args.net+"-amp", settings.TIME_NOW))
    input_tensor = torch.Tensor(1, 3, 32, 32)
    if args.gpu:
        input_tensor = input_tensor.cuda()
    writer.add_graph(net, input_tensor)

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

    # add amp related code here
    scaler = torch.cuda.amp.GradScaler(enabled=True)

    for epoch in range(1, settings.EPOCH + 1):
        if epoch > args.warm:
            train_scheduler.step(epoch)

        if args.resume:
            if epoch <= resume_epoch:
                continue

        train(epoch, scaler)
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

    writer.close()
    
    #throughputs.append([finish, epoch, th, epoch_loss, batchsize])
    df = pd.DataFrame(throughputs, columns=['Timestamps', 'Epoch', 'Thput (img/s)','Epoch Loss', 'Bsize'])
    df.to_csv(logpath, index=False)
