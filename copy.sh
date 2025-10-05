#!/bin/bash

IMG="/tmp/screenshot.png"
TXT="/tmp/screenshot.txt"

grim -g "$(slurp)" "$IMG"

tesseract "$IMG" "$TXT" -l eng

cat "$TXT.txt" | wl-copy

notify-send "OCR" "Extracted text copied to clipboard!"
