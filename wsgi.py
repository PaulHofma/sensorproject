from app import create_app
from main import MessageAnnouncer, DataCollector
import threading
import atexit
import signal

ANNOUNCER = MessageAnnouncer()
application = create_app(ANNOUNCER)

print(f"application master starting up, should run only once...") 
FAIL_COUNTER = []
TEMP = []
HMD = []
TIME = []
dataCollector = DataCollector(TEMP, HMD, TIME, FAIL_COUNTER, ANNOUNCER)

def background():
    global dataCollector
    print('start background process...')
    dataCollector.main_process()
    print('should not get here')
    return

mp = threading.Thread(name='bg', target=background)
mp.start()

def close_threads(a=0, b=0):
    print('shutting down threads and stopping process...')
    dataCollector.terminate()
    print(f'stop event set to: {dataCollector.stop_event.is_set()}, joining threads...')
    if mp.is_alive():
        mp.join(10)
    if mp.is_alive():
        mp.kill()
        mp.join()
    print('done!')
    raise Exception("get outta here.")
atexit.register(close_threads)
signal.signal(signal.SIGINT, close_threads)

if __name__ == "__main__":
    application.run()
