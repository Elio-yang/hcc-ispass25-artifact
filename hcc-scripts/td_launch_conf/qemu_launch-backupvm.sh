sudo  numactl --cpunodebind=1 --physcpubind=16-31 --membind=1 ./start-qemu-new.sh -i build/ubuntu-22.04/guest-image/new-td-guest-ubuntu-22.04.qcow2 -b grub
