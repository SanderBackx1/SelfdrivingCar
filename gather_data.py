from inputs import devices
from inputs import GamePad
from inputs import get_gamepad
import numpy as np
from PIL import ImageGrab
import cv2
import time

counter = 0
game_pad = None

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

    file = open("data/inputs.csv", "a")
    file.write(str(counter) + "_image.png" + "," + str(steering_x_captured) + "," + str(steering_y_captured) + "," + str(throttle_captured) + "," + str(brake_captured) + "\n")
    file.close()


def run():
    global counter
    record = False
    while True:
        
        #smoll screen 
        # printscreen = np.array(ImageGrab.grab(bbox=(0, 80, 1024, 700)))
        # cv2.imshow('window', cv2.cvtColor(printscreen, cv2.COLOR_BGR2RGB))


        #big screen
        resolutionx, resolutiony = (1600,900)
        margin = 40
        printscreen = np.array(ImageGrab.grab(bbox=(0, margin, resolutionx, resolutiony+margin)))

        smoll = resized = cv2.resize(printscreen, (int(resolutionx/2),int(resolutiony/2)))
        cv2.imshow('window', cv2.cvtColor(smoll, cv2.COLOR_BGR2RGB))

        

        ##change to your preferred folder

        if record:
            record_game_pad()
            cv2.imwrite(f'D:/Desktop/images/{counter}_image.png', printscreen)
            print('took screen 😁')
            counter +=1        

        ##Check fps if needed
        # print('loop took {} seconds'.format(time.time()-last_time))
        # last_time = time.time()
        k = cv2.waitKey(25)
        if  k == ord('q'):
            cv2.destroyAllWindows()
            break
        elif k == ord('r'):
            record = not record
            print(f'Record {record}')

if __name__ == '__main__':
    print("Prepare to drive!")
    run()