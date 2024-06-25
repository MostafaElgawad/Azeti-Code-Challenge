#!/usr/bin/env sh

# Hint: Add something here to wait until the server is ready
URL="http://server:80/ready"

mkdir -p results

until [ "$(curl -s -o /dev/null -w ''%{http_code}'' $URL)" = "200" ] && [ "$(curl -s $URL)" = 'YES' ]; do
  echo "Waiting for the server to be ready..."
  sleep 5
done
echo "Server is ready!"

robot -d results test-server.robot
