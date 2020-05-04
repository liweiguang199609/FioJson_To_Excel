#!/bin/sh

echo "enable core dump"
ulimit -c unlimited

echo "stop irqbalance..."
/etc/init.d/irqbalance stop

echo "start mlnx_affinity..."
mlnx_affinity start

echo "fix cpu frequency..."

cpucount=`cat /proc/cpuinfo|grep processor|wc -l`

FLROOT=/sys/devices/system/cpu

echo "display available governors"
cat /sys/devices/system/cpu/cpu0/cpufreq/scaling_available_governors

echo "display current cpu0 governor"
cat /sys/devices/system/cpu/cpu0/cpufreq/scaling_governor

i=0
while [ $i -ne $cpucount ]
do
    FLNM="$FLROOT/cpu"$i"/cpufreq/scaling_governor"
    echo "Setting $FLNM to performance (max_freq)"  
    echo performance > $FLNM
    i=`expr $i + 1`
done 

# RedHat EL4 64 bit all kernel versions have cpuid and msr driver built in. 
# You can double check it by looking at /boot/config* file for the kernel 
# installed. And look for CPUID and MSR driver config option. It it says 'y' 
# then it is builtin the kernel. If it says 'm', then it is a module and 
# modprobe is needed.

echo "sleep a while"
sleep 1 # wait some time 

echo check cpu freq in /proc/cpuinfo
cat /proc/cpuinfo |grep -i mhz

