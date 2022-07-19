from xmlrpc.server import SimpleXMLRPCServer
from xmlrpc.server import SimpleXMLRPCRequestHandler
import sys, time
from PyQt4 import QtCore, QtGui, uic
from random import randint
terminado = False
estado = 0
estado_ter = 0
serpientes = dict()
serpiente = []
dir = 3
    
class Serpiente:
   def __init__(self, tamaño,id):
    self.tamaño = tamaño
    self.cuerpo = []
    self.id = id
    self.genera_cuerpo()    
    self.color = []
    self.colorea()
    self.direccion = 3

   def dame_color(self):
   	color = {
   		"r":str(self.color[0]),
   		"g":str(self.color[1]),
   		"b":str(self.color[2]) 
   	}
   	return color
   def datos(self):
   	datos = {
   		"id": self.id,
   		"camino": self.cuerpo,
   		"color": self.dame_color(),
   	}
   	return datos

    
   def genera_cuerpo(self):
    for x in range(0,self.tamaño):
      self.cuerpo.append([x,int(self.id)])  

   def colorea(self):
    self.color.append(randint(1,255))
    self.color.append(randint(1,255))
    self.color.append(randint(1,255))
   def cambia_dir(self,dir):
    self.direccion = dir 

class Servidor(QtGui.QMainWindow):
    def __init__(self): 
        super(Servidor, self).__init__()
        uic.loadUi('servidor.ui', self)
        self.tableWidget.horizontalHeader().setResizeMode(QtGui.QHeaderView.Stretch)
        self.tableWidget.verticalHeader().setResizeMode(QtGui.QHeaderView.Stretch)
        self.tableWidget.clicked.connect(self.focus)
        self.spinBox.valueChanged.connect(self.cambia_columnas)
        self.spinBox_2.valueChanged.connect(self.cambia_filas)
        self.doubleSpinBox.valueChanged.connect(self.cambia_ms)
        self.pushButton_2.clicked.connect(self.inicia)
        self.pushButton_3.clicked.connect(self.termina)
        self.spinBox_4.valueChanged.connect(self.cambia_timeout)
        self.timer = QtCore.QTimer(self)
        self.timer.timeout.connect(self.corre_juego)
        self.k = self.doubleSpinBox.value()
        self.timer.setInterval(self.k)
        self.timerServer = QtCore.QTimer(self)       
        self.pushButton.clicked.connect(self.inicia_servidor)             
        self.setFocus()
        self.show()    
          
        
    # Inicio del juego     
    def inicia(self):
      global estado    
      self.pushButton_3.setText("Terminar")
      self.setFocus()      
      if estado == 0:
        estado = 1      
        self.colorea_serpientes()
        self.pushButton_2.setText("Pausar")
        self.corre_juego()
        self.timer.start()        
      elif estado == 1:
        estado = 2
        self.pushButton_2.setText("Renaudar")
        self.timer.stop()
        self.timerServer.stop()  
      elif estado == 2:
        estado = 1
        self.pushButton_2.setText("Pausar")
        self.corre_juego()
        self.timer.start()
        self.timerServer.start()  
      elif estado == 3:
        estado = 0
        self.inicia()    
    #Terminar el juego
    def corre_juego(self):           
      self.cambia_ms()
      self.mueve_serpientes()
      
         
    def termina(self):
      global estado
      global dir
      global terminado
      terminado = True            
      estado = 3
      dir = 3
      print("El juego ha terminado")
      self.timer.stop()
      self.timerServer.stop()
      self.pushButton_2.setText("Reiniciar")
      self.tableWidget.setColumnCount(0)
      self.tableWidget.setRowCount(0)    
      self.spinBox_2.setProperty("value", 20)
      self.doubleSpinBox.setProperty("value", 30.00)
      self.tableWidget.setColumnCount(self.spinBox.value())
      self.tableWidget.setRowCount(self.spinBox_2.value())
      serpientes.clear()
    #Cambia el delay del programa y en este se actualizan las serpientes    
    def cambia_ms(self):
      global dir         
      tiempo = self.doubleSpinBox.value()      
      self.timer.setInterval(tiempo)
    def cambia_timeout(self):
   		timeout = self.spinBox_5.value()
   		self.timerServer.setInterval(timeout)	  
    def mueve_serpientes(self):
   	    for serpiente in serpientes.values():
   	    	self.mueve_serpiente(serpiente,serpiente.direccion)
   		
    #Quita la cola y actualiza la cabeza con respecto a la dirección    
    def mueve_serpiente(self,serp,direc):           
      self.tableWidget.item(serp.cuerpo[0][0],serp.cuerpo[0][1]).setBackground(QtGui.QColor(255,255,255))
      limit_col = int(self.spinBox.value())-1
      limit_row = int(self.spinBox_2.value())-1
      cabeza = serp.cuerpo[-1]
      serp.cuerpo.pop(0)
      if direc == 1:
        if cabeza != [0, serp.cuerpo[-1][1]]: 
          serp.cuerpo.append([serp.cuerpo[-1][0]-1,serp.cuerpo[-1][1]]) #Movimiento hacia arriba
        else:
          serp.cuerpo.append([limit_row,serp.cuerpo[-1][1]])
      if direc == 2:
        if cabeza != [serp.cuerpo[-1][0],0]:
          serp.cuerpo.append([serp.cuerpo[-1][0],serp.cuerpo[-1][1]-1]) #Movimiento hacia la izquierda                                      
        else:
          serp.cuerpo.append([serp.cuerpo[-1][0], limit_row])
      if direc == 3:
        if cabeza != [limit_row, serp.cuerpo[-1][1]]:
          serp.cuerpo.append([serp.cuerpo[-1][0]+1,serp.cuerpo[-1][1]]) #Movimiento hacia abajo
        else:
          serp.cuerpo.append([0,serp.cuerpo[-1][1]])
      if direc == 4: 
        if cabeza != [serp.cuerpo[-1][0],limit_col]:
         serp.cuerpo.append([serp.cuerpo[-1][0], serp.cuerpo[-1][1]+1]) #Movimiento hacia la derecha
        else:    
          serp.cuerpo.append([serp.cuerpo[-1][0], 0])
      for x in range(0,len(serp.cuerpo)-1):        
        self.colorea_serpientes()
      colisiones = 0  
      for serpiente in serpientes.values():      		
      		if cabeza in serpiente.cuerpo:
      			colisiones+=1
      if colisiones > 1:
     		self.termina() 				
      for cuerpo in serp.cuerpo:
        if serp.cuerpo.count(cuerpo)>1:
          self.termina()
    #Cambio de columnas dinámico        
    def cambia_columnas(self):
      Columnas = int(self.tableWidget.columnCount())
      total = int(self.spinBox.value())
      if Columnas >= total:
        while Columnas >= total:
          self.tableWidget.removeColumn(Columnas)
          Columnas -= 1
      elif Columnas < total:
        while Columnas < total:
          self.tableWidget.insertColumn(Columnas)
          Columnas += 1
    #Cambio de filas dinámico      
    def cambia_filas(self):
      filas = int(self.tableWidget.rowCount())
      total = int(self.spinBox_2.value())
      if filas >= total:
        while filas >= total:
          self.tableWidget.removeRow(filas)
          filas -= 1
      elif filas < total:
        while filas < total:
          self.tableWidget.insertRow(filas)
          filas += 1      
    def juego_terminado(self):
    	return terminado           
    def colorea_serpientes(self):
      for x in serpientes.values():
        for cuerpo in x.cuerpo:
          self.tableWidget.setItem(cuerpo[0],cuerpo[1], QtGui.QTableWidgetItem())
          self.tableWidget.item(cuerpo[0],cuerpo[1]).setBackground(QtGui.QColor(x.color[0],x.color[1],x.color[2]))
    def focus(self):
      self.setFocus()            
    def ping(self):
      return "¡Pong!"
    def yo_juego(self):
      serpiente = Serpiente(11,len(serpientes))      
      serpientes[len(serpientes)] = serpiente
      datos = {
      	"id":serpiente.id,
      	"color":serpiente.dame_color()
      }
      return datos
        
    def cambia_direccion(self,id,dir):
       serpientes[id].cambia_dir(dir)
       return (str(serpientes[id])+"ha cambiado de direccion a"+str(dir))

    def estado_del_juego(self):
    	serpientx = [serpiente.datos() for serpiente in serpientes.values()]
    	datos = {
    		"espera":str(self.spinBox_5.value()),
    		"tamaño X":str(self.spinBox_2.value()),
    		"tamaño Y":str(self.spinBox.value()),
    		"serpientes":serpientx   		
    	}
    	return datos

    def inicia_servidor(self):      
      servidor = self.lineEdit.text()
      puerto = self.spinBox_4.value()
      timeou = self.spinBox_5.value()     

    # Crea el servidor para alojar a más serpientes
      server = SimpleXMLRPCServer((servidor,puerto))
      server.register_multicall_functions()      
      server.register_function(self.ping,'ping')
      server.register_function(self.yo_juego,'yo_juego')
      server.register_function(self.cambia_direccion,'cambia_direccion')
      server.register_function(self.estado_del_juego,'estado_del_juego')
      server.register_function(self.juego_terminado,'juego_terminado')
      server.register_introspection_functions()
      server.timeout = timeou
      print(server.server_address[0])
      self.spinBox_4.setValue(server.server_address[1])
      print("Servidor iniciado Servidor: "+str(servidor)+" puerto: "+str(server.server_address[1])+" timeout: "+ str(timeou))
      self.timerServer.timeout.connect(server.handle_request)
      timeout = self.spinBox_5.value()
      self.timerServer.setInterval(timeout)
      self.timerServer.start()
        


if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)
    serv = Servidor()
    sys.exit(app.exec_())        
        
