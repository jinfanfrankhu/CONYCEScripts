import os
import re

# Set this to the path where your files are 
directory = r"C:\Users\jinfa\Desktop\CONYCE\Force Aligned Textgrids"

pattern = re.compile(r'^conyce_aligned_(.+)\.TextGrid$')

for filename in os.listdir(directory):
    match = pattern.match(filename)
    if match:
        id_part = match.group(1)
        new_filename = f'conyce_{id_part}.TextGrid'
        src = os.path.join(directory, filename)
        dst = os.path.join(directory, new_filename)
        os.rename(src, dst)
        print(f'Renamed: {filename} -> {new_filename}')
