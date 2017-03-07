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


USERNAMES = ['darkflame91','Wyox','paoper']

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

prev = {}
for name in USERNAMES:
	prev[name] = artist+album+track+"lol"


def buildImage(cover,flipper, boxes):
	black = Image.new('RGB',(width,height),(0,0,0))
	
	currentheight = height-PlayBox.boxheight
	for box in boxes:
		boximg = box.buildBox()
		black.paste(boximg,(int(width*0.99)-box.boxwidth,int(currentheight)))
		currentheight -= PlayBox.boxheight

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

def getFont(txt):
	fontsize = 1
	fontname = "Roboto.ttf"
	font = ImageFont.truetype(fontname, fontsize)
	while font.getsize(txt)[1] <= height*0.012:
	    fontsize += 1
	    font = ImageFont.truetype(fontname, fontsize)
	fontsize -= 1
	font = ImageFont.truetype(fontname, fontsize)
	return font


class PlayBox:

	boxcount = 0
	font = getFont("txt")
	fontheight = font.getsize("txt")[1]
	size = int(height*0.2)
	boxheight = size + fontheight*5

	def __init__(self, artist="Unknown Artist", album="Unknown Album", track="Unknown track", cover=Image.open("default.jpg"), username = "darkflame91"):
		#artist,album,track,cover = getLastPlayedDeets(username,artist,album,track,cover)
		self.artist = artist
		self.album = album
		self.track = track
		self.cover = cover
		self.cover.thumbnail((size,size))
		self.cover = self.cover.convert('LA')
		self.username = username
		self.boxwidth = 0
		PlayBox.boxcount += 1

	def buildBox(self):
		#artist,album,track,cover = getLastPlayedDeets(username,artist,album,track,cover)
		for text in [self.artist, self.album, self.track]:
			if self.boxwidth < PlayBox.font.getsize(text)[0]:
				self.boxwidth = PlayBox.font.getsize(text)[0]
		self.boxwidth = size if size > self.boxwidth else self.boxwidth
		box = Image.new('RGB',(self.boxwidth,size+PlayBox.fontheight*5),(0,0,0))
		box.paste(self.cover,(self.boxwidth-size,0))
		boxdraw = ImageDraw.Draw(box)

		lastsize = size

		for txt in [self.track,self.artist,self.album]:
			boxdraw.text((self.boxwidth - PlayBox.font.getsize(txt)[0], lastsize+PlayBox.fontheight*0.5), txt, font=PlayBox.font)
			lastsize += PlayBox.fontheight
		return box

	def getLastPlayedDeets(self,username,artist,album,track,cover):
		try:
			res = requests.get('http://ws.audioscrobbler.com/2.0/?method=user.getrecenttracks&user='+username+'&api_key=1d9f9f8b8e813cd77cc15f1978ca6c0f&format=json&limit=1')
			pres = json.loads(res.text)
		except Exception as err:
			print err
			sys.exit()
			time.sleep(timer)

		if pres['recenttracks']['track'][0]['artist']['#text'] != '':
			self.artist = pres['recenttracks']['track'][0]['artist']['#text']
		if pres['recenttracks']['track'][0]['album']['#text'] != '':
			self.album = pres['recenttracks']['track'][0]['album']['#text']
		if pres['recenttracks']['track'][0]['name'] != '':
			self.track = pres['recenttracks']['track'][0]['name']

		if pres['recenttracks']['track'][0]['image'][-1]['#text'] != '':
			self.cover = Image.open(requests.get(pres['recenttracks']['track'][0]['image'][-1]['#text'], stream=True).raw)
			self.cover.thumbnail((size,size))
			self.cover = self.cover.convert('LA')

		return artist,album,track,cover



while True:
	pres = ""
	artist = "Unknown Artist"
	album = "Unknown Album"
	track = "Unknown Track"
	cover = Image.open("default.jpg")
	samesong = 0

	boxes = []
	for name in USERNAMES:
		boxes.append(PlayBox(username=name))

	for box in boxes:
		box.getLastPlayedDeets(box.username,artist,album,track,cover)
		print box.username+" : "+box.track+" | "+box.artist+" | "+box.album
		if prev[box.username] == box.artist+box.album+box.track:
			samesong += 1

	if samesong == len(USERNAMES):
		print "Still playing the same songs!"
		time.sleep(10)
		continue

	flipper = buildImage(cover,flipper,boxes)
	
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

	for box in boxes:
		prev[box.username] = box.artist+box.album+box.track