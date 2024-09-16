#!/bin/bash

while :
do 
  cpuUsage=$(top -bn1 | awk '/Cpu/ { print $2}')
  memUsage=$(free -m | awk '/Mem/{print $3}')

  echo "CPU Usage: $cpuUsage%"
  echo "Memory Usage: $memUsage MB"
 
  sleep 1
done 
