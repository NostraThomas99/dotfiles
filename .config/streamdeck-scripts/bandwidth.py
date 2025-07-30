#!/usr/bin/env python3
import subprocess
import json
import time
import datetime
import matplotlib.pyplot as plt
import os

# --- Configuration ---
LOG_INTERVAL_SECONDS = 30
HISTORY_POINTS = 100  # Number of data points to show on the graph
CACHE_FILE = os.path.join(os.path.expanduser("~"), ".bandwidth_cache.json")
OUTPUT_IMAGE = "net.png"

# --- Data storage ---
history = {
    "timestamps": [],
    "download": [],
    "upload": [],
}

last_successful_data = {"download": 0, "upload": 0, "ping": 0}

def load_cache():
    """Loads previous data from a cache file."""
    global last_successful_data
    if os.path.exists(CACHE_FILE):
        with open(CACHE_FILE, "r") as f:
            try:
                last_successful_data = json.load(f)
            except json.JSONDecodeError:
                pass # Ignore corrupted cache

def save_cache():
    """Saves the last successful data to a cache file."""
    with open(CACHE_FILE, "w") as f:
        json.dump(last_successful_data, f)

def get_speedtest_results():
    """Runs speedtest-cli and returns the results."""
    try:
        result = subprocess.run(
            ["speedtest-cli", "--json"],
            capture_output=True,
            text=True,
            check=True,
            timeout=60,
        )
        return json.loads(result.stdout)
    except (
        subprocess.CalledProcessError,
        subprocess.TimeoutExpired,
        FileNotFoundError,
        json.JSONDecodeError,
    ) as e:
        print(f"Could not run speedtest-cli: {e}")
        return None

def update_data():
    """Gets new data and updates history."""
    global last_successful_data
    data = get_speedtest_results()

    if data:
        last_successful_data = {
            "download": data["download"] / 1e6,  # Convert to Mbps
            "upload": data["upload"] / 1e6,  # Convert to Mbps
            "ping": data["ping"],
        }
        save_cache()

    # Always add a data point to the history to keep the timeline consistent
    # Use the last successful data if the new fetch failed
    history["timestamps"].append(datetime.datetime.now())
    history["download"].append(last_successful_data["download"])
    history["upload"].append(last_successful_data["upload"])

    # Trim history
    for key in history:
        history[key] = history[key][-HISTORY_POINTS:]


def draw_graph():
    """Draws the bandwidth graph and saves it to a file."""
    plt.style.use('dark_background')
    fig, ax = plt.subplots(figsize=(10, 5))
    
    ax.plot(history["timestamps"], history["download"], label="Download (Mbps)", color='cyan')
    ax.plot(history["timestamps"], history["upload"], label="Upload (Mbps)", color='magenta')

    ax.set_xlabel("Time")
    ax.set_ylabel("Speed (Mbps)")
    ax.set_title("Internet Bandwidth")
    ax.legend()
    ax.grid(True, which='both', linestyle='--', linewidth=0.5)
    
    fig.autofmt_xdate()
    plt.tight_layout()
    plt.savefig(OUTPUT_IMAGE, bbox_inches='tight', pad_inches=0.1, transparent=True)
    plt.close(fig)


def print_caption():
    """Prints the current bandwidth stats."""
    caption = (
        f"Download: {last_successful_data['download']:.2f} Mbps | "
        f"Upload: {last_successful_data['upload']:.2f} Mbps | "
        f"Ping: {last_successful_data['ping']:.2f} ms"
    )
    print(caption)


def check_dependencies():
    """Checks for required command-line tools and Python packages."""
    try:
        subprocess.run(["speedtest-cli", "--version"], capture_output=True, check=True, text=True)
    except (FileNotFoundError, subprocess.CalledProcessError):
        print("Error: 'speedtest-cli' is not installed or not in your PATH.")
        print("Please install it, e.g., 'pip install speedtest-cli'")
        return False

    try:
        import matplotlib
    except ImportError:
        print("Error: 'matplotlib' is not installed.")
        print("Please install it, e.g., 'pip install matplotlib'")
        return False
        
    return True


if __name__ == "__main__":
    if not check_dependencies():
        exit(1)
        
    load_cache()

    while True:
        update_data()
        draw_graph()
        print_caption()
        time.sleep(LOG_INTERVAL_SECONDS)

