
import pyautogui
import pyperclip
import cv2
import numpy as np
prompt = r"""
Không sử dụng seed cũ.

Tạo 1 Hình ảnh tỷ lệ 16:9 về dây chuyền xử lý rác trong một nhà máy tại Nhật Bản. Trong cảnh có một công nhân nam đội mũ bảo hộ đang thực hiện công việc gần dây chuyền.

Xuất hiện một đến 3 bình phun sơn loại nhỏ ở đâu đó trên dây chuyền, có thể lẫn lộn trong đống rác, có thể bị các loại rác khác che mất dưới 70% bình gas (0-70%).

Mỗi lần tạo ảnh phải thay đổi môi trường, nhà máy, góc máy, vị trí và hành động của công nhân, cùng với màu sắc, hình dáng, độ méo, hướng đặt và khoảng cách của bình gas.

Bình phun sơn chỉ chiếm 3–5 % của diện tích hình ảnh, có thể ở gần hoặc xa camera, không cố định vị trí, không làm nổi bật, không khoanh vùng hay đánh dấu.

Bình phun sơn có hình dạng hơi méo khác nhau giữa các ảnh.

Phong cách hiện thực công nghiệp, ánh sáng tự nhiên, bố cục tự nhiên, không chữ, không ký hiệu, không chú thích.

thay đổi đi
"""

def auto_gen_image(prompt: str, name:str) -> bool:
    #1 click the text input area
    x, y = pyautogui.locateCenterOnScreen('tmp\image\input_text.png', confidence=0.8)
    #2 paste the prompt
    pyautogui.click(x, y)
    pyperclip.copy(prompt)
    pyautogui.hotkey("ctrl", "v")
    pyautogui.sleep(0.5)
    #enter to submit
    pyautogui.press("enter")
    pyautogui.sleep(2)
    #wait for generation
    #vùng ảnh là x,y,w,h = 285, 560, 30, 30
    #kiểm tra nếu ảnh đó chỉ có 1 màu thì chờ tiếp
    i = 0
    has_image = False
    while i < 15:
        screenshot = pyautogui.screenshot(region=(285, 560, 30, 30))
        img = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2BGR)
        
        # Chuyển sang ảnh xám để tính toán cho nhẹ
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        
        # Tính độ lệch chuẩn (độ biến thiên màu sắc)
        # mean: giá trị trung bình, std_dev: độ lệch chuẩn
        mean, std_dev = cv2.meanStdDev(gray)
        
        # Nếu độ lệch chuẩn < 3 (ngưỡng nhỏ), nghĩa là các pixel gần như giống hệt nhau (1 màu)
        # Bạn có thể chỉnh số 3 thành 0 nếu muốn tuyệt đối, hoặc 5-10 nếu ảnh có chút nhiễu
        if std_dev[0][0] < 3: 
            print(f"Ảnh đang đơn sắc (chưa load xong), đợi thêm... (Lần {i+1})")
            pyautogui.sleep(5)
            i += 1
        else:
            print("Đã phát hiện hình ảnh có chi tiết!")
            has_image = True
            break
    if not has_image:
        return False
    #4 click the download button
    print("Downloading image...")
    pyautogui.rightClick(285, 560)
    pyautogui.sleep(1)
    pyautogui.click(285 + 96, 560 +55)  # click center to save
    pyautogui.sleep(1)
    pyperclip.copy(str(name))
    pyautogui.hotkey("ctrl", "v")
    pyautogui.sleep(0.5)
    pyautogui.press("enter")
    pyautogui.sleep(1)
    return True

num_images = 50
start_name = 20
for i in range(num_images):
    name = str(start_name)
    success = auto_gen_image(prompt, name)
    if not success:
        print("Image generation failed.")
        break
    start_name += 1