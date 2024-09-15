#!/bin/bash

KEYWORD="$USER"
NUM=10
SLEEP=1s

[ x"$1" != x ] && KEYWORD="$1"
[ x"$2" != x ] && NUM="$2"
[ x"$3" != x ] && SLEEP="$3"

while true
do
    # in case of the queue system down
    PEND="$(qstat 2>&1 >/dev/null | wc -l)"
    [ $PEND -gt 0 ] && sleep $SLEEP && continue

    PEND="$(qstat | grep -E "$KEYWORD" | grep " Q " | wc -l)"
    if [ $PEND -lt $NUM ];then
        break
    fi
    sleep $SLEEP
done
