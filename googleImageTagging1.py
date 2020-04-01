import io
import os
import operator
import webcolors
from PIL import Image
import sys
# -*- coding: utf-8 -*-
import webbrowser
from fuzzywuzzy import fuzz 
from fuzzywuzzy import process 

# Imports the Google Cloud client library
from google.cloud import vision
from google.cloud.vision import types

# Instantiates a client
client = vision.ImageAnnotatorClient()
print(sys.argv[1])

# The name of the image file to annotate
file_name = os.path.join(
    os.path.dirname(__file__),
    sys.argv[1])
image = Image.open(file_name)
image.save("/Users/selka/Downloads/Cwatch.jpg","JPEG", optimize=True, quality=50)

file_name=os.path.join(
    os.path.dirname(__file__),
    '/Users/selka/Downloads/Cwatch.jpg')

# Loads the image into memory
with io.open(file_name, 'rb') as image_file:
    content = image_file.read()

image = types.Image(content=content)
final_output = {}

# Performs label detection on the image file
response_logo = client.logo_detection(image=image)
response_webDetection = client.web_detection(image=image)
response_properties = client.image_properties(image=image)
response_object_detection = client.object_localization(image=image)
response_label = client.label_detection(image=image)
response_text = client.document_text_detection(image=image)
for webEn in response_webDetection.web_detection.web_entities:
    if webEn.score >= 0.4:
        final_output[webEn.description] = webEn.score
    else:
        break

for label in response_label.label_annotations:
    if label.score >= 0.4:
        final_output[label.description] = label.score
    else:
        break

for obj in response_object_detection.localized_object_annotations:
    if obj.score >= 0.4:
        final_output[obj.name] = obj.score
    else:
        break

for logo in response_logo.logo_annotations:
    if logo.score >= 0.4:
        final_output[logo.description] = logo.score
    else:
        break
max_str = ""
for tex in response_text.text_annotations:
     if len(tex.description) > len(max_str):
         max_str = tex.description
fin_list = []
text_list = max_str.split('\n')
for tex in text_list:
    if tex.isdigit():
        continue
    else:
        fin_list.append(tex)
#print(fin_list)
tags = []

for key, value in sorted(final_output.items(), key=lambda item: item[1],reverse=True):
    print("%s: %s" % (key, value))
    tags.append(key)

def closest_colour(requested_colour):
    min_colours = {}
    for key, name in webcolors.css3_hex_to_names.items():
        r_c, g_c, b_c = webcolors.hex_to_rgb(key)
        rd = (r_c - requested_colour[0]) ** 2
        gd = (g_c - requested_colour[1]) ** 2
        bd = (b_c - requested_colour[2]) ** 2
        min_colours[(rd + gd + bd)] = name
    return min_colours[min(min_colours.keys())]

def get_colour_name(requested_colour):
    try:
        closest_name = actual_name = webcolors.rgb_to_name(requested_colour)
    except ValueError:
        closest_name = closest_colour(requested_colour)
        actual_name = None
    return actual_name, closest_name

redCol=int(response_properties.image_properties_annotation.dominant_colors.colors[0].color.red)
blueCol=int(response_properties.image_properties_annotation.dominant_colors.colors[0].color.blue)
greenCol=int(response_properties.image_properties_annotation.dominant_colors.colors[0].color.green)

requested_colour = (redCol,blueCol,greenCol)
actual_name, closest_name = get_colour_name(requested_colour)
if actual_name is None:
    actual_name = closest_name

tagNcolour = {'tag':tags,'col':actual_name,'text':fin_list}
#labels = response.label_annotations

#done print(response_logo)
#done print(response_webDetection)
#print(response_properties)
#done print(response_object_detection)
#done  print(response_label)
#print(final_output)
#print(response_text)
print(tagNcolour)






categoryFilepath = 'category.txt'
brandsFilepath = 'brands.txt'
category = []
brands = []

with open(categoryFilepath) as fp:
   line = fp.readline()
   while line:
       category.append(str(line).lower())
       line = fp.readline()
#print(category)
with open(brandsFilepath) as fp:
   line = fp.readline()
   while line:
       brands.append(str(line).lower())
       line = fp.readline()

catStr = ''
brandStr = ''
colStr = ''
tagList = tags
textList = fin_list
colList = actual_name
catFlag = False
brandFlag = False
maxCatRatio = 0
maxBrandRatio = 0

d = tagNcolour
def findMatchRatio(hayStr, valList):
   maxRatio = 0
   for i in valList:
      tempRatio = fuzz.ratio(str(hayStr).lower(), str(i))
      if tempRatio > maxRatio:
         maxRatio = tempRatio
   return maxRatio


for i in textList:
   tempCatRatio = findMatchRatio(i, category)
   print(str(tempCatRatio) + '   ' + str(i))
   if tempCatRatio > maxCatRatio:
      catStr = str(i)
      maxCatRatio = tempCatRatio

   tempBrandRatio = findMatchRatio(i, brands)
   if tempBrandRatio > maxBrandRatio:
      brandStr = str(i)
      maxBrandRatio = tempBrandRatio


for i in tagList:
   tempCatRatio = findMatchRatio(i, category)
   if tempCatRatio > maxCatRatio:
      catStr = str(i)
      maxCatRatio = tempCatRatio

   tempBrandRatio = findMatchRatio(i, brands)
   if tempBrandRatio > maxBrandRatio:
      brandStr = str(i)
      maxBrandRatio = tempBrandRatio


colStr = str(colList)

searchStr = str(brandStr + ' ' + catStr).lower()

print(searchStr)

url = "https://www.amazon.in/s?k="+(str(searchStr))
webbrowser.open_new(url)
