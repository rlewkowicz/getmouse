import os
import ctypes
import logging
import threading 
import time
from time import sleep
from pathlib import Path

P1 = Path('R:/mouse.lua')
P2 = Path('R:/active.lua')
P3 = Path('R:/xy.lua')

logging.basicConfig(level="INFO")

def dont_block(f):
    def wrap(*args):
        threading.Thread(target=f, args=args, daemon=True).start()
    return wrap

persistent_object = type('', (), {})()
persistent_object.mouse = 0
persistent_object.counter = 0
persistent_object.profile = 1
persistent_object.ar_tm = 0 
persistent_object.ar_sY = 0 
persistent_object.ar_eY = 0 
persistent_object.ar_sX = 0 
persistent_object.ar_eX = 0 
persistent_object.counter = 0
persistent_object.secondary = 0
persistent_object.multiplier = 0
persistent_object.xdirection = 1
persistent_object.ydirection = 1
persistent_object.multiplier = 0


@dont_block
def counter():
    select_profile()
    AR_V = persistent_object.ar_sY
    AR_H = persistent_object.ar_sX
    i_y = 0
    i_x = 0
    xinterval = 0
    yinterval = 0
    persistent_object.counter = 0
    persistent_object.secondary = 0
    start = time.time_ns() // 1_000_000  

    with open(P3, 'wb') as f:
        while True:
            persistent_object.multiplier = 6
            end = time.time_ns() // 1_000_000 
            if (end - start) > 1:
                start = time.time_ns() // 1_000_000
            else:
                continue
            select_profile()
            try:
                xiteration_point = (persistent_object.ar_tm / 10) / (abs(persistent_object.ar_sX - persistent_object.ar_eX))
            except:
                xiteration_point = 1 

            try:
                yiteration_point = (persistent_object.ar_tm / 10) / (abs(persistent_object.ar_sY - persistent_object.ar_eY))
            except:
                yiteration_point = 1 
                
            if persistent_object.mouse > 1:
                persistent_object.secondary  = persistent_object.secondary+1
                persistent_object.counter = persistent_object.counter+1

                if persistent_object.ar_sY < persistent_object.ar_eY: 
                    yinterval = 1
                else:
                    yinterval = -1
                if persistent_object.ar_sX < persistent_object.ar_eX: 
                    xinterval = 1
                else:
                    xinterval = -1

                i_y = i_y+1
                if i_y > yiteration_point:
                    i_y = 0
                    AR_V = AR_V + yinterval
                    if yinterval < 0:
                        if AR_V < persistent_object.ar_eY:
                            AR_V = persistent_object.ar_eY
                    else:
                        if AR_V > persistent_object.ar_eY:
                            AR_V = persistent_object.ar_eY

                i_x = i_x+1
                if i_x > xiteration_point:
                    i_x = 0
                    AR_H = AR_H + xinterval
                    if xinterval < 0:
                        if AR_H < persistent_object.ar_eX:
                            AR_H = persistent_object.ar_eX
                    else:
                        if AR_H > persistent_object.ar_eX:
                            AR_H = persistent_object.ar_eX
            else:
                AR_V = persistent_object.ar_sY
                AR_H = persistent_object.ar_sX            
                i_x = 0
                i_y = 0
                persistent_object.secondary =  0
                persistent_object.counter = 0


            b='return ' + str(abs(AR_H)) + "," + str(abs(AR_V)) + "," + str(persistent_object.xdirection*persistent_object.multiplier) + "," + str(persistent_object.ydirection*persistent_object.multiplier)
            f.seek(0,0)
            f.write("                                        ".encode('ascii'))
            f.flush()
            f.seek(0,0)
            # logging.info(b)
            f.write(b.encode('ascii'))
            f.flush()



@dont_block
def mouse():
    current = ctypes.windll.user32.GetKeyState(0x01)
    while current > 2:
        current = ctypes.windll.user32.GetKeyState(0x01)
    
    begin = time.time_ns() // 1_000_000
    new = 0 

    on = 1
    
    m4_state=-1

    with open(P1, 'wb', 0) as f:  
        while 1:
            main = ctypes.windll.user32.GetKeyState(0x01)
            m4 = 0
            m4 = ctypes.windll.user32.GetKeyState(0x05)

            if m4_state == -1:
                new = main
                persistent_object.mouse = int(str(new)[0])
            
            if int(m4) > 2:
                persistent_object.mouse = 5
                m4_state=1
                if persistent_object.profile > 0:
                    end = time.time_ns() // 1_000_000 
                    if (end - begin) > 10:
                        if on < 2:
                            on = 9
                        else:
                            on = 1
                        begin = time.time_ns() // 1_000_000
                new = on
            elif m4 < 2 and m4_state==1:                        
                new = 0
                m4_state = 0
            elif m4_state == 0:
                persistent_object.mouse = 0
                m4_state = -1
                new = 0
            # if persistent_object.counter > 300:
            #     persistent_object.secondary =  0
            #     new = 0
            b='return ' + str(new)[0]
            f.seek(0,0)
            f.write(b.encode('ascii'))
            if m4_state == 0:
                sleep(.1)

@dont_block
def active():
    state = 0
    with open(P2, 'w') as f:
        f.write('return ' + str(state))
        f.flush()
        while 1:
            # if ctypes.windll.user32.GetKeyState(0x66) > 2:
            if ctypes.windll.user32.GetKeyState(0x06) > 2:
                if state == 0:
                    state = 1
                elif state == 1:
                    state = 0    

                logging.info("state changed " + str(time.time()))
                f.seek(0, 0)
                f.write('return ' + str(state))
                f.flush()
                sleep(.5)

@dont_block
def profile():
    arr = []
    COUNT = 0
    while True:
        logging.info(persistent_object.profiley3212121)
        if ctypes.windll.user32.GetKeyState(0x59) > 2:
            COUNT = 0
            arr = []
            sleep(.2)
            while COUNT < 2:
                if ctypes.windll.user32.GetKeyState(0x31) > 2:
                    arr.append(1)
                    sleep(.2)
                    COUNT = COUNT + 1
                if ctypes.windll.user32.GetKeyState(0x32) > 2:
                    arr.append(2)
                    sleep(.2)
                    COUNT = COUNT + 1
                if ctypes.windll.user32.GetKeyState(0x33) > 2:
                    arr.append(3)
                    sleep(.2)
                    COUNT = COUNT + 1
        try:
            if ctypes.windll.user32.GetKeyState(0x32) > 2:
                persistent_object.profile = arr[1]
                sleep(.001)

            if ctypes.windll.user32.GetKeyState(0x31) > 2:
                persistent_object.profile = arr[0]
                sleep(.001)
        except:
            pass

def select_profile():
    if persistent_object.profile == 1:
        persistent_object.multiplier = 5
        persistent_object.ar_tm = 700 
        persistent_object.ar_sY = 4 
        persistent_object.ar_eY = 4 
        persistent_object.ar_sX = 47 
        persistent_object.ar_eX = 10
        persistent_object.xdirection = -1

    if persistent_object.secondary > 1000:
        pass
    elif persistent_object.secondary > 2220:
        pass
    elif persistent_object.secondary > 600:
        persistent_object.xdirection = -1
        persistent_object.ar_eX = 30
        persistent_object.ar_eY = 21
    elif persistent_object.secondary > 400:
        persistent_object.xdirection = 1
        persistent_object.ar_eX = 35
        persistent_object.ar_eY = 18
    elif persistent_object.secondary > 320:
        persistent_object.xdirection = 0
        persistent_object.ar_eX = 35
        persistent_object.ar_eY = 11
    elif persistent_object.secondary > 290:
        persistent_object.xdirection = 1
        persistent_object.ar_eX = 35
        persistent_object.ar_eY = 6
    elif persistent_object.secondary > 234:
        persistent_object.xdirection = 1
        persistent_object.ar_eX = 30
        persistent_object.ar_eY = 5
    elif persistent_object.secondary > 165:
        persistent_object.ar_eX = 8
        persistent_object.ar_eY = 4
    elif persistent_object.secondary > 150:
        persistent_object.ar_eX = 26
        persistent_object.ar_eY = 7

    if persistent_object.profile == 2:
        persistent_object.multiplier = 5
        persistent_object.ar_tm = 1000 
        persistent_object.ar_sY = 6
        persistent_object.ar_eY = 7 
        persistent_object.ar_sX = 20 
        persistent_object.ar_eX = 20
        persistent_object.xdirection = -1

        if persistent_object.secondary > 10000:
            persistent_object.ar_eY = 26 
            persistent_object.ar_eX = 60
        elif persistent_object.secondary > 600:
            persistent_object.ar_eY = 40
            persistent_object.ar_sY = 1000000
            persistent_object.ar_eY = 1 
            persistent_object.xdirection = 1
        elif persistent_object.secondary > 600:
            persistent_object.ar_eY = 40
            persistent_object.xdirection = -1
        elif persistent_object.secondary > 430:
            persistent_object.xdirection = 0
            persistent_object.ar_eY = 50
            persistent_object.ar_eX = 30
        elif persistent_object.secondary > 400:
            persistent_object.ar_eY = 25
            persistent_object.ar_eX = 50
            persistent_object.xdirection = 1
        elif persistent_object.secondary > 300:
            persistent_object.xdirection = 1
            persistent_object.ar_eY = 65
        elif persistent_object.secondary > 200:
            persistent_object.ar_eX = 30
            persistent_object.ar_eY = 39
        elif persistent_object.secondary > 100:
            persistent_object.ar_eY = 8 

    if persistent_object.profile == 3:
        persistent_object.multiplier = 2
        persistent_object.ar_tm = 1000 
        persistent_object.ar_sY = 1
        persistent_object.ar_eY = 1 
        persistent_object.ar_sX = 20 
        persistent_object.ar_eX = 20
        persistent_object.xdirection = 0

        if persistent_object.secondary > 10000:
            pass
        elif persistent_object.secondary > 300:
            persistent_object.xdirection = 0
        elif persistent_object.secondary > 200:
            persistent_object.ar_eY = 1
        elif persistent_object.secondary > 100:
            persistent_object.xdirection = -1
            persistent_object.ar_eX = 50
            persistent_object.ar_eY = 3


mouse()
active()
counter()
profile()

while True:
    sleep(1000000)
