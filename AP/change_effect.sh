#!/bin/bash

WLED_IP="10.42.0.142"

PLAYLIST_PRESET_ID=11
LOUD_PLAYLIST_PRESET_ID=25

start_playlist() {
    curl -s -m 2 -X POST "http://${WLED_IP}/json/state" \
         -H "Content-Type: application/json" \
         -d "{\"ps\":${PLAYLIST_PRESET_ID}}" > /dev/null
}

next_preset() {
    curl -s -m 2 -X POST "http://${WLED_IP}/json/state" \
         -H "Content-Type: application/json" \
         -d '{"np":true}' > /dev/null
}

start_playlist
next_preset