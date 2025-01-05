import os
import sys
import shutil
import datetime

now = datetime.datetime.now()
month = now.strftime('%b').lower()
dir = os.path.join(os.path.dirname(__file__), f"../site/blog/{now.year}/{month}/{now.day}/")

os.makedirs(dir, exist_ok=True)

old_file = sys.argv[1]
old_file_path = os.path.abspath(old_file)

shutil.copy(old_file_path, dir)

# Delete original
print(f'Deleting {old_file_path}')
os.remove(old_file_path)