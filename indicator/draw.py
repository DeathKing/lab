from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageColor

import random

# 240 x 60:
width, height = 640, 480
image = Image.new('RGB', (width, height), (255, 255, 255))
# 创建Font对象:
font = ImageFont.truetype('./Arial Black.ttf', 240)
# font = ImageFont.load_default(36)
# 创建Draw对象:
draw = ImageDraw.Draw(image)
# 填充每个像素:
# for x in range(width):
#     for y in range(height):
#         draw.point((x, y), fill=rndColor())
# 输出文字:
#for t in range(4):
draw.text((20, 10), 'A', font=font, fill=ImageColor.getrgb('red'))
# 模糊:
#image = image.filter(ImageFilter.BLUR)
image.save('code.jpg', 'jpeg')
