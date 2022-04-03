import mraa
import time
import serial
import threading
import Queue
from cgi import parse_qs
from wsgiref.simple_server import make_server


# # nameOfServer = ["mysmartfanserver_v",
# #                 "mysmartlightserver_v",
# #                 "mysmartsocketserver_v",
# #                 "mysmartdiffserver_v"] 

# status = {
#     'FAN':1,
#     'LIGHT':1,
#     'DIFFUSER':1,
#     'SOCKET':1,
# }

gpio_output = mraa.Gpio(4)

gpio_output.dir(mraa.DIR_OUT)

q = Queue.Queue()
response = Queue.Queue()

def doAction(queue, chip_id):

    def statusConvert(status, is_fan):
        retVal = 0
        if status == 'off':
            retVal = 0
        if (status == 'slow') & (is_fan == True):
            retVal = 1
        if (status == 'normal') & (is_fan == True):
            retVal = 2
        if (status == 'high') & (is_fan == True):
            retVal = 3
        if (status == 'on') & (is_fan == False):
            retVal = 4
        
        return retVal

    print('Listening')
    while(1):
        data = queue.get()['data']
        print('Inside queue: ', data)
        if (data):
            print('Output: {}'.format(data[1]))
            if data[1] == 'on':
                if chip_id == "linkit 7688 duo":        
                    serial_port.write("1")
                else:
                    gpio_output.write(1)
                response.put({"Status":"Done"})
            elif data[1] == 'off':
                if chip_id == "linkit 7688 duo":        
                    serial_port.write("0")
                else:
                    gpio_output.write(0)
                response.put({"Status":"Done"})
            else:
                response.put({"Status":"NotOK"})
        
        queue.task_done()
        
def gateway_handler(environ, start_response):
    print('listener')
    status = '200 OK'
    headers = [('Content-Type', 'text/plain:charset=utf-8')]
    start_response(status, headers)
    if environ['REQUEST_METHOD'] == 'POST':
        request_body_size = int(environ.get('CONTENT_LENGTH', 0))
        request_body = environ['wsgi.input'].read(request_body_size)
        d = parse_qs(request_body)  # turns the qs to a dict\
        print(d) # For debugging
        q.put(d)
        # return 'From POST: %s' % ''.join('%s: %s' % (k, v) for k, v in d.iteritems())
        return 'From POST: {}'.format(d)
    else:  # GET
        if response.empty():
            response.put({'Status':'NotOK'})
        # d = parse_qs(environ['QUERY_STRING'])  # turns the qs to a dict
        # text = 'From GET: {}'.format(d)
        # terminal_print(text)
        # return 'From GET: %s' % ''.join('%s: %s' % (k, v) for k, v in d.iteritems())
        return 'From GET: {}'.format(response.get()['Status'])


if __name__ == '__main__':
    file = open("/IoT/examples/chip_info.txt")
    chip_id = file.readline()
    print(chip_id)
    if (chip_id == "linkit 7688 duo"):
        global serial_port
        serial_port = serial.Serial("/dev/ttyS0",57600)
    httpd = make_server('', 1337, gateway_handler)
    # httpd.server_close()
    t1 = threading.Thread(target=httpd.serve_forever)
    t2 = threading.Thread(target=doAction, args=(q,chip_id))
    t1.start()
    t2.start()
    # t1 = threading.Thread(target=blinking, args=(gpio_socket,))
    # t2 = threading.Thread(target=blinking, args=(gpio_light,))
    # t3 = threading.Thread(target=blinking, args=(gpio_diffuser,))
    # t4 = threading.Thread(target=blinking, args=(gpio_fan,))
    # t1.start()
    # t2.start()
    # t3.start()
    # t4.start()
        