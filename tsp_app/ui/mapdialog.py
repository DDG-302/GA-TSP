from PyQt5.QtWidgets import QDialog
from PyQt5.QtGui import QPainter,QPen,QColor
from PyQt5.QtCore import QThread
from ai.tsp import TSP
import random

class MapDialog(QDialog):
    def __init__(self,node_position, epoch, init_size, p_mutation, size_of_population):
        # 传入初始节点位置
        super(MapDialog,self).__init__()
        self.setWindowTitle("遗传算法处理TSP")
        self.resize(800,800)
        self.move(400,100)
        self.tsp =TSP(epoch=epoch,init_size=init_size,p_mutation=p_mutation,size_of_population=size_of_population)
        self.tsp.draw_dlg.connect(self.set_route_and_draw)
        self.tsp.start()
        self.node_position = node_position # 节点位置
        # 设置画笔
        self.color = QColor(255,0,255)
        self.pen = QPen(self.color, 2.0)
        self.switch = 1 # 控制绘图事件
        self.route = [i for i in range(1, len(self.node_position) + 1)] 
        self.repaint()

    

    def set_route_and_draw(self,route):
        self.route = route
        self.repaint()


    
    def paintEvent(self,e):
        # self.draw_map()
        painter = QPainter(self)
        painter.setPen(self.pen)
        self.draw_map(painter)
        self.draw_line(painter)
        # print("draw")



    def draw_map(self,g):
        for x1,y1 in self.node_position:     
           g.drawRect(x1, y1, 9, 9)
            

    def draw_line(self,g):
        color = QColor(0,0,0)
        pen = QPen(color, 4.0)
        g.setPen(pen)
        for i in range(len(self.route)-1):
            x1 = self.node_position[self.route[i]-1][0]
            y1 = self.node_position[self.route[i]-1][1]
            x2 = self.node_position[self.route[i+1]-1][0]
            y2 = self.node_position[self.route[i+1]-1][1]
            g.drawLine(x1,y1,x2,y2)



