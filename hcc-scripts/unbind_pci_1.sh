#!/bin/bash
#echo 0000:5a:00.0 >  /sys/bus/pci/devices/0000:5a:00.0/driver/unbind

# must unbind vfio first [unbind_vfio.sh]
# set dma buffer limit
# unbind pci driver
# bind to vfio


# the gpu with cc on
gpu="0000:5a:00.0"
gpu_vd="$(cat /sys/bus/pci/devices/$gpu/vendor) $(cat /sys/bus/pci/devices/$gpu/device)"
#echo "$gpu_vd"
echo 1048576 > "/sys/module/vfio_iommu_type1/parameters/dma_entry_limit"
echo "$gpu" > "/sys/bus/pci/devices/$gpu/driver/unbind"
echo "$gpu_vd" > /sys/bus/pci/drivers/vfio-pci/new_id