#ifndef MAINWINDOW_H
#define MAINWINDOW_H

#include <QMainWindow>
#include <QShortcut>
#include <QKeySequence>
#include <qwt_plot.h>
#include <qwt_plot_curve.h>
#include <qwt_legend.h>  // Include the header for QwtLegend
#include <algorithm>
#include <cmath>

// My libraries
#include "DisplayWindow.h"


QT_BEGIN_NAMESPACE
namespace Ui { class MainWindow; }
QT_END_NAMESPACE

class MainWindow : public QMainWindow
{
    Q_OBJECT

public:
    MainWindow(QWidget *parent = nullptr);
    ~MainWindow();


private:
    QwtPlot *plot;
    Ui::MainWindow *ui;
    uint32_t expTime = 200;
    QString strexpTime = "200";

};
#endif // MAINWINDOW_H
