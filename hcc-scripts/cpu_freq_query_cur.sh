#/bin/bash

# cpu power unavailable in current kernel
#sudo cpupower --cpu all frequency-info | grep "current CPU frequency"


#!/bin/bash
for cpu in $(seq 0 63); do
    path="/sys/devices/system/cpu/cpu${cpu}/cpufreq/scaling_cur_freq"
    if [ -f "$path" ]; then
        echo "CPU $cpu: $(cat $path) kHz"
    else
        echo "CPU $cpu: cur_freq file not found"
    fi
done
