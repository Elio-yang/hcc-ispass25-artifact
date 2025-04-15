#!/bin/bash

DESIRED_FREQ=2100000  # Frequency in kHz (2100 MHz)

echo "Governor set to userspace."
for cpu in $(seq 0 63); do
    path="/sys/devices/system/cpu/cpu${cpu}/cpufreq/scaling_governor"
    if [ -f "$path" ]; then
        echo "userspace" | sudo tee $path > /dev/null
        echo "cpu $cpu: set to userspace"
    else
        echo "CPU $cpu: governer file not found"
    fi
done

echo "Frequency set to ${DESIRED_FREQ} kHz."
for cpu in $(seq 0 63); do
    path="/sys/devices/system/cpu/cpu${cpu}/cpufreq/scaling_max_freq"
    if [ -f "$path" ]; then
        echo $DESIRED_FREQ | sudo tee $path > /dev/null
        echo "cpu $cpu: set max to ${DESIRED_FREQ} kHz"
    else
        echo "CPU $cpu: scaling file not found"
    fi
done

echo "Frequency cur set to ${DESIRED_FREQ} kHz."
for cpu in $(seq 0 63); do
    path="/sys/devices/system/cpu/cpu${cpu}/cpufreq/scaling_setspeed"
    if [ -f "$path" ]; then
        echo $DESIRED_FREQ | sudo tee $path > /dev/null
        echo "cpu $cpu: set to ${DESIRED_FREQ} kHz"
    else
        echo "CPU $cpu: scaling file not found"
    fi
done


echo "CPU boost disabled."
echo 0 | sudo tee /sys/devices/system/cpu/cpufreq/boost > /dev/null
echo "Done."


# cpupower not available in current kernel
#sudo cpupower --cpu all frequency-set --freq 2100MHz
#sudo sh -c 'echo 0 > /sys/devices/system/cpu/cpufreq/boost'