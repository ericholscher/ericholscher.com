```{post} Jan 05, 2025
:category: link-blog
```

# AI makes computers do what I want them to do

I am trying to do more writing, and while I love my git-based blog, I
also wanted a nice way to author content on my phone. Using Substack for
that has been great, but I wanted to keep the articles in sync between
the two posts.

I was able to get a substack RSS feed importer working for my blog in a
couple easy steps:

I started by VS Code and GitHub Copilot Edits, and loaded some blog
files into the context:

![](/_static/img/substack/ai-makes-computers-do-what-i-want_image_1.png)

Then I used the prompt:

> Make a script to import an RSS feed from substack that has HTML posts
> and then convert them into Markdown with the metadata for ablog used,
> converted with pandoc.

The big things I wanted the context to know were:

-   The metadata syntax format for my blog posts, which was shown in the
    \`money and identity\` post.

-   The file to write the script in.

-   The configuration for my Sphinx project.

It initially only wrote the script, which added some dependencies, so I
then asked it to add the dependencies as well:

![](/_static/img/substack/ai-makes-computers-do-what-i-want_image_2.png)

It turns out I didn't need a pandoc dependency in my requirements, since
the script calls out to the pandoc executable, so I removed that.

Then all I had to do was paste the RSS feed of my blog, and I have
automatic syncing of my Substack posts to my blog!

The main thing it doesn't sync is tags, which aren't in the RSS feed for
some reason.

### Full Script

I had to do another couple rounds of edits to get images working for
this post, and the final script is:

    import feedparser
    import os
    import subprocess
    import requests
    from datetime import datetime
    from bs4 import BeautifulSoup

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
    rss_url = 'https://ericholscher.substack.com/feed'
    feed = feedparser.parse(rss_url)

    # Directory to save the converted posts
    output_dir = os.path.join(os.path.dirname(__file__), 'drafts/substack_posts')
    os.makedirs(output_dir, exist_ok=True)

    # Directory to save the media files
    site_dir = os.path.join(os.path.dirname(__file__), 'site')
    media_dir = os.path.join(site_dir, '_static/img/substack')
    os.makedirs(media_dir, exist_ok=True)

    # Process each entry in the feed
    for entry in feed.entries:
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
