#!/bin/bash
#####
#
#带宽和IOPS测试
#
#
#####
# default value:
size="256G"
runtime=60
thread=1
direct=1
norandommap=1
ramp_time=2
ioengine="spdk"
# numjob: 
numjobs=(1 2 4)

# iodepth: 
iodepths=(1 32 64)

# block size(k): 
bss=(4 1024 2048)

args=($@)
if [ ${#args[@]} -lt 1 ]; then
  echo "Usage: fio_test.sh  <result_dir> [repeat_time]"
  echo "    result_dir: it must be a dir"
  echo "    repeat_times: times of every single testing, must be a integer, default value is 1"
  echo "Example:" 
  exit
fi

if [ ! -d $1 ]; then
  echo "Error: \"$1\" is not a dir, or is not exited."
  exit
fi
RESULT=$1

REPEAT=1
if [ ${#args[@]} -ge 2 ]; then
  expr $2 + 0 &> /dev/null
  rst=$?
  if [ $rst -ne 0 -o $2 -le 0 ]; then
    echo "Error: repeat_time must be a integer, and bigger then 0."
    exit
  elif [ $2 -gt 0 ]; then
    REPEAT=$2
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
echo "Target: trtype=RDMA adrfam=IPv4 traddr=192.168.2.110 trsvcid=4420 ns=1" >> $infofile
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
  index=$5
  rw_print="r"
  if [ $rw_type == "randwrite" ]; then
    rw_print="w"
  fi
  # name: <r/w>_<bs>_<numjob>_<iodepth>_<index>
  name="${rw_print}_${bs}_${numjob}_${iodepth}_${index}"
  output="${RESULT}/${name}"
  echo "LD_PRELOAD=/home/lwg/spdk/myfiles/fio_plugin fio -rw=${rw_type} -bs=${bs}k -size=${size} -runtime=${runtime} -iodepth=${iodepth} \
         -ioengine=${ioengine} -thread=${thread} -direct=${direct} -group_reporting -numjobs=${numjob} -norandommap=${norandommap} -name ${name} \
         --ramp_time=${ramp_time} --output ${output} --output-format=json '--filename=trtype=PCIe traddr=0000.08.00.0 ns=1'"
  LD_PRELOAD=/home/lwg/spdk/myfiles/fio_plugin fio -rw=${rw_type} -bs=${bs}k -size=${size} -runtime=${runtime} -iodepth=${iodepth} \
       -ioengine=${ioengine} -thread=${thread} -direct=${direct} -group_reporting -numjobs=${numjob} -norandommap=${norandommap} -name ${name} \
       --ramp_time=${ramp_time} --output ${output} --output-format=json '--filename=trtype=PCIe traddr=0000.08.00.0 ns=1'
  echo "${name}: $(now)" >> $infofile
}

# begin to test
rw_types=("randread" "randwrite")

for (( t = 1; t <= $REPEAT; t += 1 ));
do
  for bs in ${bss[@]}; 
  #for (( bs = $bs_min; bs <= $bs_max; bs *= 4 ))
  do
    for rw_type in ${rw_types[@]}; 
    do
      for numjob in ${numjobs[@]};
      #for (( numjob = $numjob_min; numjob <= numjob_max; numjob *= 2 ));
      do
        for iodepth in ${iodepths[@]};
        # for (( iodepth = $iodepth_min; iodepth <= $iodepth_max; iodepth *= 4 ))
        do  
          if (( iodepth != 64 )) || ((numjob != 4 )) || ((bs != 2048 )); then
            do_test $numjob $iodepth $rw_type $bs $t
          fi
        done   
      done  
    done
  done
done

echo "Finish Time: $(now)" >> $infofile
echo "Finish."
