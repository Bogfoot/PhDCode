#include "inc/MainWindow.h"

#include <QApplication>
#include <QLineEdit>
#include <QWidget>

int main(int argc, char *argv[])
{
    QApplication app(argc, argv);
    MainWindow window;


    window.setWindowTitle("Bogfoot's Corner");
    window.show();

    return app.exec();
}
