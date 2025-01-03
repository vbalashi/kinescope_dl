import subprocess
import csv
import argparse
import sys
import os
from datetime import datetime
import re

"""
Video Downloader for Kinescope.io
This script downloads videos from Kinescope.io using N_m3u8DL-RE.exe.
It processes a CSV file containing video information in the format:
title;referrer;mpd_url

Usage:
    python kdy.py [--help]
    python kdy.py --list path/to/list.csv --folder my_downloads
"""

def sanitize_filename(filename):
    # Remove or replace special characters
    filename = re.sub(r'[<>:"/\\|?*]', '_', filename)
    # Replace multiple spaces with single space
    filename = re.sub(r'\s+', ' ', filename)
    # Trim spaces from ends
    filename = filename.strip()
    return filename

def parse_arguments():
    parser = argparse.ArgumentParser(
        description='Download videos from Kinescope.io using a CSV list',
        formatter_class=argparse.RawTextHelpFormatter
    )
    parser.add_argument(
        '--list', 
        type=str,
        default='dl_list.csv',
        help='Path to CSV file with video list (default: dl_list.csv)\n'
             'CSV format: title;referrer;mpd_url'
    )
    parser.add_argument(
        '--folder',
        type=str,
        help='Download folder name (default: download_YYYYMMDD_HHMMSS)'
    )
    return parser.parse_args()

m3u8DL_RE_path = 'N_m3u8DL-RE.exe'

def main():
    args = parse_arguments()
    
    # Create download folder with absolute path
    if args.folder:
        download_folder = args.folder
    else:
        current_time = datetime.now().strftime("%Y%m%d_%H%M%S")
        download_folder = f"download_{current_time}"
    
    # Convert to absolute path
    download_folder = os.path.abspath(download_folder)
    os.makedirs(download_folder, exist_ok=True)
    
    try:
        # Read and process the CSV file
        with open(args.list, 'r', encoding='utf-8') as csvfile:
            csv_reader = csv.reader(csvfile, delimiter=';')
            last_referrer = None  # Store the last non-empty referrer
            
            for row in csv_reader:
                # Extract data from CSV row
                title, referrer, mpd_url = row
                
                # Sanitize the title for use as filename
                safe_title = sanitize_filename(title)
                
                # Use previous referrer if current is empty
                if not referrer.strip():
                    referrer = last_referrer
                else:
                    last_referrer = referrer
                
                print(f'\nDownloading: {title}')
                print(f'MPD URL: {mpd_url}')
                print(f'Referrer: {referrer}')
                
                # Create full path for the output file
                output_path = os.path.join(download_folder, f"{safe_title}.mp4")
                
                run_args = [
                    m3u8DL_RE_path,
                    '--concurrent-download',
                    '-H', f'referer: {referrer}',
                    '--log-level', 'INFO',
                    '--del-after-done',
                    '-M', 'format=mp4:muxer=ffmpeg',
                    '--save-dir', download_folder,  # Specify output directory
                    '--save-name', safe_title,      # Use sanitized filename
                    '--auto-select',  # Will select best quality automatically
                    mpd_url
                ]
                
                try:
                    subprocess.run(run_args)
                    print(f'Finished downloading: {title}')
                except Exception as e:
                    print(f'Error downloading {title}: {str(e)}')
                    continue
                    
    except FileNotFoundError:
        print(f"Error: Could not find CSV file '{args.list}'")
        sys.exit(1)
    except Exception as e:
        print(f"Error: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()
