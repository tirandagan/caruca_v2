#!/bin/bash
# Runs on the Mac. Once a minute: power source and battery (pmset -g batt). Sleep/wake events are read
# afterwards from pmset -g log for the run window. Stops when the file STOP_POWER_WATCH exists.
dest="$(cd "$(dirname "$0")" && pwd)"
while [ ! -e "$dest/STOP_POWER_WATCH" ]; do
  src=$(pmset -g batt | head -1 | sed "s/.*'\(.*\)'.*/\1/")
  pct=$(pmset -g batt | grep -o '[0-9]*%' | head -1)
  echo "$(date '+%Y-%m-%d %H:%M:%S %z')	$src	$pct" >> "$dest/power_watch.tsv"
  sleep 60
done
