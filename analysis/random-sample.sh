#!/bin/sh
# a program to randomly sample a file
awk 'BEGIN {srand()} !/^%/ {if (rand() < 0.1) print $0}' tweets.json |\
    jq -c 'select(.text) | {created_at, text}' > 5percent.json
