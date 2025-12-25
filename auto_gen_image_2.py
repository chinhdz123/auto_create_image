"""Cho phép up 1 ảnh background và tạo ảnh mới dựa trên prompt."""

import pyautogui
import pyperclip
import cv2
import numpy as np
import random
from prompts.prompt2 import prompts
from image_aere import image_x, image_y
import os
def is_similar_to_dark(img, dark_img, threshold=5):
    gray1 = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    gray2 = cv2.cvtColor(dark_img, cv2.COLOR_BGR2GRAY)

    diff = cv2.absdiff(gray1, gray2)
    mean_diff = diff.mean()

    return mean_diff < threshold

def auto_gen_image(prompt: str, name:str) -> bool:
    #click add image button
    try:
        x_add, y_add = pyautogui.locateCenterOnScreen(r'tmp/image/add.png', confidence=0.8)
        pyautogui.click(x_add, y_add)
    except Exception as e:
        pyautogui.press("esc")
        pyautogui.sleep(1)
        return True
    pyautogui.sleep(1)
    #click choose file button
    try:
        x_choose, y_choose = pyautogui.locateCenterOnScreen(r'tmp/image/upload.png', confidence=0.8)
        pyautogui.click(x_choose, y_choose)
    except Exception as e:
        pyautogui.press("esc")
        pyautogui.sleep(1)
        return True
    
    pyautogui.sleep(2)
    #paste the name of the image
    pyperclip.copy(str(name))
    pyautogui.hotkey("ctrl", "v")
    pyautogui.sleep(0.5)
    pyautogui.press("enter")
    pyautogui.sleep(2)


    # 1 click the text input area
    try:
        x, y = pyautogui.locateCenterOnScreen(r'tmp/image/input_text.png', confidence=0.8)
    except Exception as e:
        pyautogui.press("esc")
        pyautogui.sleep(1)
        return True
    # 2 paste the prompt

    pyautogui.click(x, y)
    pyperclip.copy(prompt)
    pyautogui.hotkey("ctrl", "v")
    pyautogui.sleep(0.5)
    #enter to submit
    pyautogui.press("enter")
    pyautogui.sleep(2)
    #cuộn xuống để thấy ảnh
    pyautogui.scroll(-500)
    #wait for generation
    #vùng ảnh là x,y,w,h = image_x, image_y, 30, 30
    #kiểm tra nếu ảnh đó chỉ có 1 màu thì chờ tiếp
    i = 0
    has_image = False
    while i < 20:
        dark_screen_img = cv2.imread(r'tmp/image/dark_screen.png')
        dark_w, dark_h, _ = dark_screen_img.shape
        screenshot = pyautogui.screenshot(region=(image_x, image_y, dark_h, dark_w))
        img = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2BGR)
        
        has_image = is_similar_to_dark(img, dark_screen_img, threshold=5)
        # Nếu độ lệch chuẩn < 3 (ngưỡng nhỏ), nghĩa là các pixel gần như giống hệt nhau (1 màu)
        # Bạn có thể chỉnh số 3 thành 0 nếu muốn tuyệt đối, hoặc 5-10 nếu ảnh có chút nhiễu
        if has_image:
            print(f"Ảnh đang đơn sắc (chưa load xong), đợi thêm... (Lần {i+1})")
            pyautogui.click(50, image_y)
            pyautogui.scroll(-500)
            pyautogui.sleep(5)
            i += 1
        else:
            print("Đã phát hiện hình ảnh có chi tiết!")
            has_image = True
            break
    # if not has_image:
    #     return False
    #4 click the download button
    print("Downloading image...")
    pyautogui.rightClick(image_x, image_y)
    pyautogui.sleep(1)
    pyautogui.click(image_x + 96, image_y +55)  # click center to save
    pyautogui.sleep(1)
    pyperclip.copy(str(name))
    pyautogui.hotkey("ctrl", "v")
    pyautogui.sleep(0.5)
    pyautogui.press("enter")
    pyautogui.sleep(1)
    return True

def change_conv():
    x, y = pyautogui.locateCenterOnScreen(r'tmp/image/tab.png', confidence=0.8)
    pyautogui.click(x, y)
    pyautogui.sleep(1)
    x1, y1 = pyautogui.locateCenterOnScreen(r'tmp/image/new_conv.png', confidence=0.8)
    pyautogui.click(x1, y1)
    pyautogui.sleep(2)
    #clich tác nhân
    x2, y2 = pyautogui.locateCenterOnScreen(r'tmp/image/tacnhan.png', confidence=0.8)
    pyautogui.click(x2, y2)
    pyautogui.sleep(2)
    #clich tạo hình ảnh
    pyautogui.click(x2 + 10, y2 - 130)
    pyautogui.sleep(2)

thresh_change = 20

path_folder_background = r"D:\arrow\project\hazardous\dataset\Data.segmentation.Version 3.yolo\Data.segmentation.Version 3.yolo\val\images"
images_names = [name for name in os.listdir(path_folder_background)] #lấy tên tất cả ảnh trong folder
pre_name = "" # nhập tên ảnh muốn bắt đầu từ đó, để trống nếu muốn từ đầu
if pre_name and pre_name in images_names:
    images_names = images_names[images_names.index(pre_name)+1:] #lấy tên tất cả ảnh trong folder từ ảnh có tên pre_name trở đi

for i in range(len(images_names)):
    #nếu i % thresh_change == 0 và i != 0 thì đổi conversation
    if i % thresh_change == 0 and i != 0:
        change_conv()
    name = images_names[i]
    prompt = random.choice(prompts)
    success = auto_gen_image(prompt, name)
    if not success:
        print("Image generation failed.")
        break
    print("Generated image for background:", images_names[i])
