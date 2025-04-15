shutdown VM
qemu-img resize xxxx.qcow2 +50G
restart VM

fdisk -l

# Disk /dev/vda: 552.2 GiB, 592919396352 bytes, 1158045696 sectors
# Units: sectors of 1 * 512 = 512 bytes
# Sector size (logical/physical): 512 bytes / 512 bytes
# I/O size (minimum/optimal): 512 bytes / 512 bytes
# Disklabel type: gpt
# Disk identifier: FE7BB212-3C91-4528-85BE-2CE0D239F205

# Device      Start       End   Sectors  Size Type
# /dev/vda1  227328 109469662 109242335 52.1G Linux filesystem
# /dev/vda14   2048     10239      8192    4M BIOS boot
# /dev/vda15  10240    227327    217088  106M EFI System

growpart /dev/vda 1
resize2fs /dev/vda1