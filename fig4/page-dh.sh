#!/bin/bash

# Array to store start and end values in bytes, doubling from 64B to 1GB (1073741824 bytes)
sizes=(64 128 256 512 1024 2048 4096 8192 16384 32768 65536 131072 262144 524288 1048576 2097152 4194304 8388608 16777216 33554432 67108864 134217728 268435456 536870912 1073741824)
output_file="bandwidth-page-dh.csv"
# Loop through each size and generate the command
for size in "${sizes[@]}"; do
    echo "Running test with size: $size bytes"
    ./bandwidthTest --csv --device=0 --memory=pageable --mode=range --start=$size --end=$size --increment=4096 --dtoh >> "$output_file" 2>&1
    pid=$!
    wait $pid
    echo "End test with size: $size bytes"
done