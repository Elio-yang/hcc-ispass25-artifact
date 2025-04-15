#!/usr/bin/python3
import sys
sys.path.append("..")
from common import *


# add csv header
# sed -i '1i type,bw,lat,size,id' *.csv

rootpath = "/Users/yangyang/Desktop/ispass_25_artifact/fig3/"
output_dir = "/Users/yangyang/Desktop/ispass_25_artifact/figure/"


dirs = ["cc-2100MHZ-csv", "nor-2100MHZ-csv"]
files = ["bandwidth-dd.csv","bandwidth-page-dh.csv","bandwidth-page-hd.csv","pin-bandwidth-dh.csv","pin-bandwidth-hd.csv"]

# sizes = [
#     "64B", "128B", "256B", "512B", "1KB", "2KB", "4KB", "8KB", "16KB", 
#     "32KB", "64KB", "128KB", "256KB", "512KB", "1MB", "2MB", "4MB", 
#     "8MB", "16MB", "32MB", "64MB", "128MB", "256MB", "512MB", "1GB"
# ]
# 6 to 30
sizes = ["6", "7", "8", "9", "10", "11", "12", "13", "14",
         "15", "16", "17", "18", "19", "20", "21", "22", 
         "23", "24", "25", "26", "27", "28", "29", "30"]



if __name__ == "__main__":

    default_alpha = 0.9

    freq_2100_dd = {}
    freq_2100_page_dh = {}
    freq_2100_page_hd = {}
    freq_2100_pin_dh = {}
    freq_2100_pin_hd = {}

    for ddir in dirs:
        for file in files:
            filename = rootpath + ddir + "/" + file
            filename = filename.replace(".csv", "_processed.csv")
            type_bw = ddir[0:-4]
            mode = type_bw.split("-")[0]
            freq = type_bw.split("-")[1][0:-3]
            op = None
            if file==files[0]:
                op = "dd"
            elif file==files[1]:
                op = "page-dh"
            elif file==files[2]:
                op = "page-hd"
            elif file==files[3]:
                op = "pin-dh"
            elif file==files[4]:
                op = "pin-hd"
            df = process_pd(filename)
            if freq == "2100":
                if op == "dd":
                    freq_2100_dd[mode] = df
                elif op == "page-dh":
                    freq_2100_page_dh[mode] = df
                elif op == "page-hd":
                    freq_2100_page_hd[mode] = df
                elif op == "pin-dh":
                    freq_2100_pin_dh[mode] = df
                elif op == "pin-hd":
                    freq_2100_pin_hd[mode] = df
    
    plinewidth = 1.5
    # h2d, d2h
    cc_marker = '^'
    nor_marker = 's'
    marker_size = 3

    cc_marker = ['^', 'v', 's', 'p']
    
    colors = ['#99cccc', '#666699', '#333366',"#3366cc"]
    x_rotation = 0
    x_font_size = 5
    default_alpha = 0.9
    tfigsize = (7, 3.5)

    plt.figure(figsize=(3.5, 1.5))

    mode = "nor"
    plt.plot(sizes, freq_2100_pin_dh[mode]['bw'], label='base-pin-d2h', color=colors[3], alpha = default_alpha,marker = cc_marker[2], linewidth=plinewidth, markersize=marker_size)
    plt.plot(sizes, freq_2100_pin_hd[mode]['bw'], label='base-pin-h2d', color=colors[3], alpha = default_alpha, marker = cc_marker[3], linewidth=plinewidth, markersize=marker_size)
    plt.plot(sizes, freq_2100_page_dh[mode]['bw'], label='base-page-d2h', color=colors[2], alpha = default_alpha,marker = cc_marker[0], linewidth=plinewidth, markersize=marker_size)
    plt.plot(sizes, freq_2100_page_hd[mode]['bw'], label='base-page-h2d', color=colors[2], alpha = default_alpha,marker = cc_marker[1], linewidth=plinewidth, markersize=marker_size)
    mode = "cc"
    plt.plot(sizes, freq_2100_pin_dh[mode]['bw'], label='cc-pin-d2h', color=colors[1], alpha = default_alpha,marker = cc_marker[2], linewidth=plinewidth, markersize=marker_size)
    plt.plot(sizes, freq_2100_pin_hd[mode]['bw'], label='cc-pin-h2d', color=colors[1], alpha = default_alpha, marker = cc_marker[3], linewidth=plinewidth, markersize=marker_size)
    plt.plot(sizes, freq_2100_page_dh[mode]['bw'], label='cc-page-d2h', color=colors[0], alpha = default_alpha-0.2,marker = cc_marker[0], linewidth=plinewidth, markersize=marker_size)
    plt.plot(sizes, freq_2100_page_hd[mode]['bw'], label='cc-page-h2d', color=colors[0], alpha = default_alpha-0.2,marker = cc_marker[1], linewidth=plinewidth, markersize=marker_size)

    plt.axhline(y=3.03, color=colors[1], linestyle='--', linewidth=0.7)
    plt.text(1, 4, '3.03 GB/s', fontsize=8, color=colors[1], alpha = default_alpha)

    x_values = range(len(sizes))
    plt.xlim(0, len(sizes)-0.5) 
    plt.xticks(ticks=x_values, labels=sizes, rotation=x_rotation, fontsize=x_font_size)
    plt.yticks(fontsize=8)
    plt.legend(ncol=1, fontsize=5)
    plt.ylabel('Bandwidth (GB/s)',fontsize=10)
    plt.xlabel('Size (2^i B)',fontsize=10)
    
    plt.savefig(output_dir+"fig-bandwidth.pdf", format='pdf', dpi=900, bbox_inches="tight")
            