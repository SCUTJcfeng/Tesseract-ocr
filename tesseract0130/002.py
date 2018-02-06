from PIL import Image,ImageDraw
import pytesseract

def Binarization(img,threshold = 180):
    #threshold = 180
    table = list()
    for i in range(256):
        if i<threshold:
            table.append(0)
        else:
            table.append(1)
    return img.point(table,'1')

def GetPixel(image,x,y,threshold,number = 4):
    L = image.getpixel((x,y))
    #L像素值大于threshold，L即没有可能是噪点 L=1为白色 L=0为黑色
    if L > threshold:
        return None
    else:
        nearDots = 0
        #如果左上角像素值大于threshold（=1），L是噪点的可能性+1
        if (image.getpixel((x-1,y-1)) > threshold):
            nearDots += 1
        if (image.getpixel((x-1,y)) > threshold):
            nearDots += 1
        if (image.getpixel((x-1,y+1)) > threshold):
            nearDots += 1
        if (image.getpixel((x,y-1)) > threshold):
            nearDots += 1
        if (image.getpixel((x,y+1)) > threshold):
            nearDots += 1
        if (image.getpixel((x+1,y-1)) > threshold):
            nearDots += 1
        if (image.getpixel((x+1,y)) > threshold):
            nearDots += 1
        if (image.getpixel((+1,y+1)) > threshold):
            nearDots += 1
        if nearDots >= number:
            #如果是噪点，返回上面一个像素值
            #return image.getpixel((x,y-1))
            return 1
        else:
            return None

def ClearNoise(image,threshold,number = 4,times = 2):
    for i in range(0,times):
        for x in range(1,image.size[0] - 1):
            for y in range(1,image.size[1] - 1):
                color = GetPixel(image,x,y,threshold,number)
                if color != None:
                    ImageDraw.Draw(image).point((x,y),fill=color)

def main():
    for i in range(1,100):
        image = Image.open('ValidateCode/%d.jpg' % i)
        #灰度
        image = image.convert('L')
        #image.show()
        #二值化
        image = Binarization(image,175)
        #image.save(str(45) + '_Binarization.jpg')
        #image.show()
        ClearNoise(image,0.5,7,2)
        #image.show()
        code = pytesseract.image_to_string(image)
        if code != '':
            image.save(str(i) + '_' + str(code) + '_ClearNoise.jpg')
        else:
            image.save(str(i) + '_ClearNoise.jpg')
        print(str(i) + ' : ' +code)

if __name__ == '__main__':
    main()