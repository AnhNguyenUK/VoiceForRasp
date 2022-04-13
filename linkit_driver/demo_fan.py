import mraa
import time
import threading
import Queue
from cgi import parse_qs
from wsgiref.simple_server import make_server

gpio_output = mraa.Gpio(19)

q = Queue.Queue()
response = Queue.Queue()

fan_speed_mode = {"off":0.01, "low":0.33, "normal":0.67, "high":0.99}

def doAction(queue):
    
    print('Listening')
    while(1):
        data = queue.get()['data']
        print('Inside queue: ', data)
        if (data):
            currState = data[1]
            print('Output: {}'.format(currState))
            response.put({"Status":"Done"})
        
        gpio_output.write(1)
        time.sleep(1-fan_speed_mode[currState])
        gpio_output.write(0)
        time.sleep(1-fan_speed_mode[currState])
        
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
    
    global currState
    currState = 0
    httpd = make_server('', 1337, gateway_handler)
    # httpd.server_close()
    t1 = threading.Thread(target=httpd.serve_forever)
    t2 = threading.Thread(target=doAction, args=(q))
    t1.start()
    t2.start()
