#!/bin/bash

# screenlock.sh - Screen lock script for system tray
# Attempts to lock the screen using available methods

# Try loginctl first (systemd)
if command -v loginctl &> /dev/null; then
    loginctl lock-session
    exit 0
fi

# Fallback to qdbus (KDE/Qt)
if command -v qdbus &> /dev/null; then
    qdbus org.freedesktop.ScreenSaver /ScreenSaver Lock
    exit 0
fi

# Additional fallbacks for other desktop environments
if command -v gnome-screensaver-command &> /dev/null; then
    gnome-screensaver-command --lock
    exit 0
fi

if command -v xdg-screensaver &> /dev/null; then
    xdg-screensaver lock
    exit 0
fi

if command -v dm-tool &> /dev/null; then
    dm-tool lock
    exit 0
fi

# If nothing works, show an error
echo "No screen lock method available" >&2
exit 1
