#!/usr/bin/python3

# switched to python3 on October 20th, 2020

from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QWidget, QLineEdit, QDoubleSpinBox, QLabel, QGraphicsScene
from pyqtgraph import ImageView

import pyqtgraph as pg

from PyQt5 import QtCore, QtGui, QtWidgets

from PyQt5.QtCore import QTimer, QLocale

import numpy as np
import time

from modelsvideo import Camera

# import QGraphics

class StartWindow(QMainWindow):
  def __init__(self, camera = None, save_frames=False):
    super(StartWindow, self).__init__()
    self.camera = camera
    #--- added by Kristof
    self.save_frames = save_frames
    if self.save_frames:
        self.time_array = []
        self.frames_array = []
    #---
    
    #self.camera.initialize()
    self.central_widget = QWidget()
    self.central_widget.setObjectName("central_widget") 
    self.central_widget.setLocale(QLocale("US_en"));
    self.set_frame_geometry(640, 480)
    super(StartWindow, self).resize(self.areaWidth + 600, self.areaHeight)

    self.XstepSize = 1
    self.YstepSize = 1
    self.CMx = 0
    self.CMy = 0
    self.centerCircle = True
    self.circleRadius = 10;

    self.videoArea = QtCore.QRectF(600, 0, self.areaWidth, self.areaHeight)

    #self.scene = QtGui.QGraphicsScene(self.videoArea)
    self.scene = QGraphicsScene(self.videoArea)

    pen = QtGui.QPen()
    pen.setColor(QtGui.QColor(0,200,0,255))
    #pen.setcolor(Qt::red)
    brush = QtGui.QBrush(QtGui.QColor(0,200,0,255))
    #QBrush brush(Qt::red, Qt::CrossPattern)
    self.centerCircle = self.scene.addEllipse(QtCore.QRectF(self.CMx-self.circleRadius,self.CMy-self.circleRadius,2*self.circleRadius,2*self.circleRadius), pen, brush);

    self.graphicsView = QtWidgets.QGraphicsView(self.central_widget)
    self.graphicsView.setGeometry(QtCore.QRect(10, 40, 601, 411))
    self.graphicsView.setObjectName("graphicsView")
    self.graphicsView.setScene(self.scene)

    self.buttonUp = QPushButton('Up', self.central_widget)
    self.buttonUp.setObjectName("buttonUp")  
    self.buttonDown = QPushButton('Down', self.central_widget) 
    self.buttonDown.setObjectName("buttonDown") 
    self.buttonLeft = QPushButton('Left', self.central_widget)
    self.buttonLeft.setObjectName("buttonLeft") 
    self.buttonRight = QPushButton('Right', self.central_widget) 
    self.buttonRight.setObjectName("buttonRight") 
    self.buttonQUIT = QPushButton('QUIT', self.central_widget)
    self.buttonQUIT.setObjectName("buttonQUIT") 
    self.DXspinBox = QDoubleSpinBox(self.central_widget)
    self.DXspinBox.setObjectName("DXspinBox") 
    self.DYspinBox = QDoubleSpinBox(self.central_widget)
    self.DYspinBox.setObjectName("DYspinBox") 
    self.XspinBox = QDoubleSpinBox(self.central_widget)
    self.XspinBox.setObjectName("XspinBox") 
    self.YspinBox = QDoubleSpinBox(self.central_widget)
    self.YspinBox.setObjectName("YspinBox")
    font = QtGui.QFont()
    self.CMyPos = QLineEdit(self.central_widget)
    self.CMyPos.setObjectName("CMyPos")
    self.CMxPos = QLineEdit(self.central_widget)
    self.CMxPos.setObjectName("CMxPos")
    Palette= QtGui.QPalette()
    Palette.setColor(QtGui.QPalette.Text, QtGui.QColor(180,180,180,255))
    self.CMxPos.setPalette(Palette)
    self.CMyPos.setPalette(Palette)
    font.setPointSize(30)
    font.setBold(True)
    font.setWeight(75) 
    self.QyPos = QLineEdit(self.central_widget)
    self.QyPos.setObjectName("CMyPos")
    self.QxPos = QLineEdit(self.central_widget)
    self.QxPos.setObjectName("CMxPos")
    self.QxPos.setReadOnly(True)
    self.QyPos.setReadOnly(True)
    self.QxPos.setFont(font)
    self.QyPos.setFont(font)
    self.QxPos.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
    self.QyPos.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)

    self.sumIntensity = QLineEdit(self.central_widget)
    self.sumIntensity.setObjectName("sumIntensity")
    self.sumIntensity.setReadOnly(True)
    self.sumIntensity.setFont(font)
    self.sumIntensity.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)

    self.buttonUp.setGeometry(QtCore.QRect(80,40,90,25))
    self.buttonDown.setGeometry(QtCore.QRect(80,100,90,25))
    self.buttonLeft.setGeometry(QtCore.QRect(30, 70, 90, 25))
    self.buttonRight.setGeometry(QtCore.QRect(130, 70, 90, 25))
    self.buttonQUIT.setGeometry(70,150,100,60) 

    self.DXspinBox.setGeometry(QtCore.QRect(320, 50, 80, 25))
    self.DYspinBox.setGeometry(QtCore.QRect(320, 90, 80, 25))
    self.XspinBox.setGeometry(QtCore.QRect(490, 50, 80, 25))
    self.YspinBox.setGeometry(QtCore.QRect(490, 90, 80, 25))

    self.CMyPos.setGeometry(QtCore.QRect(390, 185,180, 45))
    self.CMxPos.setGeometry(QtCore.QRect(390, 135, 180, 45))

    self.QyPos.setGeometry(QtCore.QRect(390, 290,180, 45))
    self.QxPos.setGeometry(QtCore.QRect(390, 240, 180, 45))

    self.sumIntensity.setGeometry(QtCore.QRect(350, 360, 220, 45))


    self.DXspinBox.setValue(self.XstepSize)
    self.DXspinBox.setMinimum(1)
    self.DXspinBox.setMaximum(20)
    self.DYspinBox.setValue(self.XstepSize)
    self.DYspinBox.setMinimum(1)
    self.DYspinBox.setMaximum(20)


    self.XspinBox.setMinimum(0)
    self.XspinBox.setMaximum(self.areaWidth)
    self.XspinBox.setValue(self.Xcenter)

    self.YspinBox.setMinimum(0)
    self.YspinBox.setMaximum(self.areaHeight)
    self.YspinBox.setValue(self.Ycenter)

    self.Ylabel = QLabel(self.central_widget)
    self.Ylabel.setGeometry(QtCore.QRect(450, 90, 60, 20))
    self.Ylabel.setObjectName("Ylabel")

    font.setPointSize(24)
    self.buttonQUIT.setFont(font)

    self.YposLabel = QLabel(self.central_widget)
    self.YposLabel.setGeometry(QtCore.QRect(200, 180, 180, 50))
    self.YposLabel.setFont(font)
    self.YposLabel.setObjectName("YposLabel")

    self.XposLabel = QLabel(self.central_widget)
    self.XposLabel.setGeometry(QtCore.QRect(200, 130, 180,50))
    self.XposLabel.setFont(font)
    self.XposLabel.setObjectName("XposLabel")

    self.sumLabel = QLabel(self.central_widget)
    self.sumLabel.setGeometry(QtCore.QRect(115, 355, 250,50))
    self.sumLabel.setFont(font)
    self.sumLabel.setObjectName("sumLabel")

    self.QXlabel = QtWidgets.QLabel(self.central_widget)
    self.QXlabel.setFont(font)
    self.QXlabel.setGeometry(QtCore.QRect(250, 235, 130, 50))
    self.QXlabel.setObjectName("QXlabel")
    self.QYlabel = QtWidgets.QLabel(self.central_widget)
    self.QYlabel.setFont(font)
    self.QYlabel.setGeometry(QtCore.QRect(250, 285, 130, 50))
    self.QYlabel.setObjectName("QYlabel")


    self.Xlabel = QLabel(self.central_widget)
    self.Xlabel.setGeometry(QtCore.QRect(450, 50, 60, 20))
    self.Xlabel.setObjectName("Xlabel")


    font.setPointSize(30)
    self.CMxPos.setFont(font)
    self.CMxPos.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
    self.CMyPos.setFont(font)
    self.CMyPos.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
    self.CMxPos.setReadOnly(True)
    self.CMxPos.setObjectName("CMxPos")    
    self.CMyPos.setReadOnly(True)
    self.CMyPos.setObjectName("CMyPos")

    font.setPointSize(20)
    self.DXlabel = QtWidgets.QLabel(self.central_widget)
    self.DXlabel.setGeometry(QtCore.QRect(240, 50, 71, 20))
    self.DXlabel.setObjectName("DXlabel")
    self.DYlabel = QtWidgets.QLabel(self.central_widget)
    self.DYlabel.setGeometry(QtCore.QRect(240, 90, 71, 20))
    self.DYlabel.setObjectName("DYlabel")    


    self.buttonUp.clicked.connect(self.stepUp)
    self.buttonDown.clicked.connect(self.stepDown)
    self.buttonLeft.clicked.connect(self.stepLeft)
    self.buttonRight.clicked.connect(self.stepRight)
    self.buttonQUIT.clicked.connect(self.myquit)

    self.image_view = ImageView(self.central_widget)
    self.image_view.ui.histogram.hide()
    self.image_view.ui.roiBtn.hide()
    self.image_view.ui.menuBtn.hide()
    #self.image_view.roi.hide()
    #self.image_view.roiCurve.hide()
    #self.image_view.normRgn.hide()
    #self.image_view.normRoi.hide()
    #self.image_view.ui.roiPlot.hideAxis('bottom')
    #self.image_view.timeLine.hide()
    #self.image_view.ui.splitter.hide()
    #self.image_view.autoRange = False
    self.image_view.setGeometry(self.videoArea.toRect())
    self.image_view.show()

    self.timer = QTimer(self)
    self.timer.timeout.connect(self.update_image)
    self.timer.setInterval(100)
    self.timer.start()
    #self.drawCircle()
        
    self.retranslateUi(self.central_widget)
    QtCore.QMetaObject.connectSlotsByName(self.central_widget)

    self.setCentralWidget(self.central_widget)

  def retranslateUi(self, mywidget):
    _translate = QtCore.QCoreApplication.translate
    mywidget.setWindowTitle(_translate("central_widget", "PSeye Capture"))
    self.buttonLeft.setText(_translate("central_widget", "Left"))
    self.buttonRight.setText(_translate("central_widget", "Right"))
    self.buttonUp.setText(_translate("central_widget", "Up"))
    self.buttonDown.setText(_translate("central_widget", "Down"))
    self.buttonQUIT.setText(_translate("central_widget", "QUIT"))
    self.DXlabel.setText(_translate("central_widget", "X stepsize:"))
    self.DYlabel.setText(_translate("central_widget", "Y stepsize:"))
    self.Xlabel.setText(_translate("central_widget", "C_x:"))
    self.Ylabel.setText(_translate("central_widget", "C_y:"))   
    self.CMxPos.setText(_translate("central_widget", "131"))
    self.CMyPos.setText(_translate("central_widget", "131"))
    self.XposLabel.setText(_translate("central_widget", "CM_x - C_x:"))
    self.YposLabel.setText(_translate("central_widget", "CM_y - C_y:"))
    Palette = self.XposLabel.palette()
    Palette.setColor(QtGui.QPalette.WindowText, QtGui.QColor(180,180,180,255))
    self.XposLabel.setPalette(Palette)
    self.YposLabel.setPalette(Palette)
    self.sumLabel.setText(_translate("central_widget", "Sum intensity:"))
    self.QXlabel.setText(_translate("central_widget", "Quad_x:"))
    self.QYlabel.setText(_translate("central_widget", "Quad_y:"))

  def set_frame_geometry(self, w, h):
    self.areaWidth = w
    self.areaHeight = h
    self.Xcenter = int(round(w))/2
    self.Ycenter = int(round(h))/2

  def drawCircle(self):
    #self.graphicsView.paint() 
    print("boohoo")

  def update_image(self):
    frame = self.camera.get_frame()
    
    #--- added by Kristof
    if self.save_frames:
        self.time_array.append(time.time())
        self.frames_array.append(frame)
    #---

    self.image_view.setImage(frame.T)
    (myCMy, myCMx) = self.camera.getCM()
    self.CMx = myCMx-self.Xcenter
    self.CMy = myCMy-self.Ycenter
    Xstr = "{:.2f}".format(self.CMx)
    Ystr = "{:.2f}".format(self.CMy)
    self.CMxPos.setText(Xstr)
    self.CMyPos.setText(Ystr)
    (QuadX, QuadY) = self.camera.getQuad(np.array((round(self.Xcenter), round(self.Ycenter))))
    Xstr = "{:.2f}".format(100*QuadX)
    Ystr = "{:.2f}".format(100*QuadY)
    self.QxPos.setText(Xstr)
    self.QyPos.setText(Ystr)
    Isum = self.camera.getSum()
    IsumText = "{0:d}".format(Isum)
    self.sumIntensity.setText(IsumText)

  def stepUp(self):
    self.Ycenter += self.DYspinBox.value()
    #print("up");
    self.YspinBox.setValue(self.Ycenter)

  def stepDown(self):
    self.Ycenter -= self.DYspinBox.value()
    self.YspinBox.setValue(self.Ycenter)

  def stepLeft(self):
    self.Xcenter -= self.DXspinBox.value()
    self.XspinBox.setValue(self.Xcenter)

  def stepRight(self):
    self.Xcenter += self.DXspinBox.value()
    self.XspinBox.setValue(self.Xcenter)

  def myquit(self):
    self.camera.close_camera()
    self.image_view.close()
    #if timer.isActive():
    self.timer.stop()
    
    #---added by Kristof
    if self.save_frames:
        np.savez(file="recorded_frames_{:s}".format(time.strftime("%Y-%m-%d_%H-%M-%S")), time=self.time_array, frames=self.frames_array)
    #---
    return self.close()

if __name__ == '__main__':
  print("IN THE MAIN OF >>webcam.py<<")
  cam = Camera(0)
  cam.initialize()
  print(cam)
  frame = cam.get_frame() #to je problem
  print(frame)
  cam.set_brightness(0.5)
  print(cam.get_brightness())
  cam.set_brightness(1)
  print(cam.get_brightness())
  cam.close_camera()
