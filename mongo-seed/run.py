from PIL import Image
from PIL.ExifTags import TAGS
import os
import base64
import json
import time

directory = "./images/"
j_ = {}

for filename in os.listdir(directory):
    if filename.endswith(".jpg") or filename.endswith(".png"):
        imageName = os.path.join(directory, filename)
        image = Image.open(imageName)
        encoded_string = str(base64.b64encode(open(imageName, 'rb').read()))
        exif = {
            TAGS[k]: str(v)
            for k, v in image.getexif().items()
            if k in TAGS
        }
        exif['file_encoded'] = encoded_string
        j_[filename] = exif

j = json.dumps(j_)
with open('./output/population_' + str(time.time()) + '.json', 'w') as f:
    f.write(j)
    f.close
