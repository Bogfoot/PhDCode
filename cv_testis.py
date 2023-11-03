import numpy as np, cv2 as cv, matplotlib.pyplot as plt
from skimage import draw

coords = start_pt, end_pt = None, None


def get_pts(event, x, y, flags, param):
    global start_pt, end_pt
    if event == cv.EVENT_LBUTTONDOWN:
        coords = start_pt, end_pt = None, None
        start_pt = [x, y]
    if event == cv.EVENT_LBUTTONUP:
        end_pt = [x, y]
        print(start_pt, end_pt)


def plot_profile(data):
    plt.cla()
    plt.plot(data[:, 0])
    plt.draw()
    plt.pause(0.0001)
    plt.ylim((0, 255))


cap = cv.VideoCapture(1)
cv.namedWindow("frame")
cv.setMouseCallback("frame", get_pts)

if not cap.isOpened():
    print("zajebo se negde")
    quit()

while True:
    ret, frame = cap.read()
    if not ret:
        print("opet se zajebo neš")
        break
    frame_copy = frame.copy()
    gray = cv.cvtColor(frame_copy, cv.COLOR_BGR2GRAY)

    if end_pt:
        cv.line(frame, start_pt, end_pt, (255, 255, 255), 2)
        line = np.array(draw.line(*start_pt, *end_pt)).T
        data = frame_copy.copy()[line[:, 1], line[:, 0], :]
        plot_profile(data)
    cv.imshow("frame", frame)
    if cv.waitKey(1) == ord("q"):
        break

cap.release()
cv.destroyAllWindows()
