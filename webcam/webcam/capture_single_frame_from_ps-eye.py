#!/usr/bin/python

# I am trying to get a hang of capturing images using webcams. This short snippet shows the image of the built-in
# webcam on my laptop

import cv2 as mycv
from scipy import ndimage
import numpy as np


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
