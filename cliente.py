import xmlrpc.client
import sys, time
from PyQt4 import QtCore, QtGui, uic

dir = 3
class Cliente(QtGui.QMainWindow):
    def __init__(self): 
        super(Cliente, self).__init__()
        uic.loadUi('cliente.ui', self)
        self.tableWidget.horizontalHeader().setResizeMode(QtGui.QHeaderView.Stretch)
        self.tableWidget.verticalHeader().setResizeMode(QtGui.QHeaderView.Stretch)
        self.tableWidget.clicked.connect(self.focus)
        self.pushButton.clicked.connect(self.ping)
        self.pushButton_2.clicked.connect(self.participar)
        self.cliente = object()
        self.part = object()
        self.estado = object()
        self.setFocus()
        self.timer = QtCore.QTimer(self)
        self.timer.timeout.connect(self.actualiza)                
        self.show()

        #Conecta a un servidor
    def ping(self):
        servidor = self.lineEdit.text()
        puerto = self.spinBox_4.value()
        url = "http://"+str(servidor)+":"+str(puerto)
        self.cliente = xmlrpc.client.ServerProxy(url)
        print
        try: 
            pong = self.cliente.ping()
            self.pushButton.setText("pinging...")
            if pong == "¡Pong!":
                self.pushButton.setText("¡Pong!")
        except:        
            self.pushButton.setText("No pong :c")

        #Crea una serpiente para poder jugar    
    def participar(self):
            self.part = self.cliente.yo_juego()
            self.lineEdit_2.setText(str(self.part["id"]))
            self.lineEdit_3.setText(str(self.part["color"]))
            color = "color: "+"rgb("+str(self.part["color"]["r"])+", "+str(self.part["color"]["g"])+", "+str(self.part["color"]["b"])+");"            
            self.lineEdit_3.setStyleSheet(color)
            self.lineEdit_2.setStyleSheet(color)
            self.timer.start()
        #Maneja los eventos de las teclas    
    def keyPressEvent(self, event):
      global dir      
      key = event.key()      
      if key == QtCore.Qt.Key_Left and dir != 4:
        dir = 2        
        self.cliente.cambia_direccion(self.part["id"],dir)
      if key == QtCore.Qt.Key_Right and dir != 2:
        dir = 4        
        self.cliente.cambia_direccion(self.part["id"],dir) 
      if key == QtCore.Qt.Key_Up and dir != 3:
        dir = 1        
        self.cliente.cambia_direccion(self.part["id"],dir) 
      if key == QtCore.Qt.Key_Down and dir != 1:
        dir = 3        
        self.cliente.cambia_direccion(self.part["id"],dir)
        #Actualiza las serpientes en el cliente
    def colorea_serpientes(self,serpientes):
        self.tableWidget.setColumnCount(0)
        self.tableWidget.setRowCount(0)
        self.tableWidget.setColumnCount(int(self.estado["tamaño X"]))
        self.tableWidget.setRowCount(int(self.estado["tamaño Y"]))
        self.focus() 
        for serp in serpientes:
            for cuerpo in serp["camino"]:
                self.tableWidget.setItem(cuerpo[0],cuerpo[1], QtGui.QTableWidgetItem())
                self.tableWidget.item(cuerpo[0],cuerpo[1]).setBackground(QtGui.QColor(int(serp["color"]["r"]),int(serp["color"]["g"]),int(serp["color"]["b"])))
        #Actualiza todos los estados        
    def actualiza(self):
        if not self.cliente.juego_terminado():
            self.estado = self.cliente.estado_del_juego()   
            espera = self.estado["espera"]
            tamx = self.estado["tamaño X"]
            if(tamx != self.tableWidget.columnCount()):
                self.cambia_columnas(int(tamx))           
            tamy = self.estado["tamaño Y"]
            if(tamy != self.tableWidget.rowCount()): 
                self.cambia_filas(int(tamy))
            serpientes = self.estado["serpientes"]
            self.colorea_serpientes(serpientes)
            self.timer.setInterval(float(espera))
        else:
            self.timer.stop()
            print("JUEGO TERMINADO")            
        #Da foco al tablewidget
    def focus(self):
      self.setFocus()
        #Cambio de columnas dinámico        
    def cambia_columnas(self,cols):
      self.tableWidget.setColumnCount(cols)
        #Cambio de filas dinámico      
    def cambia_filas(self,rows):
      self.tableWidget.setRowCount(rows)  

if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)
    serv = Cliente()
    sys.exit(app.exec_())     