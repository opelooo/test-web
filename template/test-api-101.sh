#!/bin/bash

# Check if an argument was provided
if [ -z "$1" ]; then
  echo "Usage: $0 <URL>"
  exit 1
fi

link="$1"

for i in {1..35}; do
  curl -s -I -X GET "$link" | grep HTT*
done
