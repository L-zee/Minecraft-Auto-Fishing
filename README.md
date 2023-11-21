# Minecraft-Auto-Fishing 说明

这是一个使用python语言编写的，利用OpenCV多尺度模板匹配技术的《我的世界》自动钓鱼脚本。

此程序是用于在屏幕上指定区域进行多尺度模板匹配的自动化脚本，主要应用了图像匹配和模拟鼠标点击的技术。用户可以使用如VS Code一类的代码编辑器运行程序。

以下是程序的主要原理和作用的简要介绍：

1. **选择识别范围：**
   - 运行`fish.py`后，在屏幕左上角弹出一个半透明且置顶的Tkinter窗口，提示用户将Tkinter窗口拖放并覆盖在游戏窗口右下角的字幕区域上，之后点击以确认需要进行图像匹配的范围。
   - 用户点击后，程序记录所选区域的坐标和大小，并在确认后2s关闭窗口。

2. **多尺度模板匹配：**
   - 使用OpenCV加载指定的模板图像`target_zh.png`。
   - 在用户选择的屏幕区域内截图，并将截图转换为灰度图像。
   - 通过在不同尺度上运行模板匹配算法`cv2.matchTemplate`，寻找在截图中的最佳匹配位置。（此处如果之前有成功的尺度，那么只在这个尺度的±10%范围内进行匹配）
   - 根据匹配的相似度`max_val`和位置信息`max_loc`判断是否找到合适的匹配。
   - 如果找到了相似度足够高的匹配，程序会在控制台输出匹配成功的信息，包括匹配尺度、位置和相似度。
     
3. **循环匹配，输出信息：**
   - 如果用户成功选择了识别范围，程序将进入一个无限循环，不断尝试进行模板匹配。
   - 如果匹配成功，程序会统计匹配次数、距离上次匹配时间、最小/最大/中位/平均匹配时间等信息，并在控制台以表格形式输出。
   - 如果连续40s未匹配成功（可能是电脑弹出了什么消息导致游戏暂停），程序将执行一系列操作尝试回到游戏（先后点击Tab键、Enter键和鼠标右键）。

4. **点击操作：**
   - 如果匹配成功，程序使用`pyautogui`库模拟鼠标右键点击。
   - 等待１秒进行第二次右键点击（防止鱼竿甩得很近）。
   - 再等待３秒进行后续图像识别（防止屏幕上残留的字幕触发二次点击）。



# Minecraft-Auto-Fishing Instructions

Since I play the Chinese version of Minecraft, I'm not sure how to express the in-game terms in English. The following English text is translated by GPT. If you don't understand Chinese, I hope you can use your imagination to understand the meaning I want to convey.

This is an automated script for fishing in "Minecraft" written in the Python language, utilizing the OpenCV multi-scale template matching technique.

The program is designed to perform multi-scale template matching in a specified area on the screen, employing image matching and simulated mouse clicks. Users can run the program using a code editor like VS Code.

Here is a brief overview of the main principles and functionalities of the program:

1. **Select Recognition Area:**
   - After running `fish.py`, a semi-transparent and topmost Tkinter window appears in the upper-left corner of the screen. It prompts the user to drag and drop the Tkinter window to cover the subtitle area in the bottom-right corner of the game window. Afterward, the user clicks to confirm the area for image matching.
   - Upon confirmation, the program records the coordinates and size of the selected area and closes the window after a 2-second delay.

2. **Multi-Scale Template Matching:**
   - Load the specified template image `target_zh.png` using OpenCV.
   - Capture a screenshot within the user-selected screen area and convert the screenshot to a grayscale image.
   - Perform template matching using the `cv2.matchTemplate` algorithm at different scales, searching for the best match in the screenshot. (If a successful scale was found previously, matching occurs within a ±10% range of that scale.)
   - Determine if a suitable match is found based on the similarity score `max_val` and the location information `max_loc`.
   - If a match with sufficiently high similarity is found, the program outputs success information to the console, including the matching scale, position, and similarity.

3. **Continuous Matching, Output Information:**
   - If the user successfully selects the recognition area, the program enters an infinite loop, continuously attempting template matching.
   - Upon a successful match, the program keeps track of match counts, time since the last match, and various statistics (minimum/maximum/median/average match time), presenting the information in tabular form in the console.
   - If no match occurs for 40 seconds (possibly due to a system notification pausing the game), the program executes a series of actions to attempt to return to the game (pressing Tab, Enter, and right-click).

4. **Clicking Operations:**
   - If a match is successful, the program uses the `pyautogui` library to simulate a right-click.
   - Waits for 1 second before performing a second right-click (preventing the fishing rod from being cast too close).
   - Waits for an additional 3 seconds for subsequent image recognition (preventing a second click triggered by residual subtitles on the screen).
