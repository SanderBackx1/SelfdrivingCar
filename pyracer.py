from racemodel import getOutput
import pyvjoy
import cv2
import time
from PIL import ImageGrab
import numpy as np


j = pyvjoy.VJoyDevice(1)
x_max = 32767

def sendInputs(x,z):
    print(f'X:{x*(x_max+x_max)-x_max} Z {z*512 - 255}')
    j.data.wAxisX = int(x*x_max)
    j.data.wAxisZ=int(z*x_max)

    j.data.wAxisY= int(0)
    #send data to vJoy device
    j.update()
    
def run():

    autopilot = False
    showFps = False
    last_time = time.time()
    global counter
    # print('get ready to bind in 3s')
    # time.sleep(3)
    while True:
        # printscreen = np.array(ImageGrab.grab(bbox=(0, 80, 1024, 700)))
        # resized = cv2.resize(printscreen, (244,244))
        # cv2.imshow('window', cv2.cvtColor(printscreen, cv2.COLOR_BGR2RGB))
        resolutionx, resolutiony = (1600,900)
        margin = 40
        printscreen = np.array(ImageGrab.grab(bbox=(0, margin, resolutionx, resolutiony+margin)))
        printscreen = cv2.cvtColor(printscreen, cv2.COLOR_BGR2RGB)
        resized = cv2.resize(printscreen, (480,277))
        smoll = cv2.resize(printscreen, (int(resolutionx/2),int(resolutiony/2)))
        cv2.imshow('window', resized)

        if showFps:
            ##Check fps if needed
            print('loop took {} seconds'.format(time.time()-last_time))
            last_time = time.time()

        if autopilot:
            prediction = getOutput(resized)
            # print(prediction[0][0], prediction[0][1])
            sendInputs(prediction[0][0], prediction[0][1])
        

        k = cv2.waitKey(25)
        if  k == ord('q'):
            cv2.destroyAllWindows()
            break
        elif k == ord('d'):
            time.sleep(3)
            autopilot = not autopilot
        elif k == ord('f'):
            showFps = not showFps
       

if __name__ == '__main__':
    print("Prepare to drive!")
    run()

