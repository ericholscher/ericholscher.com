import os
import sys
import shutil
import datetime

now = datetime.datetime.now()
month = now.strftime('%b').lower()
dir = "../site/blog/%s/%s/%s/" % (now.year, month, now.day)

os.makedirs(dir, exist_ok=True)

old_file = sys.argv[1]

shutil.copy(old_file, dir)

# Delete original
print(f'Deleting {old_file}')
os.remove(old_file)