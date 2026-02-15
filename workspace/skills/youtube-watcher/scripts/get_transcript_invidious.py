#!/usr/bin/env python3
"""
YouTube Transcript via Invidious
Automatically uses Invidious mirrors to bypass YouTube bot detection.
"""
import argparse
import os
import re
import subprocess
import sys
import tempfile
from pathlib import Path

# Invidious mirrors (will try in order until one works)
INVIDIOUS_MIRRORS = [
    "https://yewtu.be",
    "https://yewtu.be",
    "https://invidious.fdn.fr",
    "https://invidious.snopyta.org",
    "https://invidious.kavin.rocks",
]

def clean_vtt(content: str) -> str:
    """Clean WebVTT content to plain text."""
    lines = content.splitlines()
    text_lines = []
    seen = set()
    
    timestamp_pattern = re.compile(r'\d{2}:\d{2}:\d{2}\.\d{3}\s-->\s\d{2}:\d{2}:\d{2}\.\d{3}')
    
    for line in lines:
        line = line.strip()
        if not line or line == 'WEBVTT' or line.isdigit():
            continue
        if timestamp_pattern.match(line):
            continue
        if line.startswith('NOTE') or line.startswith('STYLE'):
            continue
            
        if text_lines and text_lines[-1] == line:
            continue
            
        line = re.sub(r'<[^>]+>', '', line)
        text_lines.append(line)

def extract_video_id(url: str) -> str:
    """Extract video ID from various YouTube URL formats."""
    patterns = [
        r'(?:youtube\.com/watch\?v=|youtu\.be/|youtube\.com/shorts/)([a-zA-Z0-9_-]{11})',
        r'([a-zA-Z0-9_-]{11})',
    ]
    for pattern in patterns:
        match = re.search(pattern, url)
        if match:
            return match.group(1)
    return None

def get_transcript(url: str, use_invidious: bool = True):
    video_id = extract_video_id(url)
    if not video_id:
        print("Error: Could not extract video ID from URL", file=sys.stderr)
        sys.exit(1)
    
    if use_invidious:
        # Try each Invidious mirror
        for mirror in INVIDIOUS_MIRRORS:
            invidious_url = f"{mirror}/watch?v={video_id}"
            print(f"Trying {mirror}...", file=sys.stderr)
            
            with tempfile.TemporaryDirectory() as temp_dir:
                cmd = [
                    "yt-dlp",
                    "--write-subs",
                    "--write-auto-subs",
                    "--skip-download",
                    "--sub-lang", "en,de",
                    "--output", "subs",
                    invidious_url
                ]
                
                try:
                    result = subprocess.run(cmd, cwd=temp_dir, check=True, capture_output=True)
                except subprocess.CalledProcessError as e:
                    continue  # Try next mirror
                except FileNotFoundError:
                    print("Error: yt-dlp not found.", file=sys.stderr)
                    sys.exit(1)
                
                temp_path = Path(temp_dir)
                vtt_files = list(temp_path.glob("*.vtt"))
                
                if vtt_files:
                    vtt_file = vtt_files[0]
                    content = vtt_file.read_text(encoding='utf-8')
                    clean_text = clean_vtt(content)
                    print(clean_text)
                    return
        
        print("Error: No Invidious mirror worked. Trying direct YouTube...", file=sys.stderr)
    
    # Fallback to direct YouTube
    with tempfile.TemporaryDirectory() as temp_dir:
        cmd = [
            "yt-dlp",
            "--write-subs",
            "--write-auto-subs",
            "--skip-download",
            "--sub-lang", "en,de",
            "--output", "subs",
            url
        ]
        
        try:
            subprocess.run(cmd, cwd=temp_dir, check=True, capture_output=True)
        except subprocess.CalledProcessError as e:
            print(f"Error: {e.stderr.decode()}", file=sys.stderr)
            sys.exit(1)
        
        temp_path = Path(temp_dir)
        vtt_files = list(temp_path.glob("*.vtt"))
        
        if not vtt_files:
            print("No subtitles found.", file=sys.stderr)
            sys.exit(1)
            
        vtt_file = vtt_files[0]
        content = vtt_file.read_text(encoding='utf-8')
        clean_text = clean_vtt(content)
        print(clean_text)

def main():
    parser = argparse.ArgumentParser(description="Fetch YouTube transcript via Invidious.")
    parser.add_argument("url", help="YouTube video URL")
    parser.add_argument("--no-invidious", action="store_true", help="Use direct YouTube instead of Invidious")
    args = parser.parse_args()
    
    get_transcript(args.url, use_invidious=not args.no_invidious)

if __name__ == "__main__":
    main()
