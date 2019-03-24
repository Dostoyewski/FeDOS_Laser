from PIL import Image
im = Image.open("bukva-a.jpg")
#bg = Image.new("RGB", im.size, (255,255,255))
#bg.paste(im,im)
bg = im.resize((110, 110))
bg = bg.convert('1')
bg.save("out.png")
