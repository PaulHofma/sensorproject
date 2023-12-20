from app import create_app
from main import MessageAnnouncer, DataCollector
import threading
import atexit

ANNOUNCER = MessageAnnouncer()
application = create_app(ANNOUNCER)

print(f"application master starting up, should run only once...") 
FAIL_COUNTER = []
TEMP = []
HMD = []
TIME = []

def background():
    global FAIL_COUNTER, TEMP, HMD, TIME, ANNOUNCER
    
    print('start background process...')
    DataCollector(TEMP, HMD, TIME, FAIL_COUNTER, ANNOUNCER)

mp = threading.Thread(name='bg', target=background)
mp.start()

def close_threads():
    print('shutting down threads...')
    mp.join()
    print('done!')
atexit.register(close_threads)

if __name__ == "__main__":
    application.run()
