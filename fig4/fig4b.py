#!/usr/bin/python3
import sys
sys.path.append("..")
from common import *


rootpath = "/Users/yangyang/Desktop/ispass_25_artifact/fig3/"
output_dir = "/Users/yangyang/Desktop/ispass_25_artifact/figure/"
crypto_th = "crypto-dvfs.csv"

def draw_crypt(data):

    interested_cols = ['Name', '2.1GHz', 'Grace']
    data = data[interested_cols]

    data['Base'] = data['2.1GHz']
    data['Grace'] = data['Grace']

    data.plot(
        x='Name', 
        y=['Base','Grace'], 
        width=0.7,
        kind='bar', 
        figsize=(2, 2), 
        color=['#3366cc', '#33cc66'],
        alpha = default_alpha,
        label=['Intel EMR', 'NV Grace'])
    
    
    plt.axhline(y=3.36, color='#3366cc', linestyle='--', linewidth=0.7)
    plt.text(2.5, 4, '3.36 GB/s', fontsize=8, color='#3366cc', alpha = default_alpha)

    xname = ["gcm", "ctr", "xts", "cc20", "ccp1305", "sha3", "ghash"]
    plt.xticks(range(len(xname)), xname,fontsize=5)
    plt.ylabel('Thput (GB/s)', fontsize=10)
    plt.xlabel('')
    plt.ylim(0, 10)
    plt.xticks(fontsize=8)
    plt.yticks(fontsize=8)
    plt.tight_layout()
    plt.legend(fontsize=8, loc='best')
    plt.savefig(output_dir+'fig-crypto-thput.pdf',format='pdf', dpi=900, bbox_inches="tight")
    plt.close()

if __name__ == "__main__":

    cd_path = rootpath + crypto_th
    data = process_pd(cd_path)
    
    draw_crypt(data)




    
