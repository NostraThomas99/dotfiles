import subprocess
from PIL import Image, ImageDraw, ImageFont
import os
import textwrap

# --- Configuration ---
PLAYER_NAME = "cider"
OUTPUT_IMAGE = "song.png"
IMAGE_WIDTH = 256
IMAGE_HEIGHT = 256
BACKGROUND_COLOR = "black"
TEXT_COLOR = "white"
FONT_SIZE_TITLE = 22
FONT_SIZE_ARTIST = 18

# List of common font paths to try
FONT_PATHS = [
    "/usr/share/fonts/TTF/DejaVuSans.ttf",
    "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
    "/usr/share/fonts/dejavu/DejaVuSans.ttf",
    "/System/Library/Fonts/Supplemental/Arial.ttf",
    "arial.ttf"
]

def get_font(size):
    """Try to load a font from the common paths."""
    for path in FONT_PATHS:
        try:
            return ImageFont.truetype(path, size)
        except IOError:
            continue
    print("Warning: Custom font not found. Using default font.")
    return ImageFont.load_default()

def get_track_info():
    """Gets artist and title from playerctl."""
    try:
        # Use a single call to playerctl for efficiency
        command = [
            "playerctl",
            "--player", PLAYER_NAME,
            "metadata",
            "--format", "{{artist}}\n{{title}}"
        ]
        output = subprocess.check_output(command, stderr=subprocess.DEVNULL).decode("utf-8").strip()

        if not output:
            # If output is empty, Cider might be open but not playing anything.
            status_cmd = ["playerctl", "--player", PLAYER_NAME, "status"]
            status = subprocess.check_output(status_cmd, stderr=subprocess.DEVNULL).decode("utf-8").strip()
            if status in ["Playing", "Paused"]:
                return "Cider", "..."  # No metadata available
            else:
                return "Cider", "Not Playing"

        artist, title = output.split('\n', 1)
        return artist.strip(), title.strip()

    except (subprocess.CalledProcessError, FileNotFoundError):
        return "Cider", "Not Available"

def create_track_image(artist, title):
    """Creates an image with the provided track info."""
    img = Image.new('RGB', (IMAGE_WIDTH, IMAGE_HEIGHT), color=BACKGROUND_COLOR)
    draw = ImageDraw.Draw(img)

    title_font = get_font(FONT_SIZE_TITLE)
    artist_font = get_font(FONT_SIZE_ARTIST)

    # Wrap text to fit image width
    # Estimate character width. A more precise method would be to measure text width,
    # but this is simpler and usually good enough.
    char_width_title = FONT_SIZE_TITLE / 1.8
    char_width_artist = FONT_SIZE_ARTIST / 1.8
    title_lines = textwrap.wrap(title, width=max(1, int((IMAGE_WIDTH - 20) / char_width_title)))
    artist_lines = textwrap.wrap(artist, width=max(1, int((IMAGE_WIDTH - 20) / char_width_artist)))

    # Calculate total text height to center it vertically
    title_height = sum([draw.textbbox((0, 0), line, font=title_font)[3] for line in title_lines])
    artist_height = sum([draw.textbbox((0, 0), line, font=artist_font)[3] for line in artist_lines])
    
    total_text_height = title_height + artist_height
    if title_lines and artist_lines:
        total_text_height += 10  # Padding between artist and title

    y = (IMAGE_HEIGHT - total_text_height) / 2

    # Draw title
    for line in title_lines:
        bbox = draw.textbbox((0, 0), line, font=title_font)
        line_width = bbox[2] - bbox[0]
        x = (IMAGE_WIDTH - line_width) / 2
        draw.text((x, y), line, font=title_font, fill=TEXT_COLOR)
        y += (bbox[3] - bbox[1])

    # Add padding and draw artist
    if title_lines and artist_lines:
        y += 10
    for line in artist_lines:
        bbox = draw.textbbox((0, 0), line, font=artist_font)
        line_width = bbox[2] - bbox[0]
        x = (IMAGE_WIDTH - line_width) / 2
        draw.text((x, y), line, font=artist_font, fill=TEXT_COLOR)
        y += (bbox[3] - bbox[1])

    # Save the image in the same directory as the script
    script_dir = os.path.dirname(os.path.abspath(__file__))
    output_path = os.path.join(script_dir, OUTPUT_IMAGE)
    try:
        img.save(output_path)
    except Exception as e:
        print(f"Error saving image: {e}")

if __name__ == "__main__":
    current_artist, current_title = get_track_info()
    create_track_image(current_artist or "Cider", current_title or "Not Available")


