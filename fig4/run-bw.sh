#!/bin/bash

# Number of times to execute a.sh
repeat_count=10

for i in $(seq 1 $repeat_count); do
    echo "================Starting execution P-$i"
    ./page-hd.sh
    wait $!
    echo "================Finished execution P-$i"
done


for i in $(seq 1 $repeat_count); do
    echo "================Starting execution PIN-$i"
    ./pin-hd.sh
    wait $!
    echo "================Finished execution PIN-$i"
done



for i in $(seq 1 $repeat_count); do
    echo "================Starting execution P-$i"
    ./page-dh.sh
    wait $!
    echo "================Finished execution P-$i"
done


for i in $(seq 1 $repeat_count); do
    echo "================Starting execution PIN-$i"
    ./pin-dh.sh
    wait $!
    echo "================Finished execution PIN-$i"
done



for i in $(seq 1 $repeat_count); do
    echo "================Starting execution D-$i"
    ./d2d.sh
    wait $!
    echo "================Finished execution D-$i"
done