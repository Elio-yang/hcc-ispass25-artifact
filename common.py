import subprocess
import os
import time
import fnmatch
import pandas as pd
from scipy.stats import gmean
from scipy.stats import t
import matplotlib
import matplotlib.pyplot as plt
# plt.style.use('bmh')

plt.style.use('seaborn-v0_8-bright')
# plt.style.use('classic')
from matplotlib import cm
from matplotlib import rcParams
from matplotlib import font_manager
import matplotlib.gridspec as gridspec
from matplotlib.patches import Ellipse 
from matplotlib.ticker import MultipleLocator
import matplotlib.ticker as ticker
import numpy as np


plt.rcParams['font.family'] = 'sans-serif'
plt.rcParams['font.size'] = 12



# models = [
#     "vgg16",
#     "resnet50",
#     "mobilenetv2",
#     "squeezenet",
#     "attention92",
#     "inceptionv4",
# ]
# # ml_batch_size = ["64", "128", "256", "512", "1024"]
# ml_batch_size = ["1024"]
# fp16_batch_size = ["1024"]



# only these models provides 2048 for 3 modes (fp32, fp16, amp)
# models = [
#     "vgg16","squeezenet"
# ]
# ml_batch_size = ["64", "128", "256", "512", "1024", "2048"]
# fp16_batch_size = ["1024","2048"]


# for cc
models = [
    "vgg16","squeezenet"
]
ml_batch_size = ["1024", "2048"]
fp16_batch_size = ["1024","2048"]



default_alpha = 0.8


def process_pd(file: str):
    df = pd.read_csv(file)
    # plot the data in line plot
    return df