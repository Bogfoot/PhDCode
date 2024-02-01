#!/usr/bin/python

# I am trying to get a hang of capturing images using webcams. This short snippet shows the image of the built-in
# webcam on my laptop

import cv2 as mycv
cap = mycv.VideoCapture(1)
while (True):
  ret, frame = cap.read()
  rgb = mycv.cvtColor(frame, mycv.COLOR_BGR2BGRA)
  mycv.imshow('frame', rgb)
  if mycv.waitKey(1) & 0xFF == ord('q'):
    out = mycv.imwrite('capture.jpg', frame)
    break
