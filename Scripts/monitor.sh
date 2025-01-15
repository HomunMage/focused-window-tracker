#!/bin/bash

while true; do
  window_name=$(xdotool getactivewindow getwindowname 2>/dev/null)
  if [[ -n "$window_name" ]]; then
     # Attempt to convert the window name to UTF-8.  If it fails, we'll skip.
     if ! window_name_utf8=$(echo "$window_name" | iconv -f utf-8 -t utf-8 2>/dev/null); then
        echo "ERROR: Cannot encode window name to UTF-8, skipping this entry"
        sleep 1
        continue
     fi
    escaped_window=$(echo "$window_name_utf8" | sed 's/\\/\\\\/g; s/"/\\"/g; s/\n/\\n/g')
     # Attempt the API call and handle possible errors
     if ! curl -s -X POST -H "Content-Type: application/json" -d "{\"window_name\":\"$escaped_window\"}" http://localhost:17892/update ; then
         #Log the error
         echo "ERROR: Failed to update window name. HTTP Response:" $(curl -s -w "%{http_code}\n" -X POST -H "Content-Type: application/json" -d "{\"window_name\":\"$escaped_window\"}" http://localhost:17892/update)
     fi
  fi
  sleep 1
done