#!/bin/bash

interfaces_down=()
for iface in $(ip -o link show | awk -F': ' '{print $2}')
do
    cmd=$(ip link show "$iface" up)
    if [ -z "$cmd" ]; then 
	interfaces_down+=("$iface")
    fi
done

echo ${interfaces_down}
