#!/bin/bash

### CPU 정보 ###
CPU_MODEL=$(lscpu | grep "Model name" | awk -F: '{print $2}' | sed 's/^[ \t]*//')
CORES=$(lscpu | grep "Core(s) per socket" | awk -F: '{print $2}' | sed 's/^[ \t]*//')
THREADS=$(lscpu | grep "^CPU(s):" | awk -F: '{print $2}' | sed 's/^[ \t]*//')
FREQ_MIN=$(lscpu | grep "CPU min MHz" | awk -F: '{print $2}' | awk '{printf "%.1f", $1/1000}')
FREQ_MAX=$(lscpu | grep "CPU max MHz" | awk -F: '{print $2}' | awk '{printf "%.1f", $1/1000}')
L3_CACHE=$(lscpu | grep "L3" | awk -F: '{print $2}' | sed 's/^[ \t]*//')

### Memory 정보 ###
MEM_RAW=$(sudo dmidecode --type 17 | grep -Ei 'Size:|Type:|Speed:' | grep -v "No Module Installed")
MEM_SIZE=$(echo "$MEM_RAW" | grep "Size:" | awk '{sum += $2} END {print sum}')
MEM_UNIT=$(echo "$MEM_RAW" | grep "Size:" | head -1 | awk '{print $3}')
MEM_TYPE=$(echo "$MEM_RAW" | grep "Type:" | grep -v "Detail" | head -1 | awk -F: '{print $2}' | sed 's/^[ \t]*//')
MEM_SPEED=$(echo "$MEM_RAW" | grep "Speed:" | head -1 | awk -F: '{print $2}' | sed 's/^[ \t]*//')

### SSD/HDD 정보 ###
DISK_LINE=$(lsblk -d -o NAME,MODEL,SIZE,ROTA,TYPE | grep -v loop | grep disk | head -n 1)

DEVICE=$(echo "$DISK_LINE" | awk '{print $1}')
DISK_MODEL=$(echo "$DISK_LINE" | awk '{for (i=2; i<=NF-3; i++) printf $i " "; print ""}' | sed 's/[ \t]*$//')
SIZE=$(echo "$DISK_LINE" | awk '{print $(NF-2)}')
ROTA=$(echo "$DISK_LINE" | awk '{print $(NF-1)}')

# 용량 단위 보정
function convert_size() {
  RAW=$1
  UNIT=${RAW: -1}
  NUM=$(echo $RAW | sed 's/[A-Za-z]*$//')

  case $UNIT in
    K|k) echo "$(awk "BEGIN {printf \"%.0fGB\", $NUM / 1024 / 1024}")" ;;
    M|m) echo "$(awk "BEGIN {printf \"%.0fGB\", $NUM / 1024}")" ;;
    G|g) echo "$(awk "BEGIN {printf \"%.0fGB\", $NUM}")" ;;
    T|t) echo "$(awk "BEGIN {printf \"%.0fTB\", $NUM}")" ;;
    *) echo "$RAW" ;;
  esac
}

SIZE_HUMAN=$(convert_size $SIZE)

# 인터페이스 판별
if [[ "$DEVICE" == nvme* ]]; then
  INTERFACE="NVMe"
else
  INTERFACE="SATA"
fi

if [ "$ROTA" == "0" ]; then
  DISK_TYPE="SSD"
else
  DISK_TYPE="HDD"
fi

### 최종 출력 ###
echo "- $CPU_MODEL ($L3_CACHE L3 Cache, $CORES Cores, $THREADS Threads, ${FREQ_MIN}GHz to ${FREQ_MAX}GHz Turbo)"
echo "- ${MEM_SIZE}${MEM_UNIT} (${MEM_TYPE} ${MEM_SPEED})"
echo "- $DISK_TYPE: $SIZE_HUMAN ($INTERFACE)"
echo "- OS: $(grep '^PRETTY_NAME=' /etc/os-release | cut -d= -f2 | tr -d '"')"
