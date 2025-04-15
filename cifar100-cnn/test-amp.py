#test.py
#!/usr/bin/env python3

""" test neuron network performace
print top1 and top5 err on test dataset
of a model

author baiyu
"""

import argparse

from matplotlib import pyplot as plt
import time
import pandas as pd
import torch
import torchvision.transforms as transforms
from torch.utils.data import DataLoader
from torch.cuda.amp import autocast


from conf import settings
from utils import get_network, get_test_dataloader

datas = []

def infer(net):
    net.eval()
    correct_1 = 0.0
    correct_5 = 0.0
    total_img = len(cifar100_test_loader.dataset)
    start = time.time()
    net=net.to('cuda')
    with torch.no_grad():
        for n_iter, (image, label) in enumerate(cifar100_test_loader):
            if args.gpu:
                image = image.cuda()
                label = label.cuda()

            # add amp
            with torch.autocast(device_type='cuda', dtype=torch.float16):
                output = net(image)
                # fp 16
                # print("output: ", output.dtype)
                _, pred = output.topk(5, 1, largest=True, sorted=True)

            label = label.view(label.size(0), -1).expand_as(pred)
            correct = pred.eq(label).float()
            correct_5 += correct[:, :5].sum()
            correct_1 += correct[:, :1].sum()

    end = time.time()
    th = total_img / (end - start)
    top1 = correct_1.cpu().item() / len(cifar100_test_loader.dataset)
    top5 = correct_5.cpu().item() / len(cifar100_test_loader.dataset)
    print('Evaluating Network.....')
    print('Top1 Accuracy: {:.4f},Top5 Accuracy: {:.4f},Throughput:{:.4f} ,Time consumed:{:.2f}s'.format(
        top1,
        top5,
        th,
        end - start
    ))
    datas.append([th, args.b, top1, top5])



if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument('-net', type=str, required=True, help='net type')
    parser.add_argument('-weights', type=str, required=True, help='the weights file you want to test')
    parser.add_argument('-gpu', action='store_true', default=False, help='use gpu or not')
    parser.add_argument('-b', type=int, default=16, help='batch size for dataloader')
    parser.add_argument('-mode', type=str, default='nor', help='cc or nor')
    parser.add_argument('-times', type=int, default=15, help='inference repeat times')
    args = parser.parse_args()

    net = get_network(args)

    cifar100_test_loader = get_test_dataloader(
        settings.CIFAR100_TRAIN_MEAN,
        settings.CIFAR100_TRAIN_STD,
        #settings.CIFAR100_PATH,
        num_workers=4,
        batch_size=args.b,
    )
    net.load_state_dict(torch.load(args.weights))
    # print(net)

    for i in range(args.times):
        infer(net)

    compute_mode = args.mode
    my_logfile_name = args.net+"-"+compute_mode+"-e"+str(settings.EPOCH)+"-b"+str(cifar100_test_loader.batch_size)+"_amp_test_throughputs.csv"
    abspath = "/shared/cifar100-cnn/mylogs/"
    logpath = abspath + my_logfile_name
    print("Logging to: ", logpath)

    df = pd.DataFrame(datas, columns=['Thput (img/s)','Bsize', 'Top-1', 'Top-5'])
    df.to_csv(logpath, index=False)
