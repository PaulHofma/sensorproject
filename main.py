import queue
from sensors import getReadout
import itertools
import time
import random
import threading

class MessageAnnouncer:

    def __init__(self):
        print('initializing announcer???')
        self.listeners = []
        self.name = str(random.randint(0,999))
        self.lock = threading.Lock()
        
    def __str__(self):
        return F"announcer (name: {self.name}, listeners: {len(self.listeners)})"
        
    def listen(self):
        with self.lock:
            print('???' + str(self))
            q = queue.Queue(maxsize=5)
            self.listeners.append(q)
        return q
    
    def getL(self):
        return len(self.listeners)
    
    def announce(self, msg):
        print('whazzup?' + str(len(self.listeners)))
        print(self.getL())
        for i in reversed(range(len(self.listeners))):
            try:
                print('msg: ' + self.tostring())
                self.listeners[i].put_nowait(msg)
            except queue.Full:
                del self.listeners[i]
                
class DataCollector:
    
    def __init__(self, temp_arr, hmd_arr, time_arr, fail_arr, announcer):
        print("application starting!")
        
        self.temp_arr = temp_arr
        self.hmd_arr = hmd_arr
        self.time_arr = time_arr
        self.fail_arr = fail_arr
        self.announcer = announcer
        print(F"started with announcer: {self.announcer}")
        
        self.main = self.main_process()

    def main_process(self):
        for _ in enumerate(itertools.count()):
            print('ping:' + str(self.announcer))
            result = self.get_data()
            self.announcer.announce(result)
            self.fail_arr = [x for x in self.fail_arr if (x+3600) > time.time()]
            time.sleep(5.0)          
        
    def get_data(self):
        result = getReadout()
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

