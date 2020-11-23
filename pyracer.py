from racemodel import getOutput
import pyvjoy
import cv2
import time
from PIL import ImageGrab
import numpy as np


j = pyvjoy.VJoyDevice(1)
x_max = 32767

def sendInputs(x,z):
    x_to_send = x * x_max
    z_to_send = z * x_max
    j.data.wAxisX = int(x_to_send)
    j.data.wAxisZ=int(z_to_send)
    #send data to vJoy device
    j.update()


def run():

    autopilot = False
    showFps = False
    last_time = time.time()
    global counter
    while True:
        printscreen = np.array(ImageGrab.grab(bbox=(0, 80, 1024, 700)))
        resized = cv2.resize(printscreen, (244,244))
        cv2.imshow('window', cv2.cvtColor(printscreen, cv2.COLOR_BGR2RGB))
        
        if showFps:
            ##Check fps if needed
            print('loop took {} seconds'.format(time.time()-last_time))
            last_time = time.time()

        if autopilot:
            prediction = getOutput(resized)
            print(prediction[0][0], prediction[0][1])
            sendInputs(prediction[0][0], prediction[0][1])
        

        k = cv2.waitKey(25)
        if  k == ord('q'):
            cv2.destroyAllWindows()
            break
        elif k == ord('a'):
            autopilot = not autopilot
        elif k == ord('f'):
            showFps = not showFps
       

if __name__ == '__main__':
    print("Prepare to drive!")
    run()

