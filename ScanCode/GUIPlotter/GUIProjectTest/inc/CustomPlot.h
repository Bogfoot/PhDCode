#ifndef CUSTOMPLOT_H
#define CUSTOMPLOT_H

#include <qwt_plot.h>
#include <QMouseEvent>
#include <QPen>

#include "DisplayWindow.h"

class CustomPlot : public QwtPlot {
    Q_OBJECT

public:
    explicit CustomPlot(QWidget *parent = nullptr);

protected:
    void mousePressEvent(QMouseEvent *event) override;
};

#endif // CUSTOMPLOT_H
