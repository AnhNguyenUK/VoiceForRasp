import requests
import re

class Server_list:
    def __init__(self) -> None:
        self.fanServerUrl = "http://root@mysmartfanserver.local:1337"
        self.lightServerUrl = "http://root@mysmartlightserver.local:1337"
        self.diffuserServerUrl = "http://root@mysmartdiffserver.local:1337"
        self.socketServerUrl = "http://root@mysmartsocketserver.local:1337"

class Server_socket:
    def __init__(self, name, urls) -> None:
        self.name = name
        self.data_pattern = ".*:(.*)"
        self.url = urls
        self.status = ""
        
    def get_current_status(self):
        return self.status    
        
    def get_response(self):
        status = ""
        try:
            request = requests.get(self.url)
            self.status = re.findall(self.data_pattern,request.text)[0].replace(" ","") 
            status = "success"
        except Exception:
            print("Connection error")
            status = "failed"
        return status
    
    def post_data(self, objData):
        status = ""
        try:
            request = requests.post(self.url,data = objData)
            status = "success"
        except:
            print("Connection error")
            status = "failed"
        return status
        
# For testing only
if __name__ == '__main__':
    server_list = Server_list()
    fan_client = Server_socket("SOCKET",server_list.socketServerUrl)
    errorCode = fan_client.post_data({'data':['SOCKET','on']})
    if errorCode == "success":
        errorCode = fan_client.get_response()
    if (errorCode == "success") & (fan_client.get_current_status() == "Done"):
        print('Done')
        errorCode = fan_client.post_data({'data':['SOCKET','off']})
    if errorCode == "success":
        errorCode = fan_client.get_response()
    if (errorCode == "success") & (fan_client.get_current_status() == "Done"):
        print("Done")
    # objData = {'data':['LIGHT','on']}
    # x1 = requests.post(fanServerUrl,data = objData)
    # print(x1.text)
    # objData = {'data':['LIGHT','off']}
    # x1 = requests.post(fanServerUrl,data = objData)
    # print(x1.text)
    # regex = ".*:(.*)"
    # x2 = requests.get(fanServerUrl)
    # text = re.findall(regex,x2.text)[0].replace(" ","") 
    # print(text)