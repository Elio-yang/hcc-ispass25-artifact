#!/bin/bash
#
# Launch QEMU-KVM to create Guest VM in following types:
# - Legacy VM: non-TDX VM boot with legacy(non-EFI) SEABIOS
# - EFI VM: non-TDX VM boot with EFI BIOS OVMF(Open Virtual Machine Firmware)
# - TD VM: TDX VM boot with OVMF via qemu-kvm launch parameter "kvm-type=tdx,confidential-guest-support=tdx"
#
# Prerequisite:
# 1. Build and Install TDX stack. Please refer to README.md in build/<your_distro>
# 2. Create TDX guest image with
#   - TDX guest kernel
#   - (optional)Modified Grub and Shim for TDX measurement to RTMR
#
# Note:
#
# - This script support "direct" and "grub" boot:
#   * direct: pass kernel image via "-kernel" and kernel command line via
#             "cmdline" via qemu-kvm launch parameter.
#   * grub: do not pass kernel and cmdline but leverage EFI BDS boot
#           shim->grub->kernel within guest image
# - To get consistent TD_REPORT within guest cross power cycle, please keep
#   consistent configurations for TDX guest such as same MAC address.
#

CURR_DIR=$(readlink -f "$(dirname "$0")")

#echo "Current directory: ${CURR_DIR}"
#exit 1

# Set distro related parameters according to distro
DISTRO=$(grep -w 'NAME' /etc/os-release)
if [[ "$DISTRO" =~ .*"Ubuntu".* ]]; then
    QEMU_EXEC="/usr/bin/qemu-system-x86_64"
    LEGACY_BIOS="/usr/share/seabios/bios.bin"
else
    QEMU_EXEC="/usr/libexec/qemu-kvm"
    LEGACY_BIOS="/usr/share/qemu-kvm/bios.bin"
fi

# VM configurations
CPUS=16
MEM=64G
SGX_EPC_SIZE=64M

# Installed from the package of intel-mvp-tdx-tdvf
OVMF="/usr/share/qemu/OVMF.fd"
GUEST_IMG=""
DEFAULT_GUEST_IMG="${CURR_DIR}/td-guest.qcow2"
KERNEL=""
DEFAULT_KERNEL="${CURR_DIR}/vmlinuz"
VM_TYPE="td"
BOOT_TYPE="direct"
DEBUG=false
USE_VSOCK=false
USE_SERIAL_CONSOLE=false
FORWARD_PORT=10026
MONITOR_PORT=9001
ROOT_PARTITION="/dev/vda1"
KERNEL_CMD_NON_TD="root=${ROOT_PARTITION} rw console=hvc0"
KERNEL_CMD_TD="${KERNEL_CMD_NON_TD}"
MAC_ADDR=""
QUOTE_TYPE=""

# Just log message of serial into file without input
# we can pass multi-GPUs
# -device vfio-pci,host=xx:00.0,bus=pci.2 \
# -device pcie-root-port,id=pci.2,bus=pcie.0 \
# pci.0 [RP] -- pci.1
#         |-----pci.2
# 2 gpu version
# HVC_CONSOLE="-chardev stdio,id=mux,mux=on,logfile=$CURR_DIR/vm_log_$(date +"%FT%H%M").log \
#              -device virtio-serial,romfile= \
#              -device virtconsole,chardev=mux -monitor chardev:mux \
#              -serial chardev:mux -nographic \
# 	           -no-hpet -nodefaults \
#              -device pcie-root-port,id=pci.1,bus=pcie.0,chassis=1,slot=1 \
#              -device vfio-pci,host=5a:00.0,bus=pci.1 \
#              -device pcie-root-port,id=pci.2,bus=pcie.0,chassis=2,slot=2 \
#              -device vfio-pci,host=d8:00.0,bus=pci.2 \
#              -fw_cfg name=opt/ovmf/X-PciMmio64,string=262144"

# 5a:00.0 
# HVC_CONSOLE="-chardev stdio,id=mux,mux=on,logfile=$CURR_DIR/vm_log_$(date +"%FT%H%M").log \
#              -device virtio-serial,romfile= \
#              -device virtconsole,chardev=mux -monitor chardev:mux \
#              -serial chardev:mux -nographic \
# 	         -no-hpet -nodefaults \
#              -device pcie-root-port,id=pci.1,bus=pcie.0,chassis=1,slot=1 \
#              -device vfio-pci,host=5a:00.0,bus=pci.1 \
#              -fw_cfg name=opt/ovmf/X-PciMmio64,string=262144"

# no gpu
HVC_CONSOLE="-chardev stdio,id=mux,mux=on,logfile=$CURR_DIR/vm_log_$(date +"%FT%H%M").log \
             -device virtio-serial,romfile= \
             -device virtconsole,chardev=mux -monitor chardev:mux \
             -serial chardev:mux -nographic \
	         -no-hpet -nodefaults \
             -fw_cfg name=opt/ovmf/X-PciMmio64,string=262144"

# d8:00.0
# HVC_CONSOLE="-chardev stdio,id=mux,mux=on,logfile=$CURR_DIR/vm_log_$(date +"%FT%H%M").log \
#              -device virtio-serial,romfile= \
#              -device virtconsole,chardev=mux -monitor chardev:mux \
#              -serial chardev:mux -nographic \
# 	         -no-hpet -nodefaults \
#              -device pcie-root-port,id=pci.1,bus=pcie.0,chassis=1,slot=1 \
#              -device vfio-pci,host=d8:00.0,bus=pci.1 \
#              -fw_cfg name=opt/ovmf/X-PciMmio64,string=262144"

# # 1 gpu version
# HVC_CONSOLE="-chardev stdio,id=mux,mux=on,logfile=$CURR_DIR/vm_log_$(date +"%FT%H%M").log \ 
#                 -device virtio-serial,romfile= \ 
#                 -device virtconsole,chardev=mux -monitor chardev:mux \ 
#                 -serial chardev:mux -nographic \
#                 -no-hpet -nodefaults \
#                 -device pcie-root-port,id=pci.1,bus=pcie.0 \
#                 -device vfio-pci,host=5a:00.0,bus=pci.1 \
#                 -fw_cfg name=opt/ovmf/X-PciMmio64,string=26214"
#


# old version
# HVC_CONSOLE="-chardev stdio,id=mux,mux=on,logfile=$CURR_DIR/vm_log_$(date+"%FT%H%M").log \
#               -device virtio-serial,romfile= \
#               -device virtconsole,chardev=mux -monitor chardev:mux \
#               -serial chardev:mux -nographic \
#               -no-hpet -nodefaults \
#               -device pcie-root-port,id=pci.1,bus=pcie.0 \
#               -device vfio-pci,host=5a:00.0,bus=pci.1 \
#               -fw_cfg name=opt/ovmf/X-PciMmio64,string=262144"

# In grub boot, serial consle need input to select grub menu instead of HVC
# Please make sure console=ttyS0 is added in grub.cfg since no virtconsole
#
SERIAL_CONSOLE="-serial stdio"

# Default template for QEMU command line
QEMU_CMD="${QEMU_EXEC} -accel kvm \
          -name process=tdxvm,debug-threads=on \
          -m $MEM -vga none \
          -monitor pty \
          -no-hpet -nodefaults"

# PARAM_CPU=" -cpu host,+msr \
#                -object memory-backend-ram,id=mem1,size=64G \
#                -numa node,cpus=0-15,nodeid=0,memdev=mem1"

# PARAM_CPU=" -numa node,nodeid=0,cpus=0-15, memdev=ram1\
#             -cpu host"

PARAM_CPU=" -cpu host,-kvm-steal-time,pmu=off"


PARAM_MACHINE=" -machine q35"

usage() {
    cat << EOM
Usage: $(basename "$0") [OPTION]...
  -i <guest image file>     Default is td-guest.qcow2 under current directory
  -k <kernel file>          Default is vmlinuz under current directory
  -t [legacy|efi|td|sgx]    VM Type, default is "td"
  -b [direct|grub]          Boot type, default is "direct" which requires kernel binary specified via "-k"
  -p <Monitor port>         Monitor via telnet
  -f <SSH Forward port>     Host port for forwarding guest SSH
  -o <OVMF file>            BIOS firmware device file, for "td" and "efi" VM only
  -m <11:22:33:44:55:66>    MAC address, impact TDX measurement RTMR
  -q [tdvmcall|vsock]       Support for TD quote using tdvmcall or vsock
  -c <number>               Number of CPUs, default is 1
  -r <root partition>       root partition for direct boot, default is /dev/vda1
  -v                        Flag to enable vsock
  -d                        Flag to enable "debug=on" for GDB guest
  -s                        Flag to use serial console instead of HVC console
  -h                        Show this help
EOM
}

error() {
    echo -e "\e[1;31mERROR: $*\e[0;0m"
    exit 1
}

warn() {
    echo -e "\e[1;33mWARN: $*\e[0;0m"
}

process_args() {
    while getopts ":i:k:t:b:p:f:o:a:m:vdshq:c:r:" option; do
        case "$option" in
            i) GUEST_IMG=$OPTARG;;
            k) KERNEL=$OPTARG;;
            t) VM_TYPE=$OPTARG;;
            b) BOOT_TYPE=$OPTARG;;
            p) MONITOR_PORT=$OPTARG;;
            f) FORWARD_PORT=$OPTARG;;
            o) OVMF=$OPTARG;;
            m) MAC_ADDR=$OPTARG;;
            v) USE_VSOCK=true;;
            d) DEBUG=true;;
            s) USE_SERIAL_CONSOLE=true;;
            q) QUOTE_TYPE=$OPTARG;;
            c) CPUS=$OPTARG;;
            r) ROOT_PARTITION=$OPTARG;;
            h) usage
               exit 0
               ;;
            *)
               echo "Invalid option '-$OPTARG'"
               usage
               exit 1
               ;;
        esac
    done

    if [[ ! -f ${QEMU_EXEC} ]]; then
        error "Please install QEMU which supports TDX."
    fi

    # Validate the number of CPUs
    if ! [[ ${CPUS} =~ ^[0-9]+$ && ${CPUS} -gt 0 ]]; then
        error "Invalid number of CPUs: ${CPUS}"
    fi

    GUEST_IMG="${GUEST_IMG:-${DEFAULT_GUEST_IMG}}"
    if [[ ! -f ${GUEST_IMG} ]]; then
        usage
        error "Guest image file ${GUEST_IMG} not exist. Please specify via option \"-i\""
    fi

    # Create temparory firmware device file from OVMF.fd
    if [[ ${OVMF} == "/usr/share/qemu/OVMF.fd" ]]; then
        if [[ ! -f /usr/share/qemu/OVMF.fd ]]; then
            error "Could not find /usr/share/qemu/OVMF.fd. Please install TDVF(Trusted Domain Virtual Firmware)."
        fi
    fi

    # Check parameter MAC address
    if [[ -n ${MAC_ADDR} ]]; then
        if [[ ! ${MAC_ADDR} =~ ^([[:xdigit:]]{2}:){5}[[:xdigit:]]{2}$ ]]; then
            error "Invalid MAC address: ${MAC_ADDR}"
        fi
    fi

    case ${GUEST_IMG##*.} in
        qcow2) FORMAT="qcow2";;
          img) FORMAT="raw";;
            *) echo "Unknown disk image's format"; exit 1 ;;
    esac

    # Guest rootfs changes
    if [[ ${ROOT_PARTITION} != "/dev/vda1" ]]; then
        KERNEL_CMD_NON_TD=${KERNEL_CMD_NON_TD//"/dev/vda1"/${ROOT_PARTITION}}
        KERNEL_CMD_TD="${KERNEL_CMD_NON_TD}"
    fi

    QEMU_CMD+=" -drive file=$(readlink -f "${GUEST_IMG}"),if=virtio,format=$FORMAT "
    QEMU_CMD+=" -monitor telnet:127.0.0.1:${MONITOR_PORT},server,nowait "

    if [[ ${DEBUG} == true ]]; then
        OVMF="/usr/share/qemu/OVMF.debug.fd"
	QEMU_CMD+=" -s -S "
	KERNEL_CMD_NON_TD+=" nokaslr"
	KERNEL_CMD_TD+=" nokaslr"
    fi

    if [[ -n ${QUOTE_TYPE} ]]; then
        case ${QUOTE_TYPE} in
            "tdvmcall") ;;
            "vsock")
                USE_VSOCK=true
                ;;
            *)
                error "Invalid quote type \"$QUOTE_TYPE\", must be [vsock|tdvmcall]"
                ;;
        esac
    fi

    case ${VM_TYPE} in
        "td")
            cpu_tsc=$(grep 'cpu MHz' /proc/cpuinfo | head -1 | awk -F: '{print $2/1024}')
            if (( $(echo "$cpu_tsc < 1" |bc -l) )); then
                PARAM_CPU+=",tsc-freq=1000000000"
            fi

            # Note: "pic=no" could only be used in TD mode but not for non-TD mode
            PARAM_MACHINE+=",kernel_irqchip=split,confidential-guest-support=tdx,memory-backend=ram1"
            QEMU_CMD+=" -bios ${OVMF}"
            QEMU_CMD+=" -object tdx-guest,sept-ve-disable,id=tdx"
            if [[ ${QUOTE_TYPE} == "tdvmcall" ]]; then
                QEMU_CMD+=",quote-generation-service=vsock:2:4050"
            fi
            if [[ ${DEBUG} == true ]]; then
                QEMU_CMD+=",debug=on"
            fi
            QEMU_CMD+=" -object memory-backend-memfd-private,id=ram1,size=${MEM}"
            ;;
        "efi")
            PARAM_MACHINE+=",kernel_irqchip=split"
            QEMU_CMD+=" -bios ${OVMF}"
            ;;
        "legacy")
            if [[ ! -f ${LEGACY_BIOS} ]]; then
                error "${LEGACY_BIOS} does not exist!"
            fi
            QEMU_CMD+=" -bios ${LEGACY_BIOS} "
            ;;
        "sgx")
            PARAM_MACHINE+=",sgx-epc.0.memdev=mem0,sgx-epc.0.node=0"
            QEMU_CMD+=" -cpu host,+sgx-provisionkey,+sgxlc,+sgx1"
            QEMU_CMD+=" -object memory-backend-epc,id=mem0,size=${SGX_EPC_SIZE},prealloc=on"
            ;;
        *)
            error "Invalid ${VM_TYPE}, must be [legacy|efi|td|sgx]"
            ;;
    esac

    QEMU_CMD+=$PARAM_CPU
    QEMU_CMD+=$PARAM_MACHINE
    QEMU_CMD+=" -device virtio-net-pci,netdev=mynet0"

    # Specify the number of CPUs
    QEMU_CMD+=" -smp ${CPUS} "

    # Customize MAC address. NOTE: it will impact TDX measurement RTMR.
    if [[ -n ${MAC_ADDR} ]]; then
        QEMU_CMD+=",mac=${MAC_ADDR}"
    fi

    # Forward SSH port to the host
    QEMU_CMD+=" -netdev user,id=mynet0,hostfwd=tcp::$FORWARD_PORT-:22 "

    # Enable vsock
    if [[ ${USE_VSOCK} == true ]]; then
        QEMU_CMD+=" -device vhost-vsock-pci,guest-cid=3 "
    fi

    case ${BOOT_TYPE} in
        "direct")
            KERNEL="${KERNEL:-${DEFAULT_KERNEL}}"
            if [[ ! -f ${KERNEL} ]]; then
                usage
                error "Kernel image file ${KERNEL} not exist. Please specify via option \"-k\""
            fi

            QEMU_CMD+=" -kernel $(readlink -f "${KERNEL}") "
            if [[ ${VM_TYPE} == "td" ]]; then
                # shellcheck disable=SC2089
                QEMU_CMD+=" -append \"${KERNEL_CMD_TD}\" "
            else
                # shellcheck disable=SC2089
                QEMU_CMD+=" -append \"${KERNEL_CMD_NON_TD}\" "
            fi
            ;;
        "grub")
            if [[ ${USE_SERIAL_CONSOLE} == false ]]; then
                warn "Using HVC console for grub, could not accept key input in grub menu"
            fi
            ;;
        *)
            echo "Invalid ${BOOT_TYPE}, must be [direct|grub]"
            exit 1
            ;;
    esac

    echo "========================================="
    echo "Guest Image       : ${GUEST_IMG}"
    echo "Kernel binary     : ${KERNEL}"
    echo "OVMF              : ${OVMF}"
    echo "VM Type           : ${VM_TYPE}"
    echo "CPUS              : ${CPUS}"
    echo "Boot type         : ${BOOT_TYPE}"
    echo "Monitor port      : ${MONITOR_PORT}"
    echo "Enable vsock      : ${USE_VSOCK}"
    echo "Enable debug      : ${DEBUG}"
    if [[ -n ${MAC_ADDR} ]]; then
        echo "MAC Address       : ${MAC_ADDR}"
    fi
    if [[ ${USE_SERIAL_CONSOLE} == true ]]; then
        QEMU_CMD+=" ${SERIAL_CONSOLE} "
        echo "Console           : Serial"
    else
        QEMU_CMD+=" ${HVC_CONSOLE} "
        echo "Console           : HVC"
    fi
    if [[ -n ${QUOTE_TYPE} ]]; then
        echo "Quote type        : ${QUOTE_TYPE}"
    fi
    echo "========================================="
}

launch_vm() {
    # remap CTRL-C to CTRL ]
    echo "Remapping CTRL-C to CTRL-]"
    stty intr ^]
    echo "Launch VM:"
    # shellcheck disable=SC2086,SC2090
    echo ${QEMU_CMD}
    # shellcheck disable=SC2086
    eval ${QEMU_CMD}
    # restore CTRL-C mapping
    stty intr ^c
}

process_args "$@"
launch_vm

