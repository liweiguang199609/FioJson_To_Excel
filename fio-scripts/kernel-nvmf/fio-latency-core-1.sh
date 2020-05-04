#!/bin/bash

# default value:
size="256G"
runtime=60
thread=1
direct=1
norandommap=1
ramp_time=2
ioengine="libaio"
# numjob: 
numjobs=(1)

# iodepth: 
iodepths=(1)

# block size(k): 
bss=(4)

# rw type:
rw_types=("randread" "randwrite")

# rate_iops:
rate_iopss=(100 1000)
rate_iops_min=10000
rate_iops_max=510000

args=($@)
if [ ${#args[@]} -lt 2 ]; then
  echo "Usage: fio_test.sh <target_file> <result_dir> [repeat_time]"
  echo "    target_file: name of the target file, such /dev/nvme0n1"
  echo "    result_dir: it must be a dir"
  echo "    repeat_times: times of every single testing, must be a integer, default value is 1"
  echo "Example:" 
  echo "    fio_test.sh /dev/nvme0n1 /root/fio_result"
  echo "    fio_test.sh /dev/sdb1 /root/fio_reuslt 5"
  exit
fi

if [ ! -e $1 ]; then
  echo "Error: \"$1\" is not a file, or is not exited."
  exit
fi
TARGET=$1

if [ ! -d $2 ]; then
  echo "Error: \"$2\" is not a dir, or is not exited."
  exit
fi
RESULT=$2

REPEAT=1
if [ ${#args[@]} -ge 3 ]; then
  expr $3 + 0 &> /dev/null
  rst=$?
  if [ $rst -ne 0 -o $3 -le 0 ]; then
    echo "Error: repeat_time must be a integer, and bigger then 0."
    exit
  elif [ $3 -gt 0 ]; then
    REPEAT=$3
  fi   
fi

now()
{
  date "+%Y-%m-%d %H:%M:%S"
}

# echo "Target: ${TARGET}"
echo "Result Dir: ${RESULT}"
echo "Repeat Times: ${REPEAT}"
echo "Date: $(now)"

infofile="${RESULT}/info.txt"

rm -rf ${RESULT}/*
touch $infofile

# save infomation to info.txt
echo "Target: $filename" >> $infofile
echo "Result Dir: $RESULT" >> $infofile
echo "Repeat Times: $REPEAT" >> $infofile
echo "All Size: $size" >> $infofile
echo "Runtime: ${runtime}s" >> $infofile
echo "Direct: $direct" >> $infofile
echo "IOEngine: $ioengine" >> $infofile
echo "Number of Jobs: $numjobs" >> $infofile
echo "Depth of IO: $iodepths" >> $infofile
echo "Block Size: $bss" >> $infofile
echo "Start Time: $(now)" >> $infofile
echo "Records:" >> $infofile

do_test() {
  numjob=$1
  iodepth=$2
  rw_type=$3
  bs=$4
  rate_iops=$5
  index=$6
  rw_print="r"
  if [ $rw_type == "randwrite" ]; then
    rw_print="w"
  fi
  # name: <r/w>_<bs>_<numjob>_<iodepth>_${rate_iops}_<index>
  name="${rw_print}_${bs}_${numjob}_${iodepth}_${rate_iops}_${index}"
  output="${RESULT}/${name}"
  echo "fio --filename=${TARGET} -rw=${rw_type} -bs=${bs}k -size=${size} -runtime=${runtime} -iodepth=${iodepth} \
         -ioengine=${ioengine} -thread=${thread} -direct=${direct} -group_reporting -numjobs=${numjob} -norandommap=${norandommap} -name ${name} \
         --ramp_time=${ramp_time} --rate_iops=${rate_iops} --output ${output} --output-format=json ''"
  fio --filename=${TARGET} -rw=${rw_type} -bs=${bs}k -size=${size} -runtime=${runtime} -iodepth=${iodepth} \
       -ioengine=${ioengine} -thread=${thread} -direct=${direct} -group_reporting -numjobs=${numjob} -norandommap=${norandommap} -name ${name} \
       --ramp_time=${ramp_time} --rate_iops=${rate_iops} --output ${output} --output-format=json 
  echo "${name}: $(now)" >> $infofile
}

# begin to test 1 depth

for (( t = 1; t <= $REPEAT; t += 1 ));
do
  for bs in ${bss[@]}; 
  do
    for rw_type in ${rw_types[@]}; 
    do
      for numjob in ${numjobs[@]};
      do
        for iodepth in ${iodepths[@]};
        do
          for rate_iops in ${rate_iopss[@]};
          do
            do_test $numjob $iodepth $rw_type $bs $rate_iops $t
			sync
			echo 3 >/proc/sys/vm/drop_caches
          done 
        done   
      done  
    done
  done
done


echo "Finish Time: $(now)" >> $infofile
echo "Finish."
