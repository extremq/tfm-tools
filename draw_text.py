import math
import pyautogui
import time
import re
from svg.path import Path, Line, Arc, parse_path

# Use https://danmarshall.github.io/google-font-to-svg-path/ to generate your text (separate characters)
svgpath = """
<svg width="252.3" height="139.8" viewBox="0 0 252.3 139.8" xmlns="http://www.w3.org/2000/svg"><g id="svgGroup" stroke-linecap="round" fill-rule="evenodd" font-size="9pt" stroke="#000" stroke-width="0.25mm" fill="none" style="stroke:#000;stroke-width:0.25mm;fill:none"><path d="M 66 105 L 66 57.15 L 14.25 57.15 L 14.25 105 L 0 105 L 0 0 L 14.25 0 L 14.25 44.85 L 66 44.85 L 66 0 L 80.25 0 L 80.25 105 L 66 105 Z" id="0" vector-effect="non-scaling-stroke"/><path d="M 168.9 71.55 L 114.3 71.55 A 36.132 36.132 0 0 0 116.009 79.087 Q 118.012 84.806 121.95 88.65 Q 128.25 94.8 138.6 94.8 A 55.094 55.094 0 0 0 145.013 94.444 A 41.363 41.363 0 0 0 150.75 93.375 Q 156.15 91.95 161.1 89.7 L 164.25 101.25 Q 158.85 103.8 152.1 105.3 A 61.067 61.067 0 0 1 144.462 106.47 A 81.911 81.911 0 0 1 136.95 106.8 A 43.767 43.767 0 0 1 128.256 105.97 A 35.412 35.412 0 0 1 121.8 104.025 Q 115.05 101.25 110.325 96.075 A 33.191 33.191 0 0 1 104.856 87.825 A 41.361 41.361 0 0 1 103.05 83.325 Q 100.5 75.75 100.5 66 A 52.317 52.317 0 0 1 101.705 54.605 A 45.895 45.895 0 0 1 103.05 49.8 A 41.549 41.549 0 0 1 107.271 40.877 A 36.228 36.228 0 0 1 110.25 36.825 Q 114.9 31.35 121.35 28.275 Q 127.8 25.2 135.75 25.2 Q 144.15 25.2 150.45 28.05 A 30.074 30.074 0 0 1 159.012 33.785 A 28.251 28.251 0 0 1 160.95 35.85 A 32.917 32.917 0 0 1 166.944 46.48 A 37.821 37.821 0 0 1 167.25 47.4 A 45.523 45.523 0 0 1 169.345 60.663 A 51.089 51.089 0 0 1 169.35 61.35 A 112.805 112.805 0 0 1 168.914 71.395 A 103.961 103.961 0 0 1 168.9 71.55 Z M 114.15 60.6 L 156.9 60.6 A 36.533 36.533 0 0 0 156.294 53.722 Q 155.55 49.846 153.894 46.81 A 18.633 18.633 0 0 0 151.2 43.05 Q 145.5 36.9 135.45 36.9 A 21.282 21.282 0 0 0 128.324 38.048 A 18.328 18.328 0 0 0 120.975 42.9 A 22.108 22.108 0 0 0 116.786 49.508 Q 115.549 52.441 114.828 56.041 A 48.43 48.43 0 0 0 114.15 60.6 Z" id="1" vector-effect="non-scaling-stroke"/><path d="M 176.1 136.8 L 179.1 125.55 A 15.386 15.386 0 0 0 180.833 126.411 Q 181.745 126.799 182.803 127.133 A 27.385 27.385 0 0 0 183.525 127.35 Q 185.985 128.053 189.169 128.097 A 31.031 31.031 0 0 0 189.6 128.1 A 19.613 19.613 0 0 0 194.204 127.572 A 17.729 17.729 0 0 0 195.525 127.2 A 13.922 13.922 0 0 0 198.988 125.493 A 17.841 17.841 0 0 0 200.85 124.05 Q 203.4 121.8 205.725 117.9 Q 207.532 114.868 209.294 110.658 A 92.604 92.604 0 0 0 210.3 108.15 L 213.75 99.15 L 206.55 99.15 L 176.1 30.6 L 188.1 25.2 L 217.2 90.15 L 239.85 25.8 L 252.3 30.6 L 223.65 108.9 A 110.392 110.392 0 0 1 221.122 115.218 Q 219.711 118.436 218.237 121.137 A 55.997 55.997 0 0 1 216.675 123.825 Q 213 129.75 208.8 133.35 A 25.503 25.503 0 0 1 202.852 137.206 A 22.79 22.79 0 0 1 199.725 138.375 A 36.011 36.011 0 0 1 191.442 139.746 A 41.755 41.755 0 0 1 189.3 139.8 Q 184.8 139.8 181.425 138.9 A 30.49 30.49 0 0 1 179.273 138.246 Q 178.267 137.896 177.435 137.51 A 12.921 12.921 0 0 1 176.1 136.8 Z" id="2" vector-effect="non-scaling-stroke"/></g></svg>
"""
words = re.findall(r'<path d="([QALMZ0-9\. ]+)" id="\d+" vector-effect="non-scaling-stroke"/>', svgpath)
print(words)
paths = []
for word in words:
    paths.append(parse_path(word))
n = 200  # number of lines


pts = []
for path in paths:
    pt = []
    for i in range(0, n+1):
        f = i/n
        complex_point = path.point(f)
        pt.append((complex_point.real, complex_point.imag))
    pts.append(pt)

print(pts)


def absolute_dif(p1, p2):
    return math.sqrt((p1[0] - p2[0])**2 + (p1[1] - p2[1])**2)


time.sleep(3)
for pt in pts:
    started = False
    for i in range(0, len(pt) - 1):
        # offset for 1366 x 768
        if absolute_dif(pt[i], pt[i - 1]) > 6:
            pyautogui.mouseUp()
            pyautogui.moveTo(pt[i][0] + 500, pt[i][1] + 200, 0)
            time.sleep(0.20)
            pyautogui.mouseDown()
        else:
            pyautogui.moveTo(pt[i][0] + 500, pt[i][1] + 200, 0)

        if not started:
            started = True
            pyautogui.mouseDown()

    pyautogui.mouseUp()
    time.sleep(0.20)
