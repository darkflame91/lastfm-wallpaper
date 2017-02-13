import sys
import json
import time
import subprocess
import os
import platform
import sqlite3
try:
	from PIL import Image, ImageFilter, ImageEnhance, ImageFont, ImageDraw
except:
	print "Get the python Pillow library!"
	sys.exit()
try:
	import requests
except:
	print "Get the python Requests library!"
	sys.exit()


USERNAME = 'darkflame91'

timer = 10
size = 200
flipper = "2.jpg"

def getFont(txt):
	fontsize = 1
	fontname = "Roboto.ttf"
	font = ImageFont.truetype(fontname, fontsize)
	while font.getsize(txt)[0] < size and font.getsize(txt)[1] < 15:
	    fontsize += 1
	    font = ImageFont.truetype(fontname, fontsize)
	fontsize -= 1
	font = ImageFont.truetype(fontname, fontsize)
	return font



pres = ""
artist = "Unknown Artist"
album = "Unknown Album"
track = "Unknown Track"
cover = Image.open("default.jpg")
try:
	res = requests.get('http://ws.audioscrobbler.com/2.0/?method=user.getrecenttracks&user='+USERNAME+'&api_key=1d9f9f8b8e813cd77cc15f1978ca6c0f&format=json&limit=1')
	pres = json.loads(res.text)
except Exception as err:
	print err
	sys.exit()
	time.sleep(timer)

if pres['recenttracks']['track'][0]['artist']['#text'] != '':
	artist = pres['recenttracks']['track'][0]['artist']['#text']
if pres['recenttracks']['track'][0]['album']['#text'] != '':
	album = pres['recenttracks']['track'][0]['album']['#text']
if pres['recenttracks']['track'][0]['name'] != '':
	track = pres['recenttracks']['track'][0]['name']

if pres['recenttracks']['track'][0]['image'][-1]['#text'] != '':
	cover = Image.open(requests.get(pres['recenttracks']['track'][0]['image'][-1]['#text'], stream=True).raw)





black = Image.new('RGB',(1920,1080),(0,0,0))

cover.thumbnail((size,size))
#cover = ImageEnhance.Sharpness(cover).enhance(2.0)
#cover = cover.filter(ImageFilter.SMOOTH_MORE)
#cover = cover.filter(ImageFilter.SHARPEN)
# cover = cover.filter(ImageFilter.SMOOTH_MORE)
# cover = cover.filter(ImageFilter.SHARPEN)
# cover = cover.filter(ImageFilter.SMOOTH_MORE)
# cover = cover.filter(ImageFilter.SHARPEN)
# cover = cover.filter(ImageFilter.SMOOTH_MORE)
# cover = cover.filter(ImageFilter.SHARPEN)
#cover = cover.filter(ImageFilter.FIND_EDGES)
cover = cover.convert('LA')
# for i in range(300):
# 	for j in range(300):
# 		temp = px[i,j]
# 		counter = 0
# 		for el in temp:
# 			counter += el
# 		if counter/3 > 50:
# 			px[i,j] = (255,255,255)
# 		else:
# 			px[i,j] = (0,0,0)

# for i in range(300):
# 	for j in range(300):
# 		if px[i,j] > 100:
# 			px[i,j] = 255
# 		else:
# 			px[i,j] = 0


black.paste(cover,(1700,810))
draw = ImageDraw.Draw(black)
lastsize = 1010

for txt in [track,artist,album]:
	font = getFont(txt)
	draw.text((1700, lastsize+8), txt, font=font)
	lastsize += font.getsize(txt)[1]

#black.show()
if flipper == "1.jpg":
	flipper = "2.jpg"
else:
	flipper = "1.jpg"
try:
	os.remove(flipper)
except:
	print "File's ah'ready gon sah!"
black.save(flipper)

if platform.system() == "Linux":
	wallcommand = "gsettings set org.gnome.desktop.background draw-background false"
	setwallout = subprocess.check_output(wallcommand.split())
	wallcommand = "gsettings set org.gnome.desktop.background picture-uri file://"+os.environ.get('PWD')+"/"+flipper
	setwallout = subprocess.check_output(wallcommand.split())
	wallcommand = "gsettings set org.gnome.desktop.background draw-background true"
	setwallout = subprocess.check_output(wallcommand.split())
	print setwallout
elif platform.system() == "Darwin":
	setwallout = subprocess.check_output(["sh","apple.sh",os.environ.get('PWD')+"/",flipper])
	print setwallout
