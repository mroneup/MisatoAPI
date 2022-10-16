from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw
def makememe(image, top, bottom,file):
    img = Image.open(image)
    draw = ImageDraw.Draw(img)
    font = ImageFont.truetype("impact.ttf", 42)

    def drawTextWithOutline(text, x, y):
        draw.text((x-2, y-2), text, (0, 0, 0), font=font)
        draw.text((x+2, y-2), text, (0, 0, 0), font=font)
        draw.text((x+2, y+2), text, (0, 0, 0), font=font)
        draw.text((x-2, y+2), text, (0, 0, 0), font=font)
        draw.text((x, y), text, (255, 255, 255), font=font)
        return

    def drawText(text, pos):
        text = text.upper()
        w, h = draw.textsize(text, font)  # measure the size the text will take

        lineCount = 1
        if w > img.width:
            lineCount = int(round((w / img.width) + 1))

        #print("lineCount: {}".format(lineCount))

        lines = []
        if lineCount > 1:

            lastCut = 0
            isLast = False
            for i in range(0, lineCount):
                if lastCut == 0:
                    cut = (len(text) / lineCount) * i
                else:
                    cut = lastCut

                if i < lineCount-1:
                    nextCut = (len(text) / lineCount) * (i+1)
                else:
                    nextCut = len(text)
                    isLast = True

                #print("cut: {} -> {}".format(cut, nextCut))

                # make sure we don't cut words in half
                if nextCut == int(len(text)) or text[int(nextCut)] == " ":
                    #print("may cut")
                    pass
                else:
                    #print("may not cut")
                    while text[int(nextCut)] != " ":
                        nextCut += 1
                    #print("new cut: {}".format(nextCut))

                line = text[int(cut):int(nextCut)].strip()

                # is line still fitting ?
                w, h = draw.textsize(line, font)
                if not isLast and w > img.width:
                    #print("overshot")
                    nextCut -= 1
                    while text[nextCut] != " ":
                        nextCut -= 1
                    #print("new cut: {}".format(nextCut))

                lastCut = nextCut
                lines.append(text[int(cut):int(nextCut)].strip())

        else:
            lines.append(text)

        #print(lines)

        lastY = -h
        if pos == "bottom":
            lastY = img.height - h * (lineCount+1) - 10

        for i in range(0, lineCount):
            w, h = draw.textsize(lines[i], font)
            x = img.width/2 - w/2
            y = lastY + h
            drawTextWithOutline(lines[i], x, y)
            lastY = y

    drawText(top, "top")
    drawText(bottom, "bottom")

    img.save(file)
