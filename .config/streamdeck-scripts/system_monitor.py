
import os
import time
from PIL import Image, ImageDraw, ImageFont
import common

def get_cpu_load():
    """Get CPU load from /proc/loadavg (1 min average)"""
    try:
        with open('/proc/loadavg', 'r') as f:
            load = float(f.read().split()[0])
        # Get number of CPUs to calculate percentage
        with open('/proc/cpuinfo', 'r') as f:
            cpu_count = f.read().count('processor')
        return (load / cpu_count) * 100
    except:
        return 0.0

def get_ram_usage():
    """Get RAM usage from /proc/meminfo"""
    try:
        with open('/proc/meminfo', 'r') as f:
            lines = f.readlines()
        
        meminfo = {}
        for line in lines:
            if ':' in line:
                key, value = line.split(':', 1)
                meminfo[key.strip()] = int(value.strip().split()[0]) * 1024  # Convert KB to bytes
        
        total = meminfo['MemTotal'] / (1024**3)  # Convert to GiB
        available = meminfo['MemAvailable'] / (1024**3)  # Convert to GiB
        used = total - available
        return used, total
    except:
        return 0.0, 0.0

def get_disk_io():
    """Get disk I/O from /proc/diskstats"""
    def read_diskstats():
        io_stats = {}
        try:
            with open('/proc/diskstats', 'r') as f:
                for line in f:
                    fields = line.split()
                    if len(fields) >= 14:
                        device = fields[2]
                        # Skip loop devices and partitions (focus on whole disks)
                        if not device.startswith('loop') and not any(char.isdigit() for char in device[-1:]):
                            read_bytes = int(fields[5]) * 512  # sectors to bytes
                            write_bytes = int(fields[9]) * 512  # sectors to bytes
                            io_stats[device] = read_bytes + write_bytes
        except:
            pass
        return sum(io_stats.values())
    
    try:
        start_bytes = read_diskstats()
        time.sleep(1)
        end_bytes = read_diskstats()
        return (end_bytes - start_bytes) / (1024**2)  # Convert to MB/s
    except:
        return 0.0

def create_badge(value, unit, path, color_threshold=None):
    """Create a PNG badge with the given value and unit"""
    img = Image.new('RGB', (72, 72), color='#2b2b2b')
    d = ImageDraw.Draw(img)
    
    # Try to load a better font
    try:
        font_large = ImageFont.truetype("/usr/share/fonts/TTF/DejaVuSans-Bold.ttf", 16)
        font_small = ImageFont.truetype("/usr/share/fonts/TTF/DejaVuSans.ttf", 12)
    except (IOError, OSError):
        try:
            font_large = ImageFont.truetype("arial.ttf", 16)
            font_small = ImageFont.truetype("arial.ttf", 12)
        except (IOError, OSError):
            font_large = ImageFont.load_default()
            font_small = ImageFont.load_default()
    
    # Choose color based on value (if thresholds provided)
    text_color = '#ffffff'
    if color_threshold:
        if value > color_threshold[1]:  # High usage - red
            text_color = '#ff4444'
        elif value > color_threshold[0]:  # Medium usage - yellow
            text_color = '#ffaa00'
        else:  # Low usage - green
            text_color = '#44ff44'
    
    # Draw the value (larger font)
    value_text = f'{value:.1f}'
    value_bbox = d.textbbox((0, 0), value_text, font=font_large)
    value_width = value_bbox[2] - value_bbox[0]
    value_height = value_bbox[3] - value_bbox[1]
    
    # Draw the unit (smaller font)
    unit_bbox = d.textbbox((0, 0), unit, font=font_small)
    unit_width = unit_bbox[2] - unit_bbox[0]
    
    # Center the text
    total_width = max(value_width, unit_width)
    value_x = (72 - value_width) // 2
    unit_x = (72 - unit_width) // 2
    
    d.text((value_x, 15), value_text, font=font_large, fill=text_color)
    d.text((unit_x, 40), unit, font=font_small, fill=text_color)
    
    # Ensure directory exists
    os.makedirs(os.path.dirname(path), exist_ok=True)
    img.save(path)

if __name__ == "__main__":
    icon_dir = common.get_icon_dir()

    # CPU
    cpu_load = get_cpu_load()
    create_badge(cpu_load, '%', os.path.join(icon_dir, 'cpu.png'), color_threshold=(50, 80))

    # RAM
    ram_used, ram_total = get_ram_usage()
    ram_percent = (ram_used / ram_total) * 100 if ram_total > 0 else 0
    create_badge(ram_used, 'GiB', os.path.join(icon_dir, 'ram.png'), color_threshold=(70, 90))

    # Disk I/O
    disk_io = get_disk_io()
    create_badge(disk_io, 'MB/s', os.path.join(icon_dir, 'io.png'), color_threshold=(100, 200))

    # Text output for StreamDeck
    print(f"CPU:{cpu_load:.0f}% RAM:{ram_used:.1f}G IO:{disk_io:.0f}MB/s")

