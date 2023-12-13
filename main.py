import queue
from sensors import getReadout
import itertools
import time

class MessageAnnouncer:

    def __init__(self):
        self.listeners = []
        
    def listen(self):
        q = queue.Queue(maxsize=5)
        self.listeners.append(q)
        return q
    
    def announce(self, msg):
        for i in reversed(range(len(self.listeners))):
            try:
                self.listeners[i].put_nowait(msg)
            except queue.Full:
                del self.listeners[i]

def main_process(temp_arr, hmd_arr, time_arr, fail_arr, announcer):
    print("application starting!")
    for _ in enumerate(itertools.count()):
        result = get_data(temp_arr, hmd_arr, time_arr, fail_arr)
        announcer.announce(result)
        fail_counter = [x for x in fail_arr if (x+3600) > time.time()]
        time.sleep(5.0)
        
def get_data(temp_arr, hmd_arr, time_arr, fail_arr):
    result = getReadout()
    if(result != "" and result != []):
        data_update(temp_arr, result['tmp'])
        data_update(hmd_arr, result['hmd'])
        data_update(time_arr, time.time())
        return 'data: {"data": "%s (%s)", "errors": %d, "tmp": %s, "hmd":%s, "timestamp":%s}\n\n' % (
            result['printable'],
            time.strftime("%y%m%d %H:%M:%S", time.localtime()),
            len(fail_arr),
            temp_arr,
            hmd_arr,
            [i * 1000 for i in time_arr]
        )
    else:
        fail_arr.append(time.time())
        return 'data: {"errors": %d}\n\n' % len(fail_arr)        

def data_update(data_in, val):
    if(len(data_in) <=10000):
        data_in = data_in.append(val)
    else:
        data_in = data_in.append(val)[1:]

