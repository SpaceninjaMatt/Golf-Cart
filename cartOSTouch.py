import pygame #This interfaces with the remote
import RPi.GPIO as GPIO #Simplier GPIO libary that is used for the steering stepper 
import time #so we can have at time for software pwm
import pigpio #Allows for hardware PWM which is used to get a clear signal for the throttle control
import PySimpleGUI as sg
import serial, sys
import pyautogui


"""#TEST BELOW
import os
if os.environ.get('DISPLAY','') == '':
	print('no display found.    Using : 0.0')
	os.environ.__setitem__('DISPLAY',':0.0')
#TEST ABOVE
"""

def make_window1():
    layout = [[sg.VPush()],
              [sg.Push(), sg.Text('Choose a control mode',font = ("Helvetica", 25)), sg.Push()],
              [sg.Push(), sg.Button('Manual', font = ("Helvetica",40), size = (6,6)), sg.Button('Xbox', font = ("Helvetica",40), size = (6,6) ), sg.Button('Serial', font = ("Helvetica",40), size = (6,6)),sg.Push()],
              [sg.Push(), sg.Button('Exit', font = ("Helvetica",30), size = (15,2)),sg.Button('Lock', font = ("Helvetica",30), size = (15,2)), sg.Push()],
              [sg.VPush()]]
    
    return sg.Window('cartOS', layout, auto_size_text = True, resizable=True, size=(800,480), no_titlebar=True, location=(0,0), keep_on_top= True)

def make_window2():
    layout = [[sg.VPush()],
              [sg.Push(), sg.Text("Choose a drive mode",font = ("Helvetica", 25)), sg.Push()],
              [sg.Push(), sg.Text("Current:",font = ("Helvetica", 30)), sg.Text("", key = '-TEXT-',font = ("Helvetica", 30)), sg.Push()],
              [sg.Push(), sg.Button('Forward', font = ("Helvetica",35), size = (6,6)), sg.Button('Neutral', font = ("Helvetica",35), size = (6,6)), sg.Button('Reverse', font = ("Helvetica",35), size = (6,6)),sg.Push()],
              [sg.Push(), sg.Button('Exit', font = ("Helvetica",30), size = (15,2)), sg.Push()],
              [sg.VPush()]]
    
    return sg.Window('cartOS', layout, resizable=True, size=(800,480), no_titlebar=True, location=(0,0), keep_on_top= True)

def make_window3():
    layout = [[sg.VPush()],
              [sg.Push(), sg.Text("Currently:",font = ("Helvetica", 30)), sg.Text("", key = '-TEXT-',font = ("Helvetica", 30)), sg.Push()],
              [sg.Push(), sg.Text("Steering (A):",font = ("Helvetica", 20)), sg.Text("ON", key = '-STR-',font = ("Helvetica", 20)), sg.Push()],
              [sg.Push(), sg.Text("Cruise Control (Bumpers):",font = ("Helvetica", 20)), sg.Text("OFF", key = '-CCTRL-',font = ("Helvetica", 20)), sg.Push()],
              [sg.Push(), sg.Text("Steering cali. (up D-pad): ",font = ("Helvetica", 20)), sg.Text("Done",key = '-HIGH-',font = ("Helvetica", 20)), sg.Push()],
              [sg.Push(), sg.Text("Idle timer (L or R D-pad):",font = ("Helvetica", 20)), sg.Text("1", key = '-IDLE_TIME-',font = ("Helvetica", 20)), sg.Push()],
              [sg.Push(), sg.Text(""), sg.Push()],
              [sg.Push(), sg.Text( "Exit Xbox (B)?",font = ("Helvetica", 20)), sg.Push()],
              [sg.Push(), sg.Button('Yes',font = ("Helvetica", 20), size = (10,10)), sg.Push()],
              [sg.VPush()]]
    
    
    return sg.Window('cartOS', layout, resizable=True, size=(800,480), no_titlebar=True, location=(0,0), keep_on_top= True)

def make_window4():
    layout = [[sg.VPush()],
              [sg.Push(), sg.Text("Last Command:",font = ("Helvetica", 35)), sg.Text("", key = '-TEXT-',font = ("Helvetica", 35)), sg.Push()],
              [sg.Push(), sg.Text(""), sg.Push()],
              [sg.Push(), sg.Text("Exit Serial?",font = ("Helvetica", 25)), sg.Push()],
              [sg.Push(), sg.Button('Yes', font = ("Helvetica",30), size = (10,5)), sg.Push()],
              [sg.VPush()]]
    
    return sg.Window('cartOS', layout, resizable=True, size=(800,480), no_titlebar=True, location=(0,0), keep_on_top= True)
def make_window5():
    layout = [[sg.VPush()],
              [sg.Push(), sg.Text("NO REMOTE DETECTED",font = ("Helvetica", 40)), sg.Push()],
              [sg.Push(), sg.Button('Okay', font = ("Helvetica",30), size = (10,5)), sg.Push()],
              [sg.VPush()]]
    
    return sg.Window('cartOS', layout, resizable=True, size=(800,480), no_titlebar=True, location=(0,0), keep_on_top= True)
    
def make_window6():
    layout = [[sg.VPush()],
              [sg.Push(), sg.Text("NO USB CONNECTED",font = ("Helvetica", 40)), sg.Push()],
              [sg.Push(), sg.Text("Error #",font = ("Helvetica", 20)), sg.Text("", key = '-ERROR-',font = ("Helvetica", 20)), sg.Push()],
              [sg.Push(), sg.Button('Okay', font = ("Helvetica",30), size = (10,5)), sg.Push()],
              [sg.VPush()]]
    
    return sg.Window('cartOS', layout, resizable=True, size=(800,480), no_titlebar=True, location=(0,0), keep_on_top= True, finalize = True)
 
def make_window7():
    layout = [[sg.VPush()],
              [sg.Push(), sg.Text("PARKING BRAKE ENGAGING",font = ("Helvetica", 40)), sg.Push()],
              [sg.Push(), sg.Text("5 seconds remaining", key = '-TIMER-',font = ("Helvetica", 35)), sg.Push()],
              [sg.VPush()]]
    
    return sg.Window('cartOS', layout, resizable=True, size=(800,480), no_titlebar=True, location=(0,0), keep_on_top= True)

def make_window8():
    layout = [[sg.VPush()],
              [sg.Push(), sg.Text("ENTER CODE",key = '-TOP-',font = ("Helvetica", 40)), sg.Push()],
              [sg.Push(), sg.Text("_", key = '-CODE1-',font = ("Helvetica", 35)), sg.Text("_", key = '-CODE2-',font = ("Helvetica", 35)),sg.Text("_", key = '-CODE3-',font = ("Helvetica", 35)),sg.Text("_", key = '-CODE4-',font = ("Helvetica", 35)),sg.Push()],
              [sg.Push(), sg.Button('1', font = ("Helvetica", 20), size = (4,2)), sg.Button('2', font = ("Helvetica", 20), size = (4,2)), sg.Button('3', font = ("Helvetica", 20), size = (4,2)),sg.Push()],
              [sg.Push(), sg.Button('4', font = ("Helvetica", 20), size = (4,2)), sg.Button('5', font = ("Helvetica", 20), size = (4,2)), sg.Button('6', font = ("Helvetica", 20), size = (4,2)),sg.Push()],
              [sg.Push(), sg.Button('7', font = ("Helvetica", 20), size = (4,2)), sg.Button('8', font = ("Helvetica", 20), size = (4,2)), sg.Button('9', font = ("Helvetica", 20), size = (4,2)),sg.Push()],
              [sg.Push(), sg.Button('Clear', font = ("Helvetica", 20), size = (4,2)),sg.Button('0', font = ("Helvetica", 20), size = (4,2)), sg.Button('Undo', font = ("Helvetica", 20), size = (4,2)),sg.Push()],
              [sg.VPush()]]
    
    return sg.Window('cartOS', layout, resizable=True, size=(800,480), no_titlebar=True, location=(0,0), keep_on_top= True)

    
last_step = time.time()
last_motor = time.time()
last_horn = time.time()

def lockScreen():
    code = ""
    window = make_window8()
    locked = True
    while locked:
        event, value= window.read()
        pyautogui.moveTo(0,0)
        if event != "Undo" and event != "Clear" and event != "__TIMEOUT__":
            code += event
            pos = len(code)
            if pos > 0:
                window['-CODE' + str(pos) + '-'].update(event)
        elif event == "Undo" and len(code) > 0:
            window['-CODE' + str(len(code)) + '-'].update("_")
            code = code[:-1]
        elif event == "Clear":
            for x in range(1,len(code)+1):
                    window['-CODE' + str(x) + '-'].update("_")
            code = ""
            
        if len(code) == 4:
            if code == "1163":
                locked = False
            else:
                window['-TOP-'].update("INCORRECT CODE")
                window.refresh()
                time.sleep(1)
                window['-TOP-'].update("INPUT CODE")
                for x in range(1,5):
                    window['-CODE' + str(x) + '-'].update("_")
                code = ""
    window.close()
last_angle = 0
def steeringControl(direction, angle): #-35 and 35 or 100 for centering
    global last_angle
    
    if direction == 'C':
        location = 'C%'
        steeringPort.write(location.encode('utf-8'))
    elif angle != last_angle:
        if(direction == 'L'):
            location = '$L'+ str(int(abs(angle)*100))+'\n'
        elif(direction == 'R'):
            location = '$R'+str(int(abs(angle)*100))+'\n'
        last_angle = angle
        print(location)
        steeringPort.write(location.encode('utf-8'))
        time.sleep(.05)
    
    
    
def sControl(string, run_time):
    sLen = len(string)
    global last_step, last_motor, last_horn
   
    if (string.startswith('$') and string.endswith('%') and sLen > 3):
        #print("Valid")
        if(string[1] == 'M'):
            #print("Motor")
            last_motor = time.time()
            GPIO.output(mainBrake, GPIO.LOW)
            GPIO.output(brakeRelease, GPIO.LOW)
            rate = 255 - (217 * .01*(float(string[3:sLen-1])))
            if(string[2] == 'F'):
                #print("Forward at",string[3:sLen-1],"%")
                GPIO.output(reverse, GPIO.LOW)
                GPIO.output(forward, GPIO.HIGH)
                if speedPIN.get_PWM_dutycycle(18) >= 230:
                    for x in range (255, int(rate), -2):
                        #print("Rate", x)
                        moving = True
                        speedPIN.set_PWM_dutycycle(18,x)
                else:
                    speedPIN.set_PWM_dutycycle(18,rate)
                #print("Duty", speedPIN.get_PWM_dutycycle(18))
                
            elif(string[2] == 'R'):
                #print("Reverse at",string[3:sLen-1],"%")
                GPIO.output(forward, GPIO.LOW)
                GPIO.output(reverse, GPIO.HIGH)
                if speedPIN.get_PWM_dutycycle(18) >= 230:
                    for x in range (255, int(rate), -2):
                        #print("Rate", x)
                        moving = True
                        speedPIN.set_PWM_dutycycle(18,x)
                else:
                    speedPIN.set_PWM_dutycycle(18,rate)
            elif(string[2] == 'N'):
                print("Neutral")
                GPIO.output(reverse, GPIO.LOW)
                GPIO.output(forward, GPIO.LOW)
                speedPIN.set_PWM_dutycycle(18, 255)
                
        elif(string[1] == 'S'): #ex: SL20 left 20 degrees
            last_step = time.time()
            #print("Stepper {}".format(last_step))
            angle = int(string[3:sLen-1])
            if(string[2] == 'L'):
                steeringControl('L', int(angle/-1))
            elif(string[2] == 'R'):
                steeringControl('R', int(angle))
            elif(string[2] == 'C'):
                steeringControl('C',0)
                
        elif(string[1] == 'P'):
            
            print("Air")
            if(string[2] == 'B'):
                moving = False
                if(string[3] == '1'):
                    GPIO.output(reverse, GPIO.LOW)
                    GPIO.output(forward, GPIO.LOW)
                    speedPIN.set_PWM_dutycycle(18, 255)
                    GPIO.output(mainBrake, GPIO.HIGH)
                    GPIO.output(brakeRelease, GPIO.HIGH)
                else:
                    GPIO.output(reverse, GPIO.LOW)
                    GPIO.output(forward, GPIO.LOW)
                    GPIO.output(mainBrake, GPIO.LOW)
                    GPIO.output(brakeRelease, GPIO.LOW)
            if(string[2] == 'H'):
                if(string[3] == '1'):
                    GPIO.output(horn, GPIO.HIGH)
                    last_horn = time.time()
                    
        
        if((time.time() - last_step) > .1):
            stepPIN.ChangeDutyCycle(0)
        if(time.time() - last_motor > .1):
            GPIO.output(reverse, GPIO.LOW)
            GPIO.output(forward, GPIO.LOW)
            speedPIN.set_PWM_dutycycle(18, 255)
        if(time.time() - last_horn > .1):
            GPIO.output(horn, GPIO.LOW)
    else:
        if((time.time() - last_step) > .1):
            stepPIN.ChangeDutyCycle(0)
        if(time.time() - last_motor > .1):
            GPIO.output(reverse, GPIO.LOW)
            GPIO.output(forward, GPIO.LOW)
            speedPIN.set_PWM_dutycycle(18, 255)
        if(time.time() - last_horn > .1):
            GPIO.output(horn, GPIO.LOW)
    
def serialF():
    pyautogui.moveTo(0,0)
    error = "1"
    window = make_window4()
    done = False
    GPIO.output(enablePIN,GPIO.HIGH)
    stepPIN.ChangeDutyCycle(0)
    try:
        ser = serial.Serial('/dev/ttyUSB0', 19200, timeout=0)
        d=''
        mStore = ""
        operations = 0
        no_command_t = time.time()
        run_time = time.time()
        error = "2"
        while not done:
            
            if((time.time() - run_time) > 5):              
                GPIO.output(pBrakePower,GPIO.LOW)
            event, value= window.Read(timeout = 0)
            if event == 'Yes':
                done = True
            try:
                d=ser.read(10) #Collects 10 bytes (timeout=0 so actually just collects constantly)
                message = d.decode("utf-8") #Makes the bytes into a string
                #if message != (""):
                    #print("Message", message) #Shows me what the message is for debugging
                mStore += message #Adds the message into the total buffer of commands to do
                if message != "":
                    start_time = time.time()
                #if mStore != (""):
                if message == "" and ((time.time() - no_command_t) > .1):
                    
                    sControl("",(time.time() - run_time))
                    #print("No input")
                    no_command_t = time.time()
                    #print("mStore", mStore) #Shows me the total buffer for debug
                if mStore.find("$") != -1 and mStore.find("%") != -1:
                    
                    d = "%" #Chosen seperator for splitting
                    s =  [e+d for e in mStore.split(d) if e] #Breaks mStore apart at '%', but KEEPS the %$ 
                    if len(s) !=0:
                        nextup=s[0] #Grabs the first command in the list which is will be sent to serial decoder
                        #print("Nextup", nextup) #Shows me what it is
                        s.pop(0) #Removes the first element of the list 
                        l = len(nextup)
                        if l != 0:
                            mStore = mStore[l:len(mStore)] #Shorts the mStore string to no longer have the nextup command in it
                        #print("Updated mStore", mStore) #Shows me the new mStore
                        window['-TEXT-'].update(nextup) #Prints the command to the GUI
                        try:
                            sControl(nextup,(time.time() - run_time))
                        except:
                            pass
                        operations += 1 #Sends the command to serial control
                        no_command_t = time.time()
                if operations != 0 and len(s) == 0:
                    
                    end_time = time.time()
                    time_lapsed = end_time - start_time
                    
                    #print("Operations:",operations,"Seconds:",time_lapsed)
                    operations = 0
                        
                    
                    
            except:
                pass
        ser.close()
        print("Operations", operations)
    except:
        print("NO USB")
        GPIO.output(mainBrake,GPIO.HIGH)
        GPIO.output(brakeRelease, GPIO.HIGH)
        stepPIN.ChangeDutyCycle(0)
        speedPIN.set_PWM_dutycycle(18, 255)
        GPIO.output(reverse, GPIO.LOW)
        GPIO.output(forward, GPIO.HIGH)
        windowF = make_window6()
        windowF['-ERROR-'].update(error)
        event, value= windowF.read()
        if event == 'Okay':
            windowF.close()
    window.close()
            

def xbox(): #xbox function
    try:
        run_time = time.time()
        pyautogui.moveTo(0,0)
        print("Xbox Mode")
        windowDis = make_window5()
        #windowDis.Read(timeout = 10)
        pygame.init()
        REMOTE_IDLE = time.time()
        dConnect_Time = time.time()
        IDLE_TIME = 1
        GPIO.setwarnings(False)
        GPIO.output(enablePIN,GPIO.HIGH)
        stepPIN.ChangeDutyCycle(0)
        GPIO.output(throttleMode, GPIO.LOW)
        steeringModifier = 0
        steeringON = 1
        cruiseRate = 0
        lastGear = 0
        steeringSpeedMin = 1000 #min turning speed in hz
        steeringSpeedMax = 3000 #max turning speed in hz
        window = make_window3()
        TextX = "Xbox"
        done = False
        throttleOn = False
        steeringOn = False
        cruiseCtl = False
        remote = False
        idle = False
        def noRemote():
            
            GPIO.output(mainBrake,GPIO.HIGH)
            GPIO.output(brakeRelease, GPIO.HIGH)
            stepPIN.ChangeDutyCycle(0)
            speedPIN.set_PWM_dutycycle(18, 255)
            GPIO.output(reverse, GPIO.LOW)
            GPIO.output(forward, GPIO.HIGH)
            
        def check_pad():
                pygame.joystick.quit()
                pygame.joystick.init()
                joystick_count = pygame.joystick.get_count()
                if joystick_count == 0:
                    noRemote()
                    return False
                    #print("reconnect")
                    time.sleep(.1)
                else:  
                    print("Reconnected")
                    return True
        #windowDis.close()
        while not remote and not done:
            try:
                remote = check_pad()
                if event1 == 'Okay':
                    done = True
                    windowDis.close()
            except:
                pass
            
            if not remote:
                event1, value = windowDis.Read(timeout = 10)
        windowDis.close()
        
        while not done:
            #check_pad()
            if((time.time() - run_time) > 5):              
                GPIO.output(pBrakePower,GPIO.LOW)
            event, value= window.Read(timeout = 10)
            windowDis.close()
            if (time.time() - REMOTE_IDLE > IDLE_TIME):
                TextX = "Idle"
                idle = True
                GPIO.output(reverse, GPIO.LOW)
                GPIO.output(forward, GPIO.LOW)
                stepPIN.ChangeDutyCycle(0)
                speedPIN.set_PWM_dutycycle(18, 230)
                #check_pad()
            try:
                for event in pygame.event.get():
                    #print(event)
                    if event.type == pygame.JOYDEVICEREMOVED:
                        throttleOn = False
                        steeringOn = False
                        print("Disconnected")
                        remote = False
                        windowDis = make_window5()
                        while not remote and not done and (time.time()-dConnect_Time > 2):
                            event1, value = windowDis.Read(timeout = 10)
                            if event1 == 'Okay':
                                done = True
                            remote = check_pad()
                            time.sleep(1)
                        if not done:
                            dConnect_Time = time.time()
                            windowDis.close()
                    REMOTE_IDLE = time.time()
                    idle = False
            except:
                print("failed at remote check")
                pass
            #pygame.event.get()
            
            window['-TEXT-'].update(TextX)
            TextX = "No active inputs"
            if event == 'Yes':
                done = True
                window.close()
            try:
                joystick_count = pygame.joystick.get_count()
                #print(joystick_count)  
                for i in range(joystick_count):
                    try:
                        joystick = pygame.joystick.Joystick(i)
                        #joystick.init()
                    except:
                        check_pad()
                        
                
                    try:
                        jid = joystick.get_instance_id()
                        
                    except AttributeError:
                        jid = joystick.get_id()
                    #print(joystick.get_axis(0))   
                    #print("Joystick name: {}".format(name))
                    if joystick.get_axis(0) != -1:
                        steeringOn = True
                    #Streering
                    if steeringOn and not idle:
                        if joystick.get_axis(0) < -0.05:
                            TextX = ("Turning Left at {} deg".format(round(joystick.get_axis(0)*-35),2))
                            steeringControl('L',(joystick.get_axis(0)+.05)*35)
                        elif joystick.get_axis(0) > 0.15:
                            TextX = ("Turning Right at {} deg".format(round((joystick.get_axis(0)-.15)*40),2))
                            steeringControl('R',(joystick.get_axis(0)-.15)*40)
                        else:
                            steeringControl('L',0)
                    
                    #Brakes
                    if joystick.get_axis(5) !=0: #so it doesnt brake immediatly
                        
                        if joystick.get_axis(5) > 0:
                            GPIO.output(mainBrake,GPIO.HIGH)
                            GPIO.output(brakeRelease, GPIO.HIGH)
                            TextX =("Brake on")
                        else:
                            GPIO.output(mainBrake,GPIO.LOW)
                            GPIO.output(emergencyBrake,GPIO.LOW)
                            GPIO.output(brakeRelease, GPIO.LOW)
                
                
                    #axis 4 is throttle (RT) axis 3 is forward/reverse (right joystick)
                    if joystick.get_axis(4) !=0:
                        throttleOn = True
                        
                    if throttleOn and not idle: # RT starts at 0 on program boot, this keeps the cart from driving into a wall
                        #print(" axis 3 val: {}".format(joystick.get_axis(3)))
                        if joystick.get_axis(3) < -.99:
                            lastGear = 1
                            GPIO.output(reverse, GPIO.LOW)
                            GPIO.output(forward, GPIO.HIGH)
                            speed =  255 - (joystick.get_axis(4) + 1) * 108
                            steeringModifier = (joystick.get_axis(4) + 1)/2
                            speedFormat = round((joystick.get_axis(4) + 1)/.02, 0)
                            TextX = ("Forward at {}% speed".format(speedFormat))
                            speedPIN.set_PWM_dutycycle(18, speed)
                            
                        elif joystick.get_axis(3) > .99:
                            lastGear = -1
                            GPIO.output(forward, GPIO.LOW)
                            GPIO.output(reverse, GPIO.HIGH)
                            speed =  255 - (joystick.get_axis(4) + 1) * 108
                            steeringModifier = (joystick.get_axis(4) + 1)/2
                            speedFormat = round(steeringModifier*100, 0)
                            TextX = ("Reversing at {}% speed".format(speedFormat))
                            speedPIN.set_PWM_dutycycle(18, speed)
            #               
                        else:
                            GPIO.output(reverse, GPIO.LOW)
                            GPIO.output(forward, GPIO.LOW)
                            speedPIN.set_PWM_dutycycle(18, 255)
                        
                        
                    #Using Buttons
                  
                    a_button = joystick.get_button(0)
                
                    if a_button == 1 and steeringON == 1:
                        GPIO.output(enablePIN,GPIO.LOW)
                        TextX = (" Steering Off")
                        window['-STR-'].update("OFF")
                        steeringON = 0
                        time.sleep(.5)
                    elif a_button == 1 and steeringON == 0:
                        GPIO.output(enablePIN,GPIO.HIGH)
                        TextX = (" Steering On")
                        window['-STR-'].update("ON")
                        steeringON = 1
                        time.sleep(.5)
                    
                    b_button = joystick.get_button(1)
                    if b_button == 1:
                        done = True
                    
                    x_button = joystick.get_button(3)
                    if x_button == 1:
                        GPIO.output(emergencyBrake,GPIO.HIGH)
                        GPIO.output(brakeRelease, GPIO.HIGH)
                        if lastGear == 1:
                            GPIO.output(forward, GPIO.LOW)
                            GPIO.output(reverse, GPIO.HIGH)
                            lastGear = 0
                            for x in range (255, 50, -2):
                        #print("Rate", x)
                                
                                speedPIN.set_PWM_dutycycle(18,x)
                        time.sleep(2)
                        TextX =("E Brake on")
                    elif lastGear == 0:
                        GPIO.output(forward, GPIO.LOW)
                        GPIO.output(reverse, GPIO.LOW)
                        speedPIN.set_PWM_dutycycle(18,255)
                        
                    y_button = joystick.get_button(4)
                    
                        
                    xbox_button = joystick.get_button(12)
                    if xbox_button == 1:
                        IDLE_TIME = 100
                        window['-IDLE_TIME-'].update(IDLE_TIME)
                    if y_button == 1:
                        GPIO.output(horn, GPIO.HIGH)
                        TextX = ("Horn!")
                    else:
                        GPIO.output(horn, GPIO.LOW)
                
                    leftBump = joystick.get_button(6)
                    rightBump = joystick.get_button(7)
                    
                    if leftBump == 1 and rightBump == 1 and not cruiseCtl:
                        cruiseCtl = True
                        cruiseRate = speedFormat
                        window['-CCTRL-'].update(cruiseRate)
                        time.sleep(.1)
                    elif (leftBump == 1 and rightBump == 1 and cruiseCtl) or (joystick.get_axis(5) !=0 and joystick.get_axis(5) > -.9):
                        cruiseCtl = False
                        cruiseRate = 0
                        print("Off")
                        time.sleep(.1)
                        window['-CCTRL-'].update("OFF")
                    
                    if leftBump == 1 and cruiseRate > 0 and cruiseCtl:
                        cruiseRate -= 1
                        window['-CCTRL-'].update(cruiseRate)
                    elif rightBump == 1 and cruiseRate < 100 and cruiseCtl:
                        cruiseRate += 1
                        window['-CCTRL-'].update(cruiseRate)
                        

                
                    d_pos = joystick.get_hat(0)
                    #print("D Position: {}".format(d_pos))
                
                    if d_pos[1] == 1:
                        TextX = ("Calibrating Steering")
                        window['-TEXT-'].update(TextX)
                        window.Read(timeout = 10)
                        window['-HIGH-'].update("Done")
                        steeringControl('C',0)
                        time.sleep(10)
                        
                        
                    if d_pos[0] == 1:
                        IDLE_TIME += .5
                        window['-IDLE_TIME-'].update(IDLE_TIME)
                        time.sleep(.5)
                    elif d_pos[0] == -1 and IDLE_TIME > 1:
                        IDLE_TIME -= .5
                        window['-IDLE_TIME-'].update(IDLE_TIME)
                        time.sleep(.5)
            except:
                print("fail 3")
        print("exit")
        window.close()
        pygame.quit()
        if not remote:
            windowDis.close()
            pygame.quit()
    except:
        print("error")
        window.close()
        pygame.quit()

def manual(): #for manual since we need to have forward and reverse
    print("Manual Mode")
    run_time = time.time()
    window2 = make_window2()
    Text = "Neutral"
    GPIO.output(enablePIN,GPIO.LOW)
    GPIO.output(throttleMode, GPIO.HIGH)
    manualLoop = True
    
    
    
    while manualLoop:
        if((time.time() - run_time) > 5):              
                GPIO.output(pBrakePower,GPIO.LOW) 
        #driveMode = input("Forward, Reverse, Neutral or Exit(Input f,r,n, or e)")
        pyautogui.moveTo(0,0)
        event, values= window2.Read(timeout = 10)
        window2['-TEXT-'].update(Text)
        if event == 'Forward':
            Text = "Forward"
            GPIO.output(reverse, GPIO.LOW)
            GPIO.output(forward, GPIO.HIGH)
        elif event == 'Reverse':
            Text = "Reverse"
            GPIO.output(forward, GPIO.LOW)
            GPIO.output(reverse, GPIO.HIGH)
        elif event == 'Neutral':
            Text = "Neutral"
            GPIO.output(reverse, GPIO.LOW)
            GPIO.output(forward, GPIO.LOW)
        elif event == 'Exit':
#             window.close()
            GPIO.output(reverse, GPIO.LOW)
            GPIO.output(forward, GPIO.LOW)
            GPIO.output(throttleMode, GPIO.LOW)
            manualLoop = False
            
    window2.close()
     
    
    




#BEGIN MAIN PART OF THE SCRIPT

#These are BCM addresses not the actual gpio pins
GPIO.setwarnings(False)
speedPIN = 18 
dirPIN = 5
stepPIN = 13
enablePIN = 6
forward = 16
reverse = 20
throttleMode = 26

mainBrake = 27 #normally 27
parkingBrake = 24
pBrakePower = 25
brakeRelease = 23
emergencyBrake = 22  #Normally 22 
horn = 17



speedPIN = pigpio.pi() #starting the pigpio class called speedPIN

GPIO.setmode(GPIO.BCM) #Tells gpio how to locate the pins
#Motor
#GPIO.setup(speedPIN, GPIO.OUT) #Sets speedPIN as an output
GPIO.setup(forward, GPIO.OUT)
GPIO.setup(reverse, GPIO.OUT)
GPIO.output(reverse, GPIO.LOW)
GPIO.output(forward, GPIO.LOW)
#Brakes
GPIO.setup(mainBrake, GPIO.OUT)
GPIO.output(mainBrake, GPIO.LOW) #starts brakes off
GPIO.setup(brakeRelease, GPIO.OUT)
GPIO.setup(emergencyBrake, GPIO.OUT)
GPIO.setup(parkingBrake, GPIO.OUT)
GPIO.setup(pBrakePower, GPIO.OUT)
#Steering stepper
GPIO.setup(dirPIN, GPIO.OUT)
GPIO.setup(stepPIN, GPIO.OUT)
GPIO.setup(enablePIN, GPIO.OUT)

#Horn
GPIO.setup(horn, GPIO.OUT)
GPIO.output(horn, GPIO.LOW)

GPIO.setup(throttleMode, GPIO.OUT)
GPIO.output(throttleMode, GPIO.LOW)

#The two PWM pins :{
#Starts the steering port
try:
    steeringPort = serial.Serial('/dev/ttyS0',9600 )
except:
    print("Fatal Error: No Steering")
    sys.exit()

stepPIN = GPIO.PWM(stepPIN, 1) #makes stepPIN a PWM signal with a frequecy of 1 hz (we change this later)
stepPIN.start(50) #step speed will always be at 50% duty

speedPIN.hardware_PWM(18, 1000, 1000000) #speedPIN as a hawrdware PWM 1000 hz and 100% duty cycle due to an inverse level shift circit

#Touch GUI stuff
sg.theme('DarkBlue7')



window1 = make_window1()
modeSelecting = True
pBrakeTime= time.time()
lockTime = time.time()
pBrake = False
failed = False
firstUnlock = False #Debug
pyautogui.FAILSAFE = False
while modeSelecting:
    speedPIN.hardware_PWM(18, 1000, 1000000)
    GPIO.output(reverse, GPIO.LOW)
    GPIO.output(forward, GPIO.LOW)
    stepPIN.ChangeDutyCycle(0)
    GPIO.output(mainBrake,GPIO.LOW)
    GPIO.output(enablePIN, GPIO.LOW)
    GPIO.output(brakeRelease, GPIO.LOW)
    event, values= window1.Read(timeout = 10)
    if not firstUnlock or (time.time()-lockTime) > 30:
        lockScreen()
        firstUnlock = True
        lockTime = time.time()
        if not pBrake:
            pBrakeTime= time.time()
    
    if ((time.time() - pBrakeTime) < 6) and not pBrake:
        GPIO.output(parkingBrake,GPIO.HIGH)
        GPIO.output(pBrakePower, GPIO.HIGH)
    pyautogui.moveTo(0,0)
    if ((time.time() - pBrakeTime) >= 6) and not pBrake:
         window7 = make_window7()
         GPIO.output(mainBrake,GPIO.HIGH)
         e_time = time.time()
         while(time.time() - e_time <= 5):
             window7.Read(timeout = 10)
             window7['-TIMER-'].update("{} seconds remaining".format(round(5 - (time.time() - e_time)),3))
         GPIO.output(mainBrake,GPIO.LOW)
         GPIO.output(pBrakePower, GPIO.LOW)
         GPIO.output(parkingBrake,GPIO.LOW)
         pBrake = True
         window7.close()

    
    
    if event == 'Xbox': #event == 'Xbox'
        GPIO.output(parkingBrake,GPIO.LOW)
        GPIO.output(pBrakePower, GPIO.HIGH)
        xbox()
        lockTime = time.time()
        pBrakeTime= time.time()
        pBrake = False
    elif event == 'Manual' or failed:
        GPIO.output(parkingBrake,GPIO.LOW)
        GPIO.output(pBrakePower, GPIO.HIGH)
        manual()
        lockTime = time.time()
        pBrakeTime= time.time()
        pBrake = False
    elif event == 'Serial':
        GPIO.output(parkingBrake,GPIO.LOW)
        GPIO.output(pBrakePower, GPIO.HIGH)
        serialF()
        lockTime = time.time()
        pBrakeTime= time.time()
        pBrake = False
    elif event == 'Exit':
        modeSelecting = False
    elif event == 'Lock':
        lockScreen()
        lockTime = time.time()
        if not pBrake:
            pBrakeTime= time.time()
    
window1.close()        
GPIO.cleanup()
pygame.quit()




