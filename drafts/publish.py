import os
import sys
import shutil
import datetime
import re

def get_post_date(file_path):
    with open(file_path, 'r') as file:
        content = file.read()
        match = re.search(r'```{post} (\w+ \d{2}, \d{4})', content)
        if match:
            return datetime.datetime.strptime(match.group(1), '%b %d, %Y')
    return datetime.datetime.now()

for old_file in sys.argv[1:]:
    old_file_path = os.path.abspath(old_file)

    post_date = get_post_date(old_file_path)
    month = post_date.strftime('%b').lower()
    dir = os.path.join(os.path.dirname(__file__), f"../site/blog/{post_date.year}/{month}/{post_date.day}/")

    os.makedirs(dir, exist_ok=True)

    shutil.copy(old_file_path, dir)

    # Delete original
    print(f'Deleting {old_file_path}')
    os.remove(old_file_path)