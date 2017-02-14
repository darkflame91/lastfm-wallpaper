import sys
import json
import time
import subprocess
import os
import platform
import signal
try:
	import Tkinter
except:
	print "Get the python Tkinter library!"
	sys.exit()
try:
	from PIL import Image, ImageFilter, ImageEnhance, ImageFont, ImageDraw
except:
	print "Get the python Pillow library!\nRun: pip install pillow"
	sys.exit()
try:
	import requests
except:
	print "Get the python Requests library!\nRun: pip install requests"
	sys.exit()


USERNAME = 'darkflame91'

timer = 10

temptk = Tkinter.Tk()
width = temptk.winfo_screenwidth()
height = temptk.winfo_screenheight()
size = int(height*0.2)
flipper = "2.jpg"
pres = ""
artist = "Unknown Artist"
album = "Unknown Album"
track = "Unknown Track"
cover = Image.open("default.jpg")
black = Image.new('RGB',(width,height),(0,0,0))
prevartist,prevalbum,prevtrack = artist,album,track


def getFont(txt):
	fontsize = 1
	fontname = "Roboto.ttf"
	font = ImageFont.truetype(fontname, fontsize)
	while font.getsize(txt)[1] <= height*0.015:
	    fontsize += 1
	    font = ImageFont.truetype(fontname, fontsize)
	fontsize -= 1
	font = ImageFont.truetype(fontname, fontsize)
	return font

def getLastPlayedDeets(artist,album,track,cover):
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
	return artist,album,track,cover

def buildImage(cover,flipper):
	black = Image.new('RGB',(width,height),(0,0,0))
	cover.thumbnail((size,size))
	cover = cover.convert('LA')
	black.paste(cover,(int(width*0.99)-size,height-(font.getsize("txt")[1]*5)-size))
	draw = ImageDraw.Draw(black)
	lastsize = height - font.getsize("txt")[1]*5

	for txt in [track,artist,album]:
		draw.text((int(width*0.99) - font.getsize(txt)[0], lastsize+font.getsize("txt")[1]*0.5), txt, font=font)
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
	return flipper

def signal_handler(signal, frame):
        print('\nStopping the lastfm script')
        sys.exit(0)


font = getFont("txt")
while True:
	pres = ""
	artist = "Unknown Artist"
	album = "Unknown Album"
	track = "Unknown Track"
	cover = Image.open("default.jpg")
	artist,album,track,cover = getLastPlayedDeets(artist,album,track,cover)
	if (prevartist,prevalbum,prevtrack) == (artist,album,track):
		time.sleep(timer)
		continue
	flipper = buildImage(cover,flipper)
	signal.signal(signal.SIGINT, signal_handler)
	if platform.system() == "Linux":
		wallcommand = "gsettings set org.gnome.desktop.background picture-uri file://"+os.environ.get('PWD')+"/"+flipper
		print wallcommand
		setwallout = subprocess.check_output(wallcommand.split())
		wallcommand = 'gsettings set org.gnome.desktop.background picture-options "spanned"'
		print wallcommand
		setwallout = subprocess.check_output(wallcommand.split())
		print setwallout
	elif platform.system() == "Darwin":
		setwallout = subprocess.check_output(["sh","apple.sh",os.environ.get('PWD')+"/",flipper])
		#print setwallout
	else:
		print "Your OS is not supported. Sorry."
	time.sleep(timer)
	prevartist,prevalbum,prevtrack = artist,album,track
