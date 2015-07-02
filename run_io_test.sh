#!/bin/bash

Dev=$1
Size=${2:-1}

if [ -z $Dev ];then
   echo "usage: $0 {device} size(in Gb[default:1G])"
fi


# Create job file
cat << EOF > /tmp/random_writes.$$
[random writes]
filename=/dev/$Dev
rw=randrw
refill_buffers
norandommap
randrepeat=0
ioengine=libaio
bs=8k
rwmixread=10
iodepth=16
numjobs=16
group_reporting
size=${Size}G
EOF

logger -t run_test "### start of run_test $Dev $Size ###"
if [[ -x /usr/sbin/smartctl ]];then
    /usr/sbin/smartctl -a /dev/$Dev > smartctl_before.$Dev
fi

fio /tmp/random_writes.$$ 2>&1 |& tee fio_random_writes_${Dev}_${Size}.log

if [[ -x /usr/sbin/smartctl ]];then
    /usr/sbin/smartctl -a /dev/$Dev > smartctl_after$Dev
fi
logger -t run_test "### end of run_test $Dev $Size ###"

rm -f /tmp/random_writes.$$
