from PyQt6 import QtWidgets as qt, uic
from PyQt6.QtGui import *
from PyQt6 import QtCore
import sys
from Image_Threshold import*
import numpy as np
from pathlib import Path
class ChooseThreshold(qt.QLabel):
    def __init__(self, window, Image):
        super().__init__()
        image = QImage()
        self.blockv = 15
        self.prv = 15
        self.koeff = 0.1
        self.setWindowTitle('Выбор формата')
        self.label1, self.label, self.label3, self.label4 = qt.QLabel(self),  qt.QLabel(self),   qt.QLabel(self),  qt.QLabel(self)
        self.bern, self.equi, self.mean, self.gaus, self.gblur, self.boxblur = qt.QPushButton(self), qt.QPushButton(self), qt.QPushButton(self),         qt.QPushButton(self), qt.QPushButton(self), qt.QPushButton(self)
        
        self.label1.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.label3.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.label4.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        
        
        self.blocklabel = qt.QLabel(self)
        self.koeflabel = qt.QLabel(self)
        self.blocksize = qt.QSpinBox(self)
        self.blocksize.setRange(1, 31)
        self.blocksize.setValue(15)
        self.blocksize.valueChanged.connect(self.changeblock)
        self.koef = qt.QDoubleSpinBox(self)
        self.koef.setRange(0.1, 0.3)
        self.koef.valueChanged.connect(self.changekoef)
        
        self.h1 = qt.QHBoxLayout()
        self.h1.addWidget(self.label)
        self.h1.addWidget(self.label3)
        self.label.setText("Локальная")
        self.label3.setText("Адаптивная")
        
        self.h = qt.QHBoxLayout()
        self.h.addWidget(self.bern)
        self.h.addWidget(self.equi)
        self.h.addWidget(self.mean)
        self.h.addWidget(self.gaus)
        self.bern.setText("Бернсен")
        self.equi.setText("Эквилл")
        self.mean.setText("Мягкая")
        self.gaus.setText("Гаусс")
        
        self.v1 = qt.QVBoxLayout()
        self.v1.addWidget(self.label1)
        self.v1.addLayout(self.h1)
        self.v1.addLayout(self.h)
        self.label1.setText("Пороговая")
        
        self.h3 = qt.QHBoxLayout()
        self.h3.addWidget(self.gblur)
        self.h3.addWidget(self.boxblur)
        self.gblur.setText("Гауссово размытие")
        self.boxblur.setText("Box размытие")
        
        self.v = qt.QVBoxLayout()
        self.v.addWidget(self.label4)
        self.v.addLayout(self.h3)
        self.label4.setText("Низкочастотные фильтры")
        self.label4.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        
        self.h4 = qt.QHBoxLayout()
        self.h4.addWidget(self.blocklabel)
        self.h4.addWidget(self.blocksize)
        self.blocklabel.setText("Размер блока")

        self.h5 = qt.QHBoxLayout()
        self.h5.addWidget(self.koeflabel)
        self.h5.addWidget(self.koef)
        self.koeflabel.setText("Коэффициент")

        self.h6 = qt.QHBoxLayout()
        self.h6.addLayout(self.v1)
        self.h6.addLayout(self.v)
             

        self.v3 = qt.QVBoxLayout(self)
        self.v3.addLayout(self.h6)
        self.v3.addLayout(self.h4)
        self.v3.addLayout(self.h5)
        
        self.image = Image
        self.changed = False
        self.bern.clicked.connect(self.bernt)
        self.equi.clicked.connect(self.equit)
        self.gaus.clicked.connect(self.gaust)
        self.boxblur.clicked.connect(self.boxt)
        self.mean.clicked.connect(self.meant)
        self.gblur.clicked.connect(self.gausblurt)
        self.name = ''
        self.Win = window
    def cv2_to_pixmap(self):
        #cv2.imshow('aboba', self.image)
        image_rgb = cv2.cvtColor(self.image, cv2.COLOR_BGR2RGB)
        _, buffer = cv2.imencode('.png', image_rgb)
        image_data = buffer.tobytes()
        q_image = QImage.fromData(image_data)
        return QPixmap.fromImage(q_image)
    #Мягкая адаптивная - blocksize, c
    #Адаптивная гауссовая - blocksize, c
    #Гауссово размытие
    #Бокс-фильтр -
    def changeblock(self, value):
        if value % 2 == 0:
            if value > self.prv:
                self.blocksize.setValue(value+1)
            else:
                self.blocksize.setValue(value - 1)
        else:
            self.prv = value
            self.blockv = value
    def changekoef(self, value):
        self.koeff = value
    def meant(self):
        self.name = 'Мягкая адаптивная обработка'
        gray_image = cv2.cvtColor(self.image, cv2.COLOR_BGR2GRAY)
        self.image = cv2.adaptiveThreshold(gray_image, 255, 
                                              cv2.ADAPTIVE_THRESH_MEAN_C, 
                                              cv2.THRESH_BINARY, 
                                              blockSize=self.blockv, 
                                              C=2)
        self.changed = True
        self.close()
    def gaust(self):
        self.name = 'Адаптивная гауссова обработка'
        gray_image = cv2.cvtColor(self.image, cv2.COLOR_BGR2GRAY)
        self.image = cv2.adaptiveThreshold(gray_image, 255, 
                                              cv2.ADAPTIVE_THRESH_GAUSSIAN_C, 
                                              cv2.THRESH_BINARY, 
                                              blockSize=self.blockv, 
                                              C=2)
        self.changed = True
        self.close()
    def gausblurt(self):
        self.name = 'Гауссов низкочастотный фильтр'
        self.image = cv2.GaussianBlur(self.image, (self.blockv, self.blockv), 0)
        self.changed = True
        self.close()
    def boxt(self):
        self.name = 'Бокс-фильтр'
        self.image = cv2.boxFilter(self.image, ddepth=-1, ksize=(self.blockv, self.blockv))
        self.changed = True
        self.close()
    def bernt(self):
        self.name = 'Бернсен'
        self.image = bernsen_thresholding(self.image, self.blockv, self.koeff)
        self.changed = True
        self.close()
    def equit(self):
        self.name = 'Эйквилл'
        self.image = equi_threshold(self.image, self.blockv)
        self.changed = True
        self.close()
    def closeEvent(self, event):
        if self.changed:
            self.Win.newImage = self.cv2_to_pixmap()
            self.Win.UpdateNew(self.name)
        self.Win.show()
        event.accept()
        
        
class Window(qt.QWidget):
    def __init__(self):
        super().__init__()
        #######################
        self.Grid = qt.QGridLayout()
        self.setLayout(self.Grid)
        self.Source_Name, self.Source_Image, self.Threshold_Image, self.Threshold_Name = qt.QLabel(self), qt.QLabel(self), qt.QLabel(self), qt.QLabel(self)
        self.ChsThres, self.Image_Choose = qt.QPushButton(self), qt.QPushButton(self)
        self.Source_Name.setText("Исходное изображение")
        self.Threshold_Name.setText("Отсутствие обработки")
        self.ChsThres.setText("Выбор обработки")
        self.Image_Choose.setText("Выбор изображения")
        self.Source_Name.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.Threshold_Name.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.Grid.addWidget(self.Source_Name, 0, 0)
        self.Grid.addWidget(self.Source_Image, 0, 1)
        self.Grid.addWidget(self.Threshold_Name, 1, 0)
        self.Grid.addWidget(self.Threshold_Image, 1, 1)
        self.Grid.addWidget(self.ChsThres, 2, 0)
        self.Grid.addWidget(self.Image_Choose, 2, 1)
        self.ChsThres.setEnabled(False)
        self.resize(600, 600)
        ########################
        self.Image_Choose.clicked.connect(self.ChoiceDialog)
        self.ChsThres.clicked.connect(self.OpChs)
        ########################
        self.pixmap = QPixmap()
        self.newImage = QPixmap()
    def OpChs(self):
            self.ct = ChooseThreshold(self, self.OpenImage)
            self.ct.show()
            self.hide()

    def ChoiceDialog(self):
        path = qt.QFileDialog.getOpenFileName(self, 'ChooseImage', '', "Image Files(*.jpg *.bmp *.BMP *.png *.pcx *.tif)")
        if path[0] != '':
            self.pixmap = QPixmap(path[0])
            self.OpenImage = cv2.imread(path[0])
            if self.OpenImage is None or self.pixmap is None:
                print("hell")
            else:
                print('ye')
                self.Source_Image.setPixmap(self.pixmap.scaled(self.Source_Image.width(), self.Source_Image.height(),
                                                           QtCore.Qt.AspectRatioMode.KeepAspectRatio))
        ################################
                self.ChsThres.setEnabled(True)
                self.OpChs()
    def UpdateNew(self, name):
        print(name)
        self.Threshold_Name.setText(name)
        self.Threshold_Image.setPixmap(self.newImage.scaled(self.Threshold_Image.width(), self.Threshold_Image.height(),
                                                       QtCore.Qt.AspectRatioMode.KeepAspectRatio))
        