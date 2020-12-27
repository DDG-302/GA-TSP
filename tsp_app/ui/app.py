from ui.mapdialog import MapDialog
import sys
from PyQt5.QtWidgets import QApplication

class Tspapp(QApplication):
    node_position = [
            [76,56],
            [144,48],
            [255,8],
            [288,293],
            [69,393],
            [142,255],
            [360,383],
            [455,260],
            [347,528],
            [206,402],
            [150,343],
            [15,50],
            [750,241],
            [343,121],
            [56,139],
            [25,776],
            [131,232],
            [76,330],
            [15,670],
            [521,144]
            ]
    def __init__(self, epoch, init_size, p_mutation, size_of_population):
        super(Tspapp,self).__init__(sys.argv)

        self.dlg = MapDialog(self.node_position,epoch, init_size, p_mutation, size_of_population)
        self.dlg.show()
        # self.dlg.run()


