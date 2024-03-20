#!/bin/bash

# This script will fetch a URL using curl at a random interval between 100ms and 5s
while true; do
    # Generate a random sleep time between 100ms and 5s
    sleep_time=$(awk -v min=0.1 -v max=5 'BEGIN{srand(); print int(min+rand()*(max-min+1))}')
    sleep "$sleep_time"

    # Fetch the URL using curl
    curl -s -o /dev/null "http://localhost:8080" 

    # Call snail api with a 50% chance
    random_number=$((RANDOM % 2))
    # If the random number is 0, execute the code
    if [ $random_number -eq 0 ]; then
        curl -s -o /dev/null "http://localhost:8080/snail" 
    fi

    # Call rabbit api with a 20% chance
    random_number=$((RANDOM % 10 + 1))
    # If the random number is 0, execute the code
    if [ $random_number -le 2 ]; then
        curl -s -o /dev/null "http://localhost:8080/rabbit" 
    fi

    # Call panda api with a 90% chance
    random_number=$((RANDOM % 10 + 1))
    # If the random number is 0, execute the code
    if [ $random_number -le 9 ]; then
        curl -s -o /dev/null "http://localhost:8080/panda" 
    fi

    # Call beaver api with a 50% chance
    random_number=$((RANDOM % 2))
    # If the random number is 0, execute the code
    if [ $random_number -eq 0 ]; then
        curl -s -o /dev/null "http://localhost:8080/beaver" 
    fi
done