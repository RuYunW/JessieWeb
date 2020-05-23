import cv2

videoCapture = cv2.VideoCapture("new.mp4")
print(videoCapture)
fps = videoCapture.get(cv2.CAP_PROP_FPS)
size = (
    int(videoCapture.get(cv2.CAP_PROP_FRAME_WIDTH)),
    int(videoCapture.get(cv2.CAP_PROP_FRAME_HEIGHT))
)

print(size)
