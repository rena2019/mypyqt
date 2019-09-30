import sys
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import QObject, QSize
from PyQt5.QtDataVisualization import (Q3DCamera, Q3DScatter,QScatter3DSeries,QScatterDataItem, QScatterDataProxy)
from PyQt5.QtGui import QVector3D
from PyQt5.QtWidgets import (QApplication, QHBoxLayout, QWidget)

#Simple QtDataVisualization example with Q3DScatter

class ScatterDataModifier(QObject):
    def __init__(self, scatter):
        super(ScatterDataModifier, self).__init__()
        self.m_graph = scatter
        self.m_graph.scene().activeCamera().setCameraPreset(Q3DCamera.CameraPresetFront)
        proxy = QScatterDataProxy()
        series = QScatter3DSeries(proxy)
        self.m_graph.addSeries(series)
        self.addData()
    
    def addData(self):
        dataArray = []
        for i in range(10):
            itm = QScatterDataItem(QVector3D(i,i,i))
            dataArray.append(itm)
        self.m_graph.seriesList()[0].dataProxy().resetArray(dataArray)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    graph = Q3DScatter()
    container = QWidget.createWindowContainer(graph)
    screenSize = graph.screen().size()
    container.setMinimumSize(QSize(screenSize.width() / 2, screenSize.height() / 1.3))
    widget = QWidget()
    hLayout = QHBoxLayout(widget)
    hLayout.addWidget(container, 1)
    modifier = ScatterDataModifier(graph)
    widget.show()
    sys.exit(app.exec())
