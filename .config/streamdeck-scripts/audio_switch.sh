#!/bin/bash

# Audio switching script for Stream Deck
# Toggles between headset and HDMI audio output

# Device identifiers
HEADSET_SINK="alsa_output.usb-SteelSeries_Arctis_Nova_Pro_Wireless-00.analog-stereo"
HDMI_SINK="alsa_output.pci-0000_01_00.1.hdmi-stereo"

# Get current default sink
current_sink=$(pactl info | grep "Default Sink:" | awk '{print $3}')

# Determine which device to switch to
if [[ "$current_sink" == "$HEADSET_SINK" ]]; then
    # Currently on headset, switch to HDMI
    pactl set-default-sink "$HDMI_SINK"
    new_device="HDMI"
    notify-send "Audio Output" "Switched to HDMI" -i audio-speakers
else
    # Currently on HDMI or other, switch to headset
    pactl set-default-sink "$HEADSET_SINK" 
    new_device="Headset"
    notify-send "Audio Output" "Switched to Headset" -i audio-headphones
fi

# Create/update audio.png with active device label
icon_dir="$HOME/.config/streamdeck-icons"
mkdir -p "$icon_dir"

# Create a simple PNG with the device name using ImageMagick
# If ImageMagick is not available, we'll create a fallback
if command -v convert >/dev/null 2>&1; then
    convert -size 144x144 xc:black \
            -fill white \
            -gravity center \
            -font DejaVu-Sans-Bold \
            -pointsize 20 \
            -annotate +0+0 "$new_device" \
            "$icon_dir/audio.png"
else
    # Fallback: create a simple text file that can be used as a reference
    echo "$new_device" > "$icon_dir/audio_status.txt"
    # Try to use a generic audio icon if available
    if [ -f "$icon_dir/audio-generic.png" ]; then
        cp "$icon_dir/audio-generic.png" "$icon_dir/audio.png"
    fi
fi

echo "Switched audio output to: $new_device"
