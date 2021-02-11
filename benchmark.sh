#!/bin/bash
TIMES=300
for i in {0..9}
do
  ganache-cli -a $TIMES -l 1000000000 -q 1>/dev/null &
  SUB_ID=$!

  echo "times $i"
  sleep 5

  echo "start==="
  truffle test ./test/benchmark-test.js | tee -a log.log

  kill $SUB_ID
  echo killed $SUB_ID
  echo "end==="
done
