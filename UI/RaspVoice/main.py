# This Python file uses the following encoding: utf-8
from ast import arg
import os
from pathlib import Path
import sys

from PySide2.QtCore import QObject, Qt, Slot, Property, Signal
from PySide2.QtGui import QGuiApplication, QStandardItemModel, QStandardItem 
from PySide2.QtQml import QQmlApplicationEngine

from server_connection import Server_list, Server_socket 


class ElementRoles:
    NameRole = Qt.UserRole
    ValueRole = Qt.UserRole + 1

class ElementModel(QStandardItemModel, ElementRoles):
    
    def __init__(self, parent=None):
        super(ElementModel, self).__init__(parent)
        roles = {
            ElementModel.NameRole: b'mcmdName',
            ElementModel.ValueRole: b'mcmdValue'
        }
        self.setItemRoleNames(roles)

    @Slot(str, str)
    def addElement(self, name, value):
        item = QStandardItem()
        item.setData(name, ElementModel.NameRole)
        item.setData(value, ElementModel.ValueRole)
        self.appendRow(item)


class Manager(QObject):
    def __init__(self, parent=None):
        super(Manager, self).__init__(parent)
        self._model = ElementModel()

    def addData(self, data):
        print(data)
        self._model.addElement(data[0],data[1])  
    
    @Property(QObject, constant=True)
    def model(self):
        return self._model
        
class serverConnector(QObject):
    def __init__(self, parent=None) :
        super(serverConnector,self).__init__(parent)
        server_list = Server_list()
        self.fan_client = Server_socket("FAN",server_list.fanServerUrl)
        self.light_client = Server_socket("LIGHT",server_list.lightServerUrl)
        self.diffuser_client = Server_socket("DIFFUSER",server_list.diffuserServerUrl)
        self.socket_client = Server_socket("SOCKET",server_list.socketServerUrl)
        self.client_list = {"FAN":self.fan_client, 
                            "LIGHT":self.light_client,
                            "DIFFUSER":self.diffuser_client,
                            "SOCKET":self.socket_client}
    
    @Slot(str,str)        
    def sendData(self,data_id,data):
        errorCode = self.client_list[data_id].post_data({'data':[data_id,data]})
        if errorCode == "success":
            errorCode = self.client_list[data_id].get_response()
        return errorCode    
    @Slot()    
    def getSendingStatus(self):
        return 
        
if __name__ == "__main__":
    app = QGuiApplication(sys.argv)
    dataModel = Manager()
    client = serverConnector()
    server_list = Server_list()
    data = [
        ["Fans", server_list.fanServerUrl],
        ["Lights", server_list.lightServerUrl],
        ["Diffuser", server_list.diffuserServerUrl],
        ["Socket", server_list.socketServerUrl]
       ]
    
    engine = QQmlApplicationEngine()
    
    for item in data:
        print(item[0],"/",item[1])
        dataModel.addData(item)
        
    engine.rootContext().setContextProperty("dataModel",dataModel)    
    engine.rootContext().setContextProperty("client",client)            
    engine.load(os.fspath(Path(__file__).resolve().parent / "main.qml"))
    if not engine.rootObjects():
        sys.exit(-1)
    sys.exit(app.exec_())
