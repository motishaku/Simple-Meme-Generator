from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw
import base64
from io import BytesIO


def draw_text(msg, pos, draw, img):
    base_font_size = 56
    lines = []

    font = ImageFont.truetype("impact.ttf", base_font_size)
    w, h = draw.textsize(msg, font)

    imgWidthWithPadding = img.width * 0.99

    lineCount = 1
    if(w > imgWidthWithPadding):
        lineCount = int(round((w / imgWidthWithPadding) + 1))

    if lineCount > 2:
        while 1:
            base_font_size -= 2
            font = ImageFont.truetype("impact.ttf", base_font_size)
            w, h = draw.textsize(msg, font)
            lineCount = int(round((w / imgWidthWithPadding) + 1))
            if lineCount < 3 or base_font_size < 10:
                break
    lastCut = 0
    isLast = False
    for i in range(0, lineCount):
        if lastCut == 0:
            cut = (len(msg) / lineCount) * i
        else:
            cut = lastCut

        if i < lineCount-1:
            nextCut = (len(msg) / lineCount) * (i+1)
        else:
            nextCut = len(msg)
            isLast = True

        if nextCut == len(msg) or msg[int(nextCut)] == " ":
            pass
        else:
            try:
                while msg[int(nextCut)] != " ":
                    nextCut += 1
            except (TypeError, IndexError) as e:
                pass

        line = msg[int(cut):int(nextCut)].strip()

        w, h = draw.textsize(line, font)
        if not isLast and w > imgWidthWithPadding:
            nextCut -= 1
            try:
                while msg[nextCut] != " ":
                    nextCut -= 1
            except (TypeError, IndexError) as e:
                pass

        lastCut = nextCut
        lines.append(msg[int(cut):int(nextCut)].strip())

    lastY = -h
    if pos == "bottom":
        lastY = img.height - h * (lineCount+1) - 10

    for i in range(0, lineCount):
        w, h = draw.textsize(lines[i], font)
        textX = img.width/2 - w/2

        textY = lastY + h
        try:
            draw.text((textX-2, textY-2), lines[i], (0, 0, 0), font=font)
            draw.text((textX+2, textY-2), lines[i], (0, 0, 0), font=font)
            draw.text((textX+2, textY+2), lines[i], (0, 0, 0), font=font)
            draw.text((textX-2, textY+2), lines[i], (0, 0, 0), font=font)
            draw.text((textX, textY), lines[i], (255, 255, 255), font=font)
        except:
            pass
        lastY = textY

    return

def make_meme(top, bottom, image_name):
    img = Image.open(image_name)
    draw = ImageDraw.Draw(img)

    draw_text(top.upper(), "top", draw, img)
    draw_text(bottom.upper(), "bottom", draw, img)

    buffer = BytesIO()
    try:
        img.save(buffer, format="JPEG")
    except OSError:
        img = img.convert('RGB')
        img.save(buffer, format="JPEG")
    img_str = base64.b64encode(buffer.getvalue())
    return img_str
