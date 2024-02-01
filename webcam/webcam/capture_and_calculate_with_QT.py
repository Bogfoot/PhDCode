#!/usr/bin/python

# I am trying to get a hang of capturing images using webcams. This short snippet shows the image of the built-in
# webcam on my laptop

import cv2 as mycv
from scipy import ndimage
import numpy as np
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QVBoxLayout, QWidget, QLineEdit, QSpinBox

Xcenter = 320
Ycenter = 240
XstepSize = 1
YstepSize = 1

def myCM(mydata):
    '''
    calculate the center of mass of mydata

    mydata is assumed to be a 2D numpy array of some arbitrary size (M, N)
    the values of the array elements are considered to be the mass density
    the indices in the array are the x-y coordinates.

    returns an ndarray with two elements for the CM coordinates
    '''
    x = np.arange(mydata.shape[0])
    y = np.arange(mydata.shape[1])
    # make 2D arrays out of these ranges:
    xarr=np.zeros(mydata.shape)
    yarr=np.zeros(mydata.shape)
    for i in x:
        xarr[i,:] = x[i]
    for i in y:
        yarr[:,i] = y[i]
    xdata = xarr*mydata
    ydata = yarr*mydata
    xsum=np.sum(xdata)
    ysum=np.sum(ydata)
    msum=np.sum(mydata)
    myCM=np.array([xsum,ysum])
    myCM/=msum
    return myCM


app = QApplication([])
win = QMainWindow()
central_widget = QWidget()
buttonUp = QPushButton('Up', central_widget) 
buttonDown = QPushButton('Down', central_widget) 
buttonLeft = QPushButton('Left', central_widget) 
buttonRight = QPushButton('Right', central_widget) 
buttonQUIT = QPushButton('QUIT', central_widget) 

Xstep = QSpinBox(central_widget)
Xstep.setGeometry(0,100,100,20)
Xstep.setValue(XstepSize)
Xstep.setMinimum(1)
Xstep.setMaximum(20)

buttonUp.setGeometry(100,0,100,50)
buttonDown.setGeometry(100,50,100,50)
buttonLeft.setGeometry(0,25,100,50)
buttonRight.setGeometry(200,25,100,50)
buttonQUIT.setGeometry(350,25,50,50)

def moveCenterRight():
    '''
    move the center of the recorded camera stream
    '''
    Xcenter += Xstep.value()
    return True

def moveCenterLeft():
    '''
    move the center of the recorded camera stream
    '''
    Xcenter -= Xstep.value()
    return True

def moveCenterUp():
    '''
    move the center of the recorded camera stream
    '''
    Ycenter -= YstepSize
    return True

def moveCenterDown():
    '''
    move the center of the recorded camera stream
    '''
    Ycenter += YstepSize
    return True

def myquit():
    '''
    close window, quit program
    '''
    return app.exit()

buttonDown.clicked.connect(moveCenterDown)
buttonUp.clicked.connect(moveCenterUp)
buttonLeft.clicked.connect(moveCenterLeft)
buttonRight.clicked.connect(moveCenterRight)
buttonQUIT.clicked.connect(myquit)

win.setCentralWidget(central_widget)

win.show()

cap = mycv.VideoCapture(1)
  
ret, frame = cap.read()
#rgb = mycv.cvtColor(frame, mycv.COLOR_BGR2BGRA)
gray = mycv.cvtColor(frame, mycv.COLOR_BGR2GRAY)
out = mycv.imwrite('capture.jpg', gray)
print('test: ', gray.shape)

myCOM = ndimage.measurements.center_of_mass(gray)
print('center of mass: ', myCOM)
print('center of mass type: ', type(myCOM))

myCOM2 = myCM(gray)
print('center of mass: ', myCOM2)

# now, let us 

cap.release()

app.exit(app.exec_())

#if __name__ == "__main__":
#  main()
