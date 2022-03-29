import mraa
import time
import threading
import Queue
from cgi import parse_qs
from wsgiref.simple_server import make_server


nameOfServer = ["mysmartfanserver",
                "mysmartlightserver",
                "mysmartsocketserver",
                "mysmart"] 

status = {
    'FAN':1,
    'LIGHT':1,
    'DIFFUSER':1,
    'SOCKET':1,
}

gpio_output = mraa.Gpio(4)

gpio_output.dir(mraa.DIR_OUT)

q = Queue.Queue()

def doAction(queue):

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
        print('Inside queue: ', queue.get())
        data = queue.get()['data']
        print(data)
        if (data):
            print('Output: {}'.format(data[1]))
            if data[1] == 'on':        
                gpio_output.write(1)
            elif data[1] == 'off':
                gpio_output.write(0)
        
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
        d = parse_qs(environ['QUERY_STRING'])  # turns the qs to a dict
        print(d)
        # return 'From GET: %s' % ''.join('%s: %s' % (k, v) for k, v in d.iteritems())
        return 'From GET: {}'.format(d)


if __name__ == '__main__':
    httpd = make_server('', 1337, gateway_handler)
    # httpd.server_close()
    t1 = threading.Thread(target=httpd.serve_forever)
    t2 = threading.Thread(target=doAction, args=(q,))
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
        