#ifndef DISPLAYWINDOW_H
#define DISPLAYWINDOW_H

#include <QDialog>
#include <QLabel>
#include <QString>
#include <QVBoxLayout>

class DisplayWindow : public QDialog {
    Q_OBJECT

public:
    explicit DisplayWindow(const QString &text, QWidget *parent = nullptr) : QDialog(parent) {
        QVBoxLayout *layout = new QVBoxLayout(this);
        QLabel *label = new QLabel(text, this);
        layout->addWidget(label);
        setLayout(layout);
        setWindowTitle("Display Window");
        resize(200, 100);
    }
};

#endif // DISPLAYWINDOW_H
