import os
import cv2

path = os.path.dirname(__file__)
filename = "recognizeface.jpg"
fullpath = os.path.join(path, filename)

cap = cv2.VideoCapture(0)
# 캡쳐 Frame
ret, frame = cap.read()

# 프레임 컬러 설정함
gray = cv2.cvtColor(frame, cv2.IMREAD_COLOR)

# 윈도우 프레레임에 보임
cv2.imshow('frame', frame)
cv2.imwrite(fullpath, gray)

# 캠 리소스 해제
cap.release()
# 윈도우즈 해제
cv2.destroyAllWindows()
