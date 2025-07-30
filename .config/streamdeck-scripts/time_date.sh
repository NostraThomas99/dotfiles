#!/bin/bash

# time_date.sh - Display time and date every minute
# Converts text to PNG using ImageMagick and prints to stdout

while true; do
    # Get the formatted date string
    date_string=$(date '+%a %d %b\n%H:%M')
    
    # Print to stdout for button title
    echo "$date_string"
    
    # Convert text to PNG using ImageMagick
    # Using echo -e to interpret newlines properly
    echo -e "$date_string" | convert \
        -background none \
        -fill white \
        -font JetBrainsMono \
        -pointsize 24 \
        -gravity center \
        label:@- \
        /tmp/time_date.png
    
    # Wait for 60 seconds (1 minute)
    sleep 60
done
