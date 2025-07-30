#!/usr/bin/env python3
import configparser
import json
import os
import subprocess

def main():
    """
    Generates a StreamDeck UI profile based on a configuration file and restarts the service.
    """
    config_path = os.path.expanduser("~/.config/streamdeck-ui/streamdeck-ui.conf")
    profile_path = os.path.expanduser("~/.cache/streamdeck-ui/profiles/default.json")
    scripts_dir = os.path.dirname(os.path.abspath(__file__))

    # Create cache directory if it doesn't exist
    os.makedirs(os.path.dirname(profile_path), exist_ok=True)

    config = configparser.ConfigParser()
    # Provide a fallback configuration if the file doesn't exist or is empty
    if not os.path.exists(config_path) or os.path.getsize(config_path) == 0:
        config['streamdeck'] = {}
    else:
        try:
            config.read(config_path)
        except configparser.Error:
            # If the config file is malformed, use a fallback
            config['streamdeck'] = {}


    buttons = [
        {
            "icon": f"{scripts_dir}/net.png",
            "text": "Bandwidth",
            "command": f"{scripts_dir}/bandwidth.py",
            "page": 0,
            "button": 0
        },
        {
            "icon": f"{scripts_dir}/song.png",
            "text": "Cider Track",
            "command": f"{scripts_dir}/cider_track.py",
            "page": 0,
            "button": 1
        },
        {
            "icon": "",
            "text": "Audio",
            "command": f"{scripts_dir}/audio_switch.sh",
            "page": 0,
            "button": 2
        },
        {
            "icon": "",
            "text": "Cider",
            "command": f"{scripts_dir}/cider_control.sh",
            "page": 0,
            "button": 3
        },
        {
            "icon": "",
            "text": "Lock",
            "command": f"{scripts_dir}/screenlock.sh",
            "page": 0,
            "button": 4
        },
        {
            "icon": "",
            "text": "System",
            "command": f"{scripts_dir}/system_monitor.py",
            "page": 0,
            "button": 5
        },
        {
            "icon": "",
            "text": "Time/Date",
            "command": f"{scripts_dir}/time_date.sh",
            "page": 0,
            "button": 6
        }
    ]

    profile_data = {
        "0": {
            "name": "Default",
            "buttons": {}
        }
    }

    for button in buttons:
        page = str(button.pop("page"))
        button_index = str(button.pop("button"))
        profile_data[page]["buttons"][button_index] = button


    with open(profile_path, "w") as f:
        json.dump(profile_data, f, indent=4)

    print(f"StreamDeck UI profile generated: {profile_path}")
    
    # Try to restart streamdeck-ui service with different possible service names
    service_names = ["streamdeck-ui", "streamdeck"]
    service_restarted = False
    
    for service_name in service_names:
        try:
            # First check if the service exists
            check_result = subprocess.run(
                ["systemctl", "--user", "is-active", service_name], 
                capture_output=True, text=True
            )
            
            # If service exists (regardless of active state), try to restart it
            subprocess.run(["systemctl", "--user", "restart", service_name], check=True)
            print(f"StreamDeck UI service '{service_name}' restarted successfully.")
            service_restarted = True
            break
            
        except (subprocess.CalledProcessError, FileNotFoundError):
            continue
    
    if not service_restarted:
        print("No StreamDeck UI service found to restart.")
        print("You may need to start streamdeck-ui manually or install it as a service.")
        print("Try running: streamdeck-ui --device 0")

if __name__ == "__main__":
    main()

