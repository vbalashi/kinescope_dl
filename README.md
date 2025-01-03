# Kinescope Video Downloader

A Python script to batch download videos from Kinescope.io using N_m3u8DL-RE.

## Prerequisites

1. **N_m3u8DL-RE**: 
   - Download the latest release from [N_m3u8DL-RE releases](https://github.com/nilaoda/N_m3u8DL-RE/releases)
   - Extract `N_m3u8DL-RE.exe` to the same directory as the script

2. **FFmpeg**:
   - Download the latest release from [FFmpeg Builds](https://github.com/BtbN/FFmpeg-Builds/releases)
   - Extract `ffmpeg.exe` to the same directory as the script or add it to your system PATH

## Usage

1. Create a CSV file with video information in the following format:
   ```
   title;referrer;mpd_url
   ```

2. Run the script:
   ```bash
   # Using default dl_list.csv
   python kdy.py

   # Using custom CSV file
   python kdy.py --list path/to/your/list.csv
   ```

## Options

- `--list`: Path to CSV file containing video information (default: dl_list.csv)
- `--help`: Show help message and exit

## CSV Format

Each line in the CSV file should contain:
- Title: Video title (will be used as filename)
- Referrer: Website domain for referrer header
- MPD URL: Direct URL to the MPD/m3u8 file

