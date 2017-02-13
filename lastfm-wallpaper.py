from PIL import Image, ImageFilter, ImageEnhance, ImageFont, ImageDraw

size = 200
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

album = Image.open("Master_Puppets.jpg")
black = Image.new('RGB',(1920,1080),(0,0,0))
print album

album.thumbnail((size,size))
#album = ImageEnhance.Sharpness(album).enhance(2.0)
#album = album.filter(ImageFilter.SMOOTH_MORE)
#album = album.filter(ImageFilter.SHARPEN)
# album = album.filter(ImageFilter.SMOOTH_MORE)
# album = album.filter(ImageFilter.SHARPEN)
# album = album.filter(ImageFilter.SMOOTH_MORE)
# album = album.filter(ImageFilter.SHARPEN)
# album = album.filter(ImageFilter.SMOOTH_MORE)
# album = album.filter(ImageFilter.SHARPEN)
#album = album.filter(ImageFilter.FIND_EDGES)
album = album.convert('LA')
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


black.paste(album,(1700,810))
draw = ImageDraw.Draw(black)
lastsize = 1010

for txt in ["Track Name","Artist Name","Album Name"]:
	font = getFont(txt)
	draw.text((1700, lastsize+8), txt, font=font)
	lastsize += font.getsize(txt)[1]

black.show()