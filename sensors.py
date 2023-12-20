#!/home/eelco/.virtualenvs/sensors/bin/python3

import time
import board
import adafruit_dht as dht


# connected on pin 18 - change as appropriate.
dhtDevice = dht.DHT22(board.D18)

# Run as application
def main():
    print('starting...')
    while True:
        try:
            temperature = dhtDevice.temperature
            humidity = dhtDevice.humidity
            print(humidity)
            if(temperature == 25.5 and humidity == 25.5):
                print("Bad data, skipping")
            yield "Temp: {:.1f}*C, Humidity: {:.1f}%".format(temperature, humidity)
        
        except RuntimeError as e:
            #GPIO access may require sudo permissions
            #Other rt errors will occur because sensors are hard to make.
            print(f"RuntimeError: {e}")
            #print("GPIO Access may need sudo permissions.")
            
            time.sleep(5.0)
            continue
        
        except Exception as error:
            dhtDevice.exit()
            raise error
        
        time.sleep(5.0)
        

# Does a single read operation  
def getReadout():
    try:
        temperature = dhtDevice.temperature
        humidity = dhtDevice.humidity
        if(temperature == 25.5 and humidity == 25.5):
            print("Bad data, skipping")
            return ""
        
        returnVal = {
            'printable': "Temp: {:.1f}*C, Humidity: {:.1f}%".format(temperature, humidity),
            'tmp': temperature,
            'hmd': humidity
            }
        return returnVal
    
    except RuntimeError as e:
        #GPIO access may require sudo permissions
        #Other rt errors will occur because sensors are hard to make.
        print(f"RuntimeError: {e}")
        #print("GPIO Access may need sudo permissions.")
        return ""
    
    except Exception as error:
        #dhtDevice.exit()
        #raise error
        print(error)
        print(f"BIG Error, trying to recover but may fail")
        #print("GPIO Access may need sudo permissions.")
        return ""
        
if __name__ == "__main__":
    main()
        

