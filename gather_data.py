from inputs import devices
from inputs import GamePad
from inputs import get_gamepad
from fdp import ForzaDataPacket
import numpy as np
from PIL import ImageGrab
import cv2
import time
import struct
import socket
import csv
from threading import Thread

counter = 0
game_pad = None
speed = 0
sock = socket.socket(socket.AF_INET, 
socket.SOCK_DGRAM) 
sock.bind(('127.0.0.1', 10001))
params = ForzaDataPacket.get_props(packet_format = 'fh4')
runLoops = True

speed = 0
brake = 0
accel = 0
steer = 0


def record_game_pad():
    global counter
    input_counter = 0
    steering_x_captured = None
    steering_y_captured = None
    throttle_captured = None
    brake_captured = None

    # while steering_x_captured == None or steering_y_captured == None or (brake_captured == None and throttle_captured == None):
    while input_counter<100:


        events = get_gamepad()
        # print(f'X: {steering_x_captured}\tY:{steering_y_captured}\tT:{throttle_captured}\tB:{brake_captured}')

        for event in events:
            input_counter+=1
            if event.code == "ABS_Z" and event.state != None:
                brake_captured = event.state
            if event.code == "ABS_RZ" and event.state != None:
                throttle_captured = event.state
            if event.code == "ABS_X" and event.state != None:
                steering_x_captured = event.state
            if event.code == "ABS_Y" and event.state != None:
                steering_y_captured = event.state

    print("  - game-pad : OK")

    brake_captured = 0 if brake_captured == None else brake_captured
    throttle_captured = 0 if throttle_captured == None else throttle_captured


    # file = open(, "a")
    # file.write(str(counter) + "_image.png" + "," + str(steering_x_captured) + "," + str(speed) + "," + str(throttle_captured) + "," + str(brake_captured) + "\n")
    # file.close()

def crop(img):
    x=0
    w=1600
    y=350
    h=900-350

    return img[y:y+h, x:x+w]
def transformX(x):
  #This removes negative values
  x_max = 32767
  new_x = x + x_max
  new_x = new_x / (x_max+x_max)

  return   new_x 
def datasteam():
    global speed
    global brake
    global accel
    global steer
    global runLoops
    while runLoops:
        data, addr = sock.recvfrom(1024)
        fdp = ForzaDataPacket(data, packet_format='fh4')
        # values = struct.unpack('<i I 27f 4i 20f 5i 12x 17f H 6B 3b x', data)
        # speed = values[61]
        # brake = values[84]
        speed = fdp.speed
        brake = fdp.brake
        accel = fdp.accel
        steer = fdp.steer

        # print(f'Speed {fdp.speed} Brake {fdp.brake} Acceleration {fdp.accel}  {fdp.steer}')
        # print(f'Speed: {speed}, Brake: {brake}, ')
        


def run():
    global counter
    global runLoops
    record = False
    sock.settimeout(3)
    framecounter = 1 
    frames = 10
    with open("./data/newdata/inputs.csv", 'a', newline='', buffering=1) as outfile:
        csv_writer = csv.writer(outfile)
        while runLoops:

            resolutionx, resolutiony = (1600,900)
            margin = 40
            printscreen = np.array(ImageGrab.grab(bbox=(0, margin, resolutionx, resolutiony+margin)))
            printscreen = cv2.cvtColor(printscreen, cv2.COLOR_BGR2RGB)
            
            printscreen = crop(printscreen)
            smoll = cv2.resize(printscreen, (int(resolutionx/2),int(resolutiony/2)))
            cv2.imshow('window', smoll)

            

            ##change to your preferred folder
            if record :
                framecounter+=1
                # record_game_pad()
                if framecounter%frames==0:
                    framecounter = framecounter-frames
                    cv2.imwrite(f'D:/Documenten/Thomasmore/AI/self_driving/data/newdata/images/{counter}_image.png', printscreen)
                    str_towrite = [str(counter) + "_image.png", speed ,steer, accel, brake]
                    csv_writer.writerow(str_towrite)
                    # file.write( + "\n")            
                    print('took screen 😁')
                    counter +=1        

            #Check fps if needed
            k = cv2.waitKey(25)
            if  k == ord('q'):
                cv2.destroyAllWindows()
                runLoops = False
                break
            elif k == ord('r'):
                record = not record
                time.sleep(5)
                print(f'Record {record}')

if __name__ == '__main__':
    print("Prepare to drive!")
    file = open("./data/newdata/inputs.csv", "a")
    # run()
    t1 = Thread(target = datasteam)
    t2 = Thread(target = run)
    t1.start()
    t2.start()
    file.close()
