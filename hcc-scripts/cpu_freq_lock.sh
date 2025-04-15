#!/bin/bash
# Frequency in kHz

#default freq 0.8GHZ
DESIRED_FREQ=800000


echo "Frequency max set to ${DESIRED_FREQ} kHz."
for cpu in $(seq 0 63); do
    path="/sys/devices/system/cpu/cpu${cpu}/cpufreq/scaling_max_freq"
    if [ -f "$path" ]; then
        echo $DESIRED_FREQ | sudo tee $path > /dev/null
    else
        echo "CPU $cpu: scaling file not found"
    fi
done

echo "Frequency cur set to ${DESIRED_FREQ} kHz."
for cpu in $(seq 0 63); do
    path="/sys/devices/system/cpu/cpu${cpu}/cpufreq/scaling_setspeed"
    if [ -f "$path" ]; then
        echo $DESIRED_FREQ | sudo tee $path > /dev/null
    else
        echo "CPU $cpu: scaling file not found"
    fi
done

echo "Done."


#echo "CPU boost disabled."
#echo 0 | sudo tee /sys/devices/system/cpu/cpufreq/boost > /dev/null
#echo "Done."


# cpupower not available in current kernel
#sudo cpupower --cpu all frequency-set --freq 2100MHz
#sudo sh -c 'echo 0 > /sys/devices/system/cpu/cpufreq/boost'
