#!/bin/bash

# Cider Control Script
# Simple media controls for Cider using playerctl via MPRIS

# Check if playerctl is installed
if ! command -v playerctl &> /dev/null; then
    echo "Error: playerctl is not installed. Please install it first."
    echo "On Ubuntu/Debian: sudo apt install playerctl"
    echo "On Arch: sudo pacman -S playerctl"
    echo "On macOS: brew install playerctl"
    exit 1
fi

# Function to display usage
show_usage() {
    echo "Usage: $0 [play-pause|next|previous|status]"
    echo ""
    echo "Commands:"
    echo "  play-pause  - Toggle play/pause"
    echo "  next        - Skip to next track"
    echo "  previous    - Go to previous track"
    echo "  status      - Show current playback status"
    echo ""
    echo "Example: $0 play-pause"
}

# Check if Cider is running
check_cider() {
    if ! playerctl --player=cider status &> /dev/null; then
        echo "Error: Cider is not running or MPRIS is not available."
        echo "Make sure Cider is running and MPRIS is enabled in settings."
        return 1
    fi
    return 0
}

# Main command handling
case "$1" in
    "play-pause")
        if check_cider; then
            playerctl --player=cider play-pause
            echo "Toggled play/pause"
        fi
        ;;
    "next")
        if check_cider; then
            playerctl --player=cider next
            echo "Skipped to next track"
        fi
        ;;
    "previous")
        if check_cider; then
            playerctl --player=cider previous
            echo "Went to previous track"
        fi
        ;;
    "status")
        if check_cider; then
            status=$(playerctl --player=cider status 2>/dev/null)
            if [[ -n "$status" ]]; then
                echo "Status: $status"
                # Try to get current track info
                artist=$(playerctl --player=cider metadata artist 2>/dev/null)
                title=$(playerctl --player=cider metadata title 2>/dev/null)
                if [[ -n "$artist" && -n "$title" ]]; then
                    echo "Now playing: $artist - $title"
                fi
            else
                echo "Unable to get status"
            fi
        fi
        ;;
    "")
        show_usage
        exit 1
        ;;
    *)
        echo "Error: Unknown command '$1'"
        echo ""
        show_usage
        exit 1
        ;;
esac
