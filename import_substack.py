import feedparser
import os
import subprocess
from datetime import datetime

# Function to convert HTML to Markdown using pandoc
def convert_html_to_md(html_content, output_file):
    with open('temp.html', 'w') as temp_html:
        temp_html.write(html_content)
    subprocess.run(['pandoc', '--from=html', '--to=markdown', '-o', output_file, 'temp.html'])
    os.remove('temp.html')

# Function to create metadata for ablog
def create_metadata(entry):
    date = datetime(*entry.published_parsed[:6])
    metadata = f"""```{{post}} {date.strftime('%b %d, %Y')}
:category: {entry.get('category', 'link-blog')}
```
"""
    return metadata

# Parse the RSS feed
rss_url = 'https://ericholscher.substack.com/feed'
feed = feedparser.parse(rss_url)

# Directory to save the converted posts
output_dir = 'drafts/substack_posts'
os.makedirs(output_dir, exist_ok=True)

# Process each entry in the feed
for entry in feed.entries:
    slug = entry.link.split('/')[-1]
    md_file = os.path.join(output_dir, f"{slug}.md")
    
    # Convert HTML to Markdown
    convert_html_to_md(entry.content[0].value, md_file)
    
    # Add metadata to the Markdown file
    with open(md_file, 'r+') as md:
        content = md.read()
        md.seek(0, 0)
        md.write(create_metadata(entry) + '\n' + content)
