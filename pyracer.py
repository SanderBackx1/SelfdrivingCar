from racemodel import getOutput
import pyvjoy
import cv2
import time
from PIL import ImageGrab
import numpy as np
import keyboard

j = pyvjoy.VJoyDevice(1)
x_max = 32767

def crop(img):
    x=0
    w=1600
    y=350
    h=900-350

    return img[y:y+h, x:x+w]
        

def sendInputs(x,z):
    if  x >= 0.51:
        x += 0.2
    elif x<=0.48:
        x -= 0.1
    print(f'X:{x*(x_max+x_max)-x_max} Z {z*512 - 255}')

    j.data.wAxisX = int(x*x_max)
    j.data.wAxisZ=int( (z*x_max) * 2 )

    j.data.wAxisY= int(0)
    #send data to vJoy device
    j.update()


def inputModel(steer, accel,brake):
    print(f'X:{steer} accel {accel} Brake:{brake}')
    #unnormalizing

    #x_max = 32767
    x_half = int(x_max/2)


    # -255 255
    #0 - 1 
    #<0.5  0.5>
    # 


    s  = steer * 32767
    a = accel * x_half 
    b = brake * x_half * -1
    j.data.wAxisX = int(s)
    j.data.wAxisZ=int( a + b)

    j.data.wAxisY= int(0)
    #send data to vJoy device
    j.update()





def resetkey():
    j.data.wAxisX = int(x_max/2)
    j.data.wAxisZ=int(x_max/2)

    j.data.wAxisY= int(x_max/2)
    #send data to vJoy device
    j.update()



def listenkeys():
    keys = ['left', 'up', 'right']    
    for k in lab_dictkey:
        keys[keys.index(k)] = keyboard.is_pressed(k)
        print("manual steering: "+str(keys))
        
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
        printscreen = crop(printscreen)
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
        if  k == ord('g') or keyboard.is_pressed('g'):
            cv2.destroyAllWindows()
            break
        elif k == ord('v') or keyboard.is_pressed('v') :
            resetkey()
            autopilot = not autopilot
            print('autopilot in 5s')
            time.sleep(5)
        elif k == ord('f') or keyboard.is_pressed('f'):
            showFps = not showFps
       

if __name__ == '__main__':
    print("Prepare to drive!")
    run()

