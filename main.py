import queue
from sensors import getReadout
import itertools
import time
import random
from threading import Lock, Event, Thread
from adafruit_dht import DHT22
import board
import atexit
import signal

class MessageAnnouncer:

    def __init__(self):
        print('initializing announcer')
        self.listeners = []
        self.name = str(random.randint(0,999))
        self.lock = Lock()
        
    def __str__(self):
        return F"announcer (name: {self.name}, listeners: {len(self.listeners)})"
        
    def listen(self):
        with self.lock:
            q = queue.Queue(maxsize=5)
            self.listeners.append(q)
            print('add listener, new length:' + str(self))
        return q
    
    def announce(self, msg):
        with self.lock:
            print(F'announcing datapoint, listener length: {str(len(self.listeners))}')
            print(self.listeners)
            for i in reversed(range(len(self.listeners))):
                try:
                    print('msg: ' + msg)
                    self.listeners[i].put_nowait(msg)
                except queue.Full:
                    print('killing a listener')
                    del self.listeners[i]
                
class DataCollector:
    
    def __init__(self, temp_arr, hmd_arr, time_arr, fail_arr, announcer):
        print("application starting!")
        
        self.temp_arr = temp_arr
        self.hmd_arr = hmd_arr
        self.time_arr = time_arr
        self.fail_arr = fail_arr
        self.announcer = announcer
        
        self.dhtDevice = DHT22(board.D18)
        self.stop_event = Event()
        print(F"started with announcer: {self.announcer}")
        print(self.dhtDevice.temperature)
        print(F'dummy read: {self.get_data()}')

    def main_process(self):
        for _ in enumerate(itertools.count()):
            print(time.time())
            print(F'{str(self)} stopping: {self.stop_event.is_set()}')
            if(self.stop_event.is_set()):
                break
            print('ping:' + str(self.announcer))
            result = self.get_data()
            print('got data')
            self.announcer.announce(result)
            self.fail_arr = [x for x in self.fail_arr if (x+3600) > time.time()]
            print('sleeping')
            time.sleep(5.0)
            
    def terminate(self):
        print('Terminating DataCollector...')
        self.stop_event.set()
        print(f'DataCollector stop event status: {self.stop_event.is_set()}')
        time.sleep(0.5)
        
    def get_data(self):
        print('start get data')
        result = getReadout(self.dhtDevice)
        print(F'got readout: {result}')
        if(result != "" and result != []):
            self.data_update(self.temp_arr, result['tmp'])
            self.data_update(self.hmd_arr, result['hmd'])
            self.data_update(self.time_arr, time.time())
            return 'data: {"data": "%s (%s)", "errors": %d, "tmp": %s, "hmd":%s, "timestamp":%s}\n\n' % (
                result['printable'],
                time.strftime("%y%m%d %H:%M:%S", time.localtime()),
                len(self.fail_arr),
                self.temp_arr,
                self.hmd_arr,
                [i * 1000 for i in self.time_arr]
            )
        else:
            self.fail_arr.append(time.time())
            return 'data: {"errors": %d}\n\n' % len(self.fail_arr)    
        
    def data_update(self, data_in, val):
        if(len(data_in) <= 10000):
            data_in = data_in.append(val)
        else:
            data_in = data_in.append(val)[1:]

if __name__ == "__main__":
    a = MessageAnnouncer()
    c = DataCollector([], [], [], [], a)
    q = a.listen()
    
    def loop():
        while not c.stop_event.is_set():
            print(c.stop_event.is_set())
            a.announce("hello!")
            print(q.get())
            print(c.get_data())
            time.sleep(2.0)
    
    mp = Thread(name='bg', target=loop)
    mp.start()
    
    def close_threads(a=0, b=0):
        print('shutting down threads and stopping process...')
        c.terminate()
        print(f'stop event set to: {c.stop_event.is_set()}, joining threads...')
        if mp.is_alive():
            mp.join(10)
        if mp.is_alive():
            mp.kill()
            mp.join()
        print('done!')
        raise Exception("get outta here.")
    atexit.register(close_threads)
    signal.signal(signal.SIGINT, close_threads)
    #signal.alarm(8)
    
    while True:
        qnew = a.listen()
        qnew.get()
        time.sleep(5.0)
            
    
