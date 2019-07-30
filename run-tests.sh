#!/usr/bin/env bash
set -e
if [ ! -z ${DEBUG:+X} ]; then
  set -x;
fi

echo "[Info] Building test service containers, wait for a moment"
docker-compose -f docker-compose.test.yml up -d >/dev/null 2>&1

if [ $? -ne 0 ]; then
  echo "[Error] docker-compose failed to create containers check with docker-compose -f docker-compose.test.yml up  command"
  exit 1
else
  sleep 15
  echo "[Info] Finished building containers"
fi

echo "[Info]Start testing"

docker-compose -f docker-compose.test.yml exec test_api python -m pytest tests -v

if [ $? -ne 0 ]; then
  echo "[Error] Fatal error occoured while testing, please check above logs"
  exit 1
else
  echo "[Info] Successful test execution"
fi

echo "[Info] Removing test service containers"
docker-compose -f docker-compose.test.yml down >/dev/null 2>&1
echo "[Info] Finished removing test service containers"