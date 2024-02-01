#!/usr/bin/python

# based on the example given here: https://www.pythonforthelab.com/blog/step-by-step-guide-to-building-a-gui/
# date: 19-22.2.2019
# author: Rainer Kaltenbaek

import cv2
import numpy as np


class Camera:
  def __init__(self, cam_num):
    self.cap = None
    self.cam_num = cam_num
    self.mycount = 0

  def get_frame(self):
    ret, self.last_frame = self.cap.read()
    self.mycount = self.mycount + 1
    if not ret:
      print "error in getting frame"
    else:
      print "got frame nr. %d" % (self.mycount)
    return self.last_frame

  def acquire_movie(self, num_frames):
    movie = []
    for _ in range(num_frames):
      movie.append(self.get_frame())
    return movie

  def set_brightness(self, value):
    self.cap.set(cv2.CAP_PROP_BRIGHTNESS, value)

  def get_brightness(self):
    return self.cap.get(cv2.CAP_PROP_BRIGHTNESS)

  def get_saturation(self):
    return self.cap.get(cv2.CAP_PROP_SATURATION)

  def __str__(self):
    return 'OpenCV Camera {}'.format(self.cam_num)

  def close_camera(self):
    self.cap.release()

  def initialize(self):
    ##self.cap = cv2.VideoCapture(self.cam_num)
    self.cap = cv2.VideoCapture("/dev/video4")
    # cv2.CAP_DSHOW
    if not self.cap:
        print "error opening webcam\n"
        sys.exit(1)
    #self.cap.set(cv2.CAP_PROP_AUTO_EXPOSURE, -4)
    ##print("HELLO WORLD")
    self.cap.set(cv2.CAP_PROP_AUTO_EXPOSURE, 0.25)
    ##print("test 1")
    # seemingly not supported: self.cap.set(cv2.CAP_PROP_EXPOSURE, 0.1) 
    ##print("test 2")
    self.cap.set(cv2.CAP_PROP_SATURATION, 1.0)
    ##print("test 3")
    self.cap.set(cv2.CAP_PROP_BRIGHTNESS, 0.5)
    ##self.cap.set(cv2.CAP_PROP_CONTRAST, 0.1)        
    ##self.cap.set(cv2.CAP_PROP_GAIN, 0.0)   
    #self.cap.set(cv2.CAP_PROP_BACKLIGHT, 1)
    ##self.cap.set(cv2.CAP_PROP_GAMMA, 120)    
    #self.CAP_PROP_AUTO_EXPOSURE = -4
    #self.CAP_PROP_AUTO_WB = 0.25
    #self.CAP_PROP_AUTOFOCUS = 0.25

  def myCM(self, mydata):
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
    #print(xsum/msum)
    myCM/=msum
    return myCM

  def myQuad(self, cpos, mydata):
    '''
    calculates the for quadrant sums and returns the X_diff and Y_diff
    '''
    totalSum = 1.0*np.sum(mydata)
    leftData = 1.0*mydata[:,:cpos[0]]
    rightData = 1.0*mydata[:,cpos[0]:]
    topData = 1.0*mydata[:cpos[1],:]
    bottomData = mydata[cpos[1]:,:]
    diffX = int(round((np.sum(rightData)-np.sum(leftData))/totalSum))
    diffY = int(round((np.sum(topData)-np.sum(bottomData))/totalSum))
    #print("diff Y: ", diffX)
    #print("diff X: ", diffY)
    return np.array((diffX,diffY))

  def getCM(self):
    gray = cv2.cvtColor(self.last_frame, cv2.COLOR_BGR2GRAY)
    #print(gray.shape)
    pos = self.myCM(gray)
    return pos

  def getQuad(self, cpos):
    gray = cv2.cvtColor(self.last_frame, cv2.COLOR_BGR2GRAY)
    #print(gray.shape)
    pos = self.myQuad(cpos, gray)
    return pos

  def getSum(self):
    gray = cv2.cvtColor(self.last_frame, cv2.COLOR_BGR2GRAY)
    #print("gain: ", self.cap.get(cv2.CAP_PROP_GAIN))
    #print("saturation: ", self.cap.get(cv2.CAP_PROP_SATURATION))
    #print("exposure: ", self.cap.get(cv2.CAP_PROP_EXPOSURE))
    return np.sum(gray)

if __name__ == '__main__':
  cam = Camera(1)
  cam.initialize()
  print(cam)
  frame = cam.get_frame()
  #print(frame)
  cam.close_camera()
