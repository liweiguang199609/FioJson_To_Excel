#!/bin/bash

# default value:
size="256G"
runtime=60
direct=1
ioengine="libaio"
numjob_min=1
numjob_max=4
# iodepth: **2
iodepth_min=1
iodepth_max=32
# block size(k): **2
bs_min=4 
bs_max=4

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

echo "Target: ${TARGET}"
echo "Result Dir: ${RESULT}"
echo "Repeat Times: ${REPEAT}"
echo "Date: $(now)"

infofile="${RESULT}/info.txt"

rm -rf ${RESULT}/*
touch $infofile

# save infomation to info.txt
echo "Target: $TARGET" >> $infofile
echo "Result Dir: $RESULT" >> $infofile
echo "Repeat Times: $REPEAT" >> $infofile
echo "All Size: $size" >> $infofile
echo "Runtime: ${runtime}s" >> $infofile
echo "Direct: $direct" >> $infofile
echo "IOEngine: $ioengine" >> $infofile
echo "Min Number of Jobs: $numjob_min" >> $infofile
echo "Max Number of Jobs: $numjob_max" >> $infofile
echo "Array Number of Jobs: ${numjob_arr[@]}" >> $infofile
echo "Min Depth of IO: $iodepth_min" >> $infofile
echo "Max Depth of IO: $iodepth_max" >> $infofile
echo "Min Block Size: $bs_min" >> $infofile
echo "Max Block Size: $bs_max" >> $infofile
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
  echo "fio -rw=${rw_type} -bs=${bs}k -size=${size} -runtime=${runtime} -iodepth=${iodepth} -filename ${TARGET} -ioengine=${ioengine} -direct=${direct} -group_reporting -numjobs=${numjob} -norandommap -name ${name} --output ${output} --output-format=json"
  fio -rw=${rw_type} -bs=${bs}k -size=${size} -runtime=${runtime} -iodepth=${iodepth} -filename ${TARGET} -ioengine=${ioengine} -direct=${direct} -group_reporting -numjobs=${numjob} -norandommap -name ${name} --output ${output} --output-format=json
  echo "${name}: $(now)" >> $infofile
}

# begin to test
rw_types=("randread" "randwrite")
bs_types=($bs_rio $bs_sio)
# for (( numjob = $numjob_min; numjob <= numjob_max; numjob += 1 ))
for (( t = 1; t <= $REPEAT; t += 1 ));
do
  for (( bs = $bs_min; bs <= $bs_max; bs *= 2 ))
  do
    for rw_type in ${rw_types[@]}; 
    do
      for (( numjob = $numjob_min; numjob <= numjob_max; numjob *= 1 ));
      do
        for (( iodepth = $iodepth_min; iodepth <= $iodepth_max; iodepth *= 2 ))
        do
          do_test $numjob $iodepth $rw_type $bs $t
        done   
      done  
    done
  done
done

echo "Finish Time: $(now)" >> $infofile
echo "Finish."
