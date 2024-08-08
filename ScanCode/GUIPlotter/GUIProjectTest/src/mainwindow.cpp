#include <QVBoxLayout>

#include "inc/MainWindow.h"
#include "inc/CustomPlot.h"

MainWindow::MainWindow(QWidget *parent)
    : QMainWindow(parent), plot(new CustomPlot(this))
    //, ui(new Ui::MainWindow)
{
    // Create a shortcut for closing the main window
    QShortcut *shortcut = new QShortcut(QKeySequence(Qt::Key_Q), this);
    connect(shortcut, &QShortcut::activated, this, &QMainWindow::close);
    //ui->setupUi(this);
    //ui->expTime_edit->setFocusPolicy(Qt::NoFocus);

    QWidget *centralWidget = new QWidget(this);
    QVBoxLayout *layout = new QVBoxLayout(centralWidget);

    QwtLegend *legend = new QwtLegend();
    plot->insertLegend(legend);

    plot->setTitle("Simple Plot");
    plot->setCanvasBackground(Qt::white);
    QPen pen(Qt::red); // Set the pen color to red
    pen.setWidth(2);  // Set the pen width

    QwtPlotCurve *curve = new QwtPlotCurve("Curve 1");
    curve->setRenderHint(QwtPlotItem::RenderAntialiased);

    QVector<double> xData = {0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10};
    QVector<double> yData = {0, 1, 4, 9, 16, 25, 36, 49, 64, 81, 100};
    curve->setSamples(xData, yData);
    curve->attach(plot);
    curve->setPen(pen);

    QwtPlotCurve *curve2 = new QwtPlotCurve("Curve 1");
    std::transform(xData.begin(), xData.end(), yData.begin(), [](double x) {
           return std::pow(x, 3);
       });
    curve2->setSamples(yData, yData);
    curve2->attach(plot);

    layout->addWidget(plot);
    setCentralWidget(centralWidget);
}

MainWindow::~MainWindow()
{
    delete plot;
}
