import math
import sys

from PyQt5.QtCore import QObject, QSize
from PyQt5.QtDataVisualization import (Q3DSurface, QSurface3DSeries, QSurfaceDataItem, QSurfaceDataProxy, QValue3DAxis)
from PyQt5.QtGui import QVector3D
from PyQt5.QtWidgets import (QApplication, QHBoxLayout, QWidget)


class SurfaceGraph(QObject):

    sampleCountX = 50
    sampleCountZ = 50
    sampleMin = -8.0
    sampleMax = 8.0

    def __init__(self, surface):
        super(SurfaceGraph, self).__init__()

        self.m_graph = surface
        self.m_graph.setAxisX(QValue3DAxis())
        self.m_graph.setAxisY(QValue3DAxis())
        self.m_graph.setAxisZ(QValue3DAxis())
        self.m_sqrtSinProxy = QSurfaceDataProxy()
        self.m_sqrtSinSeries = QSurface3DSeries(self.m_sqrtSinProxy)
        self.fillSqrtSinProxy()
        self.m_graph.addSeries(self.m_sqrtSinSeries)

    def fillSqrtSinProxy(self):
        stepX = (self.sampleMax - self.sampleMin) / (self.sampleCountX - 1)
        stepZ = (self.sampleMax - self.sampleMin) / (self.sampleCountZ - 1)

        dataArray = []
        for i in range(self.sampleCountZ):

            # Keep values within range bounds, since just adding step can cause
            # minor drift due to the rounding errors.
            z = min(self.sampleMax, (i * stepZ + self.sampleMin))
            newRow = []
            for j in range(self.sampleCountX):
                x = min(self.sampleMax, (j * stepX + self.sampleMin))
                R = math.sqrt(z * z + x * x) + 0.01
                y = (math.sin(R) / R + 0.24) * 1.61
                newRow.append(QSurfaceDataItem(QVector3D(x, y, z)))
            dataArray.append(newRow)

        self.m_sqrtSinProxy.resetArray(dataArray)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    graph = Q3DSurface()
    container = QWidget.createWindowContainer(graph)
    screenSize = graph.screen().size()
    container.setMinimumSize(QSize(screenSize.width() / 2, screenSize.height() / 1.3))
    container.setMaximumSize(screenSize)
    widget = QWidget()
    hLayout = QHBoxLayout(widget)
    hLayout.addWidget(container, 1)
    widget.setWindowTitle("Surface example")
    widget.show()
    modifier = SurfaceGraph(graph)
    sys.exit(app.exec_())
