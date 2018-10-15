# -*- coding: utf-8 -*- 
'''
颜色特征识别测试代码
'''
import numpy as np
import cv2
from color_feature import color_block_finder,draw_color_block_rect,color_block_coordinate

import serial
import serial.tools.list_ports


def test_color_block_finder_01(serialFd,lowerb = (0, 0, 70),upperb = (180, 30, 255)):
    '''
    色块识别测试样例1 从图片中读取并且识别
    '''
    # 图片路径
    img_path = "test.png"
    # # 颜色阈值下界(HSV) lower boudnary
    # lowerb = (0, 0, 221) 
    # # 颜色阈值上界(HSV) upper boundary
    # upperb = (180, 30, 255)

    # 读入素材图片 BGR
    img = cv2.imread(img_path, cv2.IMREAD_COLOR)
    img = cv2.resize(img,(1366,768),interpolation=cv2.INTER_CUBIC)

    # 检查图片是否读取成功
    if img is None:
        print("Error: 请检查图片文件路径")
        exit(1)

    # 识别色块 获取矩形区域数组
    rects = color_block_finder(img, lowerb, upperb)
    # 绘制色块的矩形区域
    canvas = draw_color_block_rect(img, rects)
    # 在HighGUI窗口 展示最终结果
    cv2.namedWindow('result', flags=cv2.WINDOW_NORMAL | cv2.WINDOW_FREERATIO)
    cv2.imshow('result', canvas)

    coordinates = color_block_coordinate(rects)
    serialFd.write("x:"+str(coordinates[0])+",y:"+str(coordinates[1]))

    # 等待任意按键按下
    cv2.waitKey(0)
    # 关闭其他窗口
    cv2.destroyAllWindows()

def test_color_block_finder_02(serialFd,lowerb = (0, 0, 170),upperb = (180, 30, 255)):
    '''
    色块识别测试样例2 从视频流中读取并且识别
    '''
    # # 颜色阈值下界(HSV) lower boudnary
    # lowerb = (0, 0, 71) 
    # # 颜色阈值上界(HSV) upper boundary
    # upperb = (180, 61, 255)
    # 读入视频流
    cap = cv2.VideoCapture(0)
    # 色块识别结果展示
    cv2.namedWindow('result', flags=cv2.WINDOW_NORMAL | cv2.WINDOW_FREERATIO)

    while(True):
        # 逐帧获取画面
        # ret ？ 画面是否获取成功
        ret, frame = cap.read()
        
        if ret:
            frame = cv2.flip(frame, 1)
            img = cv2.resize(frame,(1366,768),interpolation=cv2.INTER_CUBIC)
            # 识别色块 获取矩形区域数组
            # 同时设定最小高度还有宽度，过滤噪声
            rects = color_block_finder(img, lowerb, upperb,min_w=0,min_h=0)
            # 绘制色块的矩形区域
            canvas = draw_color_block_rect(img, rects)
            # 在HighGUI窗口 展示最终结果 更新画面
            cv2.imshow('result', canvas)

            coordinates = color_block_coordinate(rects)
            serialFd.write("x:"+str(coordinates[0])+",y:"+str(coordinates[1]))

        else:
            print("视频读取完毕或者视频路径异常")
            break

        # 这里做一下适当的延迟，每帧延时0.1s钟
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # 释放资源
    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":

    plists = list(serial.tools.list_ports.comports())
    if len(plists) <= 0:
        print("the serial port can't find")
    else:
        if len(plists)==1 and list(plists[0])[0]=="COM1":
            print("the serial port can't find")
        else:
            print("the serial ports available are follows:")
            compose = ''
            for plist in plists:
                port = list(plist)
                serialName = port[0]
                if serialName!="COM1":
                    print(serialName)
                    compose += serialName.replace("COM","")+" "
            aflag = False
            while aflag==False:
                aport = raw_input("please type the serial number like "+compose+":")
                try:
                    serialFd = serial.Serial("COM"+aport, 115200, timeout=60)
                    if serialFd:
                        print("check which[%s] port was really used>" % serialFd.name)
                        aflag=True
                except Exception as e:
                    print("there is something wrong with your input,please check and try it again")
            # while aflag==True:
            # 	hsv = raw_input("please type the color hsv like '0,0,221,180,30,255':")
            # 	try:
            # 		hsv = hsv.split(',')
            # 		print(hsv)
            # 		l_hsv = (int(hsv[0]),int(hsv[1]),int(hsv[2]))
            # 		h_hsv = (int(hsv[3]),int(hsv[4]),int(hsv[5]))
            # 		print(h_hsv,l_hsv)
            # 	except Exception as e:
            # 		print("there is something wrong with your input,please check and try it again")
            # 	if h_hsv and l_hsv:
            # 		aflag=False
            		
            # 测试图片色块识别
            # test_color_block_finder_01(serialFd,l_hsv,h_hsv)
            # 测试视频流色块识别
            test_color_block_finder_02(serialFd)
    # 0,0,62,180,30,255