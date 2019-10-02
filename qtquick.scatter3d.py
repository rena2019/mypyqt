
import sys

#QtQuick example: Data Visualization https://doc.qt.io/qt-5/qml-qtdatavisualization-scatter3d.html#details

from PyQt5.QtCore import QUrl
from PyQt5.QtGui import QGuiApplication
from PyQt5.QtQuick import QQuickView

if __name__ == '__main__':
    app = QGuiApplication(sys.argv)
    view = QQuickView()
    view.setSource(QUrl('qtquick.scatter3d.qml'))
    view.show()
    sys.exit(app.exec_())