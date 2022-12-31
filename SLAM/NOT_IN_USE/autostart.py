#! /bin/bash



from os import link
import time


def speak_funktion(text_for_speaking:link):  # status 3
    speaker.say(text_for_speaking)
    speaker.runAndWait()


def play_function(link:str):  # status 1
    # playsound(link)
    playsound.playsound(link,True)
    time.sleep(1)


def to_MEGA (char:str):  #status 2
    # this dont work with a time
    serial_port.write(char)
    if char== "L" or char== "R" or char=="C":
        time.sleep(4)
        serial_port.write(Z) # stop
        print("Z")

sentence =""
status="status"
content="content"
text_2 = "С настъпването на най-светлите празници. Искам да ви пожелая:    Весела Коледа и  Щастлива Нова година!   Хо- Хо- Хо!"
S = "S".encode()  # Start
L = "L".encode()  # left
R = "R".encode()  # right
F = "F".encode()  # Forward
B = "B".encode()  # Bakward
Z = "Z".encode()  # Stop
C = "C".encode()  # Start
M = "M".encode()  # led on
N = "N".encode()  # led off

all_commands={"stop": {"content": Z,"status":2} ,
     "back": {"content": B, "status": 2},
     "left": {"content": L, "status": 2},
     "right": {"content": R, "status": 2},
     "go": {"content": C, "status": 2},
     "how are you": {"content": "Много добре, ти как си?", "status": 3},
     "Christmas": {"content": text_2, "status": 3},
     "sleep": {"content": "Лека нощ!", "status": 3},
     "German": {"content": "/home/nanorobo/Desktop/ROBO/Python_projects/koleda_deutsch.mp3", "status": 1},
     "lights on": {"content": M, "status": 2},
     "lights off": {"content": N, "status": 2},
     "100": {"content":"/home/nanorobo/Desktop/ROBO/Python_projects/100-posh.mp3" , "status": 1},
     "new year": {"content":"/home/nanorobo/Desktop/ROBO/Python_projects/dunavsko.mp3" , "status": 1},
     "white": {"content": "ЕБАНЙЕ!!!", "status": 3},
     "boom": {"content": "/home/nanorobo/Desktop/ROBO/Python_projects/ak47.mp3" , "status": 1},
     "200": {"content": "/home/nanorobo/Desktop/ROBO/Python_projects/100-balkan.mp3" , "status": 1},
    "who are you": {"content": "Аз съм РОБО-робота. Още малък, но с голям потенциал.", "status": 3},
    "katie" : {"content": "The most wonderfull girl in the earth!!!", "status": 3} }



import speech_recognition as sr
import time
import pyttsx3
# import serial
############## uart start ############################
# import time
import serial
import playsound


serial_port = serial.Serial(
    port="/dev/ttyTHS1",
    baudrate=115200,
    bytesize=serial.EIGHTBITS,
    parity=serial.PARITY_NONE,
    stopbits=serial.STOPBITS_ONE,
)

time.sleep(1)
print("DENISLAV  START UART")

############# uart stop ##############

speaker = pyttsx3.init()
speaker.setProperty("rate", 140)
speaker.setProperty("voice", 'Bulgarian+m2')

r = sr.Recognizer()
try:
    serial_port.write(S) # start nan nesho, ako iskash
    speaker.say("Ready for work!")
    speaker.runAndWait()
    while True:
        with sr.Microphone() as source:
            r.adjust_for_ambient_noise(source, duration=0.7)  # 1  0.7
            print("Speak Anything :")
            audio = r.listen(source)
            try:
                text = r.recognize_google(audio)
                print(text)
                speaker.say(text)
                speaker.runAndWait()

                ##### komandi Izpylenie #####################################################
                sentence = text.lower()
                for comanda, content_file in all_commands.items():
                
                    if comanda in sentence:
                       
                        
                        if content_file[status] == 3:
                                speak_funktion(content_file[content])
                        elif content_file[status] == 2:
                                serial_port.write(content_file[content])
                                if content_file[content]== L or content_file[content]== R or content_file[content]== C or content_file[content]== B:
                                    time.sleep(4)
                                    serial_port.write(Z)
                                    

                        elif content_file[status] == 1:
                                playsound.playsound(content_file[content], True)

                #### komandi izpylnenie ######################################################

                ########################## uart start   ###################################3
                if serial_port.inWaiting() > 0:  # chete ot MEGA
                    data = serial_port.read()
                    print(data)
                    serial_port.write(data)

                if data == "\r".encode():
                    # For Windows boxen on the other end
                    serial_port.write("\n".encode())
            ########################## uart stop   ###################################3
            except:
                print("Sorry could not recognize what you said")

                # device_index=0,sample_rate=None,chunk_size=512



except KeyboardInterrupt:
    print("Exiting Program")

finally:
    serial_port.close()
    pass



# #####################################    RABOTI TOZI LINK   #################################



# import cv2
# import mediapipe as mp
# import time
# import pyttsx3
# import threading 

# speaker = pyttsx3.init()
# speaker.setProperty("rate", 140)
# speaker.setProperty("voice", 'Bulgarian+m2')

# speak=True
# item="омммммммм"
# itemOld=''

# def sayItem():   # funktion for speeking once time
#     global speak
#     global item
#     while True:
#         if speak ==True:
#             speaker.say(item)
#             speaker.runAndWait()
#             speak=False
# x=threading.Thread(target=sayItem, daemon=True)
# x.start()



# time.sleep(2)

# # speaker.say("Ready for work!")
# # speaker.runAndWait()

# #cap = cv2.VideoCapture(1)
# cap=cv2.VideoCapture(1)

# cap.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc('M', 'J', 'P', 'G')) # depends on fourcc available camera
# cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640) # 640
# cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)  # 480
# cap.set(cv2.CAP_PROP_FPS, 15)

# mpHands = mp.solutions.hands
# hands = mpHands.Hands()
# mpDraw = mp.solutions.drawing_utils

# pTime = 0
# cTime = 0
# fingers={} # store all date
# x="x"
# y="y"
# stop=0


# while True:
    
#     success, img = cap.read()
#     img = cv2.rotate(img, cv2.ROTATE_180) # dobavil tova
    
#     # print(results.multi_hand_landmarks)

#     if speak==False:  # moje bi tuk
#         imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
#         results = hands.process(imgRGB)

#         if results.multi_hand_landmarks:
#             for handLms in results.multi_hand_landmarks:
                
#                 for id, lm in enumerate(handLms.landmark):
#                     # if id==8:  # ako e vyrha na pokazalec
#                     #     print(cx,cy)
                    


#                     #print(id, lm) # coordinates 
#                     h, w, c = img.shape
#                     cx, cy = int(lm.x * w), int(lm.y * h)
#                     #print(id, cx, cy) # pixels on video
#                     fingers[id]={}
#                     fingers[id][x]=cx
#                     fingers[id][y]=cy
                    
#                     # if id == 4:
#                     cv2.circle(img, (cx, cy), 5, (255, 0, 255), cv2.FILLED)

#                 mpDraw.draw_landmarks(img, handLms, mpHands.HAND_CONNECTIONS)
#                 #print(fingers)
#                 # if  fingers[8][y]< fingers[6][y]: # open pokazalec
#                 #     print("open pokazalec")
#                 #     stop=5
#                 # elif  fingers[12][y]< fingers[10][y]: # open sreden
#                 #     print("open sreden")
#                 #     stop=4
#                 # elif  fingers[20][y]< fingers[18][y]: # open malyk
#                 #     print("open malyk")
#                 #     stop=3
#                 # elif  fingers[4][x]> fingers[2][x]: # open palec
#                 #     print("open palec")
#                 #     stop=2

#                 if fingers[8][y]> fingers[6][y] and fingers[12][y]> fingers[10][y] and fingers[20][y]> fingers[18][y] and fingers[4][x]< fingers[2][x]:
#                     item= "Stop!"
#                     print("Stop")
#                     # if item!=itemOld:
#                     #     speak=True
#                 else:
#                     print("Start")
#                     item="Start!"
#                     # if item!=itemOld:
#                     #     speak=True
#                 if item!=itemOld:
#                         speak=True
#                 itemOld=item
        

        

            


#     cTime = time.time()
#     fps = 1 / (cTime - pTime)
#     pTime = cTime

#     cv2.putText(img, str(int(fps)), (10, 70), cv2.FONT_HERSHEY_PLAIN, 3,
#                 (255, 0, 255), 3)

#     cv2.imshow("Image", img)
#     cv2.waitKey(1)

          
# ####################################################################################
# #@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
# ####################################################################################

# from rplidar import RPLidar
# import numpy as np
# lidar = RPLidar('/dev/ttyUSB0')
# import time
# import serial
# import pyttsx3


# serial_port = serial.Serial(
#     port="/dev/ttyTHS1",
#     baudrate=115200,
#     bytesize=serial.EIGHTBITS,
#     parity=serial.PARITY_NONE,
#     stopbits=serial.STOPBITS_ONE,
# )

# time.sleep(1)
# print("DENISLAV  START UART")


# S = "S".encode()  # Start
# L = "L".encode()  # left
# R = "R".encode()  # right
# F = "F".encode()  # Forward
# B = "B".encode()  # Bakward
# Z = "Z".encode()  # Stop
# C = "C".encode()  # Start
# M = "M".encode()  # led on
# N = "N".encode()  # led off

# # info = lidar.get_info() # info if connected
# # print(info)
# # health = lidar.get_health() # info for the serial numerb etc
# # print(health)
# speaker = pyttsx3.init()
# speaker.setProperty("rate", 140)
# speaker.setProperty("voice", 'Bulgarian+m2')


# try:
#   serial_port.write(S) # start nan nesho, ako iskash
#   speaker.say("Start the script!!")
#   speaker.runAndWait()
#   while True:
    
#     for scan in lidar.iter_scans():
#       offsets = np.array([(meas[1],meas[2]) for meas in scan])
#       comand=Z
#       for degree,dist in offsets:
#         if  (0<degree<=15) and dist>250:
#           # print('Ahead')
#           comand=C

#         elif (0<=degree<135 ) and dist<=250:
#           # print('TURN LEFT')
#           comand=R

#         elif (225<degree<360) and dist<=250:
#           # print('TURN RIGNT')
#           comand=L

#         elif (135<degree<225) and dist<=400:
#           # print("stop=back something")
#           comand=Z
#       serial_port.write(comand)

      

    

# except KeyboardInterrupt:
#   print("Exiting Program")
#   serial_port.write(Z)
  

# finally:
#   serial_port.write(Z)

#   serial_port.close()
#   lidar.stop()
#   lidar.stop_motor()
#   lidar.disconnect()

    

    

 
# # # # # #### PICAM #####################################################################################################
# # # # # ################################################################################
# import jetson.inference
# import cv2
# import numpy as np
# import os
# import pyttsx3
# import playsound
# import time

# speaker = pyttsx3.init()
# speaker.setProperty("rate", 140)
# speaker.setProperty("voice", 'Bulgarian+m2')
# #cam = jetson.utils.videoSource("csi://0")


# """  S TEZI NASTOIJKI  VYRVI"""
# cam=cv2.VideoCapture('/dev/video1')
# #cam=cv2.VideoCapture('/home/nanorobo/Desktop/Python_projects/video_1.mp4')

# cam.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc('M', 'J', 'P', 'G')) # depends on fourcc available camera
# cam.set(cv2.CAP_PROP_FRAME_WIDTH, 640) # 640
# cam.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)  # 480
# cam.set(cv2.CAP_PROP_FPS, 5)

# speaker.say("Hello!")
# speaker.runAndWait()


# playsound.playsound("/home/nanorobo/Desktop/Python_projects/talk.mp3", True)
# time.sleep(1)

# while True:
#     ret, frame=cam.read()
    
#     frame = cv2.rotate(frame, cv2.ROTATE_180)
    
#     #cv2.imshow('piCam',frame)
#     if cv2.waitKey(1)==ord('q'):
#         break
# cam.release()
# cv2.destroyAllWindows()

############################################
#######################################
#########################################################
# import cv2
# import mediapipe as mp
# import time
# import pyttsx3

# speaker = pyttsx3.init()
# speaker.setProperty("rate", 140)
# speaker.setProperty("voice", 'Bulgarian+m2')

# speaker.say("Ommmmm!")
# speaker.runAndWait()


# cap=cv2.VideoCapture(1)

# cap.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc('M', 'J', 'P', 'G')) # depends on fourcc available camera
# cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640) # 640
# cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)  # 480
# cap.set(cv2.CAP_PROP_FPS, 5)

# mpHands = mp.solutions.hands
# hands = mpHands.Hands()
# #mpDraw = mp.solutions.drawing_utils



# diff=0
# xix=0
# while True:
#     success, img = cap.read()
#     img = cv2.rotate(img, cv2.ROTATE_180) # dobavil tova
#     imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
#     results = hands.process(imgRGB)
#     if results.multi_hand_landmarks:
#         h, w, c = img.shape
#         x_5=int((results.multi_hand_landmarks[0].landmark[5].x)*w)
#         x_17=int((results.multi_hand_landmarks[0].landmark[17].x)*w)
#         diff=abs(x_5-x_17)
#         xix=x_5
#         #print(x_5)
#         speaker.say(f"{x_5}")
#         speaker.runAndWait()
#         #mpDraw.draw_landmarks(img, results.multi_hand_landmarks[0], mpHands.HAND_CONNECTIONS)
#     #cv2.imshow("Image", img)
#     #cv2.waitKey(1)
#     if cv2.waitKey(1)==ord('q'):
#         break
# cap.release()
# cv2.destroyAllWindows()


# # while True:
# #     ret, frame=cap.read()
# #     new = cv2.rotate(frame, cv2.ROTATE_180)
    
# #     cv2.imshow('piCam',new)
# #     if cv2.waitKey(1)==ord('q'):
# #         break
# # cap.release()
# # cv2.destroyAllWindows()
    

       
        
        








 



   

          
                
    




