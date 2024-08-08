#include "inc/CustomPlot.h"
#include <QDebug>
#include <qwt_scale_map.h>
#include <qwt_scale_draw.h>
#include <qwt_plot_canvas.h>

CustomPlot::CustomPlot(QWidget *parent)
    : QwtPlot(parent)
{
    // Initialization code (if needed)
}

void CustomPlot::mousePressEvent(QMouseEvent *event) {
    if (event->button() == Qt::LeftButton) {
        // Convert mouse position to plot coordinates
        QPoint pos = event->pos();
        double xValue = pos.x();
        double yValue = pos.y();    // Create and show the new display window
        DisplayWindow *displayWindow = new DisplayWindow(QString::number(xValue) + QString(", ") + QString::number(yValue) , this);
        displayWindow->exec(); // Use exec() for modal dialog, show() for non-modal
}

    // Call base class implementation if you want to retain default behavior
    QwtPlot::mousePressEvent(event);
}
