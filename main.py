from numpy.lib.twodim_base import triu_indices_from
import win32gui
import re, cv2
import numpy as np
from PIL import ImageGrab
import matplotlib.pyplot as plt
import pyautogui, time
import matplotlib
import keyboard as kb
from operator import itemgetter, pos




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

    while True:
        continue_type = False
        for i in range(1, len(arr)):
            if abs(arr[i][1] - arr[i-1][1]) <= 3:
                del arr[i]
                continue_type = True
                break
        if not continue_type:
            break

    for pt in arr:
        cv2.rectangle(img_rgb, pt, (pt[0] + w, pt[1] + h), (0,0,255), 2)
        

    return arr


    # This will write different res.png for each frame. Change this as you require
    # cv2.imwrite('res{0}.png'.format(count),img_rgb)   


def calculate_stair(arr):
    pos_arr = []
    y_max = 0
    for pt in list(reversed(arr)):
        pt = (pt[0]//52, pt[1]//25)
        pos_arr.append(pt)
    # y_max = pos_arr[0]
    y_max = 13
    for i in range(len(pos_arr)):
        if y_max - pos_arr[i][1] > 6:
            pos_arr[i] = (pos_arr[i][0], y_max-1 - pos_arr[i][1])
        elif pos_arr[i][1] == 14:
            pos_arr[i] = (pos_arr[i][0], 0)
        else:
            pos_arr[i] = (pos_arr[i][0], y_max - pos_arr[i][1])
    print(pos_arr)
    return pos_arr


def restore_stair(arr):
    while True:
        break_type = False
        end_type = False
        for i in range(1, len(arr)):
            if abs(arr[i][0] - arr[i-1][0]) == abs(arr[i][1] - arr[i-1][1]):
                for j in range(1, abs(arr[i][0] - arr[i-1][0])):
                    # print(abs(arr[i][0] - arr[i-1][0]))
                    x = min(arr[i][0], arr[i-1][0]) + j
                    y = min(arr[i][1], arr[i-1][1]) + j
                    arr.insert(i, (x,y))
                    break_type = True
                if break_type:
                    break
            if break_type:
                break
        if not break_type:
            break
    try:
        if arr[0][1] != 0:
            return [(0,0)]
    except IndexError:
        return [(0,0)]
    for i in range(1,len(arr)):
        if arr[i][1] - arr[i-1][1] != 1 or abs(arr[i][0] - arr[i-1][0]) != 1:
            return arr[:i]

    return arr

                
def press_btn(arr):
    # [(1, 0), (2, 1), (3, 2), (4, 3), (3, 4), (2, 5), (1, 6), (0, 7)]
    # _  .  .  .  . 
    # .  _  .  .  .
    # .  .  _  .  .
    # .  .  .  _  .
    # .  .  .  .  _
    # .  .  .  _  .
    # .  .  _  .  .
    # .  _  .  .  .
    # _  .  .  .  .
    # .  _  .  .  .
    global facing
    for i in range(1, len(arr)):
        if arr[i][0] < arr[i-1][0]:
            if facing == 0:
                pyautogui.press('right')
            else:
                pyautogui.press('left')
                facing = 0
        else:
            if facing == 1:
                pyautogui.press('right')
            else:
                pyautogui.press('left')
                facing = 1


hwnd = win32gui.FindWindow(None, "BlueStacks")
win32gui.SetForegroundWindow(hwnd)
win32gui.MoveWindow(hwnd, -7, 0, 400, 400, True)
bbox = win32gui.GetWindowRect(hwnd)
time.sleep(0.5)
resize_y = 225
facing = 0  # 0 : left, 1 : right
file1 = cv2.imread('images/stair.png', 0)
glod = cv2.imread('images/gold_stair.png', 0)
gameover = cv2.imread('images/gameover.png', 0)
run = False
while True:
    if kb.is_pressed('F5'):
        print('press f5')
        run = (run == False)
        facing = 0
        time.sleep(0.5)
    if run == False:
        continue
    pic = pyautogui.screenshot(region=(0, 100, bbox[2]-40, bbox[3]-100-195))
    
    img_frame = np.array(pic)
    img_frame  = cv2.cvtColor(img_frame, cv2.COLOR_RGB2BGR)

    start_list = process_img(img_frame, file1)
    a = restore_stair(calculate_stair(start_list))
    print(a)
    press_btn(a)
    
    # else:
        # time.sleep(0.5)
    # time.sleep(0.5)

    cv2.imshow('result', img_frame)
    k = cv2.waitKey(1) & 0xFF
    if k == 27:
        break
    time.sleep(0.05)
