#!/bin/bash

taskset -c 0 openssl speed -elapsed -evp aes-256-gcm        -bytes 8192
taskset -c 0 openssl speed -elapsed -evp aes-256-ctr        -bytes 8192
taskset -c 0 openssl speed -elapsed -evp aes-256-xts        -bytes 8192
taskset -c 0 openssl speed -elapsed -evp chacha20           -bytes 8192
taskset -c 0 openssl speed -elapsed -evp chacha20-poly1305  -bytes 8192
taskset -c 0 openssl speed -elapsed -evp sha3-256           -bytes 8192
taskset -c 0 openssl speed -elapsed  ghash