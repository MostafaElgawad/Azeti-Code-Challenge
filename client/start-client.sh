#!/bin/sh

URL="http://server:80/ready"

# while true; do
#     response=$(curl -s http://server:80/ready)
#     if [ "$response" = "YES" ]; then
#         echo "Server is Ready"
#         break
#     fi
#     echo "Waiting for server to be ready..."
#     sleep 5
# done
until [ "$(curl -s -o /dev/null -w ''%{http_code}'' $URL)" = "200" ] && [ "$(curl -s $URL)" = 'YES' ]; do
  echo "Waiting for the server to be ready..."
  sleep 5
done
echo "Server is ready!"

# start client itself after making sure that server is ready
python3 client.py