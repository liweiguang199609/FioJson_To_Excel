nvme_subsystem_name="nvme_subsystem_4"
dev="/dev/nvme2n1"
port_num="4"

mkdir /sys/kernel/config/nvmet/subsystems/${nvme_subsystem_name}

cd /sys/kernel/config/nvmet/subsystems/${nvme_subsystem_name}

echo 1 > attr_allow_any_host

mkdir namespaces/1

cd namespaces/1

echo -n ${dev} > device_path

echo 1 > enable

mkdir /sys/kernel/config/nvmet/ports/${port_num}

cd /sys/kernel/config/nvmet/ports/${port_num}

echo 192.168.2.112 > addr_traddr

echo rdma > addr_trtype

echo 4420 > addr_trsvcid

echo ipv4 > addr_adrfam

ln -s /sys/kernel/config/nvmet/subsystems/${nvme_subsystem_name} /sys/kernel/config/nvmet/ports/${port_num}/subsystems/${nvme_subsystem_name}
