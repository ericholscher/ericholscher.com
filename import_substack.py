"""
Usage:
    python import_substack.py [title_filter] && python drafts/publish.py drafts/substack_posts/*

Arguments:
    title_filter (optional) - A substring to filter posts by title.
"""

import feedparser
import os
import subprocess
import requests
import sys
from datetime import datetime, timezone, timedelta
from bs4 import BeautifulSoup

# Function to convert HTML to Markdown using pandoc
def convert_html_to_md(html_content, output_file):
    with open('temp.html', 'w') as temp_html:
        temp_html.write(html_content)
    subprocess.run(['pandoc', '--from=html', '--to=markdown', '-o', output_file, 'temp.html'])
    os.remove('temp.html')

# Function to create metadata for ablog
def create_metadata(entry):
    date = datetime(*entry.published_parsed[:6], tzinfo=timezone.utc).astimezone(timezone(timedelta(hours=-8)))
    metadata = f"""```{{post}} {date.strftime('%b %d, %Y')}
:category: {entry.get('category', 'link-blog')}
```
"""
    return metadata

# Function to download media files and update links
def download_media_and_update_links(html_content, media_dir, slug, site_dir):
    soup = BeautifulSoup(html_content, 'html.parser')
    for i, img in enumerate(soup.find_all('img')):
        img_url = img['src']
        img_ext = os.path.splitext(img_url)[1]
        img_name = f"{slug}_image_{i+1}{img_ext}"
        img_path = os.path.join(media_dir, img_name)
        
        # Download the image
        response = requests.get(img_url)
        with open(img_path, 'wb') as img_file:
            img_file.write(response.content)
        
        # Update the image link
        img['src'] = '/' + os.path.relpath(img_path, start=site_dir)
        
        # Remove class names and size attributes
        if 'class' in img.attrs:
            del img.attrs['class']
        if 'height' in img.attrs:
            del img.attrs['height']
        if 'width' in img.attrs:
            del img.attrs['width']
    
    # Remove div around figure
    for div in soup.find_all('div', class_='captioned-image-container'):
        div.unwrap()
    
    return str(soup)

# Parse the RSS feed
rss_url = f'https://ericholscher.substack.com/feed?name={datetime.now().strftime("%Y%m%d%H%M%S")}'
feed = feedparser.parse(rss_url)

# Directory to save the converted posts
output_dir = os.path.join(os.path.dirname(__file__), 'drafts/substack_posts')
os.makedirs(output_dir, exist_ok=True)

# Directory to save the media files
site_dir = os.path.join(os.path.dirname(__file__), 'site')
media_dir = os.path.join(site_dir, '_static/img/substack')
os.makedirs(media_dir, exist_ok=True)

# Get the title filter from command-line arguments
title_filter = sys.argv[1] if len(sys.argv) > 1 else None

# Process each entry in the feed
for entry in feed.entries:
    if title_filter and title_filter.lower() not in entry.title.lower():
        continue
    
    slug = entry.link.split('/')[-1]
    md_file = os.path.join(output_dir, f"{slug}.md")
    
    # Download media files and update links
    updated_html_content = download_media_and_update_links(entry.content[0].value, media_dir, slug, site_dir)
    
    # Convert HTML to Markdown
    convert_html_to_md(updated_html_content, md_file)
    
    # Add metadata and title to the Markdown file
    with open(md_file, 'r+') as md:
        content = md.read()
        md.seek(0, 0)
        md.write(create_metadata(entry) + '\n' + f"# {entry.title}\n\n" + content)
    
    # Output the name of the post processed
    print(f"Processed post: {entry.title}")
