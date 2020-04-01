# -*- coding: utf-8 -*-
import webbrowser
import googleImageTagging
from fuzzywuzzy import fuzz 
from fuzzywuzzy import process 

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
tagList = {}
textList = {}
colList = {}
catFlag = False
brandFlag = False
maxCatRatio = 0
maxBrandRatio = 0

d = googleImageTagging.tagNcolour 
print("output print kr")
print(d)
def findMatchRatio(hayStr, valList):
   maxRatio = 0
   for i in valList:
      tempRatio = fuzz.ratio(str(hayStr).lower(), str(i))
      if tempRatio > maxRatio:
         maxRatio = tempRatio
   return maxRatio


for key, valList in d.iteritems():
   if key == 'tag':
      tagList = valList
   elif key == 'text':
      textList = valList
   else:
      colList = valList         


for i in textList:
   tempCatRatio = findMatchRatio(i, category)
   #print(str(tempCatRatio) + '   ' + str(i))
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

searchStr = str(brandStr + ' ' + catStr + ' ' + colStr)

print(searchStr)

url = "https://www.amazon.in/s?k="+(str(searchStr))
webbrowser.open_new(url)






