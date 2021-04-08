import pyautogui
import time
import re
from svg.path import Path, Line, Arc, parse_path

# Use https://danmarshall.github.io/google-font-to-svg-path/ to generate your text
svgpath = """
<svg width="433.305" height="146.097" viewBox="0 0 433.305 146.097" xmlns="http://www.w3.org/2000/svg"><g id="svgGroup" stroke-linecap="round" fill-rule="evenodd" font-size="9pt" stroke="#000" stroke-width="0.25mm" fill="none" style="stroke:#000;stroke-width:0.25mm;fill:none"><path d="M 103.031 43.068 L 84.183 43.068 A 32.572 32.572 0 0 0 83.077 34.346 A 23.697 23.697 0 0 0 75.98 22.804 Q 68.815 16.365 56.51 15.55 A 55.608 55.608 0 0 0 52.835 15.431 A 50.806 50.806 0 0 0 44.392 16.089 Q 36.421 17.434 31.204 21.535 A 19.833 19.833 0 0 0 23.54 36.083 A 28.159 28.159 0 0 0 23.441 38.478 A 17.901 17.901 0 0 0 29.392 51.928 A 25.205 25.205 0 0 0 30.814 53.176 Q 37.033 58.241 50.615 62.577 A 157.783 157.783 0 0 0 55.911 64.162 A 182.836 182.836 0 0 1 66.236 67.375 Q 76.764 71.019 83.646 75.148 A 52.033 52.033 0 0 1 91.17 80.572 Q 95.395 84.269 98.111 88.55 A 32.212 32.212 0 0 1 98.49 89.162 Q 103.324 97.17 103.324 108.01 A 35.683 35.683 0 0 1 100.604 122.15 Q 97.27 129.967 89.847 135.695 A 47.078 47.078 0 0 1 73.108 143.772 Q 64.474 146.096 53.812 146.096 A 67.183 67.183 0 0 1 28.464 141.323 A 64.808 64.808 0 0 1 26.468 140.48 A 52.952 52.952 0 0 1 15.843 134.304 A 41.634 41.634 0 0 1 6.888 125.099 A 37.535 37.535 0 0 1 0.003 102.931 L 18.851 102.931 A 28.02 28.02 0 0 0 20.392 112.427 A 23.858 23.858 0 0 0 28.372 123.293 Q 36.918 129.997 50.615 130.685 A 63.788 63.788 0 0 0 53.812 130.763 A 58.393 58.393 0 0 0 62.412 130.172 Q 66.77 129.522 70.308 128.156 A 25.082 25.082 0 0 0 76.566 124.709 A 19.307 19.307 0 0 0 84.352 110.749 A 25.589 25.589 0 0 0 84.476 108.205 A 23.862 23.862 0 0 0 83.53 101.306 A 18.123 18.123 0 0 0 77.152 92.043 A 34.656 34.656 0 0 0 72.173 88.885 Q 64.492 84.786 50.589 80.763 A 152.266 152.266 0 0 1 37.425 76.367 Q 23.207 70.829 15.482 63.722 A 33.333 33.333 0 0 1 6.524 50.653 A 34.095 34.095 0 0 1 4.495 38.771 Q 4.495 21.974 17.923 10.988 Q 31.351 0.002 52.835 0.002 A 64.731 64.731 0 0 1 67.504 1.6 A 52.706 52.706 0 0 1 78.958 5.666 A 45.568 45.568 0 0 1 90.76 13.907 A 40.76 40.76 0 0 1 96.732 21.291 Q 103.031 31.252 103.031 43.068 Z" id="0" vector-effect="non-scaling-stroke"/><path d="M 190.14 144.142 L 189.749 133.693 Q 179.313 145.965 159.22 146.094 A 66.67 66.67 0 0 1 158.792 146.096 A 46.366 46.366 0 0 1 148.573 145.039 Q 141.766 143.501 136.797 139.723 A 27.049 27.049 0 0 1 133.06 136.281 Q 126.046 128.492 124.537 114.767 A 72.421 72.421 0 0 1 124.124 107.228 L 124.124 38.478 L 142.191 38.478 L 142.191 106.74 A 43.398 43.398 0 0 0 142.997 115.508 Q 145.751 128.797 157.916 130.51 A 27.309 27.309 0 0 0 161.722 130.763 A 42.829 42.829 0 0 0 171.742 129.675 Q 184.241 126.665 189.261 115.334 L 189.261 38.478 L 207.328 38.478 L 207.328 144.142 L 190.14 144.142 Z" id="1" vector-effect="non-scaling-stroke"/><path d="M 234.769 38.478 L 251.859 38.478 L 252.445 51.76 A 40.014 40.014 0 0 1 266.286 40.394 Q 274.243 36.525 284.085 36.525 A 42.332 42.332 0 0 1 298.163 38.671 Q 317.651 45.531 317.874 74.318 L 317.874 144.142 L 299.808 144.142 L 299.808 74.221 A 40.813 40.813 0 0 0 299.313 67.999 Q 298.198 61.182 294.583 57.326 A 15.721 15.721 0 0 0 288.276 53.311 Q 284.206 51.857 278.617 51.857 A 27.842 27.842 0 0 0 269.409 53.34 A 24.962 24.962 0 0 0 263.187 56.545 A 31.831 31.831 0 0 0 252.835 68.849 L 252.835 144.142 L 234.769 144.142 L 234.769 38.478 Z" id="2" vector-effect="non-scaling-stroke"/><path d="M 351.566 12.892 L 369.632 12.892 L 369.632 38.478 L 389.359 38.478 L 389.359 52.443 L 369.632 52.443 L 369.632 117.971 Q 369.632 124.318 372.269 127.492 A 7.799 7.799 0 0 0 375.488 129.744 Q 376.806 130.262 378.466 130.489 A 20.615 20.615 0 0 0 381.253 130.666 A 23.235 23.235 0 0 0 383.42 130.553 Q 385.703 130.337 388.809 129.71 A 89.376 89.376 0 0 0 389.847 129.494 L 389.847 144.142 A 54.738 54.738 0 0 1 380.229 145.905 A 47.936 47.936 0 0 1 375.98 146.096 A 31.799 31.799 0 0 1 368.754 145.326 Q 363.703 144.147 360.119 141.165 A 19.023 19.023 0 0 1 357.718 138.771 A 24.097 24.097 0 0 1 353.226 130.313 Q 352.137 126.808 351.762 122.588 A 52.255 52.255 0 0 1 351.566 117.971 L 351.566 52.443 L 332.328 52.443 L 332.328 38.478 L 351.566 38.478 L 351.566 12.892 Z" id="3" vector-effect="non-scaling-stroke"/><path d="M 411.376 130.867 A 13.014 13.014 0 0 0 410.843 134.67 A 13.767 13.767 0 0 0 410.876 135.635 A 10.473 10.473 0 0 0 413.626 142.189 A 8.257 8.257 0 0 0 415.48 143.694 Q 418.028 145.217 421.976 145.217 Q 427.542 145.217 430.423 142.189 A 10.141 10.141 0 0 0 432.671 138.559 A 11.554 11.554 0 0 0 433.304 134.67 Q 433.304 129.982 430.423 126.857 Q 428.465 124.733 425.266 124.053 A 15.824 15.824 0 0 0 421.976 123.732 Q 419.628 123.732 417.775 124.288 A 8.807 8.807 0 0 0 413.626 126.857 A 10.595 10.595 0 0 0 411.376 130.867 Z" id="4" vector-effect="non-scaling-stroke"/></g></svg>
"""
words = re.findall(r'<path d="([QALMZ0-9\. ]+)" id="\d+" vector-effect="non-scaling-stroke"/>', svgpath)
print(words)
paths = []
for word in words:
    paths.append(parse_path(word))
n = 75  # number of lines


pts = []
for path in paths:
    pt = []
    for i in range(0, n+1):
        f = i/n
        complex_point = path.point(f)
        pt.append((complex_point.real, complex_point.imag))
    pts.append(pt)

print(pts)

time.sleep(3)
for pt in pts:
    started = False
    for p in pt:
        # offset for 1366 x 768
        pyautogui.moveTo(p[0] + 500, p[1] + 200, 0)
        if not started:
            started = True
            pyautogui.mouseDown()
    pyautogui.mouseUp()
    time.sleep(0.20)