# import os
# import cv2
# import numpy as np

# path = os.path.dirname(__file__)
# filename = "recognizeface.jpg"
# fullpath = os.path.join(path, filename)

# cap = cv2.VideoCapture(0)
# # 캡쳐 Frame
# ret, frame = cap.read()

# # 프레임 컬러 설정함
# gray = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

# # 윈도우 프레레임에 보임
# # cv2.imshow('frame', frame)
# cv2.imwrite(fullpath, gray)

# # 캠 리소스 해제
# cap.release()
# # 윈도우즈 해제
# cv2.destroyAllWindows()


import cv2

import shutil

capture = cv2.VideoCapture(0)
capture.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
capture.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

while cv2.waitKey(33) < 0:
    ret, frame = capture.read()
    #############
    # cpimg = frame[:, :].copy()
    # cpimg.fill(0)

    shutil.move('./img/a.jpg', './img/a_tmp.jpg')

    #############
    cv2.imwrite('./img/a.jpg', frame)

capture.release()
cv2.destroyAllWindows()
