import cv2
import numpy as np
import pyautogui
import tkinter as tk
import time
from prettytable import PrettyTable
import statistics
import os

#---------------------------获取匹配图片---------------------------

# 获取程序所在的文件夹
dir_path = os.path.dirname(os.path.realpath(__file__))

# 指定图片的文件名
image_filename = 'target_zh.png'

# 拼接得到图片的完整路径
text_image_path = os.path.join(dir_path, image_filename)

# 输出图片的路径
print(f"用以匹配的图片在：{text_image_path}")

# 指定模板图片的路径，使用双斜线避免歧义
#text_image_path = 'D:\\Desktop\\auto fishing\\target_zh.png'
#-----------------------------------------------------------------


#---------------------------选定识别范围---------------------------

# 全局变量存储用户选择的区域
selected_region = None

# 用户点击确认后的回调函数
def on_confirm():
    global selected_region
    x1 = root.winfo_rootx()
    y1 = root.winfo_rooty()
    x2 = x1 + root.winfo_width()
    y2 = y1 + root.winfo_height()
    selected_region = (x1, y1, x2 - x1, y2 - y1)
    root.after(2000, root.destroy)  # 在用户点击确认后，等待2秒后关闭窗口

# 创建Tkinter窗口
root = tk.Tk()
root.title("")  # 设置窗口标题
root.geometry('400x280')  # 设置初始窗口大小
root.wm_attributes('-alpha', 0.8)  # 设置窗口半透明
root.wm_attributes('-topmost', True) # 设置窗口置顶

text_in_window="请调整窗口覆盖字幕\n点击窗口内任意位置\n即可确定范围"
confirm_button = tk.Button(root, text=text_in_window, command=on_confirm)
confirm_button.pack(fill=tk.BOTH, expand=True)

# 显示窗口直到用户点击确认
root.mainloop()
#-----------------------------------------------------------------


#---------------------------多尺度模板匹配---------------------------
start_time = time.time() # 记录程序开始运行的时间

def format_time(seconds):
    minutes, seconds = divmod(seconds, 60)
    return f"{int(minutes)}m {seconds:.3f}s"

def multi_scale_template_matching(image_path, region):
    # 读取模板图像
    template = cv2.imread(image_path, 0)

    # 截取用户选择的屏幕区域
    x, y, w, h = region
    screenshot = pyautogui.screenshot(region=(x, y, w, h))
    screenshot_gray = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2GRAY)

    # 用于记录最佳匹配的结果
    best_match = None
    max_val = 0

    # 保存成功的尺度
    successful_scale = None 

    # 在多个尺度上运行模板匹配
    scales = np.linspace(0.7, 2, 50)[::-1]
    if successful_scale is not None:
        # 如果之前有成功的尺度，那么只在这个尺度的附近进行匹配
        min_scale = max(0.7, successful_scale * 0.9)
        max_scale = min(2, successful_scale * 1.1)
        scales = np.linspace(min_scale, max_scale, 50)[::-1]
        

    for scale in scales:
        # 缩放模板图像
        resized_template = cv2.resize(template, (0, 0), fx=scale, fy=scale)
        resized_height, resized_width = resized_template.shape[:2]

        # 确保缩放后的模板不大于截图区域
        if resized_height > h or resized_width > w:
            continue

        # 模板匹配
        res = cv2.matchTemplate(screenshot_gray, resized_template, cv2.TM_CCOEFF_NORMED)
        min_val, max_val_temp, min_loc, max_loc = cv2.minMaxLoc(res)

        # 如果当前匹配结果更好，则更新最佳匹配结果
        if max_val_temp > max_val:
            max_val = max_val_temp
            best_match = max_loc, scale

    # 检查是否找到足够好的匹配结果
    if best_match and max_val > 0.75:
        max_loc, scale = best_match 
        successful_scale = scale  # 保存成功的尺度
        current_time = time.time()
        elapsed_time = current_time - start_time  # 已运行时间
        formatted_time = format_time(elapsed_time)
        print(f"已运行 {formatted_time}。匹配成功，尺度: {scale:.6f}, 位置: {max_loc}, 相似度: {max_val:.6f}")
        return True
    else:
        current_time = time.time()
        elapsed_time = current_time - start_time  # 已运行时间
        formatted_time = format_time(elapsed_time)
        print(f"已运行 {formatted_time}。未找到匹配图像。最高相似度: {max_val:.6f}")
        return False
#-----------------------------------------------------------------


#---------------------------循环匹配，输出信息---------------------------

# 检查用户是否选择了区域
if selected_region:
    print("选定区域:", selected_region)
    match_count = 0 # 匹配成功次数的计数器
    match_times = [] # 用于存储匹配时间的列表
    last_match_time = time.time() # 上一次匹配成功的时间
    no_match_start_time = time.time() # 连续未匹配成功的起始时间

    while True:
        # 调用模板匹配函数
        if multi_scale_template_matching(text_image_path, selected_region):
            match_count += 1
            current_time = time.time()
            match_interval = current_time - last_match_time
            match_times.append(match_interval)
            last_match_time = current_time
            no_match_start_time = current_time  # 重置未匹配成功的起始时间

            # 使用 PrettyTable 创建表格5
            table = PrettyTable()
            table.header = False  # 不显示表头
            table.add_row(["匹配成功次数", match_count])
            table.add_row(["距上次成功", f"{match_interval:.4f} s"])
            table.add_row(["最小时间", f"{min(match_times):.4f} s"])
            table.add_row(["最大时间", f"{max(match_times):.4f} s"])
            table.add_row(["中位时间", f"{statistics.median(match_times):.4f} s"])
            table.add_row(["平均时间", f"{sum(match_times)/len(match_times):.4f} s"])

            print(table)
            
            # 计算匹配位置并点击
            pyautogui.click(button='right')
            time.sleep(1)  # 等待１秒进行第二次右键点击
            pyautogui.click(button='right')
            time.sleep(3)  # 等待３秒进行后续图像识别

        else:
            # 检查连续未匹配成功的时间
            current_time = time.time()

            # 如果连续未匹配成功的时间超过40秒，执行一次Tab点击，再点击一次Enter，点击一次右键
            if current_time - no_match_start_time >= 40:
                print("已经40秒没有匹配成功了，尝试回到游戏并点击右键")
                pyautogui.press('tab')
                #time.sleep(1)  # 等待１秒点击enter
                pyautogui.press('enter')
                #time.sleep(1)  # 等待１秒点击右键
                pyautogui.click(button='right')
                no_match_start_time = current_time  # 重置未匹配成功的起始时间
                
        time.sleep(0.4)  # 循环检查的间隔时间
else:
    print("未选择区域")
#-----------------------------------------------------------------
