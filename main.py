from numpy.lib.twodim_base import triu_indices_from
import win32gui
import re, cv2
import numpy as np
from PIL import ImageGrab
import matplotlib.pyplot as plt
import pyautogui, time
import matplotlib
from operator import itemgetter




# img_rgb = cv2.imread('./data/mario.png')
# img_gray = cv2.cvtColor(img_rgb, cv2.COLOR_BGR2GRAY)
# template = cv2.imread('./data/coin.png',0)
# w, h = template.shape[::-1]
# res = cv2.matchTemplate(img_gray,template,cv2.TM_CCOEFF_NORMED)
# threshold = 0.8
# loc = np.where(res >= threshold)
# for pt in zip(*loc[::-1]):
#     cv2.rectangle(img_rgb, pt, (pt[0] + w, pt[1] + h), (0,0,255), 2)



def process_img(img_rgb, template):
    img_gray = cv2.cvtColor(img_rgb, cv2.COLOR_BGR2GRAY)

    w, h = template.shape[::-1]
    min_ = [0, 0]
    arr = []
    res = cv2.matchTemplate(img_gray,template,cv2.TM_CCOEFF_NORMED)
    threshold = 0.9
    loc = np.where( res >= threshold)
    for pt in zip(*loc[::-1]):
        arr.append(pt)
    arr.sort(key=itemgetter(1))
    try:
        min_ = arr[-1]
    except:
        pass
    # print(arr)
    try:
        cv2.rectangle(img_rgb, min_, (min_[0] + w, min_[1] + h), (0,0,255), 2)
        pos = (min_[0]+min_[0]+w)/2
        print(min_[1])
        # if min_[1] < 60:
        #     return -1
        # if pos == 118.0:
        if pos < (bbox[2]-40)/2:
            print('stair is 왼쪽')
            return 0
        # if pos == 228.0:
        if pos > (bbox[2]-40)/2:
            print('stair is 오른쪽')
            return 1
    except TypeError:
        print('Exception!')
    return -1

    # This will write different res.png for each frame. Change this as you require
    # cv2.imwrite('res{0}.png'.format(count),img_rgb)   


hwnd = win32gui.FindWindow(None, "BlueStacks")
win32gui.SetForegroundWindow(hwnd)
win32gui.MoveWindow(hwnd, -7, 0, 400, 400, True)
bbox = win32gui.GetWindowRect(hwnd)
time.sleep(0.5)
resize_y = 225
facing = 0  # 0 : left, 1 : right
file1 = cv2.imread('images/stair.png', 0)
glod = cv2.imread('images/gold_stair.png', 0)
while True:
    pic = pyautogui.screenshot(region=(0, 400, bbox[2]-40, bbox[3]-400-225))
    
    img_frame = np.array(pic)
    img_frame  = cv2.cvtColor(img_frame, cv2.COLOR_RGB2BGR)

    min_height = process_img(img_frame, file1)
    
    
    if min_height != -1:
        if facing == 0:
            if min_height == 0:
                pyautogui.press('right')
            else:
                pyautogui.press('left')
                facing = 1
        else:
            if min_height == 1:
                pyautogui.press('right')
            else:
                pyautogui.press('left')
                facing = 0
    # else:
        # time.sleep(0.5)
    # time.sleep(0.5)

    cv2.imshow('result', img_frame)
    k = cv2.waitKey(1) & 0xFF
    if k == 27:
        break
    # time.sleep(0.15
