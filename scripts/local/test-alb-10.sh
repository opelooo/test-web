#!/bin/bash

# Check if an argument was provided
# show error (Usage: ./test-alb-10.sh <URL>) if there is no argument
if [ -z "$1" ]; then
  echo "Usage: $0 <URL>"
  exit 1
fi

link="$1"

# for loop curl link to ten, show Headers (-I) and hide progress (-s)
# while filter text to only show X-Server-Marker
for i in {1..10}; do
  curl -s -I "$link" | grep X-Server-Marker
done
