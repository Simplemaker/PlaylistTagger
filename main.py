import argparse
import subprocess
from mutagen.id3 import ID3, TPE1, TIT2, TRCK, TALB, APIC
from PIL import Image
import requests
from io import BytesIO
import os

def read_custom_config(file_path):
    with open(file_path, 'r') as file:
        content = file.read()
    
    sections = content.strip().split('\n\n')
    result = []

    for section in sections:
        section_dict = {}
        lines = section.split('\n')
        for line in lines:
            if ':' not in line: continue
            key, value = line.split(':', 1)
            section_dict[key.strip()] = value.strip()
        if section_dict:
            result.append(section_dict)

    return result


def download_video(url, output_filename, thumbnail_art):
    command = [
        'yt-dlp',  # Ensure yt-dlp is in your PATH
        url,
        '-o', output_filename,  # Specify the output filename
        '-x', '--audio-format', 'mp3'
    ]
    if thumbnail_art:
        command.append('--write-thumbnail')
    subprocess.run(command, check=True)

def art_to_buffer(url):
    # Load the image from the URL
    response = requests.get(url)
    img = Image.open(BytesIO(response.content))


def crop_image(img):
    # Get the dimensions of the image
    width, height = img.size

    # Calculate the size of the square (the smaller dimension)
    square_size = min(width, height)

    # Calculate the coordinates for cropping
    left = (width - square_size) // 2
    top = (height - square_size) // 2
    right = left + square_size
    bottom = top + square_size

    # Crop the image
    return img.crop((left, top, right, bottom))


def image_to_buffer(image):
    # Save the cropped image to a buffer as PNG
    output_buffer = BytesIO()
    image.save(output_buffer, format='PNG')
    output_buffer.seek(0)  # Rewind the buffer to the beginning
    return output_buffer


def set_art(audio, art):
    art_buffer = image_to_buffer(art)
    audio['APIC'] = APIC(
        encoding=3,  # 3 is for UTF-8
        mime='image/jpeg',  # or 'image/png'
        type=3,  # 3 is for the cover(front) image
        desc='Cover',
        data=art_buffer.read()
    )

'''
Sections have the following fields:
title - the title of the song
artist - the artist of the song
art - url to a jpg or png of the album art. Will be cropped to a centered square automatically
yt - url of the youtube video containing the song. (required)
'''
def process_section(section):
    yt = section.get('yt')
    title = section.get('title')
    artist = section.get('artist')
    album = section.get('album')
    art = section.get('art')
    track = section.get('track')

    filename = f'{artist} - {title}.mp3'
    thumbnail_art = art == 'thumbnail'
    if thumbnail_art:
        thumbnail_filename = filename + '.webp'
    
    download_video(yt, filename, thumbnail_art)
    
    audio = ID3(filename)
    
    if title:
        audio['TIT2'] = TIT2(encoding=3, text=title)
    if artist:
        audio['TPE1'] = TPE1(encoding=3, text=artist)
    if album:
        audio['TALB'] = TALB(encoding=3, text=album)
    if track:
        audio['TRCK'] = TRCK(encoding=3, text=track)

    if art:
        if thumbnail_art:
            image = Image.open(thumbnail_filename)
        else:
            response = requests.get(art)
            image = Image.open(BytesIO(response.content))
        cropped_img = crop_image(image)
        set_art(audio, cropped_img)

    if thumbnail_art:
        os.remove(thumbnail_filename)
    audio.save(v2_version=3)

def main():
    parser = argparse.ArgumentParser(description="Read a playlist configuration file with metadata.")
    parser.add_argument('file_path', type=str, help='Path to the configuration file')
    args = parser.parse_args()

    config_data = read_custom_config(args.file_path)
    for section in config_data:
        print(section)
        process_section(section)

if __name__ == "__main__":
    main()
