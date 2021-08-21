import cv2 as cv
import os
import numpy as np
def segment(img):
    num1=img[:,26:46,:]
    num2=img[:,47:67,:]
    num3=img[:,68:88,:]
    num4=img[:,88:108,:]
    return num1,num2,num3,num4
def preprocess(img):
    img=img.astype(np.float32)
    img = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
    img /= 255.0
    for i in range(32):
        for j in range(20):
            if img[i][j] < 0.5:
                img[i][j] = 0
            else:
                img[i][j] = 1
    return img
def compare(img,i,j):
    num=cv.imread('./num'+str(i)+'/'+str(j)+'.png')
    num=preprocess(num)
    sub=abs(img-num)
    return sum(sum(sub))

def detect(img,i):
    img=preprocess(img)
    ret=0
    min=9999
    if i!=1:
        for j in range(10):
            if min>compare(img,i,j):
                ret=j
                min=compare(img,i,j)
    else:
        for j in range(1,10):
            if min>compare(img,i,j):
                ret=j
                min=compare(img,i,j)
    return ret
def recognize(img):#输入验证码图片120×32，输出4位验证码
    validatecode=segment(img)
    ret=0
    num1=detect(validatecode[0],1)
    num2=detect(validatecode[1],2)
    num3=detect(validatecode[2],3)
    num4=detect(validatecode[3],4)
    return int(str(num1)+str(num2)+str(num3)+str(num4))
    
if __name__ == '__main__':
    # test
    root='./img/'
    paths=os.listdir(root)
    for p in paths:
        img=cv.imread(root+p)
        num1=segment(img)[0]
        print(detect(num1,1))
        cv.imshow('n',num1)
        cv.waitKey(0)
