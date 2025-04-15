#!/bin/bash

echo "Governor set to ondemand."
for cpu in $(seq 0 63); do
    path="/sys/devices/system/cpu/cpu${cpu}/cpufreq/scaling_governor"
    if [ -f "$path" ]; then
        echo "ondemand" | sudo tee $path > /dev/null
        echo "cpu $cpu: set to ondemand"
    else
        echo "CPU $cpu: cpufreq directory not found"
    fi
done


echo "CPU boost enabled."
echo 1 | sudo tee /sys/devices/system/cpu/cpufreq/boost > /dev/null
echo "Done."


#sudo cpupower --cpu all frequency-set --governor ondemand