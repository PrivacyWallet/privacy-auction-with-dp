for i in {0..0}
do
  ganache-cli -a 1000 -l 1000000000 -q 1>/dev/null &
  SUB_ID=$!

  sleep 5

  truffle test ./test/benchmark-test.js

  kill $SUB_ID
  echo killed $SUB_ID
done
