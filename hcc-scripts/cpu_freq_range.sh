#!/bin/bash
for cpu in $(seq 0 63); do
    path="/sys/devices/system/cpu/cpu${cpu}/cpufreq/"
    if [ -d "$path" ]; then
        echo "CPU $cpu:"
        echo "  Min : $(cat ${path}cpuinfo_min_freq) kHz"
        echo "  Max : $(cat ${path}cpuinfo_max_freq) kHz"
    else
        echo "CPU $cpu: cpufreq directory not found"
    fi
done
