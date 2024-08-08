QT       += core gui

greaterThan(QT_MAJOR_VERSION, 4): QT += widgets

CONFIG += c++11
CONFIG += qwt

# Include path for qwt
INCLUDEPATH += /usr/local/qwt-6.3.0/include
INCLUDEPATH += $$PWD/inc

# Library path for Qwt
LIBS += -L/usr/lib -lqwt-qt5

# Library path for libtdcbase
LIBS += -L$$PWD/lib

# Libraries to link against
LIBS += -ltdcbase

SOURCES += \
    src/CustomPlot.cpp \
    main.cpp \
    src/mainwindow.cpp

HEADERS += \
    inc/CustomPlot.h \
    inc/DisplayWindow.h \
    inc/MainWindow.h

FORMS += \
    mainwindow.ui \

# Default rules for deployment.
qnx: target.path = /tmp/$${TARGET}/bin
else: unix:!android: target.path = /opt/$${TARGET}/bin
!isEmpty(target.path): INSTALLS += target

# Additional compiler flags (optional)
QMAKE_CXXFLAGS += -Wall -Wextra
